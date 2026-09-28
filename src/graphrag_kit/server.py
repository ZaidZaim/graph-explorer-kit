"""FastAPI backend for the graph explorer.

The interesting endpoint is POST /api/ask. It does two things with one question:

  1. answers it through the GraphRAG pipeline, and
  2. returns the exact subgraph the answer was drawn from,

so the front-end can light up the evidence instead of asking you to trust a
paragraph of prose. Step 2 re-runs the vector/fulltext lookup itself rather than
parsing GraphRAG's context string, because the retriever hands back formatted
text and the front-end needs element IDs.

POST /api/ask/stream does the same work as Server-Sent Events, one event per
stage of the pipeline, so the graph can unfold in step with the reasoning rather
than appearing all at once when the model finally finishes. The LLM call is
handed to a worker thread first, so the retrieval rings reach the browser while
the model is still writing.

Both endpoints also serve the Microsoft Agent Framework agent, addressed as one
more entry in the retriever list. Its evidence subgraph needs no second lookup:
the agent's tools record what they read as they go.

Two endpoints exist for understanding the graph rather than querying it:
GET /api/schema returns the project's schema as a graph — the POLE model itself,
with live counts — and GET /api/documents lists the corpus the graph was built
from. POST /api/documents extends it: upload a file and the same pipeline that
built the graph runs over it, streaming what it found.

Every label and property name here comes from the active ProjectSpec, so the
engine reads a graph another tool built without rewriting anyone's data.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import shutil
import tempfile
from collections.abc import AsyncIterator, Iterator
from concurrent.futures import ThreadPoolExecutor
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import FileResponse, Response, StreamingResponse
from fastapi.staticfiles import StaticFiles
from neo4j_graphrag.generation import GraphRAG
from neo4j_graphrag.generation.prompts import RagTemplate
from pydantic import BaseModel, Field

from graphrag_kit.adopt import blocking_constraints
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
from graphrag_kit.cypher import (
    evidence_expr,
    label_expr,
    lucene_escape,
    name_expr,
    source_name_expr,
)
from graphrag_kit.ingest import SUPPORTED_SUFFIXES, ingest_files
from graphrag_kit.memory import (
    Conversations,
    describe_memory,
    memory_wanted,
    new_session_id,
    open_memory,
    standalone_question,
)
from graphrag_kit.project import ProjectSpec, load_project
from graphrag_kit.retrievers import RETRIEVERS, build_rag_prompt, evidence_entity_ids

STATIC_DIR = Path(__file__).resolve().parent / "static"

#: Selectable alongside the retrievers, but not one of them: it *uses* them.
AGENT_MODE = "agent"

state: dict[str, Any] = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    state["project"] = load_project()
    print(f"project: {state['project'].key} ({state['project'].title})")
    print(f"models: {describe_models()}")
    print(f"agent:  {describe_agent_model()}")
    state["driver"] = get_driver()
    state["database"] = get_database()
    state["embedder"] = get_embedder()
    state["llm"] = get_llm()
    state["rag"] = {}
    state["agent"] = None
    # Conversations are opened on the first question that carries a session id.
    # Connecting the memory store sets up its own indexes, which takes a while
    # the first time, and a misconfigured store should cost the conversation
    # features, not the explorer.
    state["conversations"] = None
    state["conversations_lock"] = asyncio.Lock()
    # One ingest at a time. Two concurrent runs over the same corpus race on
    # entity resolution and produce duplicates that look like extraction bugs.
    state["ingest_lock"] = asyncio.Lock()
    yield
    if state.get("conversations") is not None:
        await state["conversations"].close()
    await state["llm"].aclose()
    state["driver"].close()


app = FastAPI(title="GraphRAG Explorer", lifespan=lifespan)


def spec() -> ProjectSpec:
    return state["project"]


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
                template=build_rag_prompt(spec()),
                expected_inputs=["context", "query_text", "examples"],
            ),
        )
    return state["rag"][retriever_name]


async def conversations() -> Conversations:
    """The conversation registry, and the memory behind it, opened on first use."""
    async with state["conversations_lock"]:
        if state["conversations"] is None:
            memory = None
            if memory_wanted():
                try:
                    memory = await open_memory()
                except Exception as exc:  # noqa: BLE001 - degrade, do not fail the ask
                    print(f"memory: unavailable ({exc}); keeping history in process")
            print(f"memory: {describe_memory(memory)}")
            state["conversations"] = Conversations(state["driver"], spec(), memory)
        return state["conversations"]


def agent():
    """The Agent Framework agent, built on first use.

    Deliberately lazy. It needs a chat client the retrievers do not — a different
    API surface, and on Azure a different api-version — so a misconfigured agent
    would otherwise take the whole explorer down at startup instead of failing
    only the requests that ask for it.
    """
    if state["agent"] is None:
        state["agent"] = build_agent(state["driver"], spec())
    return state["agent"]


# --- graph serialisation ----------------------------------------------------

#: Property keys never sent to the browser. Embedding vectors are megabytes of
#: floats that no view uses, and some are Neo4j VECTOR values that do not
#: serialise to JSON at all; `__id__` and friends are the writer's bookkeeping.
HIDDEN_PROPERTY_KEYS = {"__id__", "id", "index", "embedding"}


def visible_properties(props: dict | None) -> dict:
    """Everything worth showing about a node, in a shape JSON can carry.

    Properties are passed through wholesale rather than picked from a fixed list:
    an Observation's shape, movement, speed and altitude are the substance of
    this corpus, and a projection naming columns in advance shows none of them.
    """
    out = {}
    for key, value in (props or {}).items():
        if key in HIDDEN_PROPERTY_KEYS or "embedding" in key.lower():
            continue
        if isinstance(value, (str, int, float, bool)) or value is None:
            out[key] = value
        elif isinstance(value, (list, tuple)):
            # Lists of scalars are fine (evidence_levels); anything else is a
            # vector or a nested structure with no view behind it.
            if all(isinstance(v, (str, int, float, bool)) for v in value) and len(value) <= 32:
                out[key] = list(value)
        else:
            out[key] = str(value)
    return out


def node_projection() -> str:
    """RETURN clause for one entity, built from the project's naming rules."""
    return f"""
      elementId(n) AS id,
      {label_expr('n')} AS label,
      {name_expr('n', spec())} AS name,
      {evidence_expr('n', spec())} AS status,
      properties(n) AS props
    """


