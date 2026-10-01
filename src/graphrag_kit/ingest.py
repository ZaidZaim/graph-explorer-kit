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
import time
from pathlib import Path
from uuid import uuid4

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
from graphrag_kit.prepare import PreparedFileLoader
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


def evidence_rollup_query(spec: ProjectSpec, where: str | None) -> str:
    """Cypher that rolls each entity up to its strongest observed evidence level.

    Run BEFORE resolution, on purpose. apoc.refactor.mergeNodes is called with
    properties:'discard', so it keeps an arbitrary one of the duplicates' status
    values — an entity confirmed in one document but merely rumoured in another
    ends up with whichever the merge happened to pick. Writing the rolled-up
    value onto every duplicate first means whichever node survives already
    carries the right answer, and evidence_levels keeps the full observed set.

    The candidate filter and exact-name/label grouping match the resolver.
    In particular, normalization must not modify adopted records that resolution
    would leave alone. Call only for projects that grade evidence.
    """
    levels = spec.evidence_levels
    ordered = ", ".join(repr(level) for level in levels)
    fallback = repr(levels[-1])
    prop = "`" + spec.evidence_property.replace("`", "``") + "`"
    return f"""
    MATCH (entity:__Entity__) {where or ''}
    WITH entity WHERE entity.name IS NOT NULL
    UNWIND labels(entity) AS label
    WITH entity, label WHERE NOT label IN ['__Entity__', '__KGBuilder__']
    WITH entity.name AS key, label, collect(entity) AS dupes
    WITH dupes,
         [s IN [{ordered}] WHERE any(d IN dupes
             WHERE d.{prop} = s OR s IN coalesce(d.evidence_levels, []))] AS observed
    FOREACH (d IN dupes |
        SET d.{prop} = coalesce(head(observed), d.{prop}, {fallback}),
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


def build_pipeline(
    spec: ProjectSpec, driver, llm, embedder, database: str, lenient: bool = False
) -> SimpleKGPipeline:
    """The pipeline for one document.

    `lenient` tells the extractor to log and skip a chunk the model answers with
    malformed JSON instead of failing the whole document. Off by default, so a
    single upload reports its problem; on for a batch of hundreds of scans, where
    one unparseable answer in a 400-chunk file should cost that chunk, not the file.
    """
    return SimpleKGPipeline(
        llm=llm,
        driver=driver,
        embedder=embedder,
        schema=spec.schema,
        prompt_template=build_prompt(spec),
        lexical_graph_config=lexical_graph_config(spec),
        from_file=True,
        # PDFs are read per page with an OCR fallback (see prepare.py), so a scan
        # uploaded through the explorer does not silently ingest to nothing.
        file_loader=PreparedFileLoader(),
        # 700-token chunks keep an assertion and its qualifying sentence in one
        # extraction call; the overlap stops entities being cut in half.
        text_splitter=FixedSizeSplitter(chunk_size=700, chunk_overlap=100, approximate=True),
        # Resolution runs once at the end instead of per-file: bulk merges are cheaper.
        perform_entity_resolution=False,
        on_error="IGNORE" if lenient else "RAISE",
        neo4j_database=database,
    )


def resolution_filter(spec: ProjectSpec, sources: list[str] | None) -> str | None:
    """A WHERE clause confining entity resolution to entities from `sources`.

    Resolution merges every pair of same-label, same-name nodes it is shown, and
    the merge is not reversible. Run unscoped over a graph built by another tool
    it will happily merge records that tool kept apart on purpose — two distinct
    sightings both named "Fireball sighting", say — and the distinction is gone.

    Scoping to the document just ingested keeps the useful case (the same person
    named twice in one new file) and removes the destructive one. A project that
    owns its whole graph gets no document scope, since global resolution is
    correct there — but still the placeholder exclusion, and None only when
    there is nothing at all to exclude.

    `sources=None` widens the scope to every source file *this project* wrote —
    the `project` key stamped on each one at ingest — and still not to the
    adopted graph. That is the right scope for a corpus ingested in several
    sittings: the agency named in Tuesday's batch and again in Wednesday's
    should be one node, and the batches cannot know about each other.
    """
    clauses: list[str] = []
    if spec.placeholder_names:
        # "[REDACTED]" is not a name, and two records carrying it are not one
        # record. Applied whatever the scope, on an owned graph as much as an
        # adopted one.
        placeholders = ", ".join(repr(n.lower()) for n in spec.placeholder_names)
        clauses.append(f"NOT toLower(trim(entity.name)) IN [{placeholders}]")
    across_documents = sources is None or len(sources) > 1 or spec.owns_graph
    if across_documents and spec.cross_document_labels is not None:
        # Cross-document merges only for labels whose name is an identity, and
        # only for names with a capital or a digit in them: "USCENTCOM" and
        # "SU-27" are names, "the object" and "radar" are descriptions that
        # happen to recur.
        labels = ", ".join(repr(label) for label in spec.cross_document_labels)
        clauses.append(f"any(l IN labels(entity) WHERE l IN [{labels}])")
        clauses.append("entity.name =~ '.*[A-Z0-9].*'")
    if not spec.owns_graph:
        lex = spec.lexical
        if sources is None:
            condition = f"d.project = {spec.key!r}"
        else:
            quoted = ", ".join(repr(name) for name in sources)
            condition = (
                f"d.project = {spec.key!r} AND "
                f"d.`{lex.source_name_properties[0]}` IN [{quoted}]"
            )
        clauses.insert(
            0,
            f"EXISTS {{ (entity)-[:{lex.entity_to_chunk}]->"
            f"(:`{lex.chunk_label}`)-[:{lex.chunk_to_source}]->"
            f"(d:`{lex.source_label}`) WHERE {condition} }}",
        )
        # A record shared with an adopted source is still not ours to rewrite
        # or merge merely because a new project document also references it.
        clauses.append(
            f"NOT EXISTS {{ (entity)-[:{lex.entity_to_chunk}]->"
            f"(:`{lex.chunk_label}`)-[:{lex.chunk_to_source}]->"
            f"(foreign:`{lex.source_label}`) "
            f"WHERE foreign.project IS NULL OR foreign.project <> {spec.key!r} }}"
        )
    if not clauses:
        return None
    return "WHERE " + " AND ".join(clauses)


def ingested_sources(
    spec: ProjectSpec, driver, database: str, this_project_only: bool = False
) -> set[str]:
    """Names of the source files already in the graph, by the preferred name property.

    `this_project_only` keeps to the files this project ingested — the ones
    stamped with its key — and leaves out anything the adopted tool wrote.
    """
    lex = spec.lexical
    where = f"d.`{lex.source_name_properties[0]}` IS NOT NULL"
    if this_project_only:
        where += f" AND d.project = {spec.key!r}"
    records, _, _ = driver.execute_query(
        f"MATCH (d:`{lex.source_label}`) WHERE {where} "
        f"RETURN d.`{lex.source_name_properties[0]}` AS name",
        database_=database,
    )
    return {r["name"] for r in records}


def remove_source(spec: ProjectSpec, driver, database: str, *, ingestion_id: str) -> dict:
    """Delete only the failed ingestion attempt's contribution.

    Called when a document fails part-way through a batch. The writer commits in
    batches, so a failure can leave a source node with some chunks and some
    entities behind it; a later `--skip-ingested` would then see the name and
    skip a document that is half there. Entities are removed only if every
    chunk they came from belongs to this source — an agency also named in
    another document stays.
    """
    if not ingestion_id:
        raise ValueError("An ingestion_id is required for cleanup")
    lex = spec.lexical
    records, _, _ = driver.execute_query(
        f"""
        MATCH (d:`{lex.source_label}`)
        WHERE d.ingestion_id = $ingestion_id AND d.project = $project
        OPTIONAL MATCH (c:`{lex.chunk_label}`)-[:{lex.chunk_to_source}]->(d)
        WITH d, collect(c) AS chunks
        OPTIONAL MATCH (e:__Entity__)-[:{lex.entity_to_chunk}]->(c) WHERE c IN chunks
        WITH d, chunks, collect(DISTINCT e) AS touched
        WITH d, chunks,
             [e IN touched WHERE NOT EXISTS {{
                 (e)-[:{lex.entity_to_chunk}]->(other:`{lex.chunk_label}`)
                 WHERE NOT other IN chunks
             }}] AS orphaned
        FOREACH (e IN orphaned | DETACH DELETE e)
        FOREACH (c IN chunks | DETACH DELETE c)
        DETACH DELETE d
        RETURN size(chunks) AS chunks, size(orphaned) AS entities
        """,
        database_=database,
        ingestion_id=ingestion_id,
        project=spec.key,
    )
    return {key: sum(r[key] for r in records) for key in ("chunks", "entities")}


async def ingest_files(
    spec: ProjectSpec,
    paths: list[Path],
    driver,
    llm,
    database: str,
    resolve_entities: bool = True,
    report=print,
    continue_on_error: bool = False,
    parallel: int = 1,
    resolve_scope: str = "run",
    lenient: bool = False,
    skip_ingested: bool = False,
) -> dict:
    """Build the graph from `paths` using a caller-supplied driver and model.

    Split out from `ingest()` so the explorer can ingest an uploaded document on
    its own connection and stream progress, rather than shelling out to the CLI.
    `report` receives one human-readable line per stage.

    `parallel` documents run at once, each on its own pipeline instance; the
    LLM and driver are shared, both being safe for concurrent use. The
    extractor already fans out over a document's chunks, so this multiplies
    that fan-out — two or three is plenty against a single deployment's quota.

    With `continue_on_error` a document that fails is cleaned out of the graph
    and reported at the end instead of aborting the batch. `resolve_scope` is
    "run" (only the files ingested here) or "project" (every file this project
    ever ingested) — see `resolution_filter`.
    """
    embedder = get_embedder()
    pipelines = [
        build_pipeline(spec, driver, llm, embedder, database, lenient)
        for _ in range(max(1, parallel))
    ]
    free = asyncio.Queue()
    for pipeline in pipelines:
        free.put_nowait(pipeline)

    succeeded: list[Path] = []
    failed: list[tuple[Path, str]] = []

    async def run_one(index: int, path: Path) -> None:
        pipeline = await free.get()
        started = time.monotonic()
        ingestion_id = str(uuid4())
        try:
            # Re-checked per document, not once up front: two workers sharing a
            # corpus — one on each model deployment, say — must not both write
            # the file the other finished while this one was queued.
            if skip_ingested and path.name in await asyncio.to_thread(
                ingested_sources, spec, driver, database
            ):
                report(f"[{index}/{len(paths)}] already in the graph, skipping {path.name}")
                return
            report(f"[{index}/{len(paths)}] reading {path.name}")
            await pipeline.run_async(
                file_path=str(path),
                document_metadata={
                    "source": path.name,
                    "project": spec.key,
                    "ingestion_id": ingestion_id,
                },
            )
            succeeded.append(path)
            report(f"[{index}/{len(paths)}] done {path.name} in {time.monotonic() - started:.0f}s")
        except Exception as exc:  # noqa: BLE001 - reported, and re-raised unless asked not to
            if not continue_on_error:
                raise
            failed.append((path, f"{type(exc).__name__}: {str(exc)[:200]}"))
            removed = await asyncio.to_thread(
                remove_source, spec, driver, database, ingestion_id=ingestion_id
            )
            report(
                f"[{index}/{len(paths)}] FAILED {path.name}: {type(exc).__name__}: "
                f"{str(exc)[:200]} (removed {removed['chunks']} chunks, "
                f"{removed['entities']} entities)"
            )
        finally:
            free.put_nowait(pipeline)

    await asyncio.gather(*(run_one(i + 1, path) for i, path in enumerate(paths)))

    stats: dict = {"succeeded": len(succeeded), "failed": [f"{p.name}: {why}" for p, why in failed]}
    if resolve_entities:
        stats.update(await resolve(spec, driver, database, report, succeeded, resolve_scope))
    return stats


async def resolve(
    spec: ProjectSpec,
    driver,
    database: str,
    report=print,
    sources: list[Path] | None = None,
    scope: str = "run",
) -> dict:
    """Merge same-label, same-name entities within the allowed scope.

    Three scopes. `run` is this run's files taken together. `document` is one
    file at a time, over every file this project has ingested — the pass a
    batch run with `--no-resolve` skipped, done afterwards. `project` is all of
    those files at once, under the project's cross-document rules, which is the
    pass that turns two hundred documents' agencies and places into shared nodes.
    """
    if scope == "document":
        names = sorted(ingested_sources(spec, driver, database, this_project_only=True))
        report(f"resolving duplicates within each of {len(names)} document(s)")
        candidates = merged = 0
        for name in names:
            stats = await _run_resolver(spec, driver, database, resolution_filter(spec, [name]))
            candidates += stats["candidates"]
            merged += stats["after_merge"]
        report(f"{candidates} candidates -> {merged} nodes after merge")
        return {"candidates": candidates, "after_merge": merged}

    names = None if scope == "project" else [path.name for path in (sources or [])]
    if names is not None and not names:
        report("nothing to resolve")
        return {}
    where = resolution_filter(spec, names)
    if names is None:
        report(f"resolving duplicates across every document project {spec.key!r} ingested")
    elif where is None or spec.owns_graph:
        report("resolving duplicate entities")
    else:
        report(f"resolving duplicates within the {len(names)} new document(s)")
    stats = await _run_resolver(spec, driver, database, where)
    report(f"{stats['candidates']} candidates -> {stats['after_merge']} nodes after merge")
    return stats


async def _run_resolver(spec: ProjectSpec, driver, database: str, where: str | None) -> dict:
    if spec.grades_evidence:
        driver.execute_query(evidence_rollup_query(spec, where), database_=database)
    resolver = SinglePropertyExactMatchResolver(
        driver,
        filter_query=where,
        resolve_property="name",
        neo4j_database=database,
    )
    resolution = await resolver.run()
    # The library reports None, not 0, for the merged count when nothing qualified.
    return {
        "candidates": resolution.number_of_nodes_to_resolve or 0,
        "after_merge": resolution.number_of_created_nodes or 0,
    }


async def ingest(
    spec: ProjectSpec,
    paths: list[Path],
    resolve_entities: bool = True,
    continue_on_error: bool = False,
    parallel: int = 1,
    resolve_scope: str = "run",
    skip_ingested: bool = False,
    lenient: bool = False,
) -> int:
    driver = get_driver()
    database = get_database()
    llm = get_llm()
    try:
        if skip_ingested:
            present = ingested_sources(spec, driver, database)
            before = len(paths)
            paths = [p for p in paths if p.name not in present]
            print(f"skipping {before - len(paths)} already in the graph, {len(paths)} to ingest")
        if paths:
            stats = await ingest_files(
                spec,
                paths,
                driver,
                llm,
                database,
                resolve_entities,
                continue_on_error=continue_on_error,
                parallel=parallel,
                resolve_scope=resolve_scope,
                lenient=lenient,
                skip_ingested=skip_ingested,
            )
        elif resolve_entities:
            stats = await resolve(spec, driver, database, scope=resolve_scope)
        else:
            stats = {}
        summarise(spec, driver, database)
        failures = stats.get("failed") or []
        if failures:
            print(f"\n{len(failures)} document(s) failed and were left out of the graph:")
            for line in failures:
                print(f"  {line}")
            return 1
        return 0
    finally:
        # aclose(), not close(): we are inside asyncio.run() and the sync close()
        # raises "Cannot call close() from a running async context".
        await llm.aclose()
        driver.close()


def summarise(spec: ProjectSpec, driver, database: str) -> None:
    lex = spec.lexical

    def q(cypher):
        records, _, _ = driver.execute_query(cypher, database_=database)
        return records

    print("\nDocuments")
    rows = q(
        f"MATCH (d:`{lex.source_label}`) "
        f"OPTIONAL MATCH (c:`{lex.chunk_label}`)-[:{lex.chunk_to_source}]->(d) "
        f"RETURN coalesce({', '.join(f'd.`{p}`' for p in lex.source_name_properties)}) AS doc, "
        f"count(c) AS chunks ORDER BY chunks DESC"
    )
    for r in rows[:25]:
        print(f"  {r['doc']}: {r['chunks']} chunks")
    if len(rows) > 25:
        print(f"  ... and {len(rows) - 25} more ({sum(r['chunks'] for r in rows)} chunks in all)")

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
    parser.add_argument(
        "--no-resolve", action="store_true",
        help="Defer evidence normalization and entity resolution.",
    )
    parser.add_argument(
        "--skip-ingested",
        action="store_true",
        help="Leave out files already in the graph by source name. Makes a batch resumable.",
    )
    parser.add_argument(
        "--continue-on-error",
        action="store_true",
        help="Report a failing document at the end instead of stopping; its writes are removed.",
    )
    parser.add_argument(
        "--parallel",
        type=int,
        default=1,
        metavar="N",
        help="Documents extracted at once (default 1). Each already fans out over its chunks.",
    )
    parser.add_argument(
        "--resolve-scope",
        choices=("run", "document", "project"),
        default="run",
        help=(
            "run: within this run's files together (default). document: one file at a time, "
            "over every file this project ingested. project: across all of them, for the "
            "project's cross_document_labels only. Adopted records are never touched."
        ),
    )
    parser.add_argument(
        "--lenient",
        action="store_true",
        help="Log and skip a chunk the model answers with malformed JSON; do not fail the file.",
    )
    parser.add_argument(
        "--resolve-only",
        action="store_true",
        help="Ingest nothing; run entity resolution at --resolve-scope and stop.",
    )
    args = parser.parse_args()

    if args.resolve_only:
        paths: list[Path] = []
    else:
        paths = args.paths or discover_documents(spec.data_dir)
        if not paths:
            print(f"No documents found under {spec.data_dir}", file=sys.stderr)
            return 1
        missing = [p for p in paths if not p.is_file()]
        if missing:
            print(f"Not a file: {', '.join(str(p) for p in missing)}", file=sys.stderr)
            return 1
        # Smallest first, so most of a corpus is in the graph early and a single
        # huge file at the end cannot hold the rest hostage.
        paths = sorted(paths, key=lambda p: p.stat().st_size)

    print(f"project: {spec.key} ({len(paths)} documents)")
    print(f"models:  {describe_models()}")
    return asyncio.run(
        ingest(
            spec,
            paths,
            resolve_entities=not args.no_resolve,
            continue_on_error=args.continue_on_error,
            parallel=args.parallel,
            resolve_scope=args.resolve_scope,
            skip_ingested=args.skip_ingested,
            lenient=args.lenient,
        )
    )


if __name__ == "__main__":
    sys.exit(main())
