"""Build the knowledge graph from the active project's documents.

Produces the lexical layer:

    (:Chunk)-[:FROM_DOCUMENT]->(:Document)
    (:Chunk)-[:NEXT_CHUNK]->(:Chunk)

and the entity layer hanging off it:

    (:Person)-[:FROM_CHUNK]->(:Chunk)
    (:Person)-[:INVOLVED_IN]->(:Event)

Extracted entities also carry the reserved __Entity__ and __KGBuilder__ labels.
Which entities exist at all is decided entirely by the project's GraphSchema.
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

from neo4j_graphrag.components.resolver import SinglePropertyExactMatchResolver
from neo4j_graphrag.components.text_splitters.fixed_size_splitter import FixedSizeSplitter
from neo4j_graphrag.experimental.pipeline.kg_builder import SimpleKGPipeline

from graphrag_kit.config import (
    describe_models,
    get_database,
    get_driver,
    get_embedder,
    get_llm,
    use_utf8_stdout,
)
from graphrag_kit.project import ProjectSpec, load_project

SUPPORTED_SUFFIXES = {".md", ".txt", ".pdf"}

# Braces in the JSON example are doubled: this string is rendered with str.format(),
# so single braces would be read as placeholders and raise KeyError.
EXTRACTION_PROMPT = """
Extract the entities (nodes) and their types from the text below, and the
relationships between them.

Return result as JSON using the following format:
{{"nodes": [ {{"id": "0", "label": "Person", "properties": {{"name": "Ada Lovelace"}} }}],
"relationships": [{{"type": "INVOLVED_IN", "start_node_id": "0",
  "end_node_id": "1", "properties": {{"role": "author"}} }}] }}

Use only the following node and relationship types:
{schema}

Assign a unique ID (string) to each node, and reuse it to define relationships.
Respect the source and target node types for each relationship, and the direction.

General rules:
- Do not invent entities the text does not mention.
- Prefer the fullest name form the text uses, so the same thing is named
  identically across documents. Entities are de-duplicated by exact name match,
  so inconsistent naming leaves duplicates in the graph.
- Publications, newswires and article headlines are provenance, not entities.

__PROJECT_RULES__

Make sure you adhere to the following rules to produce valid JSON objects:
- Do not return any additional information other than the JSON in it.
- Omit any backticks around the JSON - simply output the JSON on its own.
- The JSON object must not wrapped into a list - it is its own JSON object.
- Property names must be enclosed in double quotes

Examples:
{examples}

