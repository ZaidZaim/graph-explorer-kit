# UFO Documents — a POLE knowledge graph over the war.gov/ufo releases

A GraphRAG demo over the UAP records released by the US Department of War under
PURSUE (Presidential Unsealing and Reporting System for UAP Encounters). The
graph was first built with **Neo4j Document Intelligence** from the released
PDFs; this project puts the `neo4j-graphrag` engine on top of it — schema view,
graph retrieval, an agent that picks its own tools, and ingestion for documents
added later.

```bash
GRAPHRAG_PROJECT=projects.ufo
```

## What is in the graph

1,072 extracted records across 17 labels, 808 relationships between them, and a
lexical layer of 78 passages from 10 source files.

| POLE group | Labels |
|---|---|
| **PERSON** | `Person` · `Witness` |
| **OBJECT** | `UAP_Object` · `Vehicle` · `Sensor` · `MediaAsset` |
| **LOCATION** | `Location` · `Facility` |
| **EVENT** | `Event` · `Observation` |
| **ORGANIZATION** | `Agency` |
| **RECORD** | `Document` · `Release` · `CaseFile` · `Claim` · `Evidence` · `Redaction` |

POLE (Person, Object, Location, Event) is the intelligence-analysis model used in
policing and investigations: every fact anchors to one of four entity kinds, so
heterogeneous material lands in one queryable structure. Two groups are added to
it, both because this corpus cannot be read without them — `ORGANIZATION`,
because agencies act in their own right, and `RECORD`, because **a UAP corpus is
not a corpus of facts, it is a corpus of documents asserting facts.** Keeping the
assertion and the asserter as first-class nodes is what lets the demo answer
"where does the record contradict itself?" at all.

The domain's own labels are kept rather than collapsed into the four POLE
classes. `Witness` is not merged into `Person` and `Observation` is not merged
into `Event`, because the distinction is the evidence: an Observation carries the
shape, colour, movement, speed, altitude and duration that were actually
recorded, and a Witness is the person whose testimony is the only support for
it. POLE is the lens over the labels, not a replacement for them.

The sighting chain is the spine of the graph:

```
(:Document)-[:DESCRIBES_EVENT]->(:Event)-[:HAS_OBSERVATION]->(:Observation)-[:DESCRIBES_OBJECT]->(:UAP_Object)
                                    │                              │
                          [:OCCURRED_AT]                   [:REPORTED_BY] / [:CAPTURED_BY]
                                    ▼                              ▼
                              (:Location)                (:Witness) / (:Sensor)
```

## Running it

```bash
uv sync
cp .env.example .env     # then set GRAPHRAG_PROJECT=projects.ufo and the Aura details
```

The embedding model must be the one the chunks were embedded with — see
**Embeddings** below. Then:

```bash
graphrag-adopt --dry-run    # report what adoption would change, write nothing
graphrag-adopt              # label the chunks, embed them, name the sources
graphrag-setup              # create the vector, fulltext and range indexes
graphrag-serve              # the explorer on http://127.0.0.1:8000
```

Ask from the terminal instead:

```bash
graphrag-ask "What did witnesses report over New Mexico in 1949?"
graphrag-ask --retriever text2cypher "What shapes were reported, and how often?"
graphrag-agent --show-tools "Which agencies investigated the most events?"
```

## The explorer

Three views over the one graph:

* **Graph** — every record, as the graph they form. Records with no
  relationship at all are hidden by default and counted in the rail: there are
  ~365, the residue of extraction finding a place name in a scanned table with
  nothing to attach it to. `Types` rolls the same graph up to one node per type,
  sized by how many records carry it, with each edge weighted by the
  relationships it stands for (`MENTIONS ×349`) — Document mentions everything,
  Observation hangs off Event, Witness hangs off Observation. Click a type for
  its most connected records, then click one of *those* for a single record
  drawn the way Aura draws it: the record in the middle, its neighbours around
  it, and every relationship named.
* **Schema** — the POLE model, one node per type, sized by how many records
  carry it, with the patterns the schema licenses as edges. Click a type for its
  properties and their meanings. This is the view for explaining the model.
* **Timeline** — the 82 dated events in order. Dates are as precise as the
  document allowed and no more, so some are a bare year and a few are a bare
  time of day.

Asking a question streams the pipeline's stages, and the graph unfolds a stage
at a time in the order the answer was reasoned out: the passages the question
matched, the records extracted from them, then the neighbourhood the graph
contributes on top — laid out as a graph, the way Aura draws a result. Roughly: rings by 2 seconds, answer by 14 with
`hybrid-cypher`, 45 with the agent.

Each stage is capped so the whole unfold lands just under the explorer's caption
ceiling — about thirty nodes — which is what lets an answer's evidence be drawn
the same way as the type overview: every circle named, every relationship typed.
The labels say what was cut ("16 of 107 records extracted from them"), and the
answer itself carries the detail the picture leaves out.

**Extend the graph** in the rail takes a `.md` or `.pdf` file, runs the same
pipeline, schema and extraction rules that built the corpus, and lights up what
the new document added and what it connected to.

## Adoption: reading a graph another tool built

