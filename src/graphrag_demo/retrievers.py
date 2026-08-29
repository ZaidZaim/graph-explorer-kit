"""Retriever construction.

The `retrieval_query` is the whole point of GraphRAG: after the vector/fulltext
lookup picks the best chunks, this Cypher fragment walks the graph outward from
each one and folds the neighbourhood into the context the LLM sees.

Two variables are injected by the library and must not be re-declared:
  * ``node``  — the matched :Chunk
  * ``score`` — the similarity score; it must appear in the RETURN clause
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

from graphrag_demo.config import (
    FULLTEXT_INDEX_NAME,
    VECTOR_INDEX_NAME,
    get_database,
    get_embedder,
    get_llm,
)

# Starting from the matched chunk: name its document, pull the entities extracted
# from it, and hop one step further to those entities' own relationships. That
# last hop is context a pure vector store cannot produce — the answer to
# "who works where" often lives in a chunk the query never matched.
GRAPH_CONTEXT_QUERY = """
// OPTIONAL throughout: a chunk missing its document or entities is still worth
// returning, and a required MATCH here would silently drop it from the context.
OPTIONAL MATCH (node)-[:FROM_DOCUMENT]->(doc:Document)

OPTIONAL MATCH (entity:__Entity__)-[:FROM_CHUNK]->(node)
WITH node, score, doc, collect(DISTINCT entity) AS entities

// Second hop. The scoped CALL subquery keeps this per-chunk, and its aggregation
// still yields one row when a chunk has no entities, so chunks are never dropped.
CALL (entities) {
    UNWIND entities AS e
    MATCH (e)-[rel]->(target:__Entity__)
    RETURN collect(DISTINCT
        e.name + ' -[' + type(rel) + ']-> ' + target.name
    ) AS facts
}

RETURN
  node.text AS chunk_text,
  coalesce(doc.source, doc.path) AS source_document,
  // Reserved labels are stripped: label order on a node is not guaranteed.
  [e IN entities |
     head([l IN labels(e) WHERE NOT l IN ['__Entity__', '__KGBuilder__']])
     + ': ' + coalesce(e.name, '?')] AS mentioned_entities,
  facts AS related_facts,
  score
"""

TEXT2CYPHER_EXAMPLES = [
    "USER INPUT: 'Who works at Meridian Robotics?' "
    "QUERY: MATCH (p:Person)-[:WORKS_AT]->(o:Organization) "
    "WHERE o.name CONTAINS 'Meridian' RETURN p.name, p.role",
    "USER INPUT: 'Which technologies does the Atlas platform use?' "
    "QUERY: MATCH (p:Product)-[:USES]->(t:Technology) "
    "WHERE p.name CONTAINS 'Atlas' RETURN t.name",
    "USER INPUT: 'Which companies partner with each other?' "
    "QUERY: MATCH (a:Organization)-[:PARTNERS_WITH]-(b:Organization) "
    "RETURN DISTINCT a.name, b.name",
]


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
    """Vector + fulltext. Recovers exact names and acronyms that embeddings blur."""
    return HybridRetriever(
        driver=driver,
        vector_index_name=VECTOR_INDEX_NAME,
        fulltext_index_name=FULLTEXT_INDEX_NAME,
        embedder=get_embedder(),
        return_properties=["text"],
        neo4j_database=get_database(),
    )


def vector_cypher_retriever(driver: neo4j.Driver) -> VectorCypherRetriever:
    """Vector lookup, then graph expansion via GRAPH_CONTEXT_QUERY."""
    return VectorCypherRetriever(
        driver=driver,
        index_name=VECTOR_INDEX_NAME,
        retrieval_query=GRAPH_CONTEXT_QUERY,
        embedder=get_embedder(),
        neo4j_database=get_database(),
    )


def hybrid_cypher_retriever(driver: neo4j.Driver) -> HybridCypherRetriever:
    """Vector + fulltext lookup, then graph expansion. The default for this demo."""
    return HybridCypherRetriever(
        driver=driver,
        vector_index_name=VECTOR_INDEX_NAME,
        fulltext_index_name=FULLTEXT_INDEX_NAME,
        retrieval_query=GRAPH_CONTEXT_QUERY,
        embedder=get_embedder(),
        neo4j_database=get_database(),
    )


def text2cypher_retriever(driver: neo4j.Driver) -> Text2CypherRetriever:
    """LLM writes Cypher against the live schema. No embedder involved.

    Good at aggregation and counting, which vector search cannot do at all.
    The library runs EXPLAIN on the generated Cypher and refuses to execute
    anything that writes, so a prompt-injected DELETE never reaches the graph.
    """
    return Text2CypherRetriever(
        driver=driver,
        llm=get_llm(),
        neo4j_schema=None,  # None => fetched from the database at query time
        examples=TEXT2CYPHER_EXAMPLES,
        neo4j_database=get_database(),
    )


RETRIEVERS = {
    "vector": vector_retriever,
    "hybrid": hybrid_retriever,
    "vector-cypher": vector_cypher_retriever,
    "hybrid-cypher": hybrid_cypher_retriever,
    "text2cypher": text2cypher_retriever,
}