def node_dict(record) -> dict:
    label = record["label"]
    props = visible_properties(record["props"])
    return {
        "id": record["id"],
        "label": label,
        "group": spec().group_of(label),
        "name": record["name"] or "(unnamed)",
        "status": record["status"],
        "evidence_levels": props.get("evidence_levels") or [],
        "description": props.get("description"),
        "properties": props,
    }


def rel_dict(record) -> dict:
    return {
        "id": record["id"],
        "from": record["source"],
        "to": record["target"],
        "type": record["type"],
        "properties": visible_properties(record["props"]),
    }


RELATIONSHIPS_AMONG = """
MATCH (a:__Entity__)-[r]->(b:__Entity__)
WHERE elementId(a) IN $ids AND elementId(b) IN $ids
RETURN elementId(r) AS id, elementId(a) AS source, elementId(b) AS target,
       type(r) AS type, properties(r) AS props
"""


def relationships_among(ids: list[str]) -> list[dict]:
    if not ids:
        return []
    return [rel_dict(r) for r in run(RELATIONSHIPS_AMONG, ids=ids)]


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
            RETURN {node_projection()}
            """,
            ids=ids,
        )
    else:
        node_records = run(
            f"MATCH (n:__Entity__) WHERE elementId(n) IN $ids RETURN {node_projection()}",
            ids=ids,
        )

    nodes = [node_dict(r) for r in node_records]
    return {
        "nodes": nodes,
        "relationships": relationships_among([n["id"] for n in nodes]),
        "seeds": ids,
    }


# --- API --------------------------------------------------------------------


def label_counts() -> dict[str, int]:
    records = run(
        """
        MATCH (n:__Entity__)
        UNWIND labels(n) AS label
        WITH label WHERE NOT label IN ['__Entity__','__KGBuilder__']
        RETURN label, count(*) AS count ORDER BY count DESC
        """
    )
    return {r["label"]: r["count"] for r in records}


@app.get("/api/meta")
def meta() -> dict:
    project = spec()
    lex = project.lexical
    counts = label_counts()
    isolated = run(
        "MATCH (n:__Entity__) WHERE NOT (n)-[]-(:__Entity__) RETURN count(n) AS c"
    )[0]["c"]
    docs = run(f"MATCH (d:`{lex.source_label}`) RETURN count(d) AS c")[0]["c"]
    chunks = run(f"MATCH (c:`{lex.chunk_label}`) RETURN count(c) AS c")[0]["c"]
    rels = run("MATCH (:__Entity__)-[r]->(:__Entity__) RETURN count(r) AS c")[0]["c"]

    payload = {
        "project": project.key,
        "title": project.title,
        "subtitle": project.subtitle,
        "examples": project.example_questions,
        "labels": project.labels,
        "colors": project.label_colors,
        "groups": {group: list(members) for group, members in project.groups.items()},
        "groupColors": project.group_colors,
        "retrievers": sorted(RETRIEVERS) + [AGENT_MODE],
        "counts": counts,
        "isolated": isolated,
        "documents": docs,
        "chunks": chunks,
        "relationships": rels,
        "gradesEvidence": project.grades_evidence,
        "evidenceLevels": list(project.evidence_levels),
        "hasTimeline": bool(project.date_property),
        "uploadSuffixes": sorted(SUPPORTED_SUFFIXES),
        # What the records view draws at most, so the UI can say what it cut.
        "graphLimit": GRAPH_LIMIT,
        "memory": memory_wanted(),
    }
    if project.grades_evidence:
        statuses = run(
            f"MATCH (n:__Entity__) RETURN {evidence_expr('n', project)} AS status, "
            f"count(*) AS count ORDER BY count DESC"
        )
        payload["statuses"] = {r["status"]: r["count"] for r in statuses}
    else:
        payload["statuses"] = {}
    return payload


@app.get("/api/schema")
def schema() -> dict:
    """The project's schema as a graph, with live counts.

    The point of a POLE demo is the model, not just the data: this is what the
    analyst is being taught, so it is served as a first-class view rather than
    left implicit in the colours of the node circles.
    """
    project = spec()
    counts = label_counts()
    rel_counts = {
        r["type"]: r["count"]
        for r in run(
            "MATCH (:__Entity__)-[r]->(:__Entity__) "
            "RETURN type(r) AS type, count(*) AS count"
        )
    }
    nodes = [
        {
            "id": node.label,
            "label": node.label,
            "group": project.group_of(node.label),
            "name": node.label,
            "description": node.description,
            "count": counts.get(node.label, 0),
            "properties": [
                {"name": p.name, "type": p.type, "description": p.description}
                for p in (node.properties or [])
            ],
        }
        for node in project.schema.node_types
    ]
    described = {rel.label: rel.description for rel in project.schema.relationship_types}
    # One edge per (start, type, end) pattern, which is what the schema actually
    # licenses — a bare list of relationship types cannot say what connects to what.
    relationships = [
        {
            "id": f"{start}-{rel_type}-{end}",
            "from": start,
            "to": end,
            "type": rel_type,
            "description": described.get(rel_type),
            "count": rel_counts.get(rel_type, 0),
        }
        for start, rel_type, end in (project.schema.patterns or [])
    ]
    return {
        "nodes": nodes,
        "relationships": relationships,
        "groups": {group: list(members) for group, members in project.groups.items()},
        "unused": [label for label in project.labels if not counts.get(label)],
    }


@app.get("/api/overview")
def overview(labels: str | None = None) -> dict:
    """The graph aggregated by type: one node per label, one edge per pattern.

    This is the default view, and the reason is legibility. A thousand records
    drawn at once is a disc of overlapping dots — every label is true, none is
    readable, and the structure that makes it a graph is invisible. Rolled up by
    type it is a dozen nodes and the shape of the corpus is obvious at a glance:
    Document mentions everything, Observation hangs off Event, Witness hangs off
    Observation. The instances are one click away.

    Unlike /api/schema this counts what is actually in the graph, so the edges
    carry weights and a pattern the schema allows but the corpus never uses does
    not appear at all.
    """
    project = spec()
    wanted = [x for x in (labels or "").split(",") if x] or project.labels
    counts = label_counts()
    records = run(
        f"""
        MATCH (a:__Entity__)-[r]->(b:__Entity__)
        WITH {label_expr('a')} AS from_label, type(r) AS rel_type,
             {label_expr('b')} AS to_label, count(*) AS weight
        WHERE from_label IN $labels AND to_label IN $labels
        RETURN from_label, rel_type, to_label, weight
        ORDER BY weight DESC
        """,
        labels=wanted,
    )
    nodes = [
        {
            "id": label,
            "label": label,
            "group": project.group_of(label),
            "name": f"{label} ({counts.get(label, 0)})",
            "count": counts.get(label, 0),
            "status": None,
            "evidence_levels": [],
            "description": None,
            "properties": {},
            "aggregate": True,
        }
        for label in wanted
        if counts.get(label)
    ]
    return {
        "nodes": nodes,
        "relationships": [
            {
                "id": f"{r['from_label']}-{r['rel_type']}-{r['to_label']}",
                "from": r["from_label"],
                "to": r["to_label"],
                # The weight rides on the edge label: an aggregate edge that does
                # not say how many relationships it stands for is a lie of
                # omission — MENTIONS ×349 and SAME_AS ×1 would look identical.
                "type": f"{r['rel_type']} ×{r['weight']}",
                "properties": {"count": r["weight"], "relationship": r["rel_type"]},
            }
            for r in records
        ],
    }


#: The most records the records view returns at once, and the ceiling a caller
#: may raise it to. Fifty thousand records is not a picture, it is a browser
#: tab that stops responding: the force layout is quadratic in the worst case,
#: every edge is drawn every frame, and the JSON alone is tens of megabytes.
#: The most connected records carry the structure, so those are the ones kept,
#: and the true total goes back with them.
GRAPH_LIMIT = int(os.getenv("GRAPH_RENDER_LIMIT", "400"))
GRAPH_LIMIT_CEILING = 6000


@app.get("/api/graph")
def graph(
    labels: str | None = None,
    status: str | None = None,
    connected: bool = True,
    limit: int | None = None,
) -> dict:
    """The entity graph, optionally filtered by label and evidence level.

    `connected` drops entities that take part in no relationship at all. They
    are a third of this corpus — extraction finds a place name in a scanned
    table and has nothing to attach it to — and as a default view they are a
    field of unreadable dust around the structure worth looking at. The count
    is reported in /api/meta so the UI can offer them rather than hide them.

    `limit` caps the records returned; `shown` and `total` say what was cut.
    Filtering happens before the cap, so narrowing to one type or one evidence
    level gets that type's most connected records rather than whatever of it
    survived a global cut.

    Which records make the cut decides whether the result is a picture or a
    field of dust — and of what. The top-N by degree alone is dust: each hub's
    edges mostly lead to records outside the top N. Seeds plus the neighbours
    that tie them together is a web, but a web of Documents, because in a
    corpus of records the documents are what mention everything else, and by
    degree they win every seat. So the budget is shared out by type: every
    type present gets seats for its most connected records, the rest of the
    budget goes to the neighbours that tie the most seeds together, and no
    single type may take more than a fifth of the picture. What is drawn is
    the spine of the model — events at places, observations of objects by
    witnesses, agencies and the documents that name them — as a connected
    graph, rather than the one label that happens to have the most edges.
    """
    project = spec()
    cap = max(1, min(limit or GRAPH_LIMIT, GRAPH_LIMIT_CEILING))
    wanted_labels = [x for x in (labels or "").split(",") if x] or project.labels
    params: dict[str, Any] = {"labels": wanted_labels}
    if project.grades_evidence:
        params["status"] = [x for x in (status or "").split(",") if x] or list(
            project.evidence_levels
        )

    def filters(var: str) -> list[str]:
        """The view's filters as WHERE clauses on `var`, so the same filter can
        be applied to a node and, later, to a neighbour under another name."""
        out = [f"any(l IN labels({var}) WHERE l IN $labels)"]
        if connected:
            out.append(f"({var})-[]-(:__Entity__)")
        if project.grades_evidence:
            out.append(f"{evidence_expr(var, project)} IN $status")
        return out

    clauses = filters("n")
    total = run(
        f"MATCH (n:__Entity__) WHERE {' AND '.join(clauses)} RETURN count(n) AS c",
        **params,
    )[0]["c"]
    where = " AND ".join(clauses)
    per_label_ceiling = max(8, cap // 5)
    per_label_seeds = max(3, cap // (4 * max(1, len(wanted_labels))))
    # Seeds: each type's most connected records, so every type present is in
    # the picture from the start.
    seeds = run(
        f"""
        MATCH (n:__Entity__)
        WHERE {where}
        WITH n, {label_expr("n")} AS label, count {{ (n)-[]-(:__Entity__) }} AS degree
        ORDER BY degree DESC, n.name
        WITH label, collect(elementId(n))[..$per_label] AS ids
        UNWIND ids AS id
        RETURN id, label
        """,
        per_label=per_label_seeds,
        **params,
    )
    taken: dict[str, int] = {}
    ids: list[str] = []
    for r in seeds:
        if len(ids) >= cap:
            break
        ids.append(r["id"])
        taken[r["label"]] = taken.get(r["label"], 0) + 1
    # Fill: the neighbours that tie the most seeds together, best first, each
    # type capped so the documents that mention everything cannot crowd out the
    # records they mention. The same filters apply to the neighbours (`n` is
    # the variable the clauses name), so a view narrowed to Agencies draws
    # agencies, not their documents.
    seed_ids = list(ids)
    candidates = run(
        f"""
        MATCH (s:__Entity__) WHERE elementId(s) IN $seed_ids
        MATCH (s)-[]-(n:__Entity__)
        WHERE NOT elementId(n) IN $seed_ids AND {where}
        WITH n, count(DISTINCT s) AS ties, count {{ (n)-[]-(:__Entity__) }} AS degree
        ORDER BY ties DESC, degree DESC, n.name
        LIMIT $limit
        RETURN elementId(n) AS id, {label_expr("n")} AS label
        """,
        seed_ids=seed_ids,
        limit=max(0, cap - len(seed_ids)) * 12,
        **params,
    )
    # Two passes: with the ceiling, then — if seats are still empty because the
    # pool was mostly one type — without it. A full picture of the corpus as
    # it is beats an empty seat kept for a type that has nothing more to add.
    chosen = set(ids)
    for enforce_ceiling in (True, False):
        for r in candidates:
            if len(ids) >= cap:
                break
            if r["id"] in chosen:
                continue
            if enforce_ceiling and taken.get(r["label"], 0) >= per_label_ceiling:
                continue
            ids.append(r["id"])
            chosen.add(r["id"])
            taken[r["label"]] = taken.get(r["label"], 0) + 1
    # A seed from a small type — a Release, a Redaction — may connect to nothing
    # else on screen. Give each one its best neighbour while seats remain within
    # the cap, and leave out whatever is still alone: a dot with no edge says
    # nothing about a graph.
    lonely = run(
        """
        MATCH (n:__Entity__) WHERE elementId(n) IN $ids
        AND NOT EXISTS { (n)-[]-(m:__Entity__) WHERE elementId(m) IN $ids }
        RETURN elementId(n) AS id
        """,
        ids=ids,
    )
    lonely_ids = [r["id"] for r in lonely]
    if lonely_ids:
        companions = run(
            f"""
            MATCH (n:__Entity__) WHERE elementId(n) IN $lonely
            MATCH (n)-[]-(m:__Entity__)
            WHERE NOT elementId(m) IN $ids AND {" AND ".join(filters("m"))}
            WITH n, m, count {{ (m)-[]-(:__Entity__) }} AS degree
            ORDER BY degree DESC
            WITH n, head(collect(elementId(m))) AS best
            RETURN elementId(n) AS id, best
            """,
            lonely=lonely_ids,
            ids=ids,
            **params,
        )
        rescued = set()
        for r in companions:
            if r["best"] is None:
                continue
            if r["best"] in chosen:
                rescued.add(r["id"])
                continue
            if len(ids) >= cap:
                break
            ids.append(r["best"])
            chosen.add(r["best"])
            rescued.add(r["id"])
        ids = [i for i in ids if i not in set(lonely_ids) - rescued]
    records = run(
        f"MATCH (n:__Entity__) WHERE elementId(n) IN $ids RETURN {node_projection()}",
        ids=ids,
    )
    nodes = [node_dict(r) for r in records]
    return {
        "nodes": nodes,
        "relationships": relationships_among([n["id"] for n in nodes]),
        "shown": len(nodes),
        "total": total,
        "limit": cap,
    }


#: Instances drawn when drilling into one type. Each one brings its neighbours,
#: so thirty Observations arrive as roughly a hundred nodes — which is about
#: where a force layout stops being a picture and starts being a blob. The true
#: total goes back with them, so the view never implies it is showing everything.
INSTANCE_LIMIT = 30


@app.get("/api/instances")
def instances(label: str, limit: int = INSTANCE_LIMIT) -> dict:
    """Records of one type, with their neighbours — the drill-down from the
    aggregate overview.

    Ordered by connectedness, because that is what makes a legible picture: the
    records that tie the most others together carry the structure, and a random
    hundred Observations tell you nothing about how Observations sit in the graph.
    """
    project = spec()
    if label not in project.labels:
        raise HTTPException(400, f"unknown label {label!r}")
    total = run(
        f"MATCH (n:`{label}`:__Entity__) RETURN count(n) AS c",
    )[0]["c"]
    seeds = run(
        f"""
        MATCH (n:`{label}`:__Entity__)
        WITH n, count {{ (n)-[]-(:__Entity__) }} AS degree
        ORDER BY degree DESC, n.name
        LIMIT $limit
        RETURN elementId(n) AS id
        """,
        limit=max(1, min(limit, 400)),
    )
    subgraph = subgraph_for_ids([r["id"] for r in seeds], include_neighbours=True)
    return {
        **subgraph,
        "label": label,
        "shown": len(seeds),
        "total": total,
    }


#: Neighbours pulled in when a node is expanded in place. A hub like "FBI" has
#: five hundred; drawn all at once they bury the node that was expanded. The
#: most connected come first, and the total goes back so the note can say
#: "+60 of 533".
EXPAND_LIMIT = 60


@app.get("/api/expand")
def expand(id: str, limit: int = EXPAND_LIMIT) -> dict:
    """One node, its most connected neighbours up to `limit`, and every edge
    among them — the unit of Aura-style expansion: double-click, and the
    graph grows outward from that node without redrawing the rest."""
    cap = max(1, min(limit, 400))
    total = run(
        """
        MATCH (seed:__Entity__) WHERE elementId(seed) = $id
        MATCH (seed)-[]-(nbr:__Entity__)
        RETURN count(DISTINCT nbr) AS c
        """,
        id=id,
    )
    if not total:
        raise HTTPException(404, "no such node")
    records = run(
        f"""
        MATCH (seed:__Entity__) WHERE elementId(seed) = $id
        OPTIONAL MATCH (seed)-[]-(nbr:__Entity__)
        WITH seed, nbr, count {{ (nbr)-[]-(:__Entity__) }} AS degree
        ORDER BY degree DESC, nbr.name
        WITH seed, [x IN collect(DISTINCT nbr) WHERE x IS NOT NULL][..$limit] AS nbrs
        UNWIND [seed] + nbrs AS n
        RETURN {node_projection()}
        """,
        id=id,
        limit=cap,
    )
    nodes = [node_dict(r) for r in records]
    return {
        "nodes": nodes,
        "relationships": relationships_among([n["id"] for n in nodes]),
        "seeds": [id],
        "shown": max(0, len(nodes) - 1),
        "total": total[0]["c"],
    }


@app.get("/api/search")
def search(q: str, limit: int = 15) -> dict:
    if not q.strip():
        return {"nodes": []}
    records = run(
        f"""
        CALL db.index.fulltext.queryNodes($index, $q, {{limit: $limit}})
        YIELD node AS n, score
        RETURN {node_projection()}, score
        """,
        index=ENTITY_FULLTEXT_INDEX_NAME,
        q=lucene_escape(q),
        limit=limit,
    )
    return {"nodes": [node_dict(r) for r in records]}


#: Dated records the timeline lists. Thousands of rows is a scroll, not a
#: timeline; the most connected dated records are the ones worth a line.
TIMELINE_LIMIT = 600


@app.get("/api/timeline")
def timeline(limit: int = TIMELINE_LIMIT) -> dict:
    """Dated entities in order — a timeline view, when the schema has dates."""
    project = spec()
    if not project.date_property:
        return {"nodes": []}
    total = run(
        f"MATCH (n:__Entity__) WHERE n.`{project.date_property}` IS NOT NULL RETURN count(n) AS c"
    )[0]["c"]
    records = run(
        f"""
        MATCH (n:__Entity__) WHERE n.`{project.date_property}` IS NOT NULL
        WITH n, count {{ (n)-[]-(:__Entity__) }} AS degree
        ORDER BY degree DESC LIMIT $limit
        WITH n, n.`{project.date_property}` AS date ORDER BY date
        RETURN {node_projection()}, date
        """,
        limit=max(1, min(limit, GRAPH_LIMIT_CEILING)),
    )
    return {
        "nodes": [{**node_dict(r), "date": r["date"]} for r in records],
        "dateProperty": project.date_property,
        "shown": len(records),
        "total": total,
    }


@app.get("/api/documents")
def documents() -> dict:
    """The corpus behind the graph: source files, and how much each contributed."""
    project = spec()
    lex = project.lexical
    records = run(
        f"""
        MATCH (d:`{lex.source_label}`)
        OPTIONAL MATCH (c:`{lex.chunk_label}`)-[:{lex.chunk_to_source}]->(d)
        OPTIONAL MATCH (e:__Entity__)-[:{lex.entity_to_chunk}]->(c)
        RETURN elementId(d) AS id,
               {source_name_expr('d', project)} AS name,
               count(DISTINCT c) AS chunks,
               count(DISTINCT e) AS entities
        ORDER BY name
        """
    )
    return {
        "sources": [
            {
                "id": r["id"],
                "name": r["name"] or "(unnamed)",
                "chunks": r["chunks"],
                "entities": r["entities"],
            }
            for r in records
        ]
    }


class AskRequest(BaseModel):
    question: str
    retriever: str = "hybrid-cypher"
    top_k: int = Field(default=5, ge=1, le=25)
    #: A conversation to continue. Omitted, the question is answered on its own,
    #: exactly as before conversations existed. Any non-empty string is a valid
    #: id; the browser mints one per thread.
    session_id: str | None = Field(default=None, max_length=128)


def clean_session_id(value: str | None) -> str | None:
    value = (value or "").strip()
    return value or None


@app.post("/api/ask")
async def ask(req: AskRequest) -> dict:
    question = req.question.strip()
    if not question:
        raise HTTPException(400, "question is required")
    session_id = clean_session_id(req.session_id)
    if req.retriever == AGENT_MODE:
        return await ask_via_agent(question, req.top_k, session_id)
    # A follow-up ("and in 1949?") is rewritten against the conversation before
    # it is embedded; the rewrite is returned so nothing happens silently.
    asked, interpreted = question, None
    if session_id:
        turns = await (await conversations()).recent_turns(session_id)
        asked = await run_in_threadpool(standalone_question, state["llm"], turns, question)
        interpreted = asked if asked != question else None
    # The GraphRAG pipeline is synchronous all the way down. Off the event loop
    # it goes, or one question blocks every other request for its whole duration.
    result = await run_in_threadpool(ask_via_pipeline, asked, req.retriever, req.top_k)
    if session_id:
        await (await conversations()).record(session_id, question, result["answer"], req.retriever)
    return {**result, "interpreted": interpreted, "session_id": session_id}


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


#: How much of the agent's trail is drawn. An agent that calls nine tools reads
#: several hundred entities, and all of them plus their neighbours is a thousand
#: nodes in a single ring — a smear of edges, not a picture of the evidence.
#: The count it read is reported either way.
AGENT_EVIDENCE_LIMIT = 24


def most_connected(ids: list[str], limit: int) -> list[str]:
    """The `limit` most connected of `ids`. Connectedness is the right ranking
    for a picture of evidence: the entities tying the most others together are
    the ones that explain how the rest hang off them."""
    if len(ids) <= limit:
        return ids
    records = run(
        """
        MATCH (n:__Entity__) WHERE elementId(n) IN $ids
        RETURN elementId(n) AS id, count { (n)-[]-(:__Entity__) } AS degree
        ORDER BY degree DESC, n.name
        LIMIT $limit
        """,
        ids=ids,
        limit=limit,
    )
    return [r["id"] for r in records]


async def ask_via_agent(question: str, top_k: int, session_id: str | None = None) -> dict:
    """The agent picks its own retrievers, and may use several.

    Its evidence subgraph comes from the trail its tools left rather than from
    `evidence_subgraph`, so what lights up is what the agent actually read —
    including entities reached by a name lookup that no chunk search returned.

    With a session id the question is a turn in a conversation: the agent sees
    the earlier turns, and this one is written to the transcript and recorded
    as a reasoning trace (see memory.py). Without one it is stateless.
    """
    if session_id:
        result = await (await conversations()).ask(session_id, question)
    else:
        result = await ask_agent(agent(), question)
    ids = result.trail.entity_ids
    if ids:
        shown = await run_in_threadpool(most_connected, ids, AGENT_EVIDENCE_LIMIT)
        # No neighbour expansion here: the agent's own trail already records the
        # neighbours its lookups returned, and expanding on top of that is what
        # turns two dozen entities back into several hundred.
        subgraph = await run_in_threadpool(subgraph_for_ids, shown, False)
    else:
        # No tool was called — a greeting, or a refusal. Fall back to the lookup
        # the fixed retrievers use so the panel is never inexplicably empty.
        subgraph = await run_in_threadpool(evidence_subgraph, question, top_k)
    return {
        "answer": result.answer,
        # Rendered into the context panel the fixed retrievers use, because the
        # tool calls are this mode's version of "show your working".
        "context": result.trail.calls or ["(the agent answered without calling a tool)"],
        "subgraph": subgraph,
        "read": len(ids),
        "session_id": session_id,
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
    project = spec()
    lex = project.lexical
    vector = state["embedder"].embed_query(question)
    records = run(
        f"""
        CALL () {{
            CALL db.index.vector.queryNodes($vector_index, $top_k, $vector)
            YIELD node, score RETURN node, score
            UNION
            CALL db.index.fulltext.queryNodes($fulltext_index, $question, {{limit: $top_k}})
            YIELD node, score RETURN node, score
        }}
        WITH node, max(score) AS score ORDER BY score DESC LIMIT $top_k
        OPTIONAL MATCH (node)-[:{lex.chunk_to_source}]->(d:`{lex.source_label}`)
        RETURN elementId(node) AS id, node.`{lex.text_property}` AS text, score,
               {source_name_expr('d', project)} AS source
        """,
        vector_index=VECTOR_INDEX_NAME,
        fulltext_index=FULLTEXT_INDEX_NAME,
        question=lucene_escape(question),
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
                "label": lex.chunk_label,
                "group": None,
                "name": r["source"] or "chunk",
                "status": None,
                "evidence_levels": [],
                "description": excerpt,
                "properties": {},
                "text": text,
                "score": r["score"],
                "source": r["source"],
            }
        )
    return chunks


#: How many extracted entities the second ring shows. A 700-token passage of a
#: scanned report can carry eighty extracted records, so five passages reach a
#: hundred and fifty — more than the fan can lay out and more than anyone reads.
#: The ones kept are those the retrieved passages have in common.
ENTITY_RING_LIMIT = 16


def entities_from_chunks(chunk_ids: list[str]) -> tuple[list[dict], list[dict], int]:
    """Entities extracted from those chunks, plus one edge per (entity, chunk).

    The edges are what make the second ring read as *derived from* the first
    rather than merely next to it. Returns the capped list, those edges, and the
    true total so the caller can say what it cut.
    """
    if not chunk_ids:
        return [], [], 0
    total = run(
        f"""
        MATCH (n:__Entity__)-[:{spec().lexical.entity_to_chunk}]->(c)
        WHERE elementId(c) IN $ids
        RETURN count(DISTINCT n) AS c
        """,
        ids=chunk_ids,
    )[0]["c"]
    records = run(
        f"""
        MATCH (n:__Entity__)-[:{spec().lexical.entity_to_chunk}]->(c)
        WHERE elementId(c) IN $ids
        WITH n, collect(DISTINCT elementId(c)) AS chunks
        // Entities several retrieved passages agree on first: those are what the
        // question actually landed on, rather than the long tail of one-offs.
        ORDER BY size(chunks) DESC, n.name
        LIMIT $limit
        RETURN {node_projection()}, chunks
        """,
        ids=chunk_ids,
        limit=ENTITY_RING_LIMIT,
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
    return nodes, links, total


#: How many of the surrounding entities the outer ring shows. Every retrieved
#: entity has neighbours, so an uncapped ring is most of the graph again — which
#: is both unreadable and a poor description of what the answer leaned on.
#: With the passage and entity rings, this lands the whole unfold just under the
#: explorer's caption ceiling, so an answer's evidence is drawn with every
#: circle named and every relationship typed.
NEIGHBOUR_LIMIT = 8


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
        RETURN {node_projection()}, ties
        """,
        ids=entity_ids,
        limit=limit,
    )
    return [node_dict(r) for r in records], total


