"""Delete everything this demo created, so ingestion can be re-run clean."""

from __future__ import annotations

import argparse
import sys

from neo4j_graphrag.indexes import drop_index_if_exists

from graphrag_kit.config import (
    ENTITY_FULLTEXT_INDEX_NAME,
    FULLTEXT_INDEX_NAME,
    VECTOR_INDEX_NAME,
    get_database,
    get_driver,
    use_utf8_stdout,
)

# Only labels this demo writes. A bare `MATCH (n) DETACH DELETE n` would take out
# anything else sharing the database.
DEMO_LABELS = ["Document", "Chunk", "__Entity__", "__KGBuilder__"]
RANGE_INDEX_NAMES = ["entity_name", "entity_status", "document_path"]


def main() -> int:
    use_utf8_stdout()
    parser = argparse.ArgumentParser(description="Delete the project graph.")
    parser.add_argument("--yes", action="store_true", help="Confirm the deletion.")
    parser.add_argument("--keep-indexes", action="store_true", help="Delete data, keep indexes.")
    args = parser.parse_args()

    if not args.yes:
        print(
            "This deletes all Document, Chunk and extracted POLE entity nodes. "
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
            for name in (VECTOR_INDEX_NAME, FULLTEXT_INDEX_NAME, ENTITY_FULLTEXT_INDEX_NAME):
                drop_index_if_exists(driver, name, neo4j_database=database)
                print(f"dropped index {name}")
            for name in RANGE_INDEX_NAMES:
                driver.execute_query(f"DROP INDEX {name} IF EXISTS", database_=database)
                print(f"dropped index {name}")
    finally:
        driver.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
