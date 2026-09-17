"""Retriever construction.

The retrieval_query is where GraphRAG earns its name: after the vector/fulltext
lookup picks the best chunks, this Cypher walks outward from each one and folds
the entity neighbourhood into the context the LLM sees.

Two variables are injected by the library and must not be re-declared:
  * ``node``  — the matched chunk
  * ``score`` — the similarity score; it must appear in the RETURN clause

Nothing here is domain-specific. The label and property *names* come from the
active project's lexical spec, and the few-shot Cypher and answering persona
from the project itself.
"""

from __future__ import annotations

import neo4j
from neo4j_graphrag.retrievers import (
    HybridCypherRetriever,
    HybridRetriever,
    Text2CypherRetriever,
    VectorCypherRetriever,
    VectorRetriever,
)

from graphrag_kit.config import (
    FULLTEXT_INDEX_NAME,
    VECTOR_INDEX_NAME,
    get_database,
    get_embedder,
    get_llm,
)
from graphrag_kit.cypher import (
    evidence_expr,
    fact_expr,
    label_expr,
    name_expr,
    source_name_expr,
)
from graphrag_kit.project import ProjectSpec, load_project


def graph_context_query(spec: ProjectSpec) -> str:
    """Chunk -> its source, the entities extracted from it, and one further hop
    to those entities' own relationships.

    That second hop is the part a vector store cannot do: "who was involved in
    what" lives in edges, not in prose.
    """
    lex = spec.lexical
    entity_line = (
        f"{label_expr('e')} + ': ' + coalesce({name_expr('e', spec)}, '?')"
        + (f" + ' [' + {evidence_expr('e', spec)} + ']'" if spec.grades_evidence else "")
    )
    return f"""
// OPTIONAL throughout: a chunk missing its source or its entities is still worth
// returning, and a required MATCH would silently drop it from the context.
OPTIONAL MATCH (node)-[:{lex.chunk_to_source}]->(doc:{lex.source_label})

OPTIONAL MATCH (entity:__Entity__)-[:{lex.entity_to_chunk}]->(node)
WITH node, score, doc, collect(DISTINCT entity) AS entities

CALL (entities) {{
    UNWIND entities AS e
    MATCH (e)-[rel]->(target:__Entity__)
    RETURN collect(DISTINCT {fact_expr('e', 'rel', 'target', spec)}) AS facts
}}

RETURN
  node.{lex.text_property} AS chunk_text,
  {source_name_expr('doc', spec)} AS source_document,
  [e IN entities | {entity_line}] AS entity_context,
  facts AS related_facts,
  score
"""


RAG_PROMPT_TEMPLATE = """__PERSONA__

Use ONLY the context below. Each item may carry the source text, the entities
extracted from it, and related graph facts.
__EVIDENCE_NOTE__
Rules:
- If the context does not answer the question, say so. Do not guess.
- Cite the source document for each claim.
- Write prose. Some context items are raw database rows rendered as
  `<Record field='value'>`; report the values, never the row syntax.
__EVIDENCE_RULES__
Context:
{context}

Examples:
{examples}

Question: {query_text}

Answer:"""

EVIDENCE_NOTE = """
Entities and facts are tagged with an evidence level in brackets, one of:
__LEVELS__.
"""

EVIDENCE_RULES = """- State the evidence level when it matters. Never present a lower-confidence
  claim as established fact.
"""


def build_rag_prompt(spec: ProjectSpec) -> str:
    """The answering prompt, with the evidence-grading paragraphs dropped for a
    corpus that has no grading — an instruction to cite a level that no context
    item carries teaches the model to invent one."""
    note = EVIDENCE_NOTE.replace("__LEVELS__", ", ".join(spec.evidence_levels))
    return (
        RAG_PROMPT_TEMPLATE
        .replace("__PERSONA__", spec.rag_persona.strip())
        .replace("__EVIDENCE_NOTE__", note if spec.grades_evidence else "")
        .replace("__EVIDENCE_RULES__", EVIDENCE_RULES if spec.grades_evidence else "")
    )


def vector_retriever(driver: neo4j.Driver) -> VectorRetriever:
    """Baseline: pure semantic similarity over chunk text. No graph, no keywords."""
    return VectorRetriever(
        driver=driver,
        index_name=VECTOR_INDEX_NAME,
        embedder=get_embedder(),
        return_properties=[load_project().lexical.text_property],
        neo4j_database=get_database(),
    )


def hybrid_retriever(driver: neo4j.Driver) -> HybridRetriever:
    """Vector + fulltext. Recovers proper nouns that embeddings blur together."""
    return HybridRetriever(
        driver=driver,
        vector_index_name=VECTOR_INDEX_NAME,
        fulltext_index_name=FULLTEXT_INDEX_NAME,
        embedder=get_embedder(),
        return_properties=[load_project().lexical.text_property],
        neo4j_database=get_database(),
    )


