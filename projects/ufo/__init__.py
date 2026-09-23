"""UFO Documents — a POLE knowledge graph over the war.gov/ufo (PURSUE) releases.

The graph this project reads was first built with Neo4j Document Intelligence
from the released PDFs; this package puts the `neo4j-graphrag` engine on top of
it — retrieval, an agent, an explorer, and ingestion for documents added later.

    GRAPHRAG_PROJECT=projects.ufo

POLE (Person, Object, Location, Event) is the intelligence-analysis model used
in policing and investigations: every fact anchors to one of four entity kinds,
so heterogeneous material lands in one queryable structure. Two groups are added
to it here, both because this corpus cannot be read without them:

  ORGANIZATION  the +O of POLE+O — agencies are actors in their own right.
  RECORD        the provenance layer. A UAP corpus is not a corpus of facts, it
                is a corpus of *documents asserting* facts, and the difference
                is the whole analytical value. Document, Release, Claim,
                Evidence and Redaction sit here.

The labels stay the domain's own — Witness is not merged into Person, and
Observation is not merged into Event — because the distinctions carry the
evidence. POLE is the lens over them, not a replacement for them.

On uncertainty: nothing in this project asserts that anything is of
extraterrestrial origin, and nothing infers a cause. The corpus records what
observers reported, what instruments captured, and what agencies concluded —
including where those disagree. Redactions are kept as entities rather than
silently dropped, because what was withheld is part of what a release tells you.
"""

from __future__ import annotations

from pathlib import Path

from graphrag_kit.project import LexicalSpec, ProjectSpec
from projects.ufo.schema import UAP_SCHEMA

# Derived from the extraction agent prompt used to build the original graph, so
# documents added through the explorer are held to the same standard as the ones
# Document Intelligence processed.
EXTRACTION_RULES = """
Corpus-specific rules:
- Do not speculate. Extract only what the document states.
- Never assert or imply extraterrestrial origin, and never infer a cause for an
  observation. Record the description, not an explanation of it.
- Preserve the source's own uncertainty. Where a document says "reported",
  "alleged", "unidentified", "not determined" or "unknown", keep that wording in
  the `description` rather than resolving it.
- Withheld text is "[REDACTED]" and never guessed. Where a document marks a
  redaction, also emit a Redaction entity with its stated reason if one is given.
- Keep provenance: every entity you extract from a document must be reachable
  from that Document via MENTIONS, and the Document node must carry the title,
  filename, release number and classification marking exactly as printed.
- A Claim is what someone asserted, not what is true. Put the assertion in
  `text` and the asserter in `speaker_source`; if the document contains material
  that cuts against it, put that in `contradictions`.
- Dates go in `date_time` on Event, as precisely as the document allows and no
  more: '1949-04-27T20:30:00Z', '1949-04-27' or '1949'. Never invent precision.
- Emit exactly ONE Event per real-world occurrence, and hang each recorded
  sighting off it as an Observation. Measurements — shape, colour, movement,
  speed, altitude, duration — belong on the Observation, with the units the
  document uses.
- OCR noise is not an entity. These are scanned documents: ignore page
  furniture, stamp fragments and garbled character runs. If a name cannot be
  read, use '[ILLEGIBLE]' rather than a guess at it.
"""

