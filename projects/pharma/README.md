# Pharma Pipeline — a molecule-to-market knowledge graph over company disclosures

A GraphRAG demo over what four pharmaceutical companies said about their own
pipelines: AbbVie's long-term guidance and pipeline update (February 2024),
Bristol Myers Squibb's Q1 2024 results deck, Johnson & Johnson's 2Q 2024
pipeline chart, and Bayer's pharmaceuticals R&D pipeline overview (July 2025).
The graph was built with **Neo4j Document Intelligence** from those four PDFs.
This project puts the `neo4j-graphrag` engine on top of it — a schema view,
graph retrieval, an agent that picks its own tools, conversations — and lets it
grow: a new deck dropped on the explorer is ingested under the same schema and
lands in the same graph.

```bash
GRAPHRAG_PROJECT=projects.pharma
```

## The use case

A pipeline deck is a table: one row per programme, columns for indication,
phase, and the next milestone. It answers "what does this company have?" well
and nothing else. The questions a competitive-intelligence analyst or a
business-development team brings to a stack of them all cross documents:

- Which companies are pursuing the same disease, and how far along is each?
- Who else is working on this target, and with what modality?
- Which regulatory decisions fall in the next two quarters, across everyone?
- What does this abbreviation mean, in this company's deck?

Four decks from four companies do not share a vocabulary. One says "MIUC", one
"muscle-invasive urothelial carcinoma"; one lists NCT numbers, one trial names;
one calls itself "BMS" on one slide and "Bristol Myers Squibb" on the next.
Flatten them to passages and a search for schizophrenia finds the deck that
says it most often, not both of the decks that have a programme in it. The
graph resolves the vocabulary into records — one Disease, one Target, one
Abbreviation with its expansion — and the decks attach to them, so the overlap
between companies becomes a pattern to match rather than a coincidence to
notice.

That is also why this corpus is a good test of extending a graph. Pipelines
update every quarter. Ingesting the next deck under the same schema attaches
its programmes to the diseases and targets the graph already knows, and the
explorer shows what it added and what it connected to.

## The ontology: molecule to market

The lens is the path a drug takes from the bench to the market, in six groups.

| Group | Labels | What it holds |
|---|---|---|
| **MOLECULE** | `Drug` · `Target` · `Gene` · `Protein` | What is being developed, and what it acts on |
| **INDICATION** | `Disease` · `Population` · `AdverseEvent` | Who it is for, and the safety findings reported along the way |
| **TRIAL** | `Study` | The trial that tests it: phase, status, NCT number, completion date |
| **REGULATORY** | `RegulatoryEvent` | The milestone that lets it be sold: submission, PDUFA date, approval |
| **COMMERCIAL** | `Organization` · `FinancialProjection` | Who owns it, who they partner with, and what it earns |
| **RECORD** | `Evidence` · `Abbreviation` · `Concept` | The paper trail: what each deck asserts, and the vocabulary it is written in |

`RECORD` exists because **a pipeline deck is a company asserting things about
its own programmes.** The graph keeps each assertion as an `Evidence` node with
an `assertion_type` ("TREATS", "REGULATORY_MILESTONE", "FINANCIAL_PROJECTION")
and the deck it came from, and points it at every entity it concerns:

```
(:Evidence {assertion_type: 'TREATS', source_document: 'Q1 2024 Results'})
        -[:ASSERTED_ABOUT_DRUG]->(:Drug {name: 'KarXT'})
        -[:ASSERTED_ABOUT_DISEASE]->(:Disease {name: 'Schizophrenia'})
        -[:ASSERTED_ABOUT_STUDY]->(:Study {name: 'EMERGENT-3', phase: 'Phase III'})
```

So the graph does not say `(Drug)-[:TREATS]->(Disease)`. It says that a
document said so, which is the honest shape for a corpus of forward-looking
statements: "approval anticipated 2025" is the company's expectation, dated as
printed, and the answer keeps the hedge.

