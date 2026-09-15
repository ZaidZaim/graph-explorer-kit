"""Adopt a knowledge graph this engine did not build.

The UAP graph was built with Neo4j Document Intelligence, which writes the same
*shape* as `neo4j-graphrag` — entities carrying `__Entity__`, hanging off a
chunk layer, hanging off source files — under different names, and embedded with
a different model. Most of that difference is handled by reading: the project's
`LexicalSpec` names DI's relationships and properties, and the engine's Cypher
follows them.

Two things cannot be handled by reading alone, and this is what they need:

1. A vector index is fixed to one label. DI's chunks carry `__Chunk__`, so the
   engine's chunk label is added alongside it — a label, on 78 nodes, adding no
   relationships and removing nothing.

2. Retrieval needs embeddings in *our* model's space. DI's are 3072-dim vectors
   from another model entirely; verbatim chunk text scores ~0.5 against them,
   which is cosine zero. So chunks are re-embedded into a second property,
   leaving DI's `embedding` and its index untouched and still working.

Everything here is additive and idempotent: run it twice and the second run
reports that there is nothing to do. `--undo` removes only what it added.
"""

from __future__ import annotations

import argparse
import sys

import neo4j

from graphrag_kit.config import (
    EMBEDDING_DIMENSIONS,
    describe_models,
    get_database,
    get_driver,
    get_embedder,
    use_utf8_stdout,
)
from graphrag_kit.project import ProjectSpec, load_project

#: Chunks embedded per API call. Large enough to keep the round trips down,
#: small enough to stay well inside the request size limit on long chunks.
EMBED_BATCH = 16


def survey(driver: neo4j.Driver, database: str, spec: ProjectSpec) -> dict:
    """What is already in place, before anything is written."""
    lex = spec.lexical

    def count(cypher: str) -> int:
        records, _, _ = driver.execute_query(cypher, database_=database)
        return records[0]["c"]

    adopted = lex.adopted_chunk_label
    return {
        "entities": count("MATCH (n:__Entity__) RETURN count(n) AS c"),
        "foreign_chunks": count(f"MATCH (c:`{adopted}`) RETURN count(c) AS c") if adopted else 0,
        "labelled_chunks": count(f"MATCH (c:`{lex.chunk_label}`) RETURN count(c) AS c"),
        "embedded": count(
            f"MATCH (c:`{lex.chunk_label}`) WHERE c.`{lex.embedding_property}` IS NOT NULL "
            f"RETURN count(c) AS c"
        ),
        "sources": count(f"MATCH (d:`{lex.source_label}`) RETURN count(d) AS c"),
    }


def add_chunk_label(driver: neo4j.Driver, database: str, spec: ProjectSpec) -> int:
    """Give the foreign chunks the engine's chunk label. Additive."""
    lex = spec.lexical
    if not lex.adopted_chunk_label:
        return 0
    records, _, _ = driver.execute_query(
        f"""
        MATCH (c:`{lex.adopted_chunk_label}`) WHERE NOT c:`{lex.chunk_label}`
        SET c:`{lex.chunk_label}`
        RETURN count(c) AS c
        """,
        database_=database,
    )
    return records[0]["c"]


def name_sources(driver: neo4j.Driver, database: str, spec: ProjectSpec) -> int:
    """Give each source file a readable name.

    Document Intelligence stores the upload URL in `path` — a signed GCS link,
    several hundred characters long and expired. That string is what every
    citation in every answer would otherwise quote. The filename is already in
    there; this lifts it out into the `source` property the engine prefers,
    which is also what `SimpleKGPipeline` writes for documents added later.
    """
    lex = spec.lexical
    first, *rest = lex.source_name_properties
    if not rest:
        return 0
    records, _, _ = driver.execute_query(
        f"""
        MATCH (d:`{lex.source_label}`)
        WHERE d.`{first}` IS NULL AND d.`{rest[0]}` IS NOT NULL
        // Strip the query string, then take the last path segment.
        SET d.`{first}` = last(split(split(d.`{rest[0]}`, '?')[0], '/'))
        RETURN count(d) AS c
        """,
        database_=database,
    )
    return records[0]["c"]


