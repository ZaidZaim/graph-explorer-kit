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

## The use case

An unreleased game with a public record that is huge and almost entirely
second-hand. Rockstar Games and Take-Two say a little, on their own schedule.
The press reports on that, and on court filings from the 2022 breach. Fans fill
the silence with datamining, leak chatter, and speculation repeated until it
reads like fact.

The questions anyone following it asks all cut across those sources:

- Who was involved in the 2022 breach, and what happened to them?
- Why was the game delayed twice, and what did the company say each time?
- How are the in-game characters connected to each other, and to the real
  people who made them?
- Which locations are part of Leonida, and what are they modelled on?
- What do we know for certain, and what is only rumour?

The last one is the point of the whole project. Marketing, court record, and
speculation describe the same people, places, and events. A passage index
returns them side by side with nothing to tell them apart. This graph carries an
evidence level on every fact, so "what do we actually know?" is a query.

## The ontology: POLE, plus Organization

POLE (Person, Object, Location, Event) is the entity model policing and
intelligence analysis use. Every fact anchors to one of four kinds, which is
what lets heterogeneous material land in one structure you can query: a
marketing trailer, a court judgment, an earnings call, and a fan wiki all
decompose into people, things, places, and happenings. This project adds
Organization, standard wherever corporate and criminal entities both appear.

| Label | Examples in this corpus | What sets it apart |
|---|---|---|
| **Person** | Jason Duval, Lucia Caminos, Arion Kurtaj, Strauss Zelnick | `role`, and `fictional` to separate characters from real people |
| **Object** | trailers, PS5, the Ultimate Edition, an Amazon Firestick | `kind`: trailer, platform, edition, vehicle, evidence |
| **Location** | Vice City, Leonida Keys, Grassrivers, Oxfordshire | `fictional`, and `inspiration` for the real place a fictional one is modelled on |
| **Event** | trailer premieres, two delay announcements, the 2022 breach, sentencing | `date` (ISO-8601 where known) and `kind`; the Timeline view orders by it |
| **Organization** | Rockstar Games, Take-Two, Netflix, Lapsus$, Only Raw Records | `kind`, and `fictional` for in-game factions and labels |

Every label carries `status`, the evidence level described below.

Ten relationship types connect them. `INVOLVED_IN` ties people, organizations,
and objects to events and carries a `role`; `MEMBER_OF`, `ASSOCIATE_OF`, and
`OWNS` describe the social and commercial ties; `OCCURRED_AT`, `APPEARS_IN`,
`BASED_IN`, and `PART_OF` place things; `PRECEDED_BY` orders events into a
timeline; and `DEPICTS` records which trailer showed which place. Sixteen
patterns say which pairs each may join, and the extractor may not invent more.
Without that constraint the model produces `Game`, `Feature`, and `Character`
labels of its own, and the four-quadrant structure stops meaning anything.

In-game and real-world **people, places, and organizations** share labels and
are separated by the `fictional` flag, so you can ask about the fiction and the
business in one query. `Object` and `Event` carry no such flag: the '95 Grotti
Cheetah and a real PS5 are both `Object`, so a blanket
`WHERE n.fictional = true` silently drops every in-game vehicle and edition.

## Evidence levels are the point

Every node carries a `status`:

- **confirmed**: stated by Rockstar Games, Take-Two, or a court record
- **reported**: credible press reporting
- **rumored**: fan speculation, datamining, or unverified leak chatter

The source documents assert the level per claim, the extractor carries it onto
the entity, and the explorer colours by it and filters on it.

Because an entity can be asserted at different levels in different documents, a
rollup pass after ingestion takes the strongest observed level. Grassrivers is a
**confirmed** location that happens to have a **rumored** claim attached to it,
and the graph says so rather than downgrading the place to a rumour. Nodes keep
the full observed set in `evidence_levels`, which the details panel shows as
"confirmed — also seen as rumored".

## Why a graph

- **Connections are the content.** "How is Boobie Ike connected to Real
  Dimez?" is a path through people, labels, and events that no single document
  spells out. In the graph it's a traversal, and the explorer draws the route.
- **Counting is a query.** "How many entities are only rumored?" is beyond any
  vector search. `text2cypher` writes the `count()` and answers it.
- **Time is structure.** `PRECEDED_BY` edges and `Event.date` turn nine
  documents' worth of announcements, delays, and hearings into one ordered
  timeline, which the Timeline view shows directly.
- **Evidence travels with the fact.** Because `status` is a property, the
  distinction between confirmed and rumoured survives retrieval, ranking, and
  summarisation. In a passage index it survives only if the model happens to
  quote it.
- **Provenance is a click away.** Each entity keeps `FROM_CHUNK` to its passage
  and each passage `FROM_DOCUMENT` to its file, and the explorer unfolds that
  chain before the answer arrives.

Ask for a count and a lookup at once and no single retriever will do:

```bash
uv run graphrag-agent --show-tools "How many entities are only rumored, and which of them touch the 2022 breach?"
```

`text2cypher` can count and never reads the prose; the hybrid retrievers read
the prose and quietly undercount. The agent runs both tools and says so.
`--show-tools` prints which it reached for, and the explorer lights up what
they read.

## On the 2022 leak

`07-the-2022-leak.md` models the September 2022 Rockstar Games breach as a
documented event: participants, method, dates, and the legal outcome, all from
court reporting and mainstream press. It deliberately does **not** catalogue,
describe, or reproduce the stolen footage or source code. The graph is about
the breach and never built from its contents.

## Corpus

Nine documents in `data/`, current as of 29 August 2026, two days after the
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

In the explorer, the same questions unfold on the graph as the pipeline runs:
the passages that matched, the entities extracted from them, then the
neighbourhood the graph adds, before the prose arrives in the chat column.

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
produced about 100 entities and only 4 `PRECEDED_BY` edges, against 14 here, so
a noticeably weaker timeline.

## Known rough edges

- Extraction is non-deterministic. Successive ingests of the same corpus produce
  slightly different entity counts, and occasional near-duplicates survive
  (`Lucia` alongside `Lucia Caminos`) because resolution is exact-match only.
  Fuzzy resolution would fix that class of duplicate, but at the default
  threshold it also merges `Trailer 1` with `Trailer 2`, which is worse.
- Corpus accuracy is as of the date above. GTA VI news moves quickly. Re-check
  before showing this to anyone who follows it closely.
