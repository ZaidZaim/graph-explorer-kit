# UFO Documents — a POLE knowledge graph over the war.gov/ufo releases

A GraphRAG demo over the UAP records released by the US Department of War under
PURSUE (Presidential Unsealing and Reporting System for UAP Encounters). The
graph was first built with **Neo4j Document Intelligence** from five of the
released PDFs. This project puts the `neo4j-graphrag` engine on top of it — a
schema view, graph retrieval, an agent that picks its own tools — and then
extends it with the rest of the release: all 240 PDFs, OCR'd where they are
scans, ingested under the same POLE schema and resolved into one graph.

```bash
GRAPHRAG_PROJECT=projects.ufo
```

## The use case

The releases are scans of typewritten reports, memos, and forms from the 1940s
onwards. Each one records what someone saw, who saw it, where, what an
instrument captured, what an agency concluded, and what was withheld. The
questions an analyst brings to them all cross documents:

- What did witnesses report over New Mexico in 1949, and which agencies looked
  into it?
- Which claims rest on a single witness, and which have instrument data behind
  them?
- Where does the record contradict itself?
- What was redacted, and under which exemption?

None of those is answered by a paragraph. A sighting appears in a witness
statement, an intelligence summary, and a redacted memo, and the three don't
agree on the date, the shape, or the count. Flatten the corpus to passages and
you keep the words but lose who said them. The graph keeps both: the assertion
and the asserter, as nodes, with the passage that carried each one a hop away.

That's also why this corpus is a good test of extending a graph. New releases
arrive as more PDFs. Ingesting one with the same schema attaches its events to
locations and agencies the graph already knows, and the explorer shows what the
document added and what it connected to.

## The ontology: POLE, plus two

POLE (Person, Object, Location, Event) is the model intelligence analysts use
in policing and investigation. Every fact anchors to one of four kinds of thing,
so heterogeneous material lands in one queryable structure. This project keeps
POLE as the lens and adds two groups the corpus can't be read without.

| Group | Labels | What it holds |
|---|---|---|
| **PERSON** | `Person` · `Witness` | Named individuals, and the people whose testimony is the only support for an observation |
| **OBJECT** | `UAP_Object` · `Vehicle` · `Sensor` · `MediaAsset` | What was seen, what the observer was in, what recorded it, and the photo or film that resulted |
| **LOCATION** | `Location` · `Facility` | Where it happened, and the base or installation involved |
| **EVENT** | `Event` · `Observation` | The sighting as an occurrence, and each individual account of it |
| **ORGANIZATION** | `Agency` | Who investigated, who concluded, who authored |
| **RECORD** | `Document` · `Release` · `CaseFile` · `Claim` · `Evidence` · `Redaction` | The paper trail itself |

`ORGANIZATION` exists because agencies act in their own right: they investigate,
conclude, and redact. `RECORD` exists because **a UAP corpus is a corpus of
documents asserting facts.** A `Claim` is a statement someone made, `Evidence`
is what supports it, and a `Redaction` is what was withheld and the exemption
cited for it. Keeping those as nodes rather than as text is what lets the demo
answer "where does the record contradict itself?" at all: two claims about one
event, asserted by two documents, are a pattern you can match.

The domain's own labels stay rather than collapsing into the four POLE classes.
`Witness` is not folded into `Person` and `Observation` is not folded into
`Event`, because the distinction is the evidence. An `Observation` carries the
shape, colour, movement, speed, altitude, and duration that were recorded, and
a `Witness` is the person whose word it rests on. POLE is the lens over the
labels, and the labels keep the detail.

The sighting chain is the spine of the graph:

```
(:Document)-[:DESCRIBES_EVENT]->(:Event)-[:HAS_OBSERVATION]->(:Observation)-[:DESCRIBES_OBJECT]->(:UAP_Object)
                                    │                              │
                          [:OCCURRED_AT]                   [:REPORTED_BY] / [:CAPTURED_BY]
                          [:INVESTIGATED_BY]                       ▼
                                    ▼                    (:Witness) / (:Sensor)
                          (:Location) / (:Agency)
```

Around it, `Document-[:MENTIONS]->` reaches every other type, `Claim-[:SUPPORTED_BY]->Evidence`
ties an assertion to its backing, `Document-[:PART_OF_RELEASE]->Release|CaseFile`
places each file in the batch it came out of, and `SAME_AS` / `POSSIBLY_SAME_AS`
between events, objects, and persons record where the documents themselves say,
or hint, that two records describe one thing. Thirteen relationship types, 30
allowed patterns, and the extractor may not invent a fourteenth.

## Why a graph

- **The answer is a path.** "Which agencies investigated events with a
  single witness?" is `Agency <- Event -> Observation -> Witness` with a
  count. No passage says it, so no embedding finds it.
- **Contradiction is a pattern.** Two `Claim` nodes about one `Event`, each
  asserted by a different `Document`, disagreeing on a property. That's a
  query, and the answer names both documents.
- **Provenance is structural.** Every entity keeps a link to the passage it
  came from, and every passage to its PDF. When the explorer answers, it draws
  that chain first, so you see the evidence before the prose.
- **The asserter is a node.** Documents, agencies, and witnesses are
  first-class, so "who says so?" is a hop rather than a search.
- **It grows without a rebuild.** A new release ingests under the same
  schema, and entity resolution scoped to the new document attaches it to the
  places and agencies already in the graph.

## What is in the graph