def vector_cypher_retriever(driver: neo4j.Driver) -> VectorCypherRetriever:
    """Vector lookup, then graph expansion."""
    return VectorCypherRetriever(
        driver=driver,
        index_name=VECTOR_INDEX_NAME,
        retrieval_query=graph_context_query(load_project()),
        embedder=get_embedder(),
        neo4j_database=get_database(),
    )


def hybrid_cypher_retriever(driver: neo4j.Driver) -> HybridCypherRetriever:
    """Vector + fulltext, then graph expansion. The default."""
    return HybridCypherRetriever(
        driver=driver,
        vector_index_name=VECTOR_INDEX_NAME,
        fulltext_index_name=FULLTEXT_INDEX_NAME,
        retrieval_query=graph_context_query(load_project()),
        embedder=get_embedder(),
        neo4j_database=get_database(),
    )


def schema_text(spec: ProjectSpec) -> str:
    """The project's schema, rendered for a text2cypher prompt.

    Passed instead of None, which makes the library introspect the live database
    on *every* call. Two reasons beyond the round trip, which an agent making
    several tool calls pays several times over:

    * The declared schema is cleaner than the live one. Introspection reports
      every property any node happens to carry, including the other tool's
      bookkeeping keys, and offers no guidance about which are meaningful.
    * It states which patterns exist. A list of labels and a list of
      relationship types does not say what connects to what, so the model
      guesses — and a guessed pattern returns zero rows rather than an error.
    """
    lines = ["Node labels and their properties:"]
    for node in spec.schema.node_types:
        props = ", ".join(p.name for p in (node.properties or [])) or "(none)"
        lines.append(f"  {node.label}: {props}")
    lines.append("\nRelationship types:")
    for rel in spec.schema.relationship_types:
        lines.append(f"  {rel.label}")
    lines.append("\nThe only patterns that exist in the graph:")
    for start, rel_type, end in spec.schema.patterns or []:
        lines.append(f"  (:{start})-[:{rel_type}]->(:{end})")
    lex = spec.lexical
    lines.append(
        "\nEvery extracted node also carries the label __Entity__, so "
        "`MATCH (n:__Entity__)` matches all of them regardless of type.\n"
        f"Source text lives on (:{lex.chunk_label} {{{lex.text_property}}}), reachable as\n"
        f"  (:__Entity__)-[:{lex.entity_to_chunk_write}]->(:{lex.chunk_label})"
        f"-[:{lex.chunk_to_source_write}]->(:{lex.source_label})\n"
        f"and the source file's name is its `{lex.source_name_properties[0]}` property."
    )
    return "\n".join(lines)


def text2cypher_retriever(driver: neo4j.Driver) -> Text2CypherRetriever:
    """LLM writes Cypher against the project's schema. No embedder.

    Handles counting and aggregation, which vector search cannot answer at all.
    The library runs EXPLAIN on the generated Cypher and refuses to execute
    anything that writes, so a prompt-injected DELETE never reaches the graph.
    """
    spec = load_project()
    return Text2CypherRetriever(
        driver=driver,
        llm=get_llm(),
        neo4j_schema=schema_text(spec),
        examples=spec.text2cypher_examples or None,
        neo4j_database=get_database(),
    )


RETRIEVERS = {
    "vector": vector_retriever,
    "hybrid": hybrid_retriever,
    "vector-cypher": vector_cypher_retriever,
    "hybrid-cypher": hybrid_cypher_retriever,
    "text2cypher": text2cypher_retriever,
}


def evidence_seed_query(spec: ProjectSpec) -> str:
    """Vector and fulltext hits are unioned rather than intersected: each recovers
    chunks the other misses, and `max(score)` keeps whichever lookup was more
    confident about a chunk both of them found."""
    return f"""
CALL () {{
    CALL db.index.vector.queryNodes($vector_index, $top_k, $vector)
    YIELD node, score RETURN node, score
    UNION
    CALL db.index.fulltext.queryNodes($fulltext_index, $question, {{limit: $top_k}})
    YIELD node, score RETURN node, score
}}
WITH node, max(score) AS score ORDER BY score DESC LIMIT $top_k
MATCH (e:__Entity__)-[:{spec.lexical.entity_to_chunk}]->(node)
RETURN DISTINCT elementId(e) AS id
"""


def evidence_entity_ids(
    driver: neo4j.Driver, embedder, question: str, top_k: int = 5
) -> list[str]:
    """Element IDs of the entities extracted from the chunks `question` retrieves.

    A second lookup rather than a parse of the retriever's output, deliberately:
    retrievers hand back rendered text, and every caller here — the explorer's
    graph highlight, the agent's evidence trail — needs element IDs.
    """
    records, _, _ = driver.execute_query(
        evidence_seed_query(load_project()),
        database_=get_database(),
        vector_index=VECTOR_INDEX_NAME,
        fulltext_index=FULLTEXT_INDEX_NAME,
        question=question,
        vector=embedder.embed_query(question),
        top_k=top_k,
    )
    return [r["id"] for r in records]
