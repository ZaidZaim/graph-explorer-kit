"""FastAPI backend for the graph explorer.

The interesting endpoint is POST /api/ask. It does two things with one question:

  1. answers it through the GraphRAG pipeline, and
  2. returns the exact subgraph the answer was drawn from,

so the front-end can light up the evidence instead of asking you to trust a
paragraph of prose. Step 2 re-runs the vector/fulltext lookup itself rather than
parsing GraphRAG's context string, because the retriever hands back formatted text
and the front-end needs element IDs.

The same endpoint serves the Microsoft Agent Framework agent, addressed as one
more entry in the retriever list. Its evidence subgraph needs no second lookup:
the agent's tools record what they read as they go.
"""

from __future__ import annotations

import argparse
import os
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from neo4j_graphrag.generation import GraphRAG
from neo4j_graphrag.generation.prompts import RagTemplate
from pydantic import BaseModel, Field

from graphrag_kit.agent import ask_agent, build_agent
from graphrag_kit.config import (
    ENTITY_FULLTEXT_INDEX_NAME,
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
