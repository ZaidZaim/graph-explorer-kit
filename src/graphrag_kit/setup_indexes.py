"""Create indexes, then wait until every index is ONLINE.

Run once before ingesting. Embeddings written while the vector index is still
populating are invisible to search, and nothing errors to tell you.

No uniqueness constraints on entity names: `Neo4jWriter` inserts extracted nodes
with `CREATE`, not `MERGE`, and de-duplicates afterwards via the resolver. A
`Person.name IS UNIQUE` constraint would abort ingestion the first time a person
is mentioned in two chunks.

Every name here comes from the active project's `lexical` spec, so pointing the
engine at a graph another tool built is a matter of configuration rather than a
second set of indexes.
"""

from __future__ import annotations

import sys
import time

import neo4j
from neo4j_graphrag.indexes import create_fulltext_index, create_vector_index

from graphrag_kit.config import (
    EMBEDDING_DIMENSIONS,
    ENTITY_FULLTEXT_INDEX_NAME,
    FULLTEXT_INDEX_NAME,
    VECTOR_INDEX_NAME,
    describe_models,
    get_database,
    get_driver,
    lexical,
    use_utf8_stdout,
)
from graphrag_kit.project import load_project

RANGE_INDEXES = [
    # Every extracted entity carries the reserved :__Entity__ label, so one index
    # serves every schema label and speeds up entity resolution.
    ("entity_name", "CREATE INDEX entity_name IF NOT EXISTS FOR (n:__Entity__) ON (n.name)"),
]


def wait_until_online(driver: neo4j.Driver, database: str, timeout_s: int = 180) -> None:
    """Poll SHOW INDEXES until nothing is left in a non-ONLINE state."""
    deadline = time.monotonic() + timeout_s
    while True:
        records, _, _ = driver.execute_query(
            "SHOW INDEXES YIELD name, state WHERE state <> 'ONLINE' RETURN name, state",
            database_=database,
        )
        if not records:
            print("All indexes ONLINE.")
            return
        pending = ", ".join(f"{r['name']}={r['state']}" for r in records)
        if time.monotonic() > deadline:
            raise TimeoutError(f"Indexes still not ONLINE after {timeout_s}s: {pending}")
        print(f"  waiting for: {pending}")
        time.sleep(3)


def main() -> int:
    use_utf8_stdout()
    print(f"models: {describe_models()}")
    spec = load_project()
    lex = lexical()
    driver = get_driver()
    database = get_database()
    try:
        statements = list(RANGE_INDEXES)
        if spec.grades_evidence:
            statements.append(
                (
                    "entity_status",
                    f"CREATE INDEX entity_status IF NOT EXISTS FOR (n:__Entity__) "
                    f"ON (n.{spec.evidence_property})",
                )
            )
        # The *preferred* name property, not the fallback: that is the one every
        # citation, document list and source lookup reads.
        statements.append(
            (
                "source_name",
                f"CREATE INDEX source_name IF NOT EXISTS FOR (d:`{lex.source_label}`) "
                f"ON (d.`{lex.source_name_properties[0]}`)",
            )
        )
        for name, statement in statements:
            driver.execute_query(statement, database_=database)
            print(f"range       {name}")

        create_vector_index(
            driver,
            name=VECTOR_INDEX_NAME,
            label=lex.chunk_label,
            embedding_property=lex.embedding_property,
            dimensions=EMBEDDING_DIMENSIONS,
            similarity_fn="cosine",
            neo4j_database=database,
        )
        print(
            f"vector      {VECTOR_INDEX_NAME} on {lex.chunk_label}.{lex.embedding_property} "
            f"({EMBEDDING_DIMENSIONS} dims, cosine)"
        )

        create_fulltext_index(
            driver,
            name=FULLTEXT_INDEX_NAME,
            label=lex.chunk_label,
            node_properties=[lex.text_property],
            neo4j_database=database,
        )
        print(f"fulltext    {FULLTEXT_INDEX_NAME} (on {lex.chunk_label}.{lex.text_property})")

        # Used by the explorer's entity search box and the agent's name lookup,
        # not by GraphRAG retrieval. Which properties hold an entity's text is
        # corpus-specific: a Claim is identified by its text, a Document by its
        # title, and neither has a `name`.
        create_fulltext_index(
            driver,
            name=ENTITY_FULLTEXT_INDEX_NAME,
            label="__Entity__",
            node_properties=list(lex.entity_text_properties),
            neo4j_database=database,
        )
        print(
            f"fulltext    {ENTITY_FULLTEXT_INDEX_NAME} "
            f"(on __Entity__.{', .'.join(lex.entity_text_properties)})"
        )

        wait_until_online(driver, database)
    finally:
        driver.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
