"""FastAPI backend for the graph explorer.

The interesting endpoint is POST /api/ask. It does two things with one question:

  1. answers it through the GraphRAG pipeline, and
  2. returns the exact subgraph the answer was drawn from,

so the front-end can light up the evidence instead of asking you to trust a
paragraph of prose. Step 2 re-runs the vector/fulltext lookup itself rather than
parsing GraphRAG's context string, because the retriever hands back formatted text
and the front-end needs element IDs.

POST /api/ask/stream does the same work as Server-Sent Events, one event per
stage of the pipeline, so the graph can unfold in step with the reasoning rather
than appearing all at once when the model finally finishes. The LLM call is
handed to a worker thread first, so the retrieval rings reach the browser while
the model is still writing.

Both endpoints also serve the Microsoft Agent Framework agent, addressed as one
more entry in the retriever list. Its evidence subgraph needs no second lookup:
the agent's tools record what they read as they go.
"""

from __future__ import annotations

import argparse
import json
import os
from collections.abc import AsyncIterator, Iterator
from concurrent.futures import ThreadPoolExecutor
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from neo4j_graphrag.generation import GraphRAG
from neo4j_graphrag.generation.prompts import RagTemplate
from pydantic import BaseModel, Field

from graphrag_kit.agent import ask_agent, build_agent
from graphrag_kit.config import (
    ENTITY_FULLTEXT_INDEX_NAME,
    FULLTEXT_INDEX_NAME,
    VECTOR_INDEX_NAME,
    describe_agent_model,
    describe_models,
    get_database,
    get_driver,
    get_embedder,
    get_llm,
)
from graphrag_kit.project import load_project
from graphrag_kit.retrievers import RETRIEVERS, build_rag_prompt, evidence_entity_ids

STATIC_DIR = Path(__file__).resolve().parent / "static"
RESERVED_LABELS = {"__Entity__", "__KGBuilder__"}

#: Selectable alongside the retrievers, but not one of them: it *uses* them.
AGENT_MODE = "agent"

state: dict[str, Any] = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    state["project"] = load_project()
    print(f"models: {describe_models()}")
    print(f"agent:  {describe_agent_model()}")
    state["driver"] = get_driver()
    state["database"] = get_database()
    state["embedder"] = get_embedder()
    state["llm"] = get_llm()
    state["rag"] = {}
    state["agent"] = None
    yield
    await state["llm"].aclose()
    state["driver"].close()


app = FastAPI(title="GraphRAG Explorer", lifespan=lifespan)


def run(cypher: str, **params) -> list:
    records, _, _ = state["driver"].execute_query(
        cypher, database_=state["database"], **params
    )
    return records


def rag_for(retriever_name: str) -> GraphRAG:
    """GraphRAG pipelines are cached per retriever — each one builds a driver-bound
    retriever, and rebuilding on every request wastes the connection pool."""
    if retriever_name not in state["rag"]:
        if retriever_name not in RETRIEVERS:
            raise HTTPException(400, f"unknown retriever {retriever_name!r}")
        state["rag"][retriever_name] = GraphRAG(
            retriever=RETRIEVERS[retriever_name](state["driver"]),
            llm=state["llm"],
            prompt_template=RagTemplate(
                template=build_rag_prompt(state["project"]),
                expected_inputs=["context", "query_text", "examples"],
            ),
        )
    return state["rag"][retriever_name]


def agent():
    """The Agent Framework agent, built on first use.

    Deliberately lazy. It needs a chat client the retrievers do not — a different
    API surface, and on Azure a different api-version — so a misconfigured agent
    would otherwise take the whole explorer down at startup instead of failing
    only the requests that ask for it.
    """
    if state["agent"] is None:
        state["agent"] = build_agent(state["driver"], state["project"])
    return state["agent"]


# --- graph serialisation ----------------------------------------------------

NODE_PROJECTION = """
  elementId(n) AS id,
  head([l IN labels(n) WHERE NOT l IN ['__Entity__','__KGBuilder__']]) AS label,
  n.name AS name,
  coalesce(n.status, 'reported') AS status,
  n.evidence_levels AS evidence_levels,
  n.description AS description,
  n.role AS role,
  n.kind AS kind,
  n.date AS date,
  n.fictional AS fictional,
  n.inspiration AS inspiration
"""


def node_dict(record) -> dict:
    return {
        "id": record["id"],
        "label": record["label"],
        "name": record["name"] or "(unnamed)",
        "status": record["status"],
        "evidence_levels": record["evidence_levels"] or [],
        "description": record["description"],
        "role": record["role"],
        "kind": record["kind"],
        "date": record["date"],
        "fictional": record["fictional"],
        "inspiration": record["inspiration"],
    }


