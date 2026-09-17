"""Delete everything this demo created, so ingestion can be re-run clean.

Refuses outright on a project whose graph was built by something else. There,
"everything this demo created" is not a set this command can compute: the
labels it would delete are the same labels the other tool wrote, and a project
that only adopted a graph has no business deleting it. Use
`graphrag-adopt --undo` to remove what adoption added.
"""

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
from graphrag_kit.project import load_project

RANGE_INDEX_NAMES = ["entity_name", "entity_status", "source_name", "document_path"]


def main() -> int:
    use_utf8_stdout()
    spec = load_project()
    parser = argparse.ArgumentParser(description="Delete the project graph.")
    parser.add_argument("--yes", action="store_true", help="Confirm the deletion.")
    parser.add_argument("--keep-indexes", action="store_true", help="Delete data, keep indexes.")
    parser.add_argument(
        "--i-know-this-graph-is-not-mine",
        action="store_true",
        help=(
            "Required for a project with owns_graph=False. Deletes a graph this "
            "project did not build. There is no undo."
        ),
    )
    args = parser.parse_args()

    if not spec.owns_graph and not args.i_know_this_graph_is_not_mine:
        print(
            f"Refusing: project {spec.key!r} declares owns_graph=False, so this graph was\n"
            f"built by something else and deleting it would destroy data this demo did not\n"
            f"create. To remove only what adoption added, run:\n\n"
            f"    graphrag-adopt --undo\n\n"
            f"If you really do mean to empty the database, pass\n"
            f"--i-know-this-graph-is-not-mine as well as --yes.",
            file=sys.stderr,
        )
        return 1

    # Only labels this demo writes. A bare `MATCH (n) DETACH DELETE n` would take
    # out anything else sharing the database.
    lex = spec.lexical
    labels = [
        lex.source_label,
        lex.chunk_label,
        "__Entity__",
        "__KGBuilder__",
    ]

    if not args.yes:
        print(
            "This deletes every node labelled "
            + ", ".join(f":{label}" for label in labels)
            + ". Re-run with --yes to confirm.",
            file=sys.stderr,
        )
        return 1

    driver = get_driver()
    database = get_database()
    try:
        # CALL { ... } IN TRANSACTIONS is only legal in an implicit transaction,
        # so this goes through session.run() rather than driver.execute_query().
        with driver.session(database=database) as session:
            for label in labels:
                session.run(
                    f"MATCH (n:`{label}`) "
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
