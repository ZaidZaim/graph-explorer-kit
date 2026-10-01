# demo-neo4j-GraphRAG-py

A reusable GraphRAG scaffold on Neo4j, built on
[`neo4j-graphrag`](https://github.com/neo4j/neo4j-graphrag-python). Point it at a
folder of documents and a schema; get a knowledge graph, five retrieval strategies,
an agent that chooses between them, and a browser explorer that answers questions
**and shows related graph context alongside the answer**. The visualization can
use a separate lookup; it is not an exact trace of the evidence used to generate
each claim. See the retrieved context and source documents when checking an answer.

```
projects/<name>/data ──► SimpleKGPipeline ──► (:Chunk)-[:FROM_DOCUMENT]->(:Document)
                                              (:Entity)-[:FROM_CHUNK]->(:Chunk)
                                              (:Entity)-[:REL]->(:Entity)
                                                        │
                              HybridCypherRetriever ────┴──── Agent Framework agent
                                                        ▼
                                              answer + related graph context
```

## Getting started

Needs [`uv`](https://docs.astral.sh/uv/) (Python 3.10+), Neo4j 5.23+ with APOC
(Docker or [Aura](https://console.neo4j.io)), and a chat plus an embedding model
(Microsoft Foundry or OpenAI).

```bash
git clone https://github.com/ZaidZaim/demo-neo4j-GraphRAG-py.git
cd demo-neo4j-GraphRAG-py
uv sync
cp .env.example .env     # set GRAPHRAG_PROJECT, NEO4J_*, and the model block
docker compose up -d     # skip if .env points at Aura
az login                 # Foundry only; or LLM_PROVIDER=openai + OPENAI_API_KEY

uv run graphrag-setup    # indexes
uv run graphrag-ingest   # chunk, embed, extract, resolve
uv run graphrag-serve    # http://localhost:8000
```

Terminal instead: `uv run graphrag-ask "…"` or `uv run graphrag-agent --chat`.

## How it is split

`src/graphrag_kit/` is domain-agnostic. A demo is one `ProjectSpec` under
`projects/` (schema, data, extraction rules, example Cypher, seed questions,
palette), selected with `GRAPHRAG_PROJECT=projects.example`. To start a new demo,
copy `projects/example`, swap the schema and corpus, and point the variable at it.

## Demos

Each demo is a branch that adds one project on top of this engine.

| Branch | Corpus | Shows |
|---|---|---|
| `main` | Fictional port-automation briefings | The scaffold; the template to copy |
| `vice-city` | Nine documents on GTA VI | Evidence grading, a POLE model, theming |
| `pharma-pipeline` | Four pharma pipeline decks | Adopting a Document Intelligence graph |
| `ufo-documents` | 240 released UAP files (scans) | OCR, batch ingest, 54k-record graph |

## Docs

[Engine manual](docs/ENGINE.md): why a graph, setup, the CLI, agent,
conversations, explorer and API, retrievers, adopting an existing graph, entity
resolution, evidence levels, gotchas, layout.
