# demo-neo4j-GraphRAG-py

A reusable GraphRAG scaffold on Neo4j, built on the official
[`neo4j-graphrag`](https://github.com/neo4j/neo4j-graphrag-python) package (v1.19).

Point it at a folder of documents and a schema; get back a knowledge graph, five
retrieval strategies, an agent that chooses between them, a terminal client, and an
interactive browser explorer that answers questions **and shows you the subgraph
the answer came from**.

It also reads graphs it did not build. Point the same engine at a graph from
Neo4j Document Intelligence or another importer, describe how that graph names
its chunk layer, and you get the retrievers, the agent and the explorer over it
without rewriting anyone's data — see **Adopting an existing graph**.

```
projects/<name>/data/*.md ──► SimpleKGPipeline ──► (:Chunk)-[:FROM_DOCUMENT]->(:Document)
                                                   (:Entity)-[:FROM_CHUNK]->(:Chunk)
                                                   (:Entity)-[:REL]->(:Entity)
                                                          │
                                    ┌─────────────────────┴─────────────────────┐
                                    ▼                                           ▼
                    HybridCypherRetriever ──► GraphRAG              Agent Framework agent
                                    │                          (retrievers as tools, n calls)
                                    └─────────────────┬─────────────────────────┘
                                                      ▼
                                            answer + evidence subgraph
```

## The split

Everything in `src/graphrag_kit/` is domain-agnostic. Everything that makes a demo
*about something* lives in a project package under `projects/`, selected by one
environment variable:

```bash
GRAPHRAG_PROJECT=projects.example
```

A project is a single `ProjectSpec`: a schema, a data directory, extraction rules,
few-shot Cypher, seed questions, and a palette. That is the whole contract — see
[project.py](src/graphrag_kit/project.py). To start a new demo, copy
`projects/example`, swap the schema and the corpus, and point the variable at it.
No engine code changes.

Four optional parts of the spec carry more weight than their size suggests:

| Field | What it buys |
|---|---|
| `groups` | A lens over the labels — POLE (Person, Object, Location, Event) in the projects here. The explorer groups its filters and colours its nodes by it, and serves the model itself as a view, so the model an analyst is taught is the model the picture shows. |
| `name_properties` | Not every entity has a `name`. A Claim is identified by its text and a Document by its title, and a graph that renders both as "(unnamed)" is useless. |
| `lexical` | How the chunk/embedding layer is *named*. The defaults are what `neo4j-graphrag` writes itself; overriding them lets the engine read a graph another tool built without rewriting anyone's data. See **Adopting an existing graph**. |
| `owns_graph` | `False` when the project only reads and extends someone else's graph. It makes the engine cautious in the two places that would otherwise change data it did not write — see **Entity resolution**. |

Branches in this repo follow that split: `main` is the scaffold plus a neutral
example, `vice-city` adds a real corpus on top of it, and `ufo-documents` adopts
a graph built by Neo4j Document Intelligence and extends it.

## Setup

**1. A Neo4j instance.** Either start one locally:

```bash
docker compose up -d
```

or point `.env` at Aura. APOC is required — the entity resolver calls
`apoc.refactor.mergeNodes`. It is bundled in the compose file and present on all
Aura tiers.

Neo4j 5.23 or newer. Vector indexes need 5.11+, and `graphrag-reset` uses the
variable-scope `CALL (n) { ... } IN TRANSACTIONS` form that arrived in 5.23 — on an
older 5.x it fails with a syntax error that says nothing about versions. The compose
file pins `neo4j:2025.10-community`.

**2. Models.** Two providers, selected with `LLM_PROVIDER`:

| | |
|---|---|
| `azure` *(default)* | Microsoft Foundry / Azure OpenAI. Authenticates with Entra ID via `DefaultAzureCredential` — an `az login` is enough and **no key is stored anywhere**. |
| `openai` | `api.openai.com` with `OPENAI_API_KEY`. |

Find your Foundry deployments:

```bash
az cognitiveservices account list -o table
az cognitiveservices account deployment list -n <resource> -g <rg> -o table
```

You need one chat deployment and one embedding deployment. They may live on
different resources — quota, region and model availability are all per-resource —
so `AZURE_OPENAI_EMBEDDING_ENDPOINT` overrides the endpoint for embeddings only.

Entra auth requires the **Cognitive Services OpenAI User** role on the resource.
Set `AZURE_AUTH_MODE=key` with `AZURE_OPENAI_API_KEY` where there is no Azure
identity (CI, for instance).

Deploying a model, if you need one:

```bash
az cognitiveservices model list -l <region> --query "[?starts_with(model.name,'gpt-5')].{name:model.name, version:model.version}" -o table
az cognitiveservices account deployment create -n <resource> -g <rg>   --deployment-name <name> --model-name <model> --model-version <version>   --model-format OpenAI --sku-name GlobalStandard --sku-capacity 500
```

**3. Environment.**

```bash
cp .env.example .env
```

Fill in `GRAPHRAG_PROJECT`, the `NEO4J_*` values, and the provider block.

**4. Dependencies.**

```bash
uv sync
```

## Run

```bash
uv run graphrag-adopt --dry-run
```

Only for a project pointed at a graph something else built: reports what adoption
would change and writes nothing. Skip it entirely for a project that builds its
own graph. See **Adopting an existing graph**.

```bash
uv run graphrag-setup
```

Creates the vector index, two fulltext indexes and supporting range indexes, then
blocks until all of them report `ONLINE`. Every label and property it indexes
comes from the project's `lexical` spec.

```bash
uv run graphrag-ingest
```

Chunks every document in the project's data directory, embeds each chunk, extracts
entities and relationships under the project's schema, rolls up evidence levels,
then merges duplicate entities. `.md`, `.markdown` and `.pdf` are picked up,
recursively — those are what the pipeline's default file loader can read, and it
raises on anything else rather than ingesting it to nothing.

Name files explicitly to ingest only those — `uv run graphrag-ingest data/one-new-note.md`
— and pass `--no-resolve` to skip the duplicate-entity merge, which is what you want
while you are still iterating on `extraction_rules`.

```bash
uv run graphrag-serve
```

Opens the explorer on <http://localhost:8000>. Or stay in the terminal:

```bash
uv run graphrag-ask "who is connected to whom?"
uv run graphrag-ask --retriever text2cypher "how many organizations are there?"
uv run graphrag-ask --show-context --chat
```

Or let an agent pick the retrievers for you:

```bash
uv run graphrag-agent --show-tools "how many organizations are there, and which is most connected?"
uv run graphrag-agent --stream --chat
```

## The agent

`graphrag-ask` runs one fixed retriever and answers in a single shot. That is the
right shape for "find the passage that answers this", and the wrong shape for the
question above: it is part lookup and part arithmetic, and whichever retriever you
pick answers half of it. Semantic search returns the top *k* passages and will
quietly undercount; `text2cypher` counts correctly and never sees the prose.

`graphrag-agent` — [agent.py](src/graphrag_kit/agent.py) — hands the retrievers to a
[Microsoft Agent Framework](https://learn.microsoft.com/en-us/agent-framework/)
agent as tools and lets the model choose, call more than one, and call again after
reading the first result. Retrieval is unchanged: same indexes, same
`GRAPH_CONTEXT_QUERY`, same graph.

| Tool | Backed by | For |
|---|---|---|
| `search_documents` | `HybridCypherRetriever` | Anything answered by the source text. The default. |
| `query_graph_with_cypher` | `Text2CypherRetriever` | Counting, aggregating, listing *every* match. |
| `look_up_entity` | entity fulltext index | A name you already have, and its connections both ways. |
| `graph_overview` | label/type counts | What kinds of things exist at all. |

`search_documents` and `look_up_entity` record the element IDs of what they read on
an `EvidenceTrail`, so the explorer still lights up the evidence — the entities the
agent *actually read* plus one hop out from them, including entities reached by a
name lookup that no chunk search returned. The other two record only the call: an
answer drawn from `query_graph_with_cypher` or `graph_overview` alone leaves no IDs
behind, and the highlight falls back to the ordinary hybrid lookup. `--show-tools`
prints the same trail in the terminal.

The agent is also the last entry in the explorer's retriever dropdown, served there
by `agent_stages()` on `POST /api/ask/stream` — the same endpoint every other mode
uses. The tool calls come back in the context panel. `POST /api/ask` answers agent
questions too, as plain JSON for scripted callers; the browser simply never calls
it.

Model configuration is shared with everything else — same deployment, same Entra
or key auth — except for the API version, which it sets itself. See
`AGENT_CHAT_API` in [.env.example](.env.example).

## The explorer

Three views over the one graph, switched in the masthead:

| View | What it shows |
|---|---|
| **Graph** | The records themselves, filtered by group or label. |
| **Schema** | The project's model — one node per type, sized by how many records carry it, with the patterns the schema licenses as edges. Click a type for its properties and their meanings. This is the view for explaining the model to someone. |
| **Timeline** | Entities carrying the project's `date_property`, in order. Hidden when the project declares none. |

- **Ask a question** — the graph unfolds in step with the pipeline rather than
  redrawing once at the end: the matched passages first, then the entities
  extracted from them, then one hop of neighbours, while the model is still
  writing. The standing graph is ghosted as the first ring lands (not when you
  ask — the agent can take a minute to choose its tools, and an empty stage for
  all of it is not a loading state), a stage line names what is running, a
  segmented indicator says how much is still to come, and the camera re-fits to
  each ring. Evidence levels in the answer are colour-coded where the corpus has
  them. `agent` mode has no rings to stream — it decides what to read as it goes
  — so it lights up what its tools touched, plus one hop out, once, at the end.
- **Filter** by group, by individual label, or by evidence level. Counts come
  from the live graph. Entities with no relationship at all are excluded by
  default and offered as their own toggle: on a large extracted corpus they can
  be a third of the nodes and they bury the structure worth looking at.
- **Click a node** for every property the extractor recorded and every
  connection, each one clickable. Properties are passed through wholesale rather
  than picked from a fixed list, because in most corpora the domain properties
  *are* the record.
- **Search** runs against a fulltext index over the project's
  `entity_text_properties`.
- **Add a document** runs the ingestion pipeline over an uploaded file and
  streams what it found, then lights up what the document added and what it
  connected to. Hidden behind nothing — it writes to the same graph you are
  looking at.

**The highlight is not the retriever's own result.** Whatever retriever answered,
the rings come from a separate vector + fulltext lookup for the question
(`retrieved_chunks` on the streaming path, `evidence_subgraph` on `/api/ask`),
because retrievers hand back rendered text and the front-end needs element IDs.
For `hybrid` and `hybrid-cypher` that hits the same two indexes that answered, so
the rings match what was read. For `vector`, `vector-cypher` and especially
`text2cypher` — which touches neither index — it is an independent lookup, so read
the rings as *what this question matches in the corpus*, not *what this retriever
read*. `agent` mode is the exception: its ring is the trail its tools actually left.

The renderer is a dependency-free canvas force layout. NVL is wired up too and
available at `?renderer=nvl`, but it is not the default: it ships ESM-only, so it
has to come from a CDN at runtime, which costs a ~10s cold load and puts a live
demo at the mercy of someone else's uptime.

### The API behind it

The explorer is just a client. Everything it does is available over HTTP, which is
also the shortest path to putting your own front-end on the graph:

| Route | Returns |
|---|---|
| `GET /api/meta` | Project title, labels, POLE groups, palette, live counts, evidence levels if the corpus has any. |
| `GET /api/schema` | The project's schema **as a graph** — one node per type with its properties and live count, one edge per pattern. The model itself, queryable. |
| `GET /api/graph?labels=&status=&connected=` | The entity graph, comma-separated filters. `connected=false` includes entities that take part in no relationship; they are excluded by default and counted in `/api/meta` as `isolated`. |
| `GET /api/expand?id=` | One node plus its direct neighbours and the edges among them. |
| `GET /api/search?q=&limit=` | Entity fulltext search. `limit` defaults to 15. Terms are Lucene-escaped, so a half-typed query is a search rather than a 500. |
| `GET /api/timeline` | Entities carrying the project's `date_property`, in order. |
| `GET /api/documents` | The corpus behind the graph: each source file with its passage and record counts. |
| `POST /api/documents` | **Extend the graph.** Multipart upload; runs the same pipeline, schema and extraction rules over the new file and streams stages as SSE, ending with the subgraph it added. |
| `POST /api/ask` | Answer, retrieved context, and evidence subgraph, as one JSON body. |
| `POST /api/ask/stream` | The same work as Server-Sent Events, one event per stage. |

Both ask routes take the same body — `retriever` and `top_k` are optional, and
`top_k` is capped at 25:

```json
{ "question": "...", "retriever": "hybrid-cypher", "top_k": 5 }
```

The stream emits five event types. `stage` announces what is running; `unfold`
carries one ring of nodes and relationships (`evidence`, `entities`, then
`neighbourhood`); `answer` carries the prose and the retrieved context; `warning`
means a ring failed but the answer is still coming; `error` ends the stream. A
failed ring is deliberately non-fatal — losing the picture should not cost you the
answer.

## Retrievers

`--retriever` on the CLI, or the dropdown in the explorer:

| Retriever | Vector | Fulltext | Graph | Notes |
|---|:---:|:---:|:---:|---|
| `vector` | ✓ | — | — | Baseline. Chunks that *sound* like the question. |
| `hybrid` | ✓ | ✓ | — | Recovers proper nouns that embeddings blur. |
| `vector-cypher` | ✓ | — | ✓ | Graph expansion, no keyword matching. |
| `hybrid-cypher` | ✓ | ✓ | ✓ | Default. |
| `text2cypher` | — | — | ✓ | LLM writes Cypher. Handles counting and aggregation, which vector search cannot do at all. |
| `agent` | ✓ | ✓ | ✓ | Explorer only, or `graphrag-agent`. Not a retriever — an agent that calls the others. |

The interesting code is `GRAPH_CONTEXT_QUERY` in
[retrievers.py](src/graphrag_kit/retrievers.py) — the Cypher that runs *after* the
vector/fulltext lookup and expands each matched chunk into its document, its
entities, and those entities' own relationships. That second hop is the part a
vector store cannot do.

Two variables are injected into that fragment by the library and must not be
re-declared: `node` (the matched `:Chunk`) and `score`. `score` must appear in the
`RETURN`.

## Adopting an existing graph

A graph built by another tool — Neo4j Document Intelligence, an earlier project,
a colleague's import — usually has the right *shape* and the wrong *names*.
`ProjectSpec.lexical` describes the names, so the engine reads it as it is:

```python
lexical=LexicalSpec(
    adopted_chunk_label="__Chunk__",        # chunks already carry this
    source_label="__Document__",            # source files, kept distinct from
                                            # any `Document` *entity* in the schema
    embedding_property="openai_embedding",  # `embedding` is taken, by another model
    entity_to_chunk="FROM_CHUNK|__NODE_TO_CHUNK__",   # read both conventions
    chunk_to_source="FROM_DOCUMENT|__CHUNK_TO_DOCUMENT__",
)
```

Cypher alternation in the relationship fields is what lets one pattern match both
the adopted wiring and the wiring of documents ingested later, without mirroring
thousands of relationships to rename them. The same spec also configures the
*writer*, through `LexicalGraphConfig`, so new documents are written in the shape
the graph already uses rather than corrected afterwards. That matters more than it
sounds: the writer reserves the label `Document` for source files, so in a schema
that has a `Document` entity type the two collide, and an extracted Document is
written as a lexical node with no `__Entity__` label — invisible to every query
the engine runs.

Three things cannot be handled by reading, and `graphrag-adopt` does them:

```bash
uv run graphrag-adopt --dry-run    # report what would change, write nothing
uv run graphrag-adopt              # apply
uv run graphrag-adopt --undo       # remove exactly what adoption added
```

1. **The engine's chunk label**, added alongside the existing one. A vector index
   is fixed to a single label.
2. **Embeddings in the configured model's space.** Vectors from two different
   models cannot share a property or an index, and they do not compare: verbatim
   chunk text scores ~0.50 against a foreign model's vectors, which is cosine
   zero dressed up as a similarity. Adoption writes ours beside theirs and leaves
   theirs working.
3. **A readable name on each source file**, where the foreign tool stored
   something unusable — a signed, expired upload URL, in DI's case, which would
   otherwise be what every citation in every answer quotes.

### Constraints block ingestion

`Neo4jWriter` inserts extracted nodes with `CREATE` and de-duplicates afterwards,
which is why `graphrag-setup` creates no uniqueness constraints of its own. A graph
that *does* carry them — `NODE KEY` on `name`, an existence constraint on a
property your extractor does not always fill — rejects the second mention of the
same entity. The pipeline logs the rejected batch and returns normally, so the
symptom is a document that ingests to nothing.

```bash
uv run graphrag-adopt --relax-constraints
```

Drops the constraints that would reject a new document, creates plain range
indexes on the same properties so lookups keep their index, and records the exact
definitions on a `:__GraphRAGAdoption__` node so `--undo` restores them. The
upload endpoint checks for them before spending a model call and refuses with the
command to run.

## Entity resolution

After an ingest, `SinglePropertyExactMatchResolver` merges entities that share a
label and an exact name. On a corpus the project built, run over everything, that
is what you want: the same person named in six documents should be one node.

On a graph the project **adopted**, it is destructive. Same-named nodes may exist
on purpose — several distinct sightings each named "Fireball sighting" — and
`apoc.refactor.mergeNodes` cannot be undone. So a project declaring
`owns_graph=False` gets a `filter_query` confining resolution to entities
reachable from the document just ingested. Duplicates *within* the new document
still merge; nothing outside it is touched.

The same flag makes `graphrag-reset` refuse without
`--i-know-this-graph-is-not-mine`, because "everything this demo created" is not a
set that command can compute on a graph it did not create.

## Evidence levels

Every entity carries a `status`. The engine treats these as ordered,
strongest-first, and the project names them in its `evidence_levels` (default:
`confirmed`, `reported`, `rumored`). This lets the graph answer "what do we actually
know?" as distinct from "what is being said?"

Because an entity can be asserted at different levels in different documents, a
rollup pass runs **before** entity resolution and writes the strongest observed
level onto every duplicate, keeping the full observed set in `evidence_levels`.
Without it, `apoc.refactor.mergeNodes` — which is called with
`properties: 'discard'` — keeps whichever value it happens to hit first, and a
court-documented fact can come out the far side marked as a rumour.

An entity the extractor left unrated is not dropped, but it is not neutral either.
Retrieval context tags it `[unrated]`, while the explorer's projection, filters and
counts all read `coalesce(n.status, 'reported')` — so on screen it *becomes*
`reported`. That is a trap if you rename the levels: a project whose
`evidence_levels` are `("high", "low")` has no bucket called `reported`, so every
ungraded entity falls outside every filter and disappears from the explorer, with no
error and a count of zero. Either keep `reported` in the tuple, or write extraction
rules that grade everything.

## Starting over

```bash
uv run graphrag-reset --yes
```

Deletes only the labels this scaffold writes — the project's source and chunk
labels, `__Entity__` and `__KGBuilder__` — and drops its indexes. Safe against a
database holding other data, and it refuses outright on a project with
`owns_graph=False`.
Because the indexes go with it, the loop back to a working graph is
`graphrag-reset` → `graphrag-setup` → `graphrag-ingest`.

Add `--keep-indexes` to clear the data and leave the indexes standing, which skips
the `graphrag-setup` rebuild and its ONLINE poll. That is the right choice when you
are re-ingesting the same corpus, and the wrong one if `EMBEDDING_DIMENSIONS` has
changed — the vector index is fixed-width and has to be recreated.

**One project per database.** The `project` key stamped onto each `Document` is
metadata; nothing queries it. Point `GRAPHRAG_PROJECT` at a second corpus without
resetting and both land in one graph, where the counts, the filters and every
retriever span the lot. Reset between projects, or give each its own
`NEO4J_DATABASE` — which needs Aura or Enterprise, since Community serves only
`neo4j`.

## Notes and gotchas

- **Embedding dimensions must match the deployment.** `text-embedding-3-small` is
  1536, `-3-large` is 3072. `EMBEDDING_DIMENSIONS` has to agree with whatever is
  actually deployed; changing it after ingesting needs a `graphrag-reset --yes`,
  then `graphrag-setup` again, then a re-ingest — the vector index is created at a
  fixed width, and `graphrag-setup` is the only thing that creates it. Re-ingesting
  straight after a reset writes embeddings into a database with no vector index,
  which fails silently: retrieval just returns nothing.
- **Temperature is opt-in.** Newer reasoning models (`gpt-5-mini` and friends)
  reject any temperature other than their default and return HTTP 400, so nothing
  is sent unless you set `LLM_TEMPERATURE`.
- **Azure auth mode is explicit, not inferred.** `AZURE_AUTH_MODE` defaults to
  `entra`. An ambient `AZURE_OPENAI_API_KEY` exported in your shell for some other
  resource is deliberately ignored — preferring any key that happens to exist
  sends resource A's key to resource B and surfaces as a 401 that reads like a
  broken endpoint.
- **On Azure, `model` is the deployment name**, not the model name. They are often
  but not always the same string.
- **No uniqueness constraints on entity names.** `Neo4jWriter` inserts extracted
  nodes with `CREATE`, not `MERGE`, and de-duplicates afterwards via the resolver.
  A `Person.name IS UNIQUE` constraint aborts the ingest the first time a person
  appears in two chunks.
- **Indexes must be `ONLINE` before ingesting.** Embeddings written to an index
  still populating are invisible to search, with no error. `graphrag-setup` polls.
- **`.env` overrides the shell.** `load_dotenv(override=True)` is deliberate: a
  stale `NEO4J_URI` exported in your shell otherwise shadows the project's `.env`
  and points the demo at the wrong database without saying so.
- **Components moved namespace in 1.19.** `neo4j_graphrag.experimental.components.*`
  is deprecated for `neo4j_graphrag.components.*` and goes away in 2.0.
  `SimpleKGPipeline` itself still lives under `experimental.pipeline`.
- **Exact-match resolution only.** Fuzzy resolution is tempting but dangerous on
  corpora with numbered entities — at the default threshold it merges "Phase 1"
  with "Phase 2". Consistent naming is enforced in the extraction prompt instead.
- **`Text2CypherRetriever` will not execute writes.** Generated Cypher is run
  through `EXPLAIN` first and rejected if it writes, so a prompt-injected `DELETE`
  never reaches the graph. The only *model-written* Cypher the agent can run goes
  through this retriever, so the same guarantee covers it — `look_up_entity` and
  `graph_overview` run fixed, read-only statements in which the model supplies
  parameters and never Cypher.
- **neo4j-graphrag's extras are unbundled, on purpose.** `[openai]` pins
  `openai<2` and `[experimental]` does the same transitively through llama-index;
  `agent-framework-openai` needs `openai>=2.25`. `pyproject.toml` therefore depends
  on `openai` and `langchain-text-splitters` directly instead — the latter being the
  only part of `[experimental]` this scaffold uses. That drops llama-index and
  neo4j-viz, neither of which is imported here. Re-adding either extra will make
  the lock unsolvable.
- **The agent sets its own Azure API version.** `AZURE_OPENAI_API_VERSION` is for
  the neo4j-graphrag clients, which speak Chat Completions and are usually pinned
  to a GA version like `2024-10-21` — a version with no `/responses` route at all.
  Passing it to the agent's client turns a working deployment into an opaque 404,
  so the agent keeps its own default per API — `preview` for `AGENT_CHAT_API=responses`
  (the default) and `2024-12-01-preview` for `chat-completions` — and its own
  override, `AGENT_AZURE_API_VERSION`. Set `AGENT_CHAT_API=chat-completions` where
  `/responses` is not served, and note that pinning the override then pins it for
  whichever API you are on.
- **Agent Framework renamed most of its Python surface in 2026.** `ChatAgent` is
  `Agent`, `chat_client=` is `client=`, `@ai_function` is `@tool`, `AgentThread` is
  `AgentSession`, and `run_stream()` is `run(..., stream=True)`. The
  `agent_framework.azure` compatibility classes are gone: Azure now goes through
  `agent_framework.openai` with an explicit `azure_endpoint`/`credential`. Most
  tutorials online still show the old names.
- **Sync agent tools run in a worker thread.** The framework invokes them via
  `asyncio.to_thread`, which copies the context in but not back — so the evidence
  trail is a *mutable object* held in a `ContextVar`, not a value the tools reassign.
  A `ContextVar.set()` inside a tool is silently lost.

## Layout

```
src/graphrag_kit/
  project.py          ProjectSpec / LexicalSpec — the engine/corpus seam
  config.py           env loading, driver / LLM / embedder factories
  cypher.py           Cypher fragments built from the project spec
  setup_indexes.py    indexes + ONLINE polling       -> graphrag-setup
  adopt.py            read a graph built elsewhere   -> graphrag-adopt
  ingest.py           SimpleKGPipeline + rollup      -> graphrag-ingest
  retrievers.py       five retrievers, retrieval_query, RAG prompt
  ask.py              terminal client                -> graphrag-ask
  agent.py            retrievers as agent tools      -> graphrag-agent
  server.py           FastAPI + JSON/SSE API         -> graphrag-serve
  reset.py            scoped teardown                -> graphrag-reset
  static/             explorer front-end (no build step)
projects/
  example/            neutral sample corpus + schema
  ufo/                UAP records, POLE, adopted from Document Intelligence
```