#: Buffering proxies will happily hold a whole SSE stream and hand it over as
#: one block at the end, which defeats the point of streaming it.
SSE_HEADERS = {"Cache-Control": "no-store", "X-Accel-Buffering": "no"}


def sse(event: str, payload: dict) -> str:
    """One Server-Sent Event. json.dumps escapes newlines, which SSE framing needs."""
    return f"event: {event}\ndata: {json.dumps(payload)}\n\n"


@app.post("/api/ask/stream")
async def ask_stream(req: AskRequest) -> StreamingResponse:
    """The same answer as /api/ask, delivered one pipeline stage at a time.

    The model is the slow part, so it starts first and runs on a worker thread
    while the retrieval rings — chunks, then their entities, then the wider
    neighbourhood — stream out ahead of it.
    """
    original = req.question.strip()
    if not original:
        raise HTTPException(400, "question is required")
    session_id = clean_session_id(req.session_id)
    if req.retriever == AGENT_MODE:
        return StreamingResponse(
            agent_stages(original, req.top_k, session_id),
            media_type="text/event-stream",
            headers=SSE_HEADERS,
        )
    rag = rag_for(req.retriever)          # raises 400 before the stream opens
    config = {} if req.retriever == "text2cypher" else {"top_k": req.top_k}
    # The conversation is read here, on the loop, so the worker thread below
    # only has synchronous work to do; the exchange is written back the same way.
    turns = await (await conversations()).recent_turns(session_id) if session_id else []
    loop = asyncio.get_running_loop()

    def stages() -> Iterator[str]:
        pool = ThreadPoolExecutor(max_workers=1)
        try:
            question = standalone_question(state["llm"], turns, original)
            if question != original:
                yield sse("stage", {"name": "interpreting", "label": f"Reading as: {question}"})
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

                entities, links, found = entities_from_chunks([c["id"] for c in chunks])
                entity_ids = [e["id"] for e in entities]
                yield sse(
                    "unfold",
                    {
                        "stage": "entities",
                        "label": (
                            f"{len(entities)} of {found} entities extracted from them"
                            if found > len(entities)
                            else f"{len(entities)} entities extracted from them"
                        ),
                        "truncated": found - len(entities),
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
            if session_id:
                asyncio.run_coroutine_threadsafe(
                    state["conversations"].record(
                        session_id, original, result.answer, req.retriever
                    ),
                    loop,
                )
            yield sse(
                "answer",
                {
                    "answer": result.answer,
                    "context": [item.content for item in items],
                    "interpreted": question if question != original else None,
                    "session_id": session_id,
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


async def agent_stages(
    question: str, top_k: int, session_id: str | None = None
) -> AsyncIterator[str]:
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
        result = await ask_via_agent(question, top_k, session_id)
        subgraph = result["subgraph"]
        shown, read = len(subgraph["nodes"]), result.get("read", 0)
        yield sse(
            "unfold",
            {
                "stage": "evidence",
                "label": (
                    f"{shown} of {read} entities the agent read"
                    if read > shown
                    else f"{shown} entities the agent read"
                ),
                "nodes": subgraph["nodes"],
                "relationships": subgraph["relationships"],
            },
        )
        yield sse(
            "answer",
            {
                "answer": result["answer"],
                "context": result["context"],
                "session_id": session_id,
            },
        )
    except Exception as exc:                              # noqa: BLE001
        yield sse("error", {"message": str(exc)})


# --- conversations ----------------------------------------------------------


@app.get("/api/conversations")
async def list_conversations() -> dict:
    """Every stored conversation, newest first: id, first question, size."""
    return {"sessions": await (await conversations()).sessions()}


@app.post("/api/conversations")
async def new_conversation() -> dict:
    """Mint an id. Nothing is stored until the first question."""
    return {"session_id": new_session_id()}


@app.get("/api/conversations/{session_id}")
async def get_conversation(session_id: str) -> dict:
    """The transcript, oldest first — what the browser rebuilds its thread from
    after a reload, and what `graphrag-agent --session` resumes."""
    turns = await (await conversations()).history(session_id)
    return {"session_id": session_id, "turns": [t.as_dict() for t in turns]}


@app.delete("/api/conversations/{session_id}")
async def forget_conversation(session_id: str) -> dict:
    """Forget a conversation: its messages, its traces, and the agent holding it."""
    await (await conversations()).forget(session_id)
    return {"session_id": session_id, "forgotten": True}


# --- extending the graph ----------------------------------------------------

#: Upload ceiling. The extraction cost of a document is linear in its length and
#: these run interactively, in front of an audience.
MAX_UPLOAD_BYTES = 20 * 1024 * 1024


@app.post("/api/documents")
# B008 is FastAPI's own idiom: File(...) in the default is how the dependency is
# declared, and it is evaluated by FastAPI rather than at import time.
async def add_document(file: UploadFile = File(...)) -> StreamingResponse:  # noqa: B008
    """Ingest an uploaded document into the existing graph, streaming progress.

    The same pipeline, schema and extraction rules that built the corpus run
    over the new file, so what arrives is merged into the same POLE structure
    rather than parked beside it. The response streams stages as SSE and ends
    with the subgraph the document added — which is the interesting part: you
    can see what the new document connected to.
    """
    name = Path(file.filename or "").name
    suffix = Path(name).suffix.lower()
    if suffix not in SUPPORTED_SUFFIXES:
        raise HTTPException(
            400,
            f"unsupported file type {suffix or '(none)'}; "
            f"expected one of {', '.join(sorted(SUPPORTED_SUFFIXES))}",
        )

    # Checked before a single model call. On a graph carrying NODE KEY or
    # existence constraints the writer's CREATE is rejected, the pipeline logs
    # the failed batch and returns normally, and the user is billed for an
    # extraction that wrote nothing. Refusing up front says why.
    blocking = await run_in_threadpool(
        blocking_constraints, state["driver"], state["database"], spec()
    )
    if blocking:
        kinds = sorted({c["type"] for c in blocking})
        raise HTTPException(
            409,
            f"{len(blocking)} constraints on this graph would reject the new records "
            f"({', '.join(kinds)}). Run `graphrag-adopt --relax-constraints` to drop "
            f"them (reversible with `graphrag-adopt --undo`), then try again.",
        )

    # Spooled to disk before anything else: the pipeline reads from a path, and
    # a 20MB PDF held in memory for the duration of an extraction is wasteful.
    tmp_dir = Path(tempfile.mkdtemp(prefix="graphrag-upload-"))
    target = tmp_dir / name
    size = 0
    with target.open("wb") as out:
        while chunk := await file.read(1024 * 1024):
            size += len(chunk)
            if size > MAX_UPLOAD_BYTES:
                shutil.rmtree(tmp_dir, ignore_errors=True)
                limit_mb = MAX_UPLOAD_BYTES // 1024 // 1024
                raise HTTPException(413, f"file is larger than {limit_mb}MB")
            out.write(chunk)
    if size == 0:
        shutil.rmtree(tmp_dir, ignore_errors=True)
        raise HTTPException(400, "the uploaded file is empty")

    async def stages() -> AsyncIterator[str]:
        queue: asyncio.Queue[str | None] = asyncio.Queue()
        try:
            if state["ingest_lock"].locked():
                yield sse("stage", {"name": "queued", "label": "Waiting for the current ingest…"})
            async with state["ingest_lock"]:
                before = await run_in_threadpool(entity_ids_snapshot)
                yield sse(
                    "stage",
                    {"name": "reading", "label": f"Reading {name} ({size // 1024} KB)…"},
                )

                loop = asyncio.get_running_loop()

                def report(line: str) -> None:
                    # ingest_files runs partly in worker threads; hop back to the
                    # loop thread rather than touching the queue from theirs.
                    loop.call_soon_threadsafe(queue.put_nowait, line)

                task = asyncio.create_task(
                    ingest_files(
                        spec(),
                        [target],
                        state["driver"],
                        state["llm"],
                        state["database"],
                        report=report,
                    )
                )
                task.add_done_callback(lambda _: queue.put_nowait(None))

                while True:
                    line = await queue.get()
                    if line is None:
                        break
                    yield sse("stage", {"name": "extracting", "label": line})
                await task  # re-raises anything the pipeline failed on

                after = await run_in_threadpool(entity_ids_snapshot)
                added = [entity_id for entity_id in after if entity_id not in before]
                subgraph = await run_in_threadpool(subgraph_for_ids, added, False)
                # Everything the new entities attached to, so the picture shows
                # the document joining the graph rather than floating beside it.
                context = await run_in_threadpool(subgraph_for_ids, added, True)
                yield sse(
                    "unfold",
                    {
                        "stage": "entities",
                        "label": f"{len(subgraph['nodes'])} new entities from {name}",
                        "nodes": context["nodes"],
                        "relationships": context["relationships"],
                    },
                )
                if not added:
                    yield sse(
                        "error",
                        {
                            "message": (
                                f"{name} was read but produced no new records. Either the "
                                f"extractor found nothing matching the schema, or the write "
                                f"was rejected — check the server log."
                            )
                        },
                    )
                    return
                yield sse(
                    "done",
                    {
                        "file": name,
                        "added": len(subgraph["nodes"]),
                        "newIds": added,
                        "counts": await run_in_threadpool(label_counts),
                    },
                )
        except Exception as exc:                          # noqa: BLE001
            yield sse("error", {"message": f"{type(exc).__name__}: {exc}"})
        finally:
            shutil.rmtree(tmp_dir, ignore_errors=True)

    return StreamingResponse(stages(), media_type="text/event-stream", headers=SSE_HEADERS)


def entity_ids_snapshot() -> set[str]:
    """Element IDs of every entity, for diffing what an ingest added.

    A diff rather than a timestamp filter: `SimpleKGPipeline` writes no created-at
    property, and entity resolution *merges* nodes, so counting is not enough.
    """
    return {r["id"] for r in run("MATCH (n:__Entity__) RETURN elementId(n) AS id")}


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


@app.get("/theme.css")
def theme_css() -> Response:
    """The project's own stylesheet, or an empty one.

    Always 200 with text/css so the <link> in index.html is unconditional, and
    never cached so editing a theme while the server runs is a plain reload.
    """
    path = spec().theme_css
    body = path.read_text(encoding="utf-8") if path and path.is_file() else ""
    return Response(body, media_type="text/css", headers={"Cache-Control": "no-cache"})


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
