"""Create indexes, then wait until every index is ONLINE.

Run this once before ingesting. Writing embeddings before the vector index is
ONLINE silently produces a graph that vector search cannot see.

Note on constraints: `Neo4jWriter` inserts extracted nodes with `CREATE`, not
`MERGE`, and de-duplicates afterwards via `SinglePropertyExactMatchResolver`. A
uniqueness constraint on e.g. `Person.name` would therefore abort ingestion the
first time a person is mentioned in two chunks. Plain range indexes give the
lookup speed without the write-time rejection.
"""

from __future__ import annotations

import sys
import time

import neo4j
from neo4j_graphrag.indexes import create_fulltext_index, create_vector_index

from graphrag_demo.config import (
    CHUNK_EMBEDDING_PROPERTY,
    CHUNK_LABEL,
    CHUNK_TEXT_PROPERTY,
    EMBEDDING_DIMENSIONS,
    FULLTEXT_INDEX_NAME,
    VECTOR_INDEX_NAME,
    get_database,
    get_driver,
)

RANGE_INDEXES = [
    # Every extracted entity carries the reserved :__Entity__ label, so one index
    # here serves Person, Organization, Product, Technology and Location lookups
    # and speeds up the entity-resolution merge.
    ("entity_name", "CREATE INDEX entity_name IF NOT EXISTS FOR (n:__Entity__) ON (n.name)"),
    ("document_path", "CREATE INDEX document_path IF NOT EXISTS FOR (d:Document) ON (d.path)"),
    ("chunk_index", "CREATE INDEX chunk_index IF NOT EXISTS FOR (c:Chunk) ON (c.index)"),
]


def wait_until_online(driver: neo4j.Driver, database: str, timeout_s: int = 120) -> None:
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
    driver = get_driver()
    database = get_database()
    try:
        for name, statement in RANGE_INDEXES:
            driver.execute_query(statement, database_=database)
            print(f"range       {name}")

        create_vector_index(
            driver,
            name=VECTOR_INDEX_NAME,
            label=CHUNK_LABEL,
            embedding_property=CHUNK_EMBEDDING_PROPERTY,
            dimensions=EMBEDDING_DIMENSIONS,
            similarity_fn="cosine",
            neo4j_database=database,
        )
        print(f"vector      {VECTOR_INDEX_NAME} ({EMBEDDING_DIMENSIONS} dims, cosine)")

        create_fulltext_index(
            driver,
            name=FULLTEXT_INDEX_NAME,
            label=CHUNK_LABEL,
            node_properties=[CHUNK_TEXT_PROPERTY],
            neo4j_database=database,
        )
        print(f"fulltext    {FULLTEXT_INDEX_NAME} (on {CHUNK_LABEL}.{CHUNK_TEXT_PROPERTY})")

        wait_until_online(driver, database)
    finally:
        driver.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