def subgraph_for_ids(ids: list[str], include_neighbours: bool = True) -> dict:
    """Nodes for `ids`, optionally their direct neighbours, and every edge among them."""
    if not ids:
        return {"nodes": [], "relationships": []}

    if include_neighbours:
        node_records = run(
            f"""
            MATCH (seed:__Entity__) WHERE elementId(seed) IN $ids
            OPTIONAL MATCH (seed)-[]-(nbr:__Entity__)
            WITH collect(DISTINCT seed) + collect(DISTINCT nbr) AS all_nodes
            UNWIND all_nodes AS n
            WITH DISTINCT n WHERE n IS NOT NULL
            RETURN {NODE_PROJECTION}
            """,
            ids=ids,
        )
    else:
        node_records = run(
            f"MATCH (n:__Entity__) WHERE elementId(n) IN $ids RETURN {NODE_PROJECTION}",
            ids=ids,
        )

    nodes = [node_dict(r) for r in node_records]
    node_ids = [n["id"] for n in nodes]

    rel_records = run(
        """
        MATCH (a:__Entity__)-[r]->(b:__Entity__)
        WHERE elementId(a) IN $ids AND elementId(b) IN $ids
        RETURN elementId(r) AS id, elementId(a) AS source, elementId(b) AS target,
               type(r) AS type, properties(r) AS props
        """,
        ids=node_ids,
    )
    relationships = [
        {
            "id": r["id"],
            "from": r["source"],
            "to": r["target"],
            "type": r["type"],
            "properties": {k: v for k, v in (r["props"] or {}).items()},
        }
        for r in rel_records
    ]
    return {"nodes": nodes, "relationships": relationships, "seeds": ids}


# --- API --------------------------------------------------------------------


@app.get("/api/meta")
def meta() -> dict:
    counts = run(
        """
        MATCH (n:__Entity__)
        UNWIND labels(n) AS label
        WITH label WHERE NOT label IN ['__Entity__','__KGBuilder__']
        RETURN label, count(*) AS count ORDER BY count DESC
        """
    )
    statuses = run(
        "MATCH (n:__Entity__) RETURN coalesce(n.status,'reported') AS status, "
        "count(*) AS count ORDER BY count DESC"
    )
    docs = run("MATCH (d:Document) RETURN count(d) AS c")
    chunks = run("MATCH (c:Chunk) RETURN count(c) AS c")
    rels = run("MATCH (:__Entity__)-[r]->(:__Entity__) RETURN count(r) AS c")
    spec = state["project"]
    return {
        "project": spec.key,
        "title": spec.title,
        "subtitle": spec.subtitle,
        "examples": spec.example_questions,
        "evidenceLevels": list(spec.evidence_levels),
        "labels": spec.labels,
        "colors": spec.palette,
        "retrievers": sorted(RETRIEVERS) + [AGENT_MODE],
        "counts": {r["label"]: r["count"] for r in counts},
        "statuses": {r["status"]: r["count"] for r in statuses},
        "documents": docs[0]["c"],
        "chunks": chunks[0]["c"],
        "relationships": rels[0]["c"],
    }


@app.get("/api/graph")
def graph(labels: str | None = None, status: str | None = None) -> dict:
    """The whole POLE graph, optionally filtered by label and evidence level."""
    spec = state["project"]
    wanted_labels = [x for x in (labels or "").split(",") if x] or spec.labels
    wanted_status = [x for x in (status or "").split(",") if x] or list(spec.evidence_levels)
    records = run(
        f"""
        MATCH (n:__Entity__)
        WHERE any(l IN labels(n) WHERE l IN $labels)
          AND coalesce(n.status, 'reported') IN $status
        RETURN {NODE_PROJECTION}
        """,
        labels=wanted_labels,
        status=wanted_status,
    )
    nodes = [node_dict(r) for r in records]
    ids = [n["id"] for n in nodes]
    rel_records = run(
        """
        MATCH (a:__Entity__)-[r]->(b:__Entity__)
        WHERE elementId(a) IN $ids AND elementId(b) IN $ids
        RETURN elementId(r) AS id, elementId(a) AS source, elementId(b) AS target,
               type(r) AS type, properties(r) AS props
        """,
        ids=ids,
    )
    return {
        "nodes": nodes,
        "relationships": [
            {
                "id": r["id"],
                "from": r["source"],
                "to": r["target"],
                "type": r["type"],
                "properties": dict(r["props"] or {}),
            }
            for r in rel_records
        ],
    }


