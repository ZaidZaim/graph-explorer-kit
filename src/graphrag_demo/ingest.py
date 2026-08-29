"""Build the knowledge graph from the documents in ./data.

SimpleKGPipeline does four things per file: load it, split it into chunks, embed
each chunk, and ask the LLM to extract entities/relationships constrained by
DEMO_SCHEMA. The result is a lexical layer:

    (:Chunk)-[:FROM_DOCUMENT]->(:Document)
    (:Chunk)-[:NEXT_CHUNK]->(:Chunk)

plus an entity layer hanging off it:

    (:Person)-[:FROM_CHUNK]->(:Chunk)
    (:Person)-[:WORKS_AT]->(:Organization)

Extracted entities also carry the reserved `__Entity__` and `__KGBuilder__` labels.
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

from neo4j_graphrag.components.resolver import SinglePropertyExactMatchResolver
from neo4j_graphrag.components.text_splitters.fixed_size_splitter import FixedSizeSplitter
from neo4j_graphrag.experimental.pipeline.kg_builder import SimpleKGPipeline

from graphrag_demo.config import DATA_DIR, get_database, get_driver, get_embedder, get_llm
from graphrag_demo.kg_schema import DEMO_SCHEMA

SUPPORTED_SUFFIXES = {".md", ".txt", ".pdf"}


def discover_documents(directory: Path) -> list[Path]:
    return sorted(p for p in directory.rglob("*") if p.suffix.lower() in SUPPORTED_SUFFIXES)


async def ingest(paths: list[Path], resolve_entities: bool = True) -> None:
    driver = get_driver()
    database = get_database()
    llm = get_llm()
    try:
        pipeline = SimpleKGPipeline(
            llm=llm,
            driver=driver,
            embedder=get_embedder(),
            schema=DEMO_SCHEMA,
            from_file=True,
            # 512-token chunks keep each extraction prompt small and focused;
            # the 64-token overlap stops entities being cut in half at boundaries.
            text_splitter=FixedSizeSplitter(chunk_size=512, chunk_overlap=64, approximate=True),
            # Resolution is run once at the end instead of per-file — bulk merges are cheaper.
            perform_entity_resolution=False,
            on_error="RAISE",
            neo4j_database=database,
        )

        for path in paths:
            print(f"ingesting {path.relative_to(DATA_DIR.parent)} ...", flush=True)
            await pipeline.run_async(
                file_path=str(path),
                document_metadata={"source": path.name, "collection": path.parent.name},
            )

        if resolve_entities:
            print("resolving duplicate entities ...", flush=True)
            # Groups every :__Entity__ sharing a label + `name` into one node,
            # merging their relationships. Makes re-ingesting the same corpus safe.
            resolver = SinglePropertyExactMatchResolver(
                driver,
                resolve_property="name",
                neo4j_database=database,
            )
            stats = await resolver.run()
            print(f"  {stats.number_of_nodes_to_resolve} candidates -> "
                  f"{stats.number_of_created_nodes} merged nodes")

        _print_summary(driver, database)
    finally:
        llm.close()
        driver.close()


def _print_summary(driver, database: str) -> None:
    docs, _, _ = driver.execute_query(
        """
        MATCH (d:Document)
        OPTIONAL MATCH (c:Chunk)-[:FROM_DOCUMENT]->(d)
        RETURN d.source AS document, count(c) AS chunks ORDER BY document
        """,
        database_=database,
    )
    print("\nDocuments")
    for record in docs:
        print(f"  {record['document']}: {record['chunks']} chunks")

    entities, _, _ = driver.execute_query(
        """
        MATCH (n:__Entity__)
        UNWIND labels(n) AS label
        WITH label WHERE NOT label IN ['__Entity__', '__KGBuilder__']
        RETURN label, count(*) AS count ORDER BY count DESC
        """,
        database_=database,
    )
    print("\nEntities")
    for record in entities:
        print(f"  {record['label']}: {record['count']}")

    rels, _, _ = driver.execute_query(
        """
        MATCH (:__Entity__)-[r]->(:__Entity__)
        RETURN type(r) AS type, count(*) AS count ORDER BY count DESC
        """,
        database_=database,
    )
    print("\nRelationships")
    for record in rels:
        print(f"  {record['type']}: {record['count']}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the demo knowledge graph.")
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        help="Files to ingest. Defaults to every supported file under ./data.",
    )
    parser.add_argument(
        "--no-resolve",
        action="store_true",
        help="Skip the entity-resolution pass at the end.",
    )
    args = parser.parse_args()

    paths = args.paths or discover_documents(DATA_DIR)
    if not paths:
        print(f"No documents found under {DATA_DIR}", file=sys.stderr)
        return 1

    missing = [p for p in paths if not p.is_file()]
    if missing:
        print(f"Not a file: {', '.join(str(p) for p in missing)}", file=sys.stderr)
        return 1

    asyncio.run(ingest(paths, resolve_entities=not args.no_resolve))
    return 0


if __name__ == "__main__":
    sys.exit(main())
