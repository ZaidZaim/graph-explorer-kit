"""A Microsoft Agent Framework agent over the project's knowledge graph.

`ask.py` runs one fixed retriever and answers in a single shot. That is the right
shape for "find the passage that answers this", and the wrong shape for anything
needing more than one look: a question that is part lookup and part arithmetic
("who is confirmed, and how many are there?") has to pick one retriever, and
whichever it picks answers half the question.

This module hands the retrievers to an agent as tools and lets the model choose,
call more than one, and call again after reading the first result. The retrieval
itself is unchanged — same indexes, same graph-expansion query, same graph.

Every tool that touches entities records their element IDs on an `EvidenceTrail`,
so the caller can still light up exactly the subgraph the answer came from — here
the subgraph the agent actually read, rather than a re-run of the lookup.

API notes for the 2026 Agent Framework release, which renamed a lot:
`ChatAgent` -> `Agent`, `chat_client=` -> `client=`, `@ai_function` -> `@tool`,
`AgentThread` -> `AgentSession`, and `run_stream()` -> `run(..., stream=True)`.
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from contextvars import ContextVar
from dataclasses import dataclass, field
from typing import Annotated

import neo4j
from agent_framework import Agent, tool
from pydantic import Field

from graphrag_kit.config import (
    ENTITY_FULLTEXT_INDEX_NAME,
    describe_agent_model,
    get_chat_client,
    get_database,
    get_driver,
    get_embedder,
    get_llm,
    use_utf8_stdout,
)
from graphrag_kit.cypher import (
    evidence_expr,
    fact_expr,
    label_expr,
    lucene_escape,
    name_expr,
    source_name_expr,
)
from graphrag_kit.project import ProjectSpec, load_project
from graphrag_kit.retrievers import (
    evidence_entity_ids,
    hybrid_cypher_retriever,
    text2cypher_retriever,
)


@dataclass
class EvidenceTrail:
    """What the agent actually touched while answering one question."""

    entity_ids: list[str] = field(default_factory=list)
    calls: list[str] = field(default_factory=list)

    def record(self, call: str, ids: list[str] | None = None) -> None:
        self.calls.append(call)
        known = set(self.entity_ids)
        for entity_id in ids or []:
            if entity_id not in known:
                known.add(entity_id)
                self.entity_ids.append(entity_id)


# A ContextVar holding a *mutable* trail, rather than a value the tools reassign:
# sync tools are invoked through asyncio.to_thread, which copies the context in
# but never copies it back, so a set() inside a tool would be lost. Mutating the
# object the caller already holds works in either direction, and keeps concurrent
# requests in the server isolated from each other.
_TRAIL: ContextVar[EvidenceTrail | None] = ContextVar("graphrag_evidence_trail", default=None)


def _trail() -> EvidenceTrail:
    """The trail for the request in flight, or a throwaway one outside a run."""
    trail = _TRAIL.get()
    return trail if trail is not None else EvidenceTrail()


AGENT_INSTRUCTIONS = """__PERSONA__

You answer from a Neo4j knowledge graph built from a document corpus. You cannot
see the graph directly — reach it only through your tools.

Choosing a tool:
- `search_documents` for anything answered by the source text: what happened, who
  was involved, what a document says. This is your default.
- `query_graph_with_cypher` for counting, aggregating, or listing every match.
  Semantic search returns the top few passages and will quietly undercount, so
  never answer "how many" from `search_documents`.
- `look_up_entity` when you already have a name and want its connections.
- `graph_overview` when you need to know what kinds of things exist at all.

Call more than one tool when a question has more than one part, and call again if
the first result is thin. Do not answer a multi-part question from a single lookup
because the first tool returned something plausible.

Be economical. Aim to answer in two or three tool calls: one per part of the
question, plus at most one follow-up where the first result was genuinely
inadequate. Keep generated Cypher simple — a query that counts what was asked
beats one that also cross-checks for duplicates. Once you can answer, answer.
Do not keep verifying a result you already have.

__EVIDENCE__Cite the source document for each claim.

If the tools do not answer the question, say so plainly. Do not fill the gap from
your own knowledge — anything not in the graph is out of scope."""


EVIDENCE_INSTRUCTION = """Entities and facts are tagged with an evidence level, one of: __LEVELS__.
State the level when it matters, and never present a lower-confidence claim as an
established fact.
"""


def build_instructions(spec: ProjectSpec) -> str:
    """The agent's instructions, with the evidence paragraph dropped for a corpus
    that carries no grading — told to cite a level it will never see, the model
    invents one."""
    evidence = (
        EVIDENCE_INSTRUCTION.replace("__LEVELS__", ", ".join(spec.evidence_levels))
        if spec.grades_evidence
        else ""
    )
    return (
        AGENT_INSTRUCTIONS
        .replace("__PERSONA__", spec.rag_persona.strip())
        .replace("__EVIDENCE__", evidence)
    )


def entity_lookup_query(spec: ProjectSpec) -> str:
    """Find entities by name, with every relationship they take part in.

    Both directions are collected: "who reports to X" and "who does X report to"
    are the same edge seen from opposite ends, and an agent handed only the
    outgoing half concludes the other half does not exist.
    """
    return f"""
