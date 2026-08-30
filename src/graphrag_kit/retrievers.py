"""Retriever construction.

The retrieval_query is where GraphRAG earns its name: after the vector/fulltext
lookup picks the best chunks, this Cypher walks outward from each one and folds
the entity neighbourhood into the context the LLM sees.

Two variables are injected by the library and must not be re-declared:
  * ``node``  — the matched :Chunk
  * ``score`` — the similarity score; it must appear in the RETURN clause

Nothing here is domain-specific. The few-shot Cypher examples and the answering
persona come from the active ProjectSpec.
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
from graphrag_kit.project import ProjectSpec, load_project

# Chunk -> its document, the entities extracted from it, and one further hop to
# those entities' own relationships. That second hop is the part a vector store
# cannot do: "who was involved in what" lives in edges, not in prose.
GRAPH_CONTEXT_QUERY = """
// OPTIONAL throughout: a chunk missing its document or entities is still worth
// returning, and a required MATCH would silently drop it from the context.
OPTIONAL MATCH (node)-[:FROM_DOCUMENT]->(doc:Document)

OPTIONAL MATCH (entity:__Entity__)-[:FROM_CHUNK]->(node)
WITH node, score, doc, collect(DISTINCT entity) AS entities

CALL (entities) {
    UNWIND entities AS e
    MATCH (e)-[rel]->(target:__Entity__)
    RETURN collect(DISTINCT
        e.name + ' -[' + type(rel) + ']-> ' + target.name +
        ' (' + coalesce(target.status, 'unrated') + ')'
    ) AS facts
}

RETURN
  node.text AS chunk_text,
  coalesce(doc.source, doc.path) AS source_document,
  // Reserved labels are stripped: label order on a node is not guaranteed.
  [e IN entities |
     head([l IN labels(e) WHERE NOT l IN ['__Entity__', '__KGBuilder__']])
     + ': ' + coalesce(e.name, '?')
     + ' [' + coalesce(e.status, 'unrated') + ']'] AS entity_context,
  facts AS related_facts,
  score
"""

RAG_PROMPT_TEMPLATE = """__PERSONA__

Use ONLY the context below. Each item may carry the source text, the entities
extracted from it, and related graph facts. Entities and facts are tagged with an
evidence level in brackets, one of: __LEVELS__.

Rules:
- State the evidence level when it matters. Never present a lower-confidence
  claim as established fact.
- If the context does not answer the question, say so. Do not guess.
- Cite the source document for each claim.

Context:
{context}

Examples:
{examples}

Question: {query_text}

Answer:"""


def build_rag_prompt(spec: ProjectSpec) -> str:
    return (
        RAG_PROMPT_TEMPLATE
        .replace("__PERSONA__", spec.rag_persona.strip())
        .replace("__LEVELS__", ", ".join(spec.evidence_levels))
    )


def vector_retriever(driver: neo4j.Driver) -> VectorRetriever:
    """Baseline: pure semantic similarity over chunk text. No graph, no keywords."""
    return VectorRetriever(
        driver=driver,
        index_name=VECTOR_INDEX_NAME,
        embedder=get_embedder(),
        return_properties=["text"],
        neo4j_database=get_database(),
    )


def hybrid_retriever(driver: neo4j.Driver) -> HybridRetriever:
    """Vector + fulltext. Recovers proper nouns that embeddings blur together."""
    return HybridRetriever(
        driver=driver,
        vector_index_name=VECTOR_INDEX_NAME,
        fulltext_index_name=FULLTEXT_INDEX_NAME,
        embedder=get_embedder(),
        return_properties=["text"],
        neo4j_database=get_database(),
    )


def vector_cypher_retriever(driver: neo4j.Driver) -> VectorCypherRetriever:
    """Vector lookup, then graph expansion."""
    return VectorCypherRetriever(
        driver=driver,
        index_name=VECTOR_INDEX_NAME,
        retrieval_query=GRAPH_CONTEXT_QUERY,
        embedder=get_embedder(),
        neo4j_database=get_database(),
    )


def hybrid_cypher_retriever(driver: neo4j.Driver) -> HybridCypherRetriever:
    """Vector + fulltext, then graph expansion. The default."""
    return HybridCypherRetriever(
        driver=driver,
        vector_index_name=VECTOR_INDEX_NAME,
        fulltext_index_name=FULLTEXT_INDEX_NAME,
        retrieval_query=GRAPH_CONTEXT_QUERY,
        embedder=get_embedder(),
        neo4j_database=get_database(),
    )


def text2cypher_retriever(driver: neo4j.Driver) -> Text2CypherRetriever:
    """LLM writes Cypher against the live schema. No embedder.

    Handles counting and aggregation, which vector search cannot answer at all.
    The library runs EXPLAIN on the generated Cypher and refuses to execute
    anything that writes, so a prompt-injected DELETE never reaches the graph.
    """
    return Text2CypherRetriever(
        driver=driver,
        llm=get_llm(),
        neo4j_schema=None,  # None => fetched from the database at query time
        examples=load_project().text2cypher_examples or None,
        neo4j_database=get_database(),
    )


RETRIEVERS = {
    "vector": vector_retriever,
    "hybrid": hybrid_retriever,
    "vector-cypher": vector_cypher_retriever,
    "hybrid-cypher": hybrid_cypher_retriever,
    "text2cypher": text2cypher_retriever,
}


# Vector and fulltext hits are unioned rather than intersected: each recovers
# chunks the other misses, and `max(score)` keeps whichever lookup was more
# confident about a chunk both of them found.
EVIDENCE_SEED_QUERY = """
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
        EVIDENCE_SEED_QUERY,
        database_=get_database(),
        vector_index=VECTOR_INDEX_NAME,
        fulltext_index=FULLTEXT_INDEX_NAME,
        question=question,
        vector=embedder.embed_query(question),
        top_k=top_k,
    )
    return [r["id"] for r in records]