Document Intelligence writes the same *shape* as `neo4j-graphrag` — entities
carrying `__Entity__`, hanging off a chunk layer, hanging off source files —
under different names. Most of that is handled by reading: the project's
`LexicalSpec` names DI's labels, relationships and properties, and the engine's
Cypher follows them. `entity_to_chunk` is `FROM_CHUNK|__NODE_TO_CHUNK__`, so one
pattern reads both DI's wiring and the wiring of documents added later.

Four things cannot be handled by reading, and `graphrag-adopt` does them. All
four are additive and idempotent, and `--undo` reverses exactly them:

1. **A `:Chunk` label on DI's `__Chunk__` nodes.** A vector index is fixed to
   one label, so the chunks need the one label the engine indexes.
2. **Embeddings in our model's space**, written to `openai_embedding` beside
   DI's untouched `embedding`. DI embedded these chunks with a different
   3072-dim model: verbatim chunk text scores ~0.50 against its vectors, which
   is cosine zero. Two models cannot share one property or one index.
3. **A readable `source` on each source file.** DI stores the upload URL in
   `path` — a signed, expired, several-hundred-character GCS link, which would
   otherwise be what every citation in every answer quotes.
4. **Dropping the constraints that reject new documents**, with
   `--relax-constraints`. This one is not additive, so it is opt-in and
   reported; see below.

## Constraints, and why uploading needs them dropped

DI creates 25 `NODE KEY` and existence constraints — `Witness.name` is a node
key, `Claim.text` must exist, and so on. `neo4j-graphrag`'s writer inserts
extracted nodes with `CREATE` and de-duplicates afterwards, so the second
mention of the same witness in one document is a `ConstraintValidationFailed`.
The pipeline logs the rejected batch and returns normally, which makes the
symptom "the document ingested to nothing" rather than an error.

```bash
graphrag-adopt --relax-constraints   # drop them; range indexes are created in their place
graphrag-adopt --undo                # restore them, and remove everything adoption added
```

The dropped definitions are recorded on a `:__GraphRAGAdoption__` node so the
restore is exact. The explorer checks for them before spending a single model
call and refuses the upload with the command to run.

## Embeddings

The chunk vectors must come from the model that wrote them. DI used a 3072-dim
model of its own; this project embeds with `text-embedding-3-large`, also 3072,
into a *separate* property, so DI's index keeps working and ours is independent.

```bash
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-3-large
EMBEDDING_DIMENSIONS=3072
```

Changing the embedding model means re-embedding: `graphrag-adopt --undo`, then
`graphrag-adopt` and `graphrag-setup` again.

## Entity resolution is scoped, deliberately

`SinglePropertyExactMatchResolver` merges every pair of same-label, same-name
nodes it is shown, and `apoc.refactor.mergeNodes` cannot be undone. This corpus
holds records that DI kept apart on purpose — several distinct sightings are
each named "Fireball sighting" — so a global resolution silently destroys
distinctions the source documents made.

The project therefore declares `owns_graph=False`, and the engine responds in
two places: entity resolution after an ingest is confined by a `filter_query` to
entities reachable from the document just ingested, and `graphrag-reset` refuses
to run at all without an explicit extra flag.

## What this demo does not claim

Nothing here asserts that anything is of extraterrestrial origin, and nothing
infers a cause for any observation. The extraction rules forbid it, the
answering prompt forbids it, and the schema has nowhere to record it. What the
graph holds is what observers reported, what instruments captured, what agencies
concluded, and where those disagree.

Two consequences worth stating plainly when demoing:

* **There is no evidence grading.** Nothing in the released documents assigns a
  confidence level, so the project sets `evidence_levels=()` and the explorer
  drops the facet rather than inventing a score per record. Provenance does that
  job instead: every claim traces to the document that makes it.
* **Redactions are entities.** What was withheld, and the exemption cited for
  it, is part of what a release tells you, so it is a node rather than a gap.

## Data quality, honestly

These are OCR'd scans of typewritten and handwritten documents from the 1940s
onwards, and the graph shows it. Worth knowing before a demo:

* Some `Agency` and `Release` records are date strings — extraction reading a
  stamp or a form field as a name. `Agency` (126) and `Location` (203) carry the
  most noise of any label.
* Several passages are largely OCR garbage. Retrieval handles this better than
  you would expect, because the hybrid lookup has clean passages to prefer.
* The same event is sometimes recorded more than once under slightly different
  names. The agent notices this unprompted when asked to count things, which
  makes a good demo moment: it reports both the number of event records and the
  number of distinct occurrences.
* Ten `Event` records that shared an exact name were merged by a global entity
  resolution run during development, before the scoping described above was in
  place. The graph has 82 dated events rather than 92.

## Files

| Path | What it is |
|---|---|
| `__init__.py` | The `ProjectSpec`: POLE groups, palette, extraction rules, seed questions, few-shot Cypher, and the `LexicalSpec` that maps DI's naming |
| `schema.py` | The 17 node types, 13 relationship types and 30 patterns, written against the live graph |
| `data/` | Empty. The corpus lives in the Aura instance; documents added through the explorer are ingested from a temporary path and not kept here |

## Source

The documents are the public PURSUE releases at
[war.gov/ufo](https://www.war.gov/ufo/). The explorer's visual design follows
that site's own idiom — near-black ground, ultra-light uppercase monospace, cyan
for anything live — but it is a demo of a knowledge graph and not an official
publication of anything.
