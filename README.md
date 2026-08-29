# demo-neo4j-GraphRAG-py

End-to-end GraphRAG demo on Neo4j using the official
[`neo4j-graphrag`](https://github.com/neo4j/neo4j-graphrag-python) Python package (v1.19).

Unstructured Markdown briefings go in; a knowledge graph comes out; questions are
answered against that graph with retrieval that walks relationships rather than
just matching vectors.

```
data/*.md ──► SimpleKGPipeline ──► (:Chunk)-[:FROM_DOCUMENT]->(:Document)
                                   (:Person)-[:FROM_CHUNK]->(:Chunk)
                                   (:Person)-[:WORKS_AT]->(:Organization)
                                          │
                                          ▼
                          HybridCypherRetriever ──► GraphRAG ──► answer
```

## Setup

**1. A Neo4j instance.** Either start one locally:

```bash
docker compose up -d
```

or point `.env` at an Aura instance. The demo needs APOC (`apoc.refactor.mergeNodes`,
used by entity resolution) — bundled in the compose file, present on all Aura tiers.

**2. Environment.**

```bash
cp .env.example .env
```

Fill in `OPENAI_API_KEY`, and `NEO4J_*` if you are not using the compose defaults.

**3. Dependencies.**

```bash
uv sync
```

(`pip install -e .` works too.)

## Run

```bash
uv run graphrag-setup
```

Creates the vector index, the fulltext index, and supporting range indexes, then
blocks until all of them report `ONLINE`.

```bash
uv run graphrag-ingest
```

Chunks every file under `data/`, embeds each chunk, extracts entities and
relationships with the LLM under the schema in
[kg_schema.py](src/graphrag_demo/kg_schema.py), then merges duplicate entities.
Prints a summary of what landed in the graph.

```bash
uv run graphrag-ask "Which terminal runs both Meridian and Kestrel systems?"
```

## What to look at

The interesting file is [retrievers.py](src/graphrag_demo/retrievers.py). Its
`GRAPH_CONTEXT_QUERY` is the `retrieval_query` — the Cypher that runs *after* the
vector/fulltext lookup and expands each matched chunk into its document, the
entities extracted from it, and those entities' own relationships. That second hop
is the part a vector store cannot do.

Two variables are injected into that fragment by the library and must not be
re-declared: `node` (the matched `:Chunk`) and `score`. `score` must appear in the
`RETURN`.

## Comparing retrievers

```bash
uv run graphrag-compare "How are Meridian Robotics and Kestrel Automation connected?"
```

Runs the same question through all five and prints them together:

| Retriever | Vector | Fulltext | Graph | Notes |
|---|:---:|:---:|:---:|---|
| `vector` | ✓ | — | — | Baseline. Returns chunks that *sound* like the question. |
| `hybrid` | ✓ | ✓ | — | Recovers exact names and acronyms embeddings blur. |
| `vector-cypher` | ✓ | — | ✓ | Graph expansion, no keyword matching. |
| `hybrid-cypher` | ✓ | ✓ | ✓ | Default. |
| `text2cypher` | — | — | ✓ | LLM writes Cypher. Handles counting and aggregation, which vector search cannot do at all. |

Pick one for a single question with `--retriever`:

```bash
uv run graphrag-ask --retriever text2cypher "How many organizations are in the graph?"
uv run graphrag-ask --retriever vector --show-context "Who is Amara Okonjo?"
```

`--show-context` prints the retrieved context before the answer, which is the
fastest way to tell a retrieval problem from a generation problem.

Multi-turn, with history:

```bash
uv run graphrag-ask --chat "Who runs Meridian Robotics?"
```

## Sample corpus

Three fictional company briefings in `data/` — Meridian Robotics (hardware),
Kestrel Automation (software), Nordhavn Terminals (their shared customer). They are
written so the interesting answers span documents: no single file says that Aarhus
is the one site running both vendors' systems, but the graph does.

Drop your own `.md`, `.txt`, or `.pdf` files into `data/` and re-run
`graphrag-ingest`. If your domain differs, edit `DEMO_SCHEMA` in
[kg_schema.py](src/graphrag_demo/kg_schema.py) first — extraction quality tracks
schema quality more than it tracks model choice.

## Starting over

```bash
uv run graphrag-reset --yes
```

Deletes only the labels this demo writes (`Document`, `Chunk`, `__Entity__`,
`__KGBuilder__`) and drops its indexes. Safe to run against a database holding
other data.

## Notes and gotchas

- **Embedding dimensions must match the model.** `text-embedding-3-small` is 1536,
  `-3-large` is 3072. Changing `EMBEDDING_MODEL` after ingesting requires a
  `graphrag-reset --yes` and a re-ingest, or the vector index will reject the writes.
- **No uniqueness constraints on entity names.** `Neo4jWriter` inserts extracted
  nodes with `CREATE`, not `MERGE`, and de-duplicates afterwards via
  `SinglePropertyExactMatchResolver`. A `Person.name IS UNIQUE` constraint would
  abort the ingest the first time a person appears in two chunks.
- **Indexes must be `ONLINE` before ingesting.** Embeddings written to an index that
  is still populating are invisible to search, with no error. `graphrag-setup` polls
  for this.
- **Components moved namespace in 1.19.** `neo4j_graphrag.experimental.components.*`
  is deprecated in favour of `neo4j_graphrag.components.*` and goes away in 2.0.
  `SimpleKGPipeline` itself still lives under `experimental.pipeline`.
- **`Text2CypherRetriever` will not execute writes.** Generated Cypher is run
  through `EXPLAIN` first and rejected if it writes, so a prompt-injected `DELETE`
  never reaches the graph.

## Layout

```
data/                          sample corpus
src/graphrag_demo/
  config.py                    env loading, driver / LLM / embedder factories
  kg_schema.py                 GraphSchema handed to the extraction LLM
  setup_indexes.py             indexes + ONLINE polling      -> graphrag-setup
  ingest.py                    SimpleKGPipeline + resolution -> graphrag-ingest
  retrievers.py                the five retrievers and the retrieval_query
  ask.py                       GraphRAG query entry point    -> graphrag-ask
  compare.py                   side-by-side comparison       -> graphrag-compare
  reset.py                     scoped teardown               -> graphrag-reset
```
