# `projects.example` — the template project

The smallest project that exercises the whole pipeline: three short briefings
about a fictional port-automation sector, a four-type ontology, and questions
written so the answers cross documents. Copy this directory to start your own
demo.

## The use case

Two vendors sell into the same ports. Meridian Robotics, in Gothenburg, builds
driverless yard tractors and inspection drones. Kestrel Automation, in
Rotterdam, sells the scheduling software that tells equipment like Meridian's
where to go, and calls itself vendor-neutral. Nordhavn Terminals runs terminals
in Aarhus and Rotterdam and is a customer of both. Aarhus is the one site where
the two vendors' systems run together.

Each company has one briefing. Each briefing describes its own company well and
mentions the others in passing. That's the position an analyst is usually in:
the facts exist, they're spread across sources, and the relationships between
sources are what nobody wrote down.

The corpus is fictional and small on purpose. It exists to prove the pipeline
end to end and to make the graph's contribution visible. Every fact carries a
status line ("Status: confirmed", "reported", or "rumored") so evidence grading
has something to grade.

## The ontology

Four entity types, five relationship types, and the patterns the text may
assert between them.

| Type | What it stands for | Properties |
|---|---|---|
| `Person` | A named individual | `name`, `role`, `description`, `status` |
| `Organization` | A company, university, or public body | `name`, `industry`, `description`, `status` |
| `Product` | A commercial product or platform | `name`, `kind`, `description`, `status` |
| `Location` | A city, region, or country | `name`, `description`, `status` |

```
(:Person)-[:WORKS_AT]->(:Organization)
(:Organization)-[:BASED_IN]->(:Location)
(:Organization)-[:PRODUCES]->(:Product)
(:Organization)-[:PARTNERS_WITH]->(:Organization)
(:Organization)-[:COMPETES_WITH]->(:Organization)
```

`additional_node_types` and `additional_relationship_types` are off, so the
extractor is held to exactly this. A model left to itself invents `Executive`,
`Company`, and `Firm` for the same idea, and the graph fragments. Naming the
types in advance is what makes "how are Meridian and Kestrel connected?"
answerable: both are `Organization`, and the question is a path between two
nodes of one label.

`status` is the evidence level, one of `confirmed`, `reported`, or `rumored`,
strongest first. The extraction rules tell the model where the text states it
and to inherit the section's status where a sentence has none. The explorer
filters on it and the answer prompt cites it, so "what is only rumored?" is a
query rather than a judgment call.

## Why a graph

Ask *"Who runs engineering at the company Kestrel competes with?"*

No briefing answers that alone. The Kestrel briefing names the competitor and
never says who works there. The Meridian briefing names Dr. Amara Okonjo and
never mentions Kestrel. A vector search finds one passage or the other, and the
passage it finds holds half the answer.

In the graph the question is two hops:

```cypher
MATCH (k:Organization {name: 'Kestrel Automation'})-[:COMPETES_WITH]-(rival)<-[:WORKS_AT]-(p:Person)
WHERE p.role CONTAINS 'Engineering'
RETURN rival.name, p.name, p.role
```

Every node on that path points back through `FROM_CHUNK` to the passage that
asserted it, so the explorer draws the answer's evidence as it forms: the two
passages, the entities extracted from them, and the relationship that joins
them. That chain is the demo. The same question against a plain vector index is
the control.

## Copy it

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

No `graphrag_kit` code changes. The engine reads everything it needs from the
`PROJECT: ProjectSpec` this package exports.

## What a project owns

Nineteen fields. The first five have no defaults, and three of them are the ones
people forget to change when they copy:

| Field | What it does |
|---|---|
| `key` | Short id, stamped onto every `Document` as `project`. |
| `title` / `subtitle` | The explorer's masthead. Change these, or your demo is still branded "Example Corpus". |
| `schema` | The `GraphSchema` the extractor is held to: node types, relationship types, and the patterns allowed between them. `additional_*=False` keeps the model from inventing labels. |
| `data_dir` | Folder of source documents, scanned **recursively** for `.md`, `.markdown`, and `.pdf`. One file per source; the filename becomes the `Document`. |
| `extraction_rules` | Appended to the extraction prompt. Where you say how `status` is stated in *your* text, and how to name entities consistently. |
| `rag_persona` | One line of framing prepended to the answer prompt. |
| `text2cypher_examples` | Few-shot pairs that teach the model your labels. Two good ones beat ten vague ones. |
| `example_questions` | Seed questions shown in the explorer's chat column. |
| `palette` | Node colour per label in the explorer. |
| `evidence_levels` | The status vocabulary, strongest first. Defaults to `("confirmed", "reported", "rumored")`. An empty tuple turns grading off, and the explorer drops the facet. |
| `name_properties` | Which property names a node, in order of preference. Defaults to `("name",)`. |
| `date_property` | The property the Timeline view orders by. `None` hides the view. |
| `groups` / `group_colors` | An optional lens over the labels, such as POLE. The explorer groups its filters by it and colours nodes by group. |
| `owns_graph` / `lexical` | For a project that reads a graph another tool built. See the main README, **Adopting an existing graph**. |
| `theme_css` | Optional stylesheet loaded after the engine's own. Override the tokens at the top of `styles.css` to give the explorer the look of your subject; the graph canvas follows the same tokens. |

Full definitions and defaults: [`project.py`](../../src/graphrag_kit/project.py).

**The explorer shows every property the extractor stored**, minus a few
internal keys (`HIDDEN_PROPERTY_KEYS` in
[server.py](../../src/graphrag_kit/server.py)). Anything your schema declares
appears in the details panel, so this project's `Organization.industry` shows up
without any front-end change.

## Try it

```bash
uv run graphrag-setup
uv run graphrag-ingest
uv run graphrag-serve
```

Then ask the question from **Why a graph** above, and watch the two passages
light up before the answer arrives.
