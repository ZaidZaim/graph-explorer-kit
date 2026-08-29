# Vice City — a POLE knowledge graph of GTA VI

Everything publicly known about Grand Theft Auto VI, modelled as a POLE
intelligence graph and queryable in plain English.

```bash
# in .env
GRAPHRAG_PROJECT=projects.vicecity
```

```bash
uv run graphrag-setup
uv run graphrag-ingest
uv run graphrag-serve      # http://localhost:8000
```

## Why POLE

POLE (Person, Object, Location, Event) is the entity model used in policing and
intelligence analysis. Every fact anchors to one of four kinds, which is what lets
genuinely heterogeneous material — a marketing trailer, a court judgment, an
earnings call, a fan wiki — land in one structure you can actually query. This
project uses POLE+O, adding Organization, standard wherever corporate and criminal
entities both appear.

| | Examples in this corpus |
|---|---|
| **Person** | Jason Duval, Lucia Caminos, Arion Kurtaj, Strauss Zelnick |
| **Object** | trailers, PS5, the Ultimate Edition, an Amazon Firestick |
| **Location** | Vice City, Leonida Keys, Grassrivers, Oxfordshire |
| **Event** | trailer premieres, two delay announcements, the 2022 breach, sentencing |
| **Organization** | Rockstar Games, Take-Two, Netflix, Lapsus$, Only Raw Records |

In-game and real-world entities share the same labels and are separated by a
`fictional` flag, so you can ask about the fiction and the business in one query.

## Evidence levels are the point

This is a corpus about an unreleased game. Some of it is marketing, some is court
record, and a great deal is speculation repeated until it sounds like fact. Every
node therefore carries a `status`:

- **confirmed** — stated by Rockstar Games, Take-Two, or a court record
- **reported** — credible press reporting
- **rumored** — fan speculation, datamining, or unverified leak chatter

The source documents assert this explicitly per claim, the extractor is instructed
to carry it onto the entity, and the explorer colours it. That makes
*"what do we actually know?"* a question the graph can answer — and it is the one
worth asking about this subject.

Because an entity can be asserted at different levels in different documents, a
rollup pass takes the strongest observed level: Grassrivers is a **confirmed**
location that happens to have a **rumored** claim attached to it, not a rumour.
Nodes keep the full observed set in `evidence_levels`, which the details panel
shows as "confirmed — also seen as rumored".

## On the 2022 leak

`07-the-2022-leak.md` models the September 2022 Rockstar Games breach as a
documented event: participants, method, dates, and the legal outcome, all from
court reporting and mainstream press. It deliberately does **not** catalogue,
describe, or reproduce the stolen footage or source code. The graph is about the
breach, not built from its contents.

## Corpus

Nine documents in `data/`, current as of 29 August 2026 — two days after the
Extended Look premiere. Citations live in [SOURCES.md](SOURCES.md), kept outside
`data/` on purpose: when citations sit in the ingested text, the extractor turns
article headlines and publication names into Event and Organization nodes.

| File | Covers |
|---|---|
| `01-release-and-editions.md` | 19 Nov 2026 date, platforms, editions, pre-orders |
| `02-protagonists.md` | Jason Duval, Lucia Caminos |
| `03-supporting-cast.md` | Cal Hampton, Boobie Ike, Dre'Quan Priest, Real Dimez |
| `04-leonida-map.md` | Leonida and its regions |
| `05-marketing-timeline.md` | Trailer 1, Trailer 2, the Extended Look |
| `06-delay-history.md` | Both delays and the statements around them |
| `07-the-2022-leak.md` | The breach, the prosecution, the sentence |
| `08-organizations.md` | Real and in-game organizations |
| `09-unverified-claims.md` | Everything that is only rumoured |

## Questions worth asking

```bash
uv run graphrag-ask "Who was involved in the 2022 Rockstar breach?"
uv run graphrag-ask "What is only rumored rather than confirmed?"
uv run graphrag-ask "How is Boobie Ike connected to Real Dimez?"
uv run graphrag-ask --retriever text2cypher "How many entities are only rumored?"
```

The last one is the case for having a graph at all: counting and aggregation are
things vector search cannot do, and `text2cypher` answers it by writing Cypher.

## How this graph was built

The committed numbers below came from `gpt-5.6-sol` on Microsoft Foundry, with
`text-embedding-3-small` (1536d) for vectors:

| | |
|---|---|
| Documents / chunks | 9 / 38 |
| Entities | 138 — Event 42, Object 31, Organization 26, Location 21, Person 18 |
| Relationships | 170, led by INVOLVED_IN (103) |
| Evidence | confirmed 105, reported 22, rumored 11 |

Extraction quality tracks the model. The same corpus through `gpt-4.1-mini`
produced ~100 entities and only 4 `PRECEDED_BY` edges, against 14 here — a
noticeably weaker timeline.

## Known rough edges

- Extraction is non-deterministic. Successive ingests of the same corpus produce
  slightly different entity counts, and occasional near-duplicates survive
  (`Lucia` alongside `Lucia Caminos`) because resolution is exact-match only.
  Fuzzy resolution would fix that class of duplicate but at the default threshold
  it also merges `Trailer 1` with `Trailer 2`, which is worse.
- Corpus accuracy is as of the date above. GTA VI news moves quickly; re-check
  before showing this to anyone who follows it closely.