@app.get("/api/expand")
def expand(id: str) -> dict:
    return subgraph_for_ids([id], include_neighbours=True)


@app.get("/api/search")
def search(q: str, limit: int = 15) -> dict:
    if not q.strip():
        return {"nodes": []}
    records = run(
        f"""
        CALL db.index.fulltext.queryNodes($index, $q, {{limit: $limit}})
        YIELD node AS n, score
        RETURN {NODE_PROJECTION}, score
        """,
        index=ENTITY_FULLTEXT_INDEX_NAME,
        q=q,
        limit=limit,
    )
    return {"nodes": [node_dict(r) for r in records]}


@app.get("/api/timeline")
def timeline() -> dict:
    """Dated Event nodes in order — a timeline view, when the schema has Events."""
    records = run(
        f"""
        MATCH (n:Event) WHERE n.date IS NOT NULL
        RETURN {NODE_PROJECTION}
        ORDER BY n.date
        """
    )
    return {"nodes": [node_dict(r) for r in records]}


class AskRequest(BaseModel):
    question: str
    retriever: str = "hybrid-cypher"
    top_k: int = Field(default=5, ge=1, le=25)


@app.post("/api/ask")
async def ask(req: AskRequest) -> dict:
    question = req.question.strip()
    if not question:
        raise HTTPException(400, "question is required")
    if req.retriever == AGENT_MODE:
        return await ask_via_agent(question, req.top_k)
    # The GraphRAG pipeline is synchronous all the way down. Off the event loop
    # it goes, or one question blocks every other request for its whole duration.
    return await run_in_threadpool(ask_via_pipeline, question, req.retriever, req.top_k)


def ask_via_pipeline(question: str, retriever: str, top_k: int) -> dict:
    """One retrieval, one generation — the fixed-strategy path."""
    rag = rag_for(retriever)
    config = {} if retriever == "text2cypher" else {"top_k": top_k}
    result = rag.search(
        query_text=question,
        retriever_config=config,
        return_context=True,
        response_fallback="Nothing in the graph covers that.",
    )

    items = result.retriever_result.items if result.retriever_result else []
    return {
        "answer": result.answer,
        "context": [item.content for item in items],
        "subgraph": evidence_subgraph(question, top_k),
    }


async def ask_via_agent(question: str, top_k: int) -> dict:
    """The agent picks its own retrievers, and may use several.

    Its evidence subgraph comes from the trail its tools left rather than from
    `evidence_subgraph`, so what lights up is what the agent actually read —
    including entities reached by a name lookup that no chunk search returned.
    """
    result = await ask_agent(agent(), question)
    ids = result.trail.entity_ids
    subgraph = await (
        run_in_threadpool(subgraph_for_ids, ids, True)
        if ids
        # No tool was called — a greeting, or a refusal. Fall back to the lookup
        # the fixed retrievers use so the panel is never inexplicably empty.
        else run_in_threadpool(evidence_subgraph, question, top_k)
    )
    return {
        "answer": result.answer,
        # Rendered into the context panel the fixed retrievers use, because the
        # tool calls are this mode's version of "show your working".
        "context": result.trail.calls or ["(the agent answered without calling a tool)"],
        "subgraph": subgraph,
    }


def evidence_subgraph(question: str, top_k: int) -> dict:
    """The entities behind the chunks this question retrieves, plus their neighbours."""
    ids = evidence_entity_ids(state["driver"], state["embedder"], question, top_k)
    return subgraph_for_ids(ids, include_neighbours=True)


# --- staged retrieval, for the streaming unfold ------------------------------

CHUNK_EXCERPT = 180


def retrieved_chunks(question: str, top_k: int) -> list[dict]:
    """The chunks the hybrid lookup actually returns, as graph nodes.

    These are the first thing the answer stands on, so they are the first ring
    the browser draws — before the model has written a word.
    """
    vector = state["embedder"].embed_query(question)
    records = run(
        """
        CALL () {
            CALL db.index.vector.queryNodes($vector_index, $top_k, $vector)
            YIELD node, score RETURN node, score
            UNION
            CALL db.index.fulltext.queryNodes($fulltext_index, $question, {limit: $top_k})
            YIELD node, score RETURN node, score
        }
        WITH node, max(score) AS score ORDER BY score DESC LIMIT $top_k
        OPTIONAL MATCH (node)-[:FROM_DOCUMENT]->(d:Document)
        RETURN elementId(node) AS id, node.text AS text, score,
               coalesce(d.source, d.path) AS source
        """,
        vector_index=VECTOR_INDEX_NAME,
        fulltext_index=FULLTEXT_INDEX_NAME,
        question=question,
        vector=vector,
        top_k=top_k,
    )
    chunks = []
    for r in records:
        text = (r["text"] or "").strip()
        excerpt = text if len(text) <= CHUNK_EXCERPT else text[:CHUNK_EXCERPT].rstrip() + "…"
        chunks.append(
            {
                "id": r["id"],
                "label": "Chunk",
                "name": r["source"] or "chunk",
                "status": None,
                "evidence_levels": [],
                "description": excerpt,
                "text": text,
                "score": r["score"],
                "source": r["source"],
            }
        )
    return chunks