PROJECT = ProjectSpec(
    key="ufo",
    title="UFO DOCUMENTS",
    subtitle="PURSUE releases · POLE knowledge graph",
    schema=UAP_SCHEMA,
    data_dir=Path(__file__).resolve().parent / "data",
    extraction_rules=EXTRACTION_RULES,
    rag_persona=(
        "You are a records analyst answering questions about the released UAP "
        "documents from a POLE knowledge graph (Person, Object, Location, Event, "
        "Organization, plus the Record layer that holds provenance). You report "
        "what the documents say, attributed to the document that says it. You "
        "never assert an origin or a cause for a reported observation, and you "
        "preserve the source's own uncertainty rather than resolving it."
    ),
    # --- POLE ------------------------------------------------------------
    groups={
        "PERSON": ("Person", "Witness"),
        "OBJECT": ("UAP_Object", "Vehicle", "Sensor", "MediaAsset"),
        "LOCATION": ("Location", "Facility"),
        "EVENT": ("Event", "Observation"),
        "ORGANIZATION": ("Agency",),
        "RECORD": ("Document", "Release", "CaseFile", "Claim", "Evidence", "Redaction"),
    },
    group_colors={
        "PERSON": "#6EE7FF",
        "OBJECT": "#FFB454",
        "LOCATION": "#4ADE80",
        "EVENT": "#A78BFA",
        "ORGANIZATION": "#60A5FA",
        "RECORD": "#94A3B8",
    },
    # Within a group, the second label is shaded so Witness reads as a kind of
    # Person at a glance without leaving the group's colour.
    palette={
        "Witness": "#2FB6D6",
        "Observation": "#7C6AE8",
        "Facility": "#2FA968",
        "Vehicle": "#E08A2E",
        "Sensor": "#C9762A",
        "MediaAsset": "#A86420",
        "Document": "#CBD5E1",
        "Claim": "#7E8CA3",
        "Evidence": "#66738C",
        "Redaction": "#4A5568",
        "Release": "#AEBACC",
        "CaseFile": "#8E9CB0",
    },
    # Only Person, Witness, UAP_Object, Location, Facility, Event, Agency,
    # Vehicle, Sensor, Release and CaseFile carry `name` in this graph. The rest
    # are identified by their content, which is what makes them worth showing.
    name_properties=("name", "title", "text", "filename", "number", "reason", "description"),
    date_property="date_time",
    # No evidence grading: nothing in the released documents assigns one, and
    # inventing a confidence score per entity would be exactly the speculation
    # the extraction rules forbid. Provenance does this job instead — every claim
    # is traced to the document that makes it.
    evidence_levels=(),
    # Document Intelligence built this graph; this project reads and extends it.
    # In particular, entity resolution is never run across the whole of it: DI
    # kept same-named records apart where the documents did, and a global
    # exact-name merge would silently destroy that — irreversibly.
    owns_graph=False,
    # Across documents, only these carry identity in their name. An Event or a
    # UAP_Object is named by description — "Reported object sighting", "the
    # object" — and the same description in two files is two records; a Claim
    # is its text; a Document entity titled "Mission Narrative" recurs in every
    # mission report and is a different narrative each time.
    cross_document_labels=(
        "Agency",
        "Location",
        "Facility",
        "Person",
        "Witness",
        "Vehicle",
        "Sensor",
        "Release",
        "CaseFile",
    ),
    lexical=LexicalSpec(
        # Document Intelligence embedded these chunks with a 3072-dim model of its
        # own, under `embedding`, with a vector index already on it. That index is
        # left exactly as it is: our embeddings go in a property beside it, because
        # two models' vectors in one index score ~0.5 against each other — cosine
        # zero, dressed up as a similarity — and the ranking is noise.
        embedding_property="openai_embedding",
        # DI's chunks. `graphrag-adopt` adds :Chunk alongside, which is the only
        # structural write this project makes to the existing graph.
        adopted_chunk_label="__Chunk__",
        # DI's source-file nodes. Kept distinct from the `Document` *entity*,
        # which is a released record with a title and a classification marking.
        source_label="__Document__",
        source_name_properties=("source", "path"),
        # Both conventions are read through one pattern: DI's names, and the ones
        # SimpleKGPipeline writes for documents uploaded later. That is cheaper
        # and less invasive than mirroring 1,400 relationships to rename them.
        entity_to_chunk="FROM_CHUNK|__NODE_TO_CHUNK__",
        chunk_to_source="FROM_DOCUMENT|__CHUNK_TO_DOCUMENT__",
        entity_text_properties=("name", "description", "text", "title", "filename"),
    ),
    text2cypher_examples=[
        "USER INPUT: 'Show observations where the object moved unusually or at speed.' "
        "QUERY: MATCH (e:Event)-[:HAS_OBSERVATION]->(o:Observation)"
        "-[:DESCRIBES_OBJECT]->(u:UAP_Object) "
        "WHERE coalesce(o.movement,'') <> '' OR coalesce(o.speed,'') <> '' "
        "RETURN e.name, e.date_time, o.movement, o.speed, o.shape, u.name LIMIT 50",
        "USER INPUT: 'How many sightings are in the graph?' "
        "QUERY: MATCH (e:Event) WHERE e.type CONTAINS 'Sighting' RETURN count(e) AS sightings",
        "USER INPUT: 'Which agencies investigated the most events?' "
        "QUERY: MATCH (e:Event)-[:INVESTIGATED_BY]->(a:Agency) "
        "RETURN a.name, count(e) AS events ORDER BY events DESC",
        "USER INPUT: 'What did witnesses report over New Mexico?' "
        "QUERY: MATCH (e:Event)-[:OCCURRED_AT]->(l:Location) "
        "WHERE l.name CONTAINS 'New Mexico' "
        "MATCH (e)-[:HAS_OBSERVATION]->(o:Observation)-[:REPORTED_BY]->(w:Witness) "
        "RETURN w.name, o.description, e.date_time",
        "USER INPUT: 'Which documents are still marked classified?' "
        "QUERY: MATCH (d:Document) WHERE d.classification IS NOT NULL "
        "RETURN d.title, d.classification, d.release_number, d.created_date "
        "ORDER BY d.created_date",
        "USER INPUT: 'Show the claims that have contradictions recorded.' "
        "QUERY: MATCH (c:Claim) WHERE c.contradictions IS NOT NULL "
        "RETURN c.text, c.speaker_source, c.contradictions",
        "USER INPUT: 'What shapes were reported and how often?' "
        "QUERY: MATCH (o:Observation) WHERE o.shape IS NOT NULL "
        "RETURN o.shape, count(*) AS reports ORDER BY reports DESC",
    ],
    # Four, not six. Each one is a sentence, and six of them wrap to four rows
    # of chips at laptop width — a third of the stage spent on prompts.
    example_questions=[
        "Show observations where the object moved unusually or at speed",
        "What did witnesses report over New Mexico in 1949?",
        "Which agencies investigated the most events?",
        "Where does the record contradict itself?",
    ],
)