Around that spine, `Organization-[:DEVELOPS|CO_DEVELOPS|LICENSES]->Drug` and
`Organization-[:CONDUCTS]->Study` say who owns what, `PARTNERS_WITH` and
`ACQUIRED` join the companies to each other (AbbVie to Cerevel and ImmunoGen,
BMS to Karuna), and `Abbreviation-[:HAS_FULL_FORM_*]->` resolves every "PFS",
"NSCLC" and "MIUC" to the record it stands for — a `Disease`, a `Target`, an
`Organization` — or to a `Concept` when it is none of those. Fourteen node
types, 23 relationship types, 23 allowed patterns, and the extractor may not
invent a twenty-fourth.

The domain's own labels stay rather than collapsing into the six groups.
`Population` is not folded into `Disease`, because "2L+ NSCLC patients" is a
different question from "NSCLC"; `Target` is not folded into `Protein`,
because a deck names PD-1 as a target without naming a UniProt accession. The
lens is placed over the labels, and the labels keep the detail.

## Why a graph

- **Overlap is a pattern.** "Which diseases are pursued by more than one
  company?" is `Organization -> Drug <- Evidence -> Disease`, grouped by
  disease, filtered to two or more organisations. No passage says it, so no
  embedding finds it; the agent writes that query and answers with a table of
  twenty-six diseases across the four decks.
- **The vocabulary is resolved once.** Document Intelligence keyed `Disease`
  on its name, so "Schizophrenia" is one node whether BMS's KarXT slide or
  AbbVie's emraclidine row mentions it. The two companies meet on that node.
- **Provenance is structural.** Every entity keeps a link to the passage it
  came from, and every passage to its PDF. When the explorer answers, it draws
  that chain first, so you see the evidence before the prose.
- **The asserter is a node.** An `Evidence` node says which deck made a claim,
  so "who says so?" is a hop rather than a search — and a projection is never
  mistaken for a result.
- **It grows without a rebuild.** Next quarter's deck ingests under the same
  schema, and entity resolution scoped to the new document attaches it to the
  drugs, targets and companies already in the graph.

## What is in the graph

After adoption on 28 September 2026: 1,750 records across 14 labels, 2,088
relationships between them, and a lexical layer of 44 passages from the 4
source files (84 slides in all). `Drug` (284), `Study` (282), `Disease` (268),
`Abbreviation` (208) and `Concept` (194) are the largest labels, which is what
four pipeline charts should look like; `BMS`, `Bayer Pharmaceuticals` and
`AbbVie` are the most connected companies. 43 regulatory events carry a date,
from "Nov 2023" to "2027", and populate the Timeline. 309 records take part in
no relationship — an abbreviation defined and never used, a concept mentioned
once — and are hidden by default.

## Running it

```bash
uv sync
cp .env.example .env     # then set GRAPHRAG_PROJECT=projects.pharma and the Aura details
```

The embedding model is yours to choose — the engine writes its own vectors
beside Document Intelligence's; see **Embeddings**. Then:

```bash
graphrag-adopt --dry-run             # report what adoption would change, write nothing
graphrag-adopt --relax-constraints   # label the chunks, embed them, name the sources
graphrag-setup                       # create the vector, fulltext and range indexes
graphrag-serve                       # the explorer on http://127.0.0.1:8000
```

That is the whole setup: the four decks are already in the graph, so there is
nothing to ingest. To add a fifth:

```bash
graphrag-ingest ~/Downloads/next-quarter-pipeline.pdf
```

or drop it on **Extend the graph** in the explorer. Born-digital investor
decks carry a clean text layer, so no OCR is involved; a scanned one would go
through the same page-by-page reader the UFO corpus needed.

Ask from the terminal instead:

```bash
graphrag-ask "Which regulatory decisions were expected in 2024?"
graphrag-ask --retriever text2cypher "How many studies are there per phase?"
graphrag-agent --show-tools "Which diseases are being pursued by more than one company, and by whom?"
```

## The explorer

Three views over the one graph:

* **Graph** — opens on the records themselves, most connected first, up to a
  limit in the rail (400 by default): the companies, the drugs they develop,
  the studies they run and the diseases those hang off, as the graph they
  form. The filter rail groups the labels by the molecule-to-market lens, so
  "only the regulatory events" or "only the molecules" is one click.
  Double-click any record, or press `expand`, and its connections grow out
  of it in place. `Types` rolls the graph up to one node per type with
  weighted edges — `Evidence -[ASSERTED_ABOUT_DRUG ×421]-> Drug`,
  `Organization -[DEVELOPS ×261]-> Drug` — which is the shape of the corpus
  in one picture.
