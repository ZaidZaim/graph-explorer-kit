# `projects.example` — the template project

The smallest thing that exercises the whole pipeline. Two fictional vendors and
the customer they share, written so the interesting answers span documents.
Copy this directory to start your own demo.

```bash
cp -r projects/example projects/mycorpus
# edit projects/mycorpus/__init__.py, drop your .md files in data/
echo "GRAPHRAG_PROJECT=projects.mycorpus" >> .env
```

No `graphrag_kit` code changes — the engine reads everything it needs from the
`PROJECT: ProjectSpec` this package exports.

## What a project owns

| Field | What it does |
|---|---|
| `schema` | The `GraphSchema` the extractor is held to. Node types, relationship types, and the patterns allowed between them. `additional_*=False` keeps the LLM from inventing labels. |
| `data_dir` | Folder of `.md` documents. One file per source; the filename becomes the `Document`. |
| `extraction_rules` | Appended to the extraction prompt. Where you say how `status` is stated in *your* text, and how to name entities consistently. |
| `rag_persona` | One line of framing prepended to the answer prompt. |
| `text2cypher_examples` | Few-shot pairs that teach the LLM your labels. Two good ones beat ten vague ones. |
| `example_questions` | Seed questions shown in the explorer. |
| `palette` | Node colour per label in the explorer. |

Full field list and defaults: [`project.py`](../../src/graphrag_kit/project.py).

## Try it

```bash
GRAPHRAG_PROJECT=projects.example uv run graphrag-setup
GRAPHRAG_PROJECT=projects.example uv run graphrag-ingest
GRAPHRAG_PROJECT=projects.example uv run graphrag-serve
```

Then ask *"How are Meridian and Kestrel connected?"* — neither document mentions
the other company. The answer comes from the shared customer, which is the whole
point of putting a graph behind retrieval.