def entities_from_chunks(chunk_ids: list[str]) -> tuple[list[dict], list[dict]]:
    """Entities extracted from those chunks, plus one edge per (entity, chunk).

    The edges are what make the second ring read as *derived from* the first
    rather than merely next to it.
    """
    if not chunk_ids:
        return [], []
    records = run(
        f"""
        MATCH (n:__Entity__)-[:FROM_CHUNK]->(c) WHERE elementId(c) IN $ids
        RETURN {NODE_PROJECTION}, collect(DISTINCT elementId(c)) AS chunks
        """,
        ids=chunk_ids,
    )
    nodes = [node_dict(r) for r in records]
    links = [
        {
            "id": f"chunk:{chunk_id}->{r['id']}",
            "from": chunk_id,
            "to": r["id"],
            "type": "MENTIONS",
            "properties": {},
        }
        for r in records
        for chunk_id in r["chunks"]
    ]
    return nodes, links


#: How many of the surrounding entities the outer ring shows. Every retrieved
#: entity has neighbours, so an uncapped ring is most of the graph again — which
#: is both unreadable and a poor description of what the answer leaned on.
NEIGHBOUR_LIMIT = 20


def neighbours_of(entity_ids: list[str], limit: int = NEIGHBOUR_LIMIT) -> tuple[list[dict], int]:
    """Entities one hop out from the retrieved ones — the graph's own contribution.

    Ranked by how many of the retrieved entities each one ties together, so the
    ring keeps the connectors and drops the long tail of single mentions.
    Returns the capped list and the true total, so the caller can say what it cut.
    """
    if not entity_ids:
        return [], 0
    total = run(
        """
        MATCH (seed:__Entity__) WHERE elementId(seed) IN $ids
        MATCH (seed)-[]-(n:__Entity__) WHERE NOT elementId(n) IN $ids
        RETURN count(DISTINCT n) AS c
        """,
        ids=entity_ids,
    )[0]["c"]
    records = run(
        f"""
        MATCH (seed:__Entity__) WHERE elementId(seed) IN $ids
        MATCH (seed)-[]-(n:__Entity__)
        WHERE NOT elementId(n) IN $ids
        WITH n, count(DISTINCT seed) AS ties
        ORDER BY ties DESC, n.name
        LIMIT $limit
        RETURN {NODE_PROJECTION}, ties
        """,
        ids=entity_ids,
        limit=limit,
    )
    return [node_dict(r) for r in records], total


def relationships_among(ids: list[str]) -> list[dict]:
    if not ids:
        return []
    records = run(
        """
        MATCH (a:__Entity__)-[r]->(b:__Entity__)
        WHERE elementId(a) IN $ids AND elementId(b) IN $ids
        RETURN elementId(r) AS id, elementId(a) AS source, elementId(b) AS target,
               type(r) AS type, properties(r) AS props
        """,
        ids=ids,
    )
    return [
        {
            "id": r["id"],
            "from": r["source"],
            "to": r["target"],
            "type": r["type"],
            "properties": dict(r["props"] or {}),
        }
        for r in records
    ]


#: Buffering proxies will happily hold a whole SSE stream and hand it over as
#: one block at the end, which defeats the point of streaming it.
SSE_HEADERS = {"Cache-Control": "no-store", "X-Accel-Buffering": "no"}


def sse(event: str, payload: dict) -> str:
    """One Server-Sent Event. json.dumps escapes newlines, which SSE framing needs."""
    return f"event: {event}\ndata: {json.dumps(payload)}\n\n"