* **Schema** — the model, one node per type, sized by how many records carry
  it, with the patterns the schema licenses as edges. Click a type for its
  properties and their meanings. This is the view for explaining the model.
* **Timeline** — the 43 dated regulatory events in order. Dates are as precise
  as the deck allowed: some are a day ("2024-06-21"), some a month, some a
  bare year.

Asking a question streams the pipeline's stages, and the graph unfolds a stage
at a time: the passages the question matched, the records extracted from them,
then the neighbourhood the graph contributes on top. Roughly: rings by 2
seconds, answer by 10 to 25 with `hybrid-cypher`, 60 to 90 with the agent.

**Which mode to demo.** The default `hybrid-cypher` answers from the passages
the question matches plus one hop of graph around them, and on four decks of
two to three thousand characters a chunk it is fast and well cited. It is
also, deliberately, the control: ask it which companies have a Parkinson's
programme and it names Bayer and J&J from the two passages it matched and
misses AbbVie's, whose row is one line in a table the question did not score
well against. Switch the dropdown to `agent`, ask again, and the agent writes
the Cypher that walks `Organization -> Drug <- Evidence -> Disease`, reads
every company's programmes, and answers with all four — then shows the tool
calls it made. The difference between those two answers is the point of the
graph.

**Ask, then follow up.** The chat column is a conversation: "What does BMS
have in Phase III?" then "and which of those read out in 2025?" works, because
the agent reads the thread and the fixed retrievers get the follow-up
rewritten into a standalone question. The thread is stored in the same Aura
instance as the graph, as `Message` and `ReasoningTrace` nodes, and survives a
reload or a restart.

## Adoption: reading a graph another tool built

Document Intelligence writes the same *shape* as `neo4j-graphrag` — entities
carrying `__Entity__`, hanging off a chunk layer, hanging off source files —
under different names. Most of that is handled by reading: the project's
`LexicalSpec` names DI's labels, relationships and properties, and the
engine's Cypher follows them. `entity_to_chunk` is
`FROM_CHUNK|__NODE_TO_CHUNK__`, so one pattern reads both DI's wiring and the
wiring of decks added later.

Four things cannot be handled by reading, and `graphrag-adopt` does them. All
four are additive and idempotent, and `--undo` reverses exactly them:

1. **A `:Chunk` label on DI's 44 `__Chunk__` nodes.** A vector index is fixed
   to one label, so the chunks need the one label the engine indexes.
2. **Embeddings in our model's space**, written to `openai_embedding` beside
   DI's untouched `embedding`. DI embedded these chunks with a 3072-dim model
   of its own, under a binary-quantised index; two models cannot share one
   property or one index.
3. **A readable `source` on each source file.** DI stores the upload path in
   `path` — a bucket prefix and three UUIDs deep — which would otherwise be
   what every citation in every answer quotes. The filename is lifted out.
4. **Dropping the 24 constraints that reject new documents**, with
   `--relax-constraints`. This one is not additive, so it is opt-in and
   reported; see below.

## Constraints, and why uploading needs them dropped

DI creates 24 `NODE KEY` and existence constraints — `Drug.identifier` is a
node key, `Study.name` must exist, `Evidence` is keyed on
`(assertion_type, source_document)`. `neo4j-graphrag`'s writer inserts
extracted nodes with `CREATE` and de-duplicates afterwards, so the second
mention of Opdivo in one deck is a `ConstraintValidationFailed`. The pipeline
logs the rejected batch and returns normally, which makes the symptom "the
document ingested to nothing" rather than an error.

```bash
graphrag-adopt --relax-constraints   # drop them; range indexes are created in their place
graphrag-adopt --undo                # restore them, and remove everything adoption added
```

The dropped definitions are recorded on a `:__GraphRAGAdoption__` node so the
restore is exact. The explorer checks for them before spending a single model
call and refuses the upload with the command to run.

## Embeddings

DI's chunk vectors are 3072-dim from a model of its own; this project embeds
with `text-embedding-3-large`, also 3072, into a *separate* property, so DI's
index keeps working and ours is independent. Any model would do — the two
never meet — as long as `EMBEDDING_DIMENSIONS` matches it.