#: Constraint kinds that stop `Neo4jWriter` writing a new document into this
#: graph. The writer inserts extracted nodes with CREATE and de-duplicates
#: afterwards (see setup_indexes), so on a graph carrying NODE KEY or uniqueness
#: constraints the second mention of a name is a ConstraintValidationFailed —
#: and an existence constraint rejects any node the extractor did not fill that
#: property on. The pipeline logs the rejected batch and returns normally, so the
#: symptom is a document that ingests to nothing.
BLOCKING_CONSTRAINT_TYPES = (
    "NODE_KEY",
    "UNIQUENESS",
    "NODE_PROPERTY_EXISTENCE",
)

#: One node holds the definitions of whatever `--relax-constraints` dropped, so
#: `--undo` can put them back exactly. It lives in the graph rather than in a
#: file because it has to survive on whichever machine runs the undo.
ADOPTION_MARKER_LABEL = "__GraphRAGAdoption__"


def blocking_constraints(driver: neo4j.Driver, database: str, spec: ProjectSpec) -> list[dict]:
    """Constraints on any label a new document writes to, that would reject it.

    The lexical labels belong in this set as much as the schema ones do. An
    existence constraint on the adopted source-file label rejects the node the
    pipeline creates for a new file, because that node has no `__id__` — the
    foreign tool's own primary key, which nothing here can supply.
    """
    records, _, _ = driver.execute_query(
        "SHOW CONSTRAINTS YIELD name, type, labelsOrTypes, properties, createStatement "
        "RETURN name, type, labelsOrTypes, properties, createStatement",
        database_=database,
    )
    lex = spec.lexical
    labels = set(spec.labels) | {
        label
        for label in (
            lex.chunk_label,
            lex.adopted_chunk_label,
            lex.source_label,
            "Document",
            "Chunk",
        )
        if label
    }
    return [
        {
            "name": r["name"],
            "type": r["type"],
            "labels": r["labelsOrTypes"],
            "properties": r["properties"],
            "create": r["createStatement"],
        }
        for r in records
        if r["type"] in BLOCKING_CONSTRAINT_TYPES and labels.intersection(r["labelsOrTypes"] or [])
    ]


def relax_constraints(driver: neo4j.Driver, database: str, spec: ProjectSpec) -> list[dict]:
    """Drop the blocking constraints, keeping their definitions for `--undo`.

    A plain range index is created on each (label, property) pair afterwards, so
    dropping the constraint does not also cost the lookup speed its backing
    index provided.
    """
    blocking = blocking_constraints(driver, database, spec)
    if not blocking:
        return []
    for constraint in blocking:
        driver.execute_query(
            f"DROP CONSTRAINT {constraint['name']} IF EXISTS", database_=database
        )
        for label in constraint["labels"] or []:
            for prop in constraint["properties"] or []:
                index = f"adopted_{label}_{prop}".replace(".", "_")[:60]
                driver.execute_query(
                    f"CREATE INDEX {index} IF NOT EXISTS FOR (n:`{label}`) ON (n.`{prop}`)",
                    database_=database,
                )
    # Appended, not assigned. A second run drops whatever the first did not see
    # — a constraint on a label only reachable once ingestion got further — and
    # overwriting here would silently discard the first run's record, leaving
    # `--undo` able to restore only the last batch.
    driver.execute_query(
        f"""
        MERGE (m:`{ADOPTION_MARKER_LABEL}` {{project: $project}})
        SET m.dropped_constraints =
              [s IN coalesce(m.dropped_constraints, []) WHERE NOT s IN $definitions]
              + $definitions,
            m.dropped_at = coalesce(m.dropped_at, datetime()),
            m.updated_at = datetime()
        """,
        database_=database,
        project=spec.key,
        definitions=[c["create"] for c in blocking],
    )
    return blocking