Input text:
{text}
"""


def build_prompt(spec: ProjectSpec) -> str:
    """Splice the project's rules into the shared extraction prompt.

    The rules are substituted here rather than at format() time so the template
    handed to the pipeline carries only the placeholders the library itself
    fills in: schema, examples, text.
    """
    return EXTRACTION_PROMPT.replace("__PROJECT_RULES__", spec.extraction_rules.strip())


def discover_documents(directory: Path) -> list[Path]:
    return sorted(p for p in directory.rglob("*") if p.suffix.lower() in SUPPORTED_SUFFIXES)


def evidence_rollup_query(levels: tuple[str, ...]) -> str:
    """Cypher that rolls each entity up to its strongest observed evidence level.

    Run BEFORE resolution, on purpose. apoc.refactor.mergeNodes is called with
    properties:'discard', so it keeps an arbitrary one of the duplicates' status
    values — an entity confirmed in one document but merely rumoured in another
    ends up with whichever the merge happened to pick. Writing the rolled-up
    value onto every duplicate first means whichever node survives already
    carries the right answer, and evidence_levels keeps the full observed set.
    """
    ordered = ", ".join(repr(level) for level in levels)
    fallback = repr(levels[len(levels) // 2])
    return f"""
    MATCH (n:__Entity__) WHERE n.name IS NOT NULL
    WITH toLower(trim(n.name)) AS key,
         head([l IN labels(n) WHERE NOT l IN ['__Entity__', '__KGBuilder__']]) AS label,
         collect(n) AS dupes
    WITH dupes,
         [s IN [{ordered}] WHERE any(d IN dupes WHERE d.status = s)] AS observed
    FOREACH (d IN dupes |
        SET d.status = coalesce(head(observed), d.status, {fallback}),
            d.evidence_levels = observed
    )
    RETURN count(*) AS groups
    """


async def ingest(spec: ProjectSpec, paths: list[Path], resolve_entities: bool = True) -> None:
    driver = get_driver()
    database = get_database()
    llm = get_llm()
    try:
        pipeline = SimpleKGPipeline(
            llm=llm,
            driver=driver,
            embedder=get_embedder(),
            schema=spec.schema,
            prompt_template=build_prompt(spec),
            from_file=True,
            # 700-token chunks keep an assertion and its qualifying sentence in one
            # extraction call; the overlap stops entities being cut in half.
            text_splitter=FixedSizeSplitter(chunk_size=700, chunk_overlap=100, approximate=True),
            # Resolution runs once at the end instead of per-file: bulk merges are cheaper.
            perform_entity_resolution=False,
            on_error="RAISE",
            neo4j_database=database,
        )

        for path in paths:
            print(f"ingesting {path.name} ...", flush=True)
            await pipeline.run_async(
                file_path=str(path),
                document_metadata={"source": path.name, "project": spec.key},
            )

        records, _, _ = driver.execute_query(
            evidence_rollup_query(spec.evidence_levels), database_=database
        )
        print(f"normalised evidence levels across {records[0]['groups']} entity groups")

        if resolve_entities:
            print("resolving duplicate entities ...", flush=True)
            resolver = SinglePropertyExactMatchResolver(
                driver, resolve_property="name", neo4j_database=database
            )
            stats = await resolver.run()
            print(
                f"  {stats.number_of_nodes_to_resolve} candidates -> "
                f"{stats.number_of_created_nodes} nodes after merge"
            )

        summarise(driver, database)
    finally:
        # aclose(), not close(): we are inside asyncio.run() and the sync close()
        # raises "Cannot call close() from a running async context".
        await llm.aclose()
        driver.close()


def summarise(driver, database: str) -> None:
    def q(cypher):
        records, _, _ = driver.execute_query(cypher, database_=database)
        return records

    print("\nDocuments")
    for r in q(
        "MATCH (d:Document) OPTIONAL MATCH (c:Chunk)-[:FROM_DOCUMENT]->(d) "
        "RETURN d.source AS doc, count(c) AS chunks ORDER BY doc"
    ):
        print(f"  {r['doc']}: {r['chunks']} chunks")

    print("\nEntities")
    for r in q(
        "MATCH (n:__Entity__) UNWIND labels(n) AS label "
        "WITH label WHERE NOT label IN ['__Entity__','__KGBuilder__'] "
        "RETURN label, count(*) AS c ORDER BY c DESC"
    ):
        print(f"  {r['label']}: {r['c']}")

    print("\nEvidence level")
    for r in q(
        "MATCH (n:__Entity__) RETURN coalesce(n.status,'unrated') AS status, "
        "count(*) AS c ORDER BY c DESC"
    ):
        print(f"  {r['status']}: {r['c']}")

    print("\nRelationships")
    for r in q(
        "MATCH (:__Entity__)-[r]->(:__Entity__) RETURN type(r) AS t, count(*) AS c ORDER BY c DESC"
    ):
        print(f"  {r['t']}: {r['c']}")


def main() -> int:
    use_utf8_stdout()
    spec = load_project()
    parser = argparse.ArgumentParser(description=f"Build the {spec.title} knowledge graph.")
    parser.add_argument("paths", nargs="*", type=Path, help="Files to ingest.")
    parser.add_argument("--no-resolve", action="store_true", help="Skip entity resolution.")
    args = parser.parse_args()

    paths = args.paths or discover_documents(spec.data_dir)
    if not paths:
        print(f"No documents found under {spec.data_dir}", file=sys.stderr)
        return 1
    missing = [p for p in paths if not p.is_file()]
    if missing:
        print(f"Not a file: {', '.join(str(p) for p in missing)}", file=sys.stderr)
        return 1

    print(f"project: {spec.key} ({len(paths)} documents)")
    print(f"models:  {describe_models()}")
    asyncio.run(ingest(spec, paths, resolve_entities=not args.no_resolve))
    return 0


if __name__ == "__main__":
    sys.exit(main())
