"""FastAPI backend for the graph explorer.

The interesting endpoint is POST /api/ask. It does two things with one question:

  1. answers it through the GraphRAG pipeline, and
  2. returns the exact subgraph the answer was drawn from,

so the front-end can light up the evidence instead of asking you to trust a
paragraph of prose. Step 2 re-runs the vector/fulltext lookup itself rather than
parsing GraphRAG's context string, because the retriever hands back formatted text
and the front-end needs element IDs.
"""

from __future__ import annotations

import argparse
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from neo4j_graphrag.generation import GraphRAG
from neo4j_graphrag.generation.prompts import RagTemplate
from pydantic import BaseModel, Field

from graphrag_kit.config import (
    ENTITY_FULLTEXT_INDEX_NAME,
    FULLTEXT_INDEX_NAME,
    VECTOR_INDEX_NAME,
    get_database,
    get_driver,
    get_embedder,
    get_llm,
)
from graphrag_kit.project import load_project
from graphrag_kit.retrievers import RETRIEVERS, build_rag_prompt

STATIC_DIR = Path(__file__).resolve().parent / "static"
RESERVED_LABELS = {"__Entity__", "__KGBuilder__"}

state: dict[str, Any] = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    state["project"] = load_project()
    state["driver"] = get_driver()
    state["database"] = get_database()
    state["embedder"] = get_embedder()
    state["llm"] = get_llm()
    state["rag"] = {}
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
        "retrievers": sorted(RETRIEVERS),
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
def ask(req: AskRequest) -> dict:
    question = req.question.strip()
    if not question:
        raise HTTPException(400, "question is required")

    rag = rag_for(req.retriever)
    config = {} if req.retriever == "text2cypher" else {"top_k": req.top_k}
    result = rag.search(
        query_text=question,
        retriever_config=config,
        return_context=True,
        response_fallback="Nothing in the graph covers that.",
    )

    items = result.retriever_result.items if result.retriever_result else []
    context = [item.content for item in items]
    return {
        "answer": result.answer,
        "context": context,
        "subgraph": evidence_subgraph(question, req.top_k),
    }


def evidence_subgraph(question: str, top_k: int) -> dict:
    """The POLE entities behind the chunks this question retrieves.

    Deliberately a second lookup rather than a parse of GraphRAG's context: the
    retriever returns rendered text, and the front-end needs element IDs to
    highlight nodes.
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
        MATCH (e:__Entity__)-[:FROM_CHUNK]->(node)
        RETURN DISTINCT elementId(e) AS id
        """,
        vector_index=VECTOR_INDEX_NAME,
        fulltext_index=FULLTEXT_INDEX_NAME,
        question=question,
        vector=vector,
        top_k=top_k,
    )
    return subgraph_for_ids([r["id"] for r in records], include_neighbours=True)


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
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--reload", action="store_true")
    args = parser.parse_args()

    import uvicorn

    uvicorn.run(
        "graphrag_kit.server:app", host=args.host, port=args.port, reload=args.reload
    )
    return 0


if __name__ == "__main__":
    main()