@app.post("/api/ask/stream")
def ask_stream(req: AskRequest) -> StreamingResponse:
    """The same answer as /api/ask, delivered one pipeline stage at a time.

    The model is the slow part, so it starts first and runs on a worker thread
    while the retrieval rings — chunks, then their entities, then the wider
    neighbourhood — stream out ahead of it.
    """
    question = req.question.strip()
    if not question:
        raise HTTPException(400, "question is required")
    if req.retriever == AGENT_MODE:
        return StreamingResponse(
            agent_stages(question, req.top_k),
            media_type="text/event-stream",
            headers=SSE_HEADERS,
        )
    rag = rag_for(req.retriever)          # raises 400 before the stream opens
    config = {} if req.retriever == "text2cypher" else {"top_k": req.top_k}

    def stages() -> Iterator[str]:
        pool = ThreadPoolExecutor(max_workers=1)
        try:
            pending = pool.submit(
                rag.search,
                query_text=question,
                retriever_config=config,
                return_context=True,
                response_fallback="Nothing in the graph covers that.",
            )
            yield sse("stage", {"name": "retrieving", "label": "Searching the corpus…"})

            try:
                chunks = retrieved_chunks(question, req.top_k)
                yield sse(
                    "unfold",
                    {
                        "stage": "evidence",
                        "label": f"{len(chunks)} passages matched",
                        "nodes": chunks,
                        "relationships": [],
                    },
                )

                entities, links = entities_from_chunks([c["id"] for c in chunks])
                entity_ids = [e["id"] for e in entities]
                yield sse(
                    "unfold",
                    {
                        "stage": "entities",
                        "label": f"{len(entities)} entities extracted from them",
                        "nodes": entities,
                        "relationships": links + relationships_among(entity_ids),
                    },
                )

                yield sse("stage", {"name": "reasoning", "label": "Reasoning over the graph…"})

                nbrs, total = neighbours_of(entity_ids)
                label = (
                    f"{len(nbrs)} of {total} connected entities the graph adds"
                    if total > len(nbrs)
                    else f"{len(nbrs)} connected entities the graph adds"
                )
                yield sse(
                    "unfold",
                    {
                        "stage": "neighbourhood",
                        "label": label,
                        "truncated": total - len(nbrs),
                        "nodes": nbrs,
                        "relationships": relationships_among(
                            entity_ids + [n["id"] for n in nbrs]
                        ),
                    },
                )
            except Exception as exc:                      # noqa: BLE001
                # A failed ring must not cost the viewer the answer.
                yield sse("warning", {"message": f"graph lookup failed: {exc}"})

            result = pending.result()
            items = result.retriever_result.items if result.retriever_result else []
            yield sse(
                "answer",
                {
                    "answer": result.answer,
                    "context": [item.content for item in items],
                },
            )
        except Exception as exc:                          # noqa: BLE001
            yield sse("error", {"message": str(exc)})
        finally:
            pool.shutdown(wait=False)

    return StreamingResponse(
        stages(),
        media_type="text/event-stream",
        headers=SSE_HEADERS,
    )


async def agent_stages(question: str, top_k: int) -> AsyncIterator[str]:
    """The agent's version of the unfold.

    There are no retrieval rings to stream here. The agent decides what to look
    up as it goes, so nothing about the subgraph is known until it stops, and
    guessing at rings ahead of it would light up entities it never read. What
    the stream still buys is the stage line, plus one ring at the end holding
    exactly what the tools touched.
    """
    try:
        yield sse(
            "stage",
            {"name": "reasoning", "label": "The agent is choosing its tools…"},
        )
        result = await ask_via_agent(question, top_k)
        subgraph = result["subgraph"]
        yield sse(
            "unfold",
            {
                "stage": "evidence",
                "label": f"{len(subgraph['nodes'])} entities the agent read",
                "nodes": subgraph["nodes"],
                "relationships": subgraph["relationships"],
            },
        )
        yield sse(
            "answer",
            {"answer": result["answer"], "context": result["context"]},
        )
    except Exception as exc:                              # noqa: BLE001
        yield sse("error", {"message": str(exc)})


@app.middleware("http")
async def no_store(request, call_next):
    """Never cache the front-end. This is a demo you will be editing live, and a
    stale ES module in the browser cache looks exactly like a code bug."""
    response = await call_next(request)
    if request.url.path == "/" or request.url.path.startswith("/static"):
        response.headers["Cache-Control"] = "no-store, must-revalidate"
    return response


@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


def main() -> int:
    parser = argparse.ArgumentParser(description="Serve the graph explorer.")
    parser.add_argument("--host", default="127.0.0.1")
    # PORT is honoured so the server can be handed a free port by whatever
    # launches it; --port still wins when given explicitly.
    parser.add_argument("--port", type=int, default=int(os.getenv("PORT", "8000")))
    parser.add_argument("--reload", action="store_true")
    args = parser.parse_args()

    import uvicorn

    uvicorn.run(
        "graphrag_kit.server:app", host=args.host, port=args.port, reload=args.reload
    )
    return 0


if __name__ == "__main__":
    main()
