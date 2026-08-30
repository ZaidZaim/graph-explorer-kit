# `projects.example` — the template project

The smallest thing that exercises the whole pipeline. Two fictional vendors and
the customer they share, written so the interesting answers span documents.
Copy this directory to start your own demo.

```bash
cp -r projects/example projects/mycorpus
rm projects/mycorpus/data/*.md    # the example corpus came along with the copy
# edit projects/mycorpus/__init__.py, drop your own documents in data/
```

Then select it **in `.env`**:

```bash
GRAPHRAG_PROJECT=projects.mycorpus
```

Not on the command line. `.env` is loaded with `override=True`, so a
`GRAPHRAG_PROJECT=... uv run ...` prefix is read and then silently overwritten by
whatever `.env` says.

No `graphrag_kit` code changes — the engine reads everything it needs from the
`PROJECT: ProjectSpec` this package exports.

## What a project owns

Eleven fields. The first five have no defaults, and three of them are the ones
people forget to change when they copy:

| Field | What it does |
|---|---|
| `key` | Short id, stamped onto every `Document` as `project`. |
| `title` / `subtitle` | The explorer's sidebar heading. Change these, or your demo is still branded "Example Corpus". |
| `schema` | The `GraphSchema` the extractor is held to. Node types, relationship types, and the patterns allowed between them. `additional_*=False` keeps the LLM from inventing labels. |
| `data_dir` | Folder of source documents, scanned **recursively** for `.md`, `.txt` and `.pdf`. One file per source; the filename becomes the `Document`. |
| `extraction_rules` | Appended to the extraction prompt. Where you say how `status` is stated in *your* text, and how to name entities consistently. |
| `rag_persona` | One line of framing prepended to the answer prompt. |
| `text2cypher_examples` | Few-shot pairs that teach the LLM your labels. Two good ones beat ten vague ones. |
| `example_questions` | Seed questions shown in the explorer. |
| `palette` | Node colour per label in the explorer. |
| `evidence_levels` | The status vocabulary, strongest first. Defaults to `("confirmed", "reported", "rumored")`. |

Full definitions and defaults: [`project.py`](../../src/graphrag_kit/project.py).

**The explorer renders a fixed set of properties.** `NODE_PROJECTION` in
[server.py](../../src/graphrag_kit/server.py) reads `name`, `description`, `status`,
`evidence_levels`, `role`, `kind`, `date`, `fictional` and `inspiration`, and the
details panel shows a subset of those. Any other property your schema declares is
extracted and stored, and then never appears — this project's
`Organization.industry` is exactly that case. Reuse those names where they fit, or
extend `NODE_PROJECTION` and `app.js` when they don't.

## Try it

```bash
uv run graphrag-setup
uv run graphrag-ingest
uv run graphrag-serve
```

Then ask *"Who runs engineering at the company Kestrel competes with?"*

Neither briefing answers that alone. `kestrel-automation.md` names the competitor
and never says who works there; `meridian-robotics.md` names Dr. Amara Okonjo and
never mentions Kestrel. The hop between them is the whole reason to put a graph
behind retrieval.

The corpus is built to reward that shape of question. All three documents lean on
Nordhavn Terminals, the customer both vendors share, and Aarhus is the one site
where both their systems run — so the sector is genuinely hard to summarise from
any single file.
