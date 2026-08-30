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

## Setup

**1. A Neo4j instance.** Either start one locally:

```bash
docker compose up -d
```

or point `.env` at Aura. APOC is required — the entity resolver calls
`apoc.refactor.mergeNodes`. It is bundled in the compose file and present on all
Aura tiers.

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
then merges duplicate entities.

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

Every tool that touches entities records their element IDs on an `EvidenceTrail`, so
the explorer still lights up the evidence — here the subgraph the agent *actually
read*, including entities reached by a name lookup that no chunk search returned.
`--show-tools` prints the same trail in the terminal.

The agent is also the last entry in the explorer's retriever dropdown. It is the
same `POST /api/ask` endpoint; the tool calls come back in the context panel.

Model configuration is shared with everything else — same deployment, same Entra
or key auth — except for the API version, which it sets itself. See
`AGENT_CHAT_API` in [.env.example](.env.example).

## The explorer

- **Ask a question** — the answer appears *and* the graph dims to just the
  entities behind it, then zooms to them. Evidence levels in the answer are
  colour-coded.
- **Filter** by entity type or evidence level; counts come from the live graph.
- **Click a node** for its properties and every connection, each one clickable.
- **Search** runs against a fulltext index over entity names and descriptions.

The renderer is a dependency-free canvas force layout. NVL is wired up too and
available at `?renderer=nvl`, but it is not the default: it ships ESM-only, so it
has to come from a CDN at runtime, which costs a ~10s cold load and puts a live
demo at the mercy of someone else's uptime.

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
strongest-first, and the project names them (default: `confirmed`, `reported`,
`rumored`). This lets the graph answer "what do we actually know?" as distinct
from "what is being said?"

Because an entity can be asserted at different levels in different documents, a
rollup pass runs **before** entity resolution and writes the strongest observed
level onto every duplicate, keeping the full observed set in `evidence_levels`.
Without it, `apoc.refactor.mergeNodes` — which is called with
`properties: 'discard'` — keeps whichever value it happens to hit first, and a
court-documented fact can come out the far side marked as a rumour.

## Starting over

```bash
uv run graphrag-reset --yes
```

Deletes only the labels this scaffold writes (`Document`, `Chunk`, `__Entity__`,
`__KGBuilder__`) and drops its indexes. Safe against a database holding other data.

## Notes and gotchas

- **Embedding dimensions must match the deployment.** `text-embedding-3-small` is
  1536, `-3-large` is 3072. `EMBEDDING_DIMENSIONS` has to agree with whatever is
  actually deployed; changing it after ingesting needs a `graphrag-reset --yes`
  and a re-ingest, because the vector index is created at a fixed width.
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
  corpora with numbered entities — at the default threshold it merges "Trailer 1"
  with "Trailer 2". Consistent naming is enforced in the extraction prompt instead.
- **`Text2CypherRetriever` will not execute writes.** Generated Cypher is run
  through `EXPLAIN` first and rejected if it writes, so a prompt-injected `DELETE`
  never reaches the graph. The agent reaches Cypher only through this retriever,
  so the same guarantee covers it.
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
  so the agent keeps its own default (`preview`) and its own override,
  `AGENT_AZURE_API_VERSION`. Set `AGENT_CHAT_API=chat-completions` where
  `/responses` is not served.
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
  server.py           FastAPI + JSON API             -> graphrag-serve
  reset.py            scoped teardown                -> graphrag-reset
  static/             explorer front-end (no build step)
projects/
  example/            neutral sample corpus + schema
```