CALL db.index.fulltext.queryNodes($index, $name, {{limit: $limit}})
YIELD node AS e, score
OPTIONAL MATCH (e)-[out]->(t:__Entity__)
OPTIONAL MATCH (s:__Entity__)-[incoming]->(e)
RETURN
  elementId(e) AS id,
  {label_expr('e')} AS label,
  {name_expr('e', spec)} AS name,
  {evidence_expr('e', spec)} AS status,
  e.description AS description,
  properties(e) AS props,
  collect(DISTINCT {fact_expr('e', 'out', 't', spec)}) AS outgoing_facts,
  collect(DISTINCT {fact_expr('s', 'incoming', 'e', spec)}) AS incoming_facts,
  [x IN collect(DISTINCT elementId(t)) + collect(DISTINCT elementId(s))
   WHERE x IS NOT NULL] AS neighbour_ids,
  score
ORDER BY score DESC
"""


OVERVIEW_QUERY = """
MATCH (n:__Entity__)
UNWIND labels(n) AS label
WITH label, n WHERE NOT label IN ['__Entity__', '__KGBuilder__']
RETURN label, count(DISTINCT n) AS count ORDER BY count DESC
"""

#: Entity properties the agent is not shown. Bookkeeping and vectors only — the
#: rest is the substance of the record and is exactly what it should be reading.
AGENT_HIDDEN_PROPERTIES = {"__id__", "id", "index", "name", "description"}


def build_agent(driver: neo4j.Driver, spec: ProjectSpec | None = None) -> Agent:
    """An Agent whose tools are this project's retrievers.

    The retrievers are built once and closed over rather than rebuilt per call:
    each one constructs an embedder, and the text2cypher one an LLM.
    """
    spec = spec or load_project()
    database = get_database()
    embedder = get_embedder()
    search = hybrid_cypher_retriever(driver)
    text2cypher = text2cypher_retriever(driver)

    def run(cypher: str, **params) -> list:
        records, _, _ = driver.execute_query(cypher, database_=database, **params)
        return records

    @tool
    def search_documents(
        question: Annotated[str, Field(description="A natural-language question or topic.")],
        top_k: Annotated[int, Field(description="How many passages to retrieve.", ge=1, le=15)] = 5,
    ) -> str:
        """Search the corpus semantically and by keyword, then expand each matching
        passage into its document, the entities extracted from it, and those
        entities' own relationships. Use for anything answered by the source text."""
        result = search.search(query_text=question, top_k=top_k)
        _trail().record(
            f"search_documents({question!r}, top_k={top_k})",
            evidence_entity_ids(driver, embedder, question, top_k),
        )
        if not result.items:
            return "No matching passages."
        return "\n\n".join(f"[{i}] {item.content}" for i, item in enumerate(result.items, 1))

    @tool
    def query_graph_with_cypher(
        question: Annotated[
            str,
            Field(description="A question about counts, totals, or every match of something."),
        ],
    ) -> str:
        """Translate the question into Cypher against the live schema and run it.
        Use for counting, aggregating, or listing every match — semantic search
        returns only the top few passages and will undercount. Read-only: the
        generated Cypher is rejected before execution if it writes."""
        result = text2cypher.search(query_text=question)
        _trail().record(f"query_graph_with_cypher({question!r})")
        if not result.items:
            return "The query returned no rows."
        return "\n".join(str(item.content) for item in result.items)

    @tool
    def look_up_entity(
        name: Annotated[str, Field(description="Name of a person, place, event or thing.")],
        limit: Annotated[int, Field(description="How many candidates to return.", ge=1, le=10)] = 3,
    ) -> str:
        """Find entities by name and return their properties, evidence level, and
        every relationship they take part in. Use when you already have a name."""
        records = run(
            entity_lookup_query(spec),
            index=ENTITY_FULLTEXT_INDEX_NAME,
            name=lucene_escape(name),
            limit=limit,
        )
        if not records:
            return f"No entity matching {name!r}."
        ids = [r["id"] for r in records] + [i for r in records for i in r["neighbour_ids"]]
        _trail().record(f"look_up_entity({name!r})", ids)

        blocks = []
        for record in records:
            grade = f" [{record['status']}]" if record["status"] else ""
            lines = [f"{record['label']}: {record['name']}{grade}"]
            if record["description"]:
                lines.append(f"  {record['description']}")
            # The measurements are the point in this corpus: an Observation's
            # shape, movement, speed and altitude say more than its description.
            details = [
                f"{key}={value}"
                for key, value in sorted((record["props"] or {}).items())
                if key not in AGENT_HIDDEN_PROPERTIES
                and "embedding" not in key.lower()
                and isinstance(value, (str, int, float, bool))
            ]
            if details:
                lines.append("  " + "; ".join(details))
            facts = [
                fact
                for fact in (record["outgoing_facts"] or []) + (record["incoming_facts"] or [])
                if fact
            ]
            lines.extend(f"  {fact}" for fact in facts or ["(no relationships)"])
            blocks.append("\n".join(lines))
        return "\n\n".join(blocks)

    @tool
    def graph_overview() -> str:
        """List the entity types in the graph, how many of each there are, and which
        documents it was built from. Use when you need to know what the graph holds
        at all before searching it."""
        _trail().record("graph_overview()")
        labels = run(OVERVIEW_QUERY)
        rels = run(
            "MATCH (:__Entity__)-[r]->(:__Entity__) "
            "RETURN type(r) AS type, count(*) AS count ORDER BY count DESC"
        )
        lex = spec.lexical
        docs = run(
            f"MATCH (d:`{lex.source_label}`) "
            f"RETURN collect({source_name_expr('d', spec)})[..40] AS sources"
        )
        return (
            "Entity types: "
            + ", ".join(f"{r['label']} ({r['count']})" for r in labels)
            + "\nRelationship types: "
            + ", ".join(f"{r['type']} ({r['count']})" for r in rels)
            + "\nDocuments: "
            + ", ".join(docs[0]["sources"])
        )

    return Agent(
        client=get_chat_client(),
        name="graphrag-agent",
        description=f"Answers questions about {spec.title} from its knowledge graph.",
        instructions=build_instructions(spec),
        tools=[search_documents, query_graph_with_cypher, look_up_entity, graph_overview],
    )