def restore_constraints(driver: neo4j.Driver, database: str, spec: ProjectSpec) -> int:
    """Recreate whatever `relax_constraints` dropped.

    Recreating a NODE KEY fails if the data now violates it — which is exactly
    what ingesting a second document may have introduced. The failure is
    reported per constraint rather than aborting, so the rest are still restored.
    """
    records, _, _ = driver.execute_query(
        f"MATCH (m:`{ADOPTION_MARKER_LABEL}` {{project: $project}}) "
        f"RETURN m.dropped_constraints AS definitions",
        database_=database,
        project=spec.key,
    )
    if not records or not records[0]["definitions"]:
        return 0
    restored = 0
    for statement in records[0]["definitions"]:
        try:
            driver.execute_query(statement, database_=database)
            restored += 1
        except neo4j.exceptions.Neo4jError as exc:
            print(f"  could not restore: {statement}\n    {exc.message}")
    driver.execute_query(
        f"MATCH (m:`{ADOPTION_MARKER_LABEL}` {{project: $project}}) DETACH DELETE m",
        database_=database,
        project=spec.key,
    )
    return restored


def embed_chunks(driver: neo4j.Driver, database: str, spec: ProjectSpec) -> int:
    """Embed every chunk that has no embedding in our model's property yet.

    Resumable by construction: the MATCH selects on the property being written,
    so an interrupted run picks up where it stopped rather than paying for the
    whole corpus again.
    """
    lex = spec.lexical
    embedder = get_embedder()
    total = 0
    while True:
        records, _, _ = driver.execute_query(
            f"""
            MATCH (c:`{lex.chunk_label}`)
            WHERE c.`{lex.embedding_property}` IS NULL AND c.`{lex.text_property}` IS NOT NULL
            RETURN elementId(c) AS id, c.`{lex.text_property}` AS text
            LIMIT $limit
            """,
            database_=database,
            limit=EMBED_BATCH,
        )
        if not records:
            return total
        rows = [
            {"id": r["id"], "vector": embedder.embed_query(r["text"])}
            for r in records
            if (r["text"] or "").strip()
        ]
        if not rows:
            # Chunks that are whitespace only would otherwise be selected for
            # ever. Mark them so the loop terminates.
            driver.execute_query(
                f"""
                UNWIND $ids AS id
                MATCH (c) WHERE elementId(c) = id
                SET c.`{lex.embedding_property}` = []
                """,
                database_=database,
                ids=[r["id"] for r in records],
            )
            total += len(records)
            continue
        driver.execute_query(
            f"""
            UNWIND $rows AS row
            MATCH (c) WHERE elementId(c) = row.id
            SET c.`{lex.embedding_property}` = row.vector
            """,
            database_=database,
            rows=rows,
        )
        total += len(rows)
        print(f"  embedded {total} chunks", flush=True)


def undo(driver: neo4j.Driver, database: str, spec: ProjectSpec) -> None:
    """Remove exactly what adoption added: the label and our embedding property."""
    lex = spec.lexical
    if lex.adopted_chunk_label:
        records, _, _ = driver.execute_query(
            f"""
            MATCH (c:`{lex.chunk_label}`:`{lex.adopted_chunk_label}`)
            REMOVE c:`{lex.chunk_label}`
            RETURN count(c) AS c
            """,
            database_=database,
        )
        print(f"removed :{lex.chunk_label} from {records[0]['c']} chunks")
    records, _, _ = driver.execute_query(
        f"""
        MATCH (c:`{lex.adopted_chunk_label or lex.chunk_label}`)
        WHERE c.`{lex.embedding_property}` IS NOT NULL
        REMOVE c.`{lex.embedding_property}`
        RETURN count(c) AS c
        """,
        database_=database,
    )
    print(f"removed .{lex.embedding_property} from {records[0]['c']} chunks")

    first = lex.source_name_properties[0]
    records, _, _ = driver.execute_query(
        f"MATCH (d:`{lex.source_label}`) WHERE d.`{first}` IS NOT NULL "
        f"REMOVE d.`{first}` RETURN count(d) AS c",
        database_=database,
    )
    print(f"removed .{first} from {records[0]['c']} source files")

    restored = restore_constraints(driver, database, spec)
    if restored:
        print(f"restored {restored} constraints")
    print(
        "\nDocument Intelligence's own embedding, its vector index and every "
        "node and relationship it wrote are untouched."
    )