After the full-corpus ingest on 23 September 2026: all 240 released PDFs,
54,044 records across 17 labels, 58,429 relationships between them, and a
lexical layer of 24,971 passages from 245 source files — the 10 Document
Intelligence built from, plus 235 this project prepared and ingested itself.
The prepared corpus is 10,214 pages: 6,759 read from a text layer, 1,499
recognised by OCR, 1,956 judged illegible (blank pages, fully redacted pages,
photographs, and scans too degraded to read). 4,240 events carry a date.
`Person` (7,973), `Event` (6,744), `Claim` (6,714) and `Document` (6,600) are
the largest labels, which is what a corpus of records asserting things should
look like; `FBI`, `Air Force`, `USCENTCOM`, `NASA` and `AARO` are the most
connected nodes.

## From 240 PDFs to one graph

The release is 240 PDFs, 4.2 GB, 10,344 pages, and most of it is scans: FBI
photostats of 1947 teletypes, Air Force incident summaries, NASA debriefing
transcripts, contractor reports. Three things about them decided the shape of
the pipeline in [prepare.py](../../src/graphrag_kit/prepare.py):

- **Many are photographic negatives** — white type on a dark ground. Tesseract
  reads nothing from them until the page is inverted, and nothing with its
  default global threshold; local (Sauvola) thresholding is what makes a grey,
  unevenly lit photostat legible.
- **Some carry a text layer that is itself bad OCR.** The FBI `62-HQ-83894`
  sections and the 173-233 incident summaries look born-digital to a file-level
  check and read as character salad. Every page is graded on its own, and a
  failing page is re-read from the image.
- **OCR of noise looks like words.** A halftone photograph comes back as `ee bd
  ane Cee vere Ser`, which passes any token-shape test. A page has to score
  against a word list too, or the extractor mints an `Agency` called "Ser".

What that buys is provenance you can read: every source file's header says how
many of its pages were read, recognised, or given up on, and the extractor was
only ever shown text that reads as text.

## Running it

```bash
uv sync
cp .env.example .env     # then set GRAPHRAG_PROJECT=projects.ufo and the Aura details
```

The embedding model must be the one the chunks were embedded with — see
**Embeddings** below. Then:

```bash
graphrag-adopt --dry-run    # report what adoption would change, write nothing
graphrag-adopt --relax-constraints   # label the chunks, embed them, name the sources
graphrag-setup              # create the vector, fulltext and range indexes
graphrag-serve              # the explorer on http://127.0.0.1:8000
```

That reads the graph Document Intelligence built. To rebuild the full corpus
on top of it — the step described under **From 240 PDFs to one graph** — with
the PDFs downloaded from war.gov/ufo into a folder:

```bash
uv sync --extra ocr                                     # pypdfium2 + Pillow; Tesseract separately
graphrag-prepare ~/Downloads/us-ufo-docs                # PDFs -> projects/ufo/data/*.md
graphrag-ingest --skip-ingested --continue-on-error --parallel 3 --no-resolve
graphrag-ingest --resolve-only --resolve-scope document  # merge duplicates within each new file
graphrag-ingest --resolve-only --resolve-scope project   # then agencies, places and people across them
```

The prepared Markdown is committed under `data/`, so the ingest steps run
without the 4 GB of PDFs or an OCR install.

Ask from the terminal instead:

```bash
graphrag-ask "What did witnesses report over New Mexico in 1949?"
graphrag-ask --retriever text2cypher "What shapes were reported, and how often?"
graphrag-agent --show-tools "Which agencies investigated the most events?"
```

## The explorer

Three views over the one graph:

* **Graph** — opens on `Types`: one node per type, sized by how many records
  carry it, with each edge weighted by the relationships it stands for
  (`MENTIONS ×37,937`) — Document mentions everything, Observation hangs off
  Event, Witness hangs off Observation. Click a type for its most connected
  records, then click one of *those* for a single record drawn the way Aura
  draws it: the record in the middle, its neighbours around it, and every
  relationship named. `Records` draws the records themselves, most connected
  first, up to a limit in the rail — 54,000 at once is not a picture, it is a
  tab that stops responding. Records with no relationship at all (13,965, the
  residue of extraction finding a place name in a scanned table with nothing
  to attach it to) are hidden by default and counted.
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

**Ask, then follow up.** The chat column is a conversation: "Which agencies
investigated events over New Mexico?" then "and which of those appear in the
2020s mission reports?" works, because the agent reads the thread and the
fixed retrievers get the follow-up rewritten into a standalone question. The
thread is stored in the same Aura instance as the graph, as `Message` and
`ReasoningTrace` nodes, and survives a reload or a restart.

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

Across the 235 documents this project ingested itself, resolution runs wider,
but not indiscriminately. `cross_document_labels` names the labels whose name
is an identity — `Agency`, `Location`, `Facility`, `Person`, `Witness`,
`Vehicle`, `Sensor`, `Release`, `CaseFile` — and only those merge between
documents; an `Event` called "Reported object sighting" or a `UAP_Object`
called "the object" is a fresh record in every file that uses the phrase, and
a `Document` entity titled "Mission Narrative" is a different narrative in each
mission report. And `[REDACTED]`, the name the extraction rules assign to a
withheld witness, is never merged anywhere: before that rule, the corpus held
forty-eight redacted witnesses across fifteen files that an exact-name merge
would have made one person. Document Intelligence's own records are outside
every scope; the thirteen agency names the new documents share with them
("FBI", "CIA", …) remain separate nodes, which is a policy choice rather than
an accident and easy to reverse with one Cypher statement if you want them
joined.

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
| `data/` | The prepared corpus: one Markdown file per released PDF, as `graphrag-prepare` wrote it — text layer where trustworthy, Tesseract OCR where not, a header saying which. Documents added through the explorer are ingested from a temporary path and not kept here |

## Source

The documents are the public PURSUE releases at
[war.gov/ufo](https://www.war.gov/ufo/). The explorer's visual design follows
that site's own idiom — near-black ground, ultra-light uppercase monospace, cyan
for anything live — but it is a demo of a knowledge graph and not an official
publication of anything.
