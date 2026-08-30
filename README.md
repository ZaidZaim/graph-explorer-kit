# demo-neo4j-GraphRAG-py

A reusable GraphRAG scaffold on Neo4j, built on the official
[`neo4j-graphrag`](https://github.com/neo4j/neo4j-graphrag-python) package (v1.19).

Point it at a folder of documents and a schema; get back a knowledge graph, five
retrieval strategies, an agent that chooses between them, a terminal client, and an
interactive browser explorer that answers questions **and shows you the subgraph
the answer came from**.

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

Branches in this repo follow that split: `main` is the scaffold plus a neutral
example, and `vice-city` adds a real corpus on top of it.

> **This is the `vice-city` branch.** It adds
> [`projects/vicecity`](projects/vicecity/README.md) — a POLE knowledge graph of
> everything publicly known about Grand Theft Auto VI, where every fact is graded
> confirmed / reported / rumored. See that README for the model and the corpus.

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
uv run graphrag-setup
```

Creates the vector index, two fulltext indexes and supporting range indexes, then
blocks until all of them report `ONLINE`.

```bash
uv run graphrag-ingest
```

Chunks every document in the project's data directory, embeds each chunk, extracts
entities and relationships under the project's schema, rolls up evidence levels,
then merges duplicate entities. `.md`, `.txt` and `.pdf` are picked up, recursively.

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

- **Ask a question** — the graph unfolds in step with the pipeline rather than
  redrawing once at the end: the matched passages first, then the entities
  extracted from them, then one hop of neighbours, while the model is still
  writing. The standing graph is ghosted the moment you ask, a stage line names
  what is running, and the camera re-fits to each ring as it lands — so by the
  time the prose arrives the view is already framed on the evidence. Evidence
  levels in the answer are colour-coded. `agent` mode has no rings to stream — it
  decides what to read as it goes — so it lights up what its tools touched, plus
  one hop out, once, at the end.
- **Filter** by entity type or evidence level; counts come from the live graph.
- **Click a node** for its properties and every connection, each one clickable.
- **Search** runs against a fulltext index over entity names and descriptions.
- **Timeline** lists dated `:Event` nodes in order. It has something to show only
  when the project's schema declares an `Event` type carrying a `date` —
  `projects.example` declares neither, so against the template's own corpus the
  button comes back empty.

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
| `GET /api/meta` | Project title, labels, evidence levels, palette, live counts. |
| `GET /api/graph?labels=&status=` | The whole graph, comma-separated filters. Both default to everything the project declares. |
| `GET /api/expand?id=` | One node plus its direct neighbours and the edges among them. |
| `GET /api/search?q=&limit=` | Entity fulltext search. `limit` defaults to 15. |
| `GET /api/timeline` | Dated `:Event` nodes in date order. |
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

Deletes only the labels this scaffold writes (`Document`, `Chunk`, `__Entity__`,
`__KGBuilder__`) and drops its indexes. Safe against a database holding other data.
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
  project.py          ProjectSpec — the engine/corpus seam
  config.py           env loading, driver / LLM / embedder factories
  setup_indexes.py    indexes + ONLINE polling       -> graphrag-setup
  ingest.py           SimpleKGPipeline + rollup      -> graphrag-ingest
  retrievers.py       five retrievers, retrieval_query, RAG prompt
  ask.py              terminal client                -> graphrag-ask
  agent.py            retrievers as agent tools      -> graphrag-agent
  server.py           FastAPI + JSON/SSE API         -> graphrag-serve
  reset.py            scoped teardown                -> graphrag-reset
  static/             explorer front-end (no build step)
projects/
  example/            neutral sample corpus + schema
  vicecity/           GTA VI POLE corpus — see its README
```