def main() -> int:
    use_utf8_stdout()
    spec = load_project()
    parser = argparse.ArgumentParser(
        description=f"Adopt an existing {spec.title} graph into the GraphRAG engine."
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Report what would change and write nothing."
    )
    parser.add_argument(
        "--undo", action="store_true", help="Remove what adoption added, and nothing else."
    )
    parser.add_argument(
        "--skip-embeddings", action="store_true", help="Label the chunks but do not embed them."
    )
    parser.add_argument(
        "--relax-constraints",
        action="store_true",
        help=(
            "Drop the NODE KEY / uniqueness / existence constraints that stop new "
            "documents being ingested. Reversible with --undo."
        ),
    )
    args = parser.parse_args()

    lex = spec.lexical
    print(f"project: {spec.key}")
    print(f"models:  {describe_models()}")
    driver = get_driver()
    database = get_database()
    try:
        before = survey(driver, database, spec)
        rows = [("entities", before["entities"])]
        if lex.adopted_chunk_label:
            rows.append((f":{lex.adopted_chunk_label} chunks", before["foreign_chunks"]))
        rows += [
            (f":{lex.chunk_label} chunks (engine)", before["labelled_chunks"]),
            (f"  with .{lex.embedding_property}", before["embedded"]),
            (f":{lex.source_label} source files", before["sources"]),
        ]
        width = max(len(label) for label, _ in rows)
        print(f"\nGraph as it stands ({database}):")
        for label, value in rows:
            print(f"  {label.ljust(width)}  {value}")

        blocking = blocking_constraints(driver, database, spec)
        if blocking:
            print(f"\n{len(blocking)} constraints would reject a new document:")
            for constraint in blocking[:6]:
                labels = "/".join(constraint["labels"] or [])
                props = ", ".join(constraint["properties"] or [])
                print(f"  {constraint['type']:<24} ({labels}.{props})")
            if len(blocking) > 6:
                print(f"  ... and {len(blocking) - 6} more")
            print(
                "  Ingesting new documents is blocked until these are dropped: the\n"
                "  writer inserts with CREATE and de-duplicates afterwards, so a name\n"
                "  that appears twice is a constraint violation. Pass --relax-constraints\n"
                "  to drop them, and --undo to put them back."
            )

        pending_label = before["foreign_chunks"] - before["labelled_chunks"]
        chunks_total = max(before["labelled_chunks"], before["foreign_chunks"])
        pending_embed = chunks_total - before["embedded"]

        if args.undo:
            print()
            undo(driver, database, spec)
            return 0

        if args.dry_run:
            print("\nWould write:")
            print(f"  add :{lex.chunk_label} to {max(pending_label, 0)} chunk nodes")
            print(
                f"  embed {max(pending_embed, 0)} chunks into .{lex.embedding_property} "
                f"({EMBEDDING_DIMENSIONS} dims)"
            )
            print(f"  set .{lex.source_name_properties[0]} on source files missing a name")
            if args.relax_constraints:
                print(f"  drop {len(blocking)} blocking constraints, keeping range indexes")
            print("  create the vector, fulltext and range indexes (graphrag-setup)")
            print("\nNothing else is touched. Re-run without --dry-run to apply.")
            return 0

        labelled = add_chunk_label(driver, database, spec)
        print(f"\nadded :{lex.chunk_label} to {labelled} chunks")

        named = name_sources(driver, database, spec)
        print(f"named {named} source files from their path")

        if args.relax_constraints:
            dropped = relax_constraints(driver, database, spec)
            print(f"dropped {len(dropped)} blocking constraints (range indexes kept)")

        if args.skip_embeddings:
            print("skipping embeddings (--skip-embeddings)")
        else:
            print(f"embedding chunks into .{lex.embedding_property} ...", flush=True)
            embedded = embed_chunks(driver, database, spec)
            print(f"embedded {embedded} chunks")
    finally:
        driver.close()

    print("\nNow run: graphrag-setup   (creates the indexes over what was just adopted)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