```bash
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-3-large
EMBEDDING_DIMENSIONS=3072
```

Changing the embedding model means re-embedding: `graphrag-adopt --undo`, then
`graphrag-adopt` and `graphrag-setup` again. Forty-four chunks take under a
minute.

## Entity resolution is scoped, deliberately

`SinglePropertyExactMatchResolver` merges every pair of same-label, same-name
nodes it is shown, and `apoc.refactor.mergeNodes` cannot be undone. This graph
holds records that DI kept apart on purpose: three `Drug` nodes named "RYZ101"
with different identifiers, two `Study` nodes named "OCEANIC-STROKE". So the
project declares `owns_graph=False`, and the engine responds in two places:
entity resolution after an ingest is confined to entities reachable from the
document just ingested, and `graphrag-reset` refuses to run at all without an
explicit extra flag.

Across decks this project ingests itself, resolution runs wider, but not
indiscriminately. `cross_document_labels` names the labels whose name is an
identity — `Organization`, `Drug`, `Disease`, `Target`, `Gene`, `Protein`,
`Study`, `AdverseEvent`, `Concept` — and only those merge between documents.
A `RegulatoryEvent` called "U.S. approval" recurs on every pipeline slide and
is a different milestone each time; a `FinancialProjection` called "Global
Net Sales" is a different number in every deck. And "the Company" — every
results deck's name for itself — sits in `placeholder_names`, so four decks'
"the Company" never become one.

## Data quality, honestly

Document Intelligence read four born-digital decks and the graph is clean by
the standards of extraction. Three things are worth knowing before a demo:

* **Evidence nodes are hubs.** DI keyed `Evidence` on
  `(assertion_type, source_document)`, so every "TREATS" statement in the
  BMS deck merged into one node, which now carries 207 edges. The statement
  text on it is whichever assertion arrived first, and the per-assertion
  pairing of drug to disease is lost at that node — the drugs and the
  diseases are all attached to it together. The graph context the retrievers
  build caps what one entity contributes (`FACTS_PER_ENTITY`) so a hub cannot
  drown the passage that matched, and the text in the passage still carries
  the pairing. The `Types` view shows the effect plainly:
  `Evidence -[ASSERTED_ABOUT_DRUG ×421]->` from 88 nodes.
* **Companies appear under several names.** "BMS" and "Bristol Myers Squibb",
  "Bayer" and "Bayer Pharmaceuticals" are separate `Organization` nodes, each
  well connected. The few-shot Cypher matches both; the agent notices
  unprompted and says so.
* **Phases are as printed.** 96 studies have no phase, and the rest use
  fifteen spellings — "Phase III", "Phase 3", "Ph3", "Ph3 Adjunctive". The
  extraction rules for new decks normalise to four values; the existing
  records were not rewritten, because they are not this project's to rewrite.

## What this demo does not claim

Nothing here is investment advice, and nothing here is a statement of fact
about a drug. What the graph holds is what four companies disclosed about
their own pipelines, on four dates, attributed to the document that discloses
it. Forward-looking statements are stored and answered as the company's
projections. Where a deck says "anticipated", so does the answer.

## Files

| Path | What it is |
|---|---|
| `__init__.py` | The `ProjectSpec`: the molecule-to-market groups, palette, extraction rules, seed questions, few-shot Cypher, and the `LexicalSpec` that maps DI's naming |
| `schema.py` | The 14 node types, 23 relationship types and 23 patterns, written against the live graph |
| `theme.css` | The explorer in the idiom of an R&D deck: lab-navy ground, mint accent, a hexagon for a seal |
| `data/` | Empty on purpose. The four decks live in the graph, not in the repo; a deck added later is ingested from wherever it is and not kept here |

## Source

The four documents are public investor materials from the companies' own
investor-relations sites: AbbVie (February 2, 2024), Bristol Myers Squibb
(April 25, 2024), Johnson & Johnson (as of July 17, 2024) and Bayer (July 25,
2025). The explorer's look borrows the idiom of such decks — a deep ground, a
mint accent, a clean sans — but it is a demo of a knowledge graph and not a
publication of any of them.
