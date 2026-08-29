"""Vice City — a POLE knowledge graph of everything publicly known about GTA VI.

POLE (Person, Object, Location, Event) is the intelligence-analysis model used in
policing and investigations. Its point is that every fact anchors to one of four
entity kinds, so heterogeneous material — marketing, news, court reporting, fan
documentation — lands in one queryable structure. This project uses POLE+O,
adding Organization, which is standard where corporate and criminal entities both
matter.

    GRAPHRAG_PROJECT=projects.vicecity

Every node carries `status`, because this is a corpus about an unreleased game:
some of it is marketing, some is court record, and a lot is speculation repeated
until it sounds like fact. Keeping that distinction in the graph is the
difference between a demo and a rumour mill.
"""

from __future__ import annotations

from pathlib import Path

from graphrag_kit.project import ProjectSpec
from projects.vicecity.schema import POLE_SCHEMA

EXTRACTION_RULES = """
Corpus-specific rules:
- Every entity MUST get a `status` property, one of: confirmed, reported, rumored.
  The text states this explicitly in lines like "Status: confirmed" or
  "Status: rumored". Use the status the text asserts for that fact. Where a
  sentence carries no explicit status, inherit the status of its section.
- Set `fictional` to true for in-game characters, places and organizations, and
  false for real people, real places and real companies.
- Real people (Strauss Zelnick, Arion Kurtaj) and in-game characters (Jason Duval,
  Lucia Caminos) are both Person nodes; distinguish them with `fictional`.
- Dates belong on Event nodes in the `date` property: ISO-8601 where the text
  gives a full date, otherwise the month or year as written.
- Emit exactly ONE Event per real-world occurrence. Do not create both
  "Trailer 1 premiere" and "Trailer 1 release" — pick one name and reuse it.
"""

PROJECT = ProjectSpec(
    key="vicecity",
    title="VICE CITY",
    subtitle="POLE knowledge graph · Grand Theft Auto VI",
    schema=POLE_SCHEMA,
    data_dir=Path(__file__).resolve().parent / "data",
    extraction_rules=EXTRACTION_RULES,
    rag_persona=(
        "You are an analyst answering questions about Grand Theft Auto VI from a "
        "POLE knowledge graph (Person, Object, Location, Event, Organization)."
    ),
    text2cypher_examples=[
        "USER INPUT: 'Who was involved in the 2022 breach?' "
        "QUERY: MATCH (p:Person)-[:INVOLVED_IN]->(e:Event) "
        "WHERE toLower(e.name) CONTAINS 'breach' RETURN p.name, p.role, e.name, e.date",
        "USER INPUT: 'What is only rumored rather than confirmed?' "
        "QUERY: MATCH (n:__Entity__) WHERE n.status = 'rumored' "
        "RETURN head([l IN labels(n) WHERE NOT l STARTS WITH '__']) AS type, n.name, n.description",
        "USER INPUT: 'Show the events in order' "
        "QUERY: MATCH (e:Event) WHERE e.date IS NOT NULL "
        "RETURN e.name, e.date, e.kind ORDER BY e.date",
        "USER INPUT: 'Which locations are in Leonida?' "
        "QUERY: MATCH (l:Location)-[:PART_OF]->(s:Location) WHERE s.name CONTAINS 'Leonida' "
        "RETURN l.name, l.inspiration",
    ],
    example_questions=[
        "Who was involved in the 2022 Rockstar breach?",
        "What is only rumored rather than confirmed?",
        "How is Boobie Ike connected to Real Dimez?",
        "Why was the game delayed twice?",
        "Which locations are part of Leonida?",
    ],
    palette={
        "Person": "#FF5A8C",
        "Object": "#FFC857",
        "Location": "#2BD9C4",
        "Event": "#9B7BFF",
        "Organization": "#5AA9FF",
    },
)
