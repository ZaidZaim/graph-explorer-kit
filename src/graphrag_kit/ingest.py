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
from neo4j_graphrag.components.types import LexicalGraphConfig
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

#: What `SimpleKGPipeline`'s default file loader can actually read. Not .txt:
#: the loader dispatches on suffix and raises UnsupportedDocumentFormatError for
#: anything outside this set, which surfaces as a document that ingests to
#: nothing rather than as an error about the file type.
SUPPORTED_SUFFIXES = {".md", ".markdown", ".pdf"}

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


def lexical_graph_config(spec: ProjectSpec) -> LexicalGraphConfig:
    """Write the lexical layer under the names this graph already uses.

    Without this the pipeline writes its own defaults — `Document` for a source
    file and `embedding` for a chunk vector — and both are already taken in an
    adopted graph, by different things:

      * `Document` here is an extracted *entity*, a released record with a title
        and a classification marking. The writer reserves that label for source
        files, so an extracted Document is written as a lexical node and never
        gets `__Entity__` — which makes it invisible to every query the engine
        runs, since they all filter on that label.
      * `embedding` holds the other tool's vectors, from a different model,
        under its own index.

    Configuring the writer is much better than correcting it afterwards: a
    post-hoc relabelling cannot reliably tell an extracted `Document` entity
    from a source file, and guessing wrong silently turns records into files.
    """
    lex = spec.lexical
    return LexicalGraphConfig(
        document_node_label=lex.source_label,
        chunk_node_label=lex.chunk_label,
        chunk_to_document_relationship_type=lex.chunk_to_source_write,
        node_to_chunk_relationship_type=lex.entity_to_chunk_write,
        chunk_text_property=lex.text_property,
        chunk_embedding_property=lex.embedding_property,
    )


def build_pipeline(spec: ProjectSpec, driver, llm, embedder, database: str) -> SimpleKGPipeline:
    return SimpleKGPipeline(
        llm=llm,
        driver=driver,
        embedder=embedder,
        schema=spec.schema,
        prompt_template=build_prompt(spec),
        lexical_graph_config=lexical_graph_config(spec),
        from_file=True,
        # 700-token chunks keep an assertion and its qualifying sentence in one
        # extraction call; the overlap stops entities being cut in half.
        text_splitter=FixedSizeSplitter(chunk_size=700, chunk_overlap=100, approximate=True),
        # Resolution runs once at the end instead of per-file: bulk merges are cheaper.
        perform_entity_resolution=False,
        on_error="RAISE",
        neo4j_database=database,
    )


def resolution_filter(spec: ProjectSpec, sources: list[str]) -> str | None:
    """A WHERE clause confining entity resolution to entities from `sources`.

    Resolution merges every pair of same-label, same-name nodes it is shown, and
    the merge is not reversible. Run unscoped over a graph built by another tool
    it will happily merge records that tool kept apart on purpose — two distinct
    sightings both named "Fireball sighting", say — and the distinction is gone.

    Scoping to the document just ingested keeps the useful case (the same person
    named twice in one new file) and removes the destructive one. Returns None
    for a project that owns its whole graph, where global resolution is correct.
    """
    if spec.owns_graph:
        return None
    lex = spec.lexical
    quoted = ", ".join(repr(name) for name in sources)
    return (
        f"WHERE EXISTS {{ (entity)-[:{lex.entity_to_chunk}]->"
        f"(:`{lex.chunk_label}`)-[:{lex.chunk_to_source}]->"
        f"(d:`{lex.source_label}`) WHERE d.`{lex.source_name_properties[0]}` IN [{quoted}] }}"
    )


async def ingest_files(
    spec: ProjectSpec,
    paths: list[Path],
    driver,
    llm,
    database: str,
    resolve_entities: bool = True,
    report=print,
) -> dict:
    """Build the graph from `paths` using a caller-supplied driver and model.

    Split out from `ingest()` so the explorer can ingest an uploaded document on
    its own connection and stream progress, rather than shelling out to the CLI.
    `report` receives one human-readable line per stage.
    """
    pipeline = build_pipeline(spec, driver, llm, get_embedder(), database)

    for path in paths:
        report(f"reading {path.name}")
        report(f"extracting entities from {path.name}")
        await pipeline.run_async(
            file_path=str(path),
            document_metadata={"source": path.name, "project": spec.key},
        )

    if spec.grades_evidence:
        records, _, _ = driver.execute_query(
            evidence_rollup_query(spec.evidence_levels), database_=database
        )
        report(f"normalised evidence levels across {records[0]['groups']} entity groups")

    stats = {}
    if resolve_entities:
        scope = resolution_filter(spec, [path.name for path in paths])
        report(
            "resolving duplicates within the new document"
            if scope
            else "resolving duplicate entities"
        )
        resolver = SinglePropertyExactMatchResolver(
            driver,
            filter_query=scope,
            resolve_property="name",
            neo4j_database=database,
        )
        resolution = await resolver.run()
        stats = {
            "candidates": resolution.number_of_nodes_to_resolve,
            "after_merge": resolution.number_of_created_nodes,
        }
        report(f"{stats['candidates']} candidates -> {stats['after_merge']} nodes after merge")
    return stats


async def ingest(spec: ProjectSpec, paths: list[Path], resolve_entities: bool = True) -> None:
    driver = get_driver()
    database = get_database()
    llm = get_llm()
    try:
        await ingest_files(spec, paths, driver, llm, database, resolve_entities)
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
