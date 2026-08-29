"""Delete everything this demo created, so `graphrag-ingest` can be re-run clean.

Deletes nodes in batches and drops the demo's indexes. Refuses to run without
`--yes` because it is destructive.
"""

from __future__ import annotations

import argparse
import sys

from neo4j_graphrag.indexes import drop_index_if_exists

from graphrag_demo.config import (
    FULLTEXT_INDEX_NAME,
    VECTOR_INDEX_NAME,
    get_database,
    get_driver,
)

# Only labels this demo writes. A bare `MATCH (n) DETACH DELETE n` would take
# out anything else living in the same database.
DEMO_LABELS = ["Document", "Chunk", "__Entity__", "__KGBuilder__"]


def main() -> int:
    parser = argparse.ArgumentParser(description="Delete the demo graph.")
    parser.add_argument("--yes", action="store_true", help="Confirm the deletion.")
    parser.add_argument(
        "--keep-indexes", action="store_true", help="Delete data but leave indexes in place."
    )
    args = parser.parse_args()

    if not args.yes:
        print(
            "This deletes all Document, Chunk and extracted entity nodes. "
            "Re-run with --yes to confirm.",
            file=sys.stderr,
        )
        return 1

    driver = get_driver()
    database = get_database()
    try:
        # CALL { ... } IN TRANSACTIONS is only legal in an implicit transaction,
        # so this goes through session.run() rather than driver.execute_query().
        with driver.session(database=database) as session:
            for label in DEMO_LABELS:
                session.run(
                    f"MATCH (n:{label}) "
                    f"CALL (n) {{ DETACH DELETE n }} IN TRANSACTIONS OF 1000 ROWS"
                ).consume()
                print(f"deleted :{label}")

        if not args.keep_indexes:
            for name in (VECTOR_INDEX_NAME, FULLTEXT_INDEX_NAME):
                drop_index_if_exists(driver, name, neo4j_database=database)
                print(f"dropped index {name}")
            for name in ("entity_name", "document_path", "chunk_index"):
                driver.execute_query(f"DROP INDEX {name} IF EXISTS", database_=database)
                print(f"dropped index {name}")
    finally:
        driver.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