@dataclass
class AgentAnswer:
    answer: str
    trail: EvidenceTrail


async def ask_agent(agent: Agent, question: str, session=None) -> AgentAnswer:
    """Run one question and return the answer alongside what the agent read."""
    trail = EvidenceTrail()
    token = _TRAIL.set(trail)
    try:
        response = await agent.run(question, session=session)
    finally:
        _TRAIL.reset(token)
    return AgentAnswer(answer=response.text, trail=trail)


# --- CLI --------------------------------------------------------------------


async def _answer(agent: Agent, question: str, args: argparse.Namespace, session) -> None:
    if args.stream:
        trail = EvidenceTrail()
        token = _TRAIL.set(trail)
        try:
            async for update in agent.run(question, session=session, stream=True):
                if update.text:
                    print(update.text, end="", flush=True)
        finally:
            _TRAIL.reset(token)
        print()
    else:
        result = await ask_agent(agent, question, session)
        trail = result.trail
        print(result.answer)

    if args.show_tools:
        print("\n--- tool calls ---")
        for call in trail.calls or ["(none)"]:
            print(f"  {call}")
        print(f"--- {len(trail.entity_ids)} entities read ---")


async def _run_cli(args: argparse.Namespace, question: str) -> None:
    spec = load_project()
    driver = get_driver()
    # text2cypher_retriever() builds its own LLM; hold a handle so it gets closed.
    llm = get_llm()
    try:
        agent = build_agent(driver, spec)
        # A session carries history across turns; one-shot runs deliberately get
        # none, so the same question always produces the same answer.
        session = agent.create_session() if args.chat else None

        if question:
            await _answer(agent, question, args, session)
        if args.chat:
            print("\n(empty line or Ctrl-D to exit)")
            while True:
                try:
                    line = input("\n> ").strip()
                except EOFError:
                    break
                if not line:
                    break
                await _answer(agent, line, args, session)
    finally:
        await llm.aclose()
        driver.close()


def main() -> int:
    use_utf8_stdout()
    parser = argparse.ArgumentParser(
        description="Ask the knowledge graph through a Microsoft Agent Framework agent."
    )
    parser.add_argument("question", nargs="*", help="The question to ask.")
    parser.add_argument("--chat", action="store_true", help="Multi-turn REPL keeping history.")
    parser.add_argument("--stream", action="store_true", help="Stream tokens as they arrive.")
    parser.add_argument(
        "--show-tools", action="store_true", help="Print which tools the agent called."
    )
    args = parser.parse_args()

    question = " ".join(args.question).strip()
    if not question and not args.chat:
        parser.error("provide a question, or pass --chat")

    print(f"agent: {describe_agent_model()}", file=sys.stderr)
    asyncio.run(_run_cli(args, question))
    return 0


if __name__ == "__main__":
    sys.exit(main())
