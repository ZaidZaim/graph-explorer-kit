"""UAP records schema, as the graph actually holds it.

Written against the live `ufo-us-DI` instance rather than from first principles:
every label, property and relationship below was observed in the graph that
Neo4j Document Intelligence built from the war.gov/ufo releases. Keeping the
schema honest to the data matters twice over — Text2CypherRetriever generates
queries against it, and the extractor for newly uploaded documents is held to
it, so a property that does not exist in the graph becomes a query that returns
nothing and an extraction that writes a field no query will ever read.

POLE grouping lives in the ProjectSpec (see __init__.py), not here: the labels
are the domain's own, and POLE is the lens placed over them.
"""

from __future__ import annotations

from neo4j_graphrag.components.schema import (
    GraphSchema,
    NodeType,
    PropertyType,
    RelationshipType,
)

#: Free text carried by most entities. Document Intelligence wrote it on some
#: labels and not others; it is declared everywhere it was observed.
_DESCRIPTION = PropertyType(
    name="description",
    type="STRING",
    description="What the source says about this entity, in the source's own terms.",
)

_TYPE = PropertyType(
    name="type",
    type="STRING",
    description="Sub-kind as the document words it, not a controlled vocabulary.",
)

UAP_SCHEMA = GraphSchema(
    node_types=[
        # --- people -------------------------------------------------------
        NodeType(
            label="Person",
            description=(
                "A named individual who is not primarily a witness: officers, "
                "investigators, officials, correspondents, signatories."
            ),
            properties=[
                PropertyType(name="name", type="STRING", description="Fullest name form used"),
                PropertyType(
                    name="role",
                    type="STRING",
                    description="e.g. 'Commanding Officer', 'Attache', 'investigator'",
                ),
                PropertyType(
                    name="affiliation",
                    type="STRING",
                    description="Unit, agency or organisation the document ties them to",
                ),
                _DESCRIPTION,
            ],
        ),
        NodeType(
            label="Witness",
            description=(
                "A person whose observation is recorded. Separate from Person "
                "because testimony is the load-bearing evidence in this corpus."
            ),
            properties=[
                PropertyType(
                    name="name",
                    type="STRING",
                    description="Name, rank and serial as printed, or '[REDACTED]'",
                ),
                _DESCRIPTION,
            ],
        ),
        # --- objects ------------------------------------------------------
        NodeType(
            label="UAP_Object",
            description=(
                "The reported object itself. Never assert an origin for it: record "
                "only what the document describes."
            ),
            properties=[
                PropertyType(name="name", type="STRING", description="How the document names it"),
                PropertyType(
                    name="type",
                    type="STRING",
                    description="e.g. 'fireball', 'disc', 'flare', 'Sphere', 'Unknown'",
                ),
                _DESCRIPTION,
            ],
        ),
        NodeType(
            label="Vehicle",
            description="A conventional craft or vehicle: aircraft, ship, balloon, rocket.",
            properties=[
                PropertyType(name="name", type="STRING"),
                _TYPE,
            ],
        ),
        NodeType(
            label="Sensor",
            description="An instrument that produced a measurement: radar, camera, theodolite.",
            properties=[
                PropertyType(name="name", type="STRING"),
                _TYPE,
            ],
        ),
        NodeType(
            label="MediaAsset",
            description="A photograph, film, plate or recording attached to the record.",
            properties=[
                PropertyType(name="filename", type="STRING", description="Asset name or number"),
                _TYPE,
            ],
        ),
        # --- places -------------------------------------------------------
        NodeType(
            label="Location",
            description="Anywhere a sighting, launch or investigation is placed.",
            properties=[
                PropertyType(name="name", type="STRING"),
                PropertyType(
                    name="type", type="STRING", description="e.g. 'city', 'state', 'test range'"
                ),
                PropertyType(name="country", type="STRING"),
            ],
        ),
        NodeType(
            label="Facility",
            description="A named installation: air base, laboratory, observatory, plant.",
            properties=[
                PropertyType(name="name", type="STRING"),
                _TYPE,
            ],
        ),
        # --- events -------------------------------------------------------
        NodeType(
            label="Event",
            description=(
                "Something that happened at a point in time: a sighting, a test, a "
                "briefing, an investigation opening."
            ),
            properties=[
                PropertyType(name="name", type="STRING"),
                PropertyType(
                    name="date_time",
                    type="STRING",
                    description=(
                        "When it happened, as precisely as the document allows: "
                        "'1949-04-27T20:30:00Z', '1949-04-27', or '1949'. Never invent "
                        "precision the source does not give."
                    ),
                ),
                PropertyType(
                    name="type",
                    type="STRING",
                    description="e.g. 'UAP Sighting', 'Investigation', 'Test Launch'",
                ),
                _DESCRIPTION,
            ],
        ),
        NodeType(
            label="Observation",
            description=(
                "One recorded act of observing — the measurable core of a sighting. "
                "Hangs off an Event and points at the object seen."
            ),
            properties=[
                PropertyType(
                    name="description",
                    type="STRING",
                    description="What was seen, in the observer's words where possible",
                ),
                PropertyType(name="shape", type="STRING"),
                PropertyType(name="color", type="STRING"),
                PropertyType(name="size", type="STRING"),
                PropertyType(name="count", type="STRING", description="How many objects"),
                PropertyType(name="movement", type="STRING", description="Described motion"),
                PropertyType(name="speed", type="STRING", description="As stated, with its unit"),
                PropertyType(
                    name="altitude", type="STRING", description="As stated, with its unit"
                ),
                PropertyType(name="duration", type="STRING"),
                PropertyType(name="luminosity", type="STRING"),
                PropertyType(name="relative_direction", type="STRING"),
                PropertyType(name="relative_distance", type="STRING"),
            ],
        ),
        # --- organisations ------------------------------------------------
        NodeType(
            label="Agency",
            description=(
                "A government body, military unit, contractor or institution: USAF, "
                "CIA, ODNI, AMC, Sandia, Project BLUE BOOK."
            ),
            properties=[
                PropertyType(name="name", type="STRING"),
                PropertyType(name="country", type="STRING"),
            ],
        ),
        # --- the record itself --------------------------------------------
        NodeType(
            label="Document",
            description=(
                "A released document as a subject in its own right: its title, file "
                "number, markings and dates. Provenance is a first-class entity here."
            ),
            properties=[
                PropertyType(name="title", type="STRING", description="Title as printed"),
                PropertyType(
                    name="filename",
                    type="STRING",
                    description=(
                        "Released filename, or the file number where that identifies it"
                    ),
                ),
                PropertyType(name="type", type="STRING", description="e.g. 'memorandum', 'report'"),
                PropertyType(name="release_number", type="STRING"),
                PropertyType(
                    name="created_date", type="STRING", description="ISO-8601 where known"
                ),
                PropertyType(name="released_date", type="STRING"),
                PropertyType(name="declassification_date", type="STRING"),
                PropertyType(
                    name="classification",
                    type="STRING",
                    description=(
                        "Marking as printed: 'CLASSIFIED', 'DECLASSIFIED', "
                        "'CONFIDENTIAL', 'UNCLASSIFIED'"
                    ),
                ),
                PropertyType(name="summary", type="STRING"),
                PropertyType(name="ocr_language", type="STRING"),
                PropertyType(name="timestamp_in_document", type="STRING"),
            ],
        ),
        NodeType(
            label="Release",
            description="A war.gov/ufo release tranche that a document was published in.",
            properties=[
                PropertyType(name="number", type="STRING", description="Release or tranche number"),
                PropertyType(name="name", type="STRING"),
                PropertyType(name="date", type="STRING"),
            ],
        ),
        NodeType(
            label="CaseFile",
            description="A named case or project file grouping several documents.",
            properties=[PropertyType(name="name", type="STRING")],
        ),
        NodeType(
            label="Claim",
            description=(
                "An assertion the record contains, kept separate from the facts it "
                "asserts so that who said what stays visible — and so a claim can be "
                "contradicted without the contradiction being resolved."
            ),
            properties=[
                PropertyType(name="text", type="STRING", description="The claim as stated"),
                PropertyType(
                    name="speaker_source",
                    type="STRING",
                    description="Who made it, or '[REDACTED]' / 'unknown'",
                ),
                PropertyType(
                    name="contradictions",
                    type="STRING",
                    description="Anything in the record that cuts against it",
                ),
                PropertyType(name="evidence_description", type="STRING"),
            ],
        ),
        NodeType(
            label="Evidence",
            description="Physical or documentary material offered in support of a claim.",
            properties=[
                PropertyType(name="description", type="STRING"),
                _TYPE,
            ],
        ),
        NodeType(
            label="Redaction",
            description=(
                "A withheld passage. Recorded as an entity on purpose: what was "
                "removed, and why, is part of what the release tells you."
            ),
            properties=[
                PropertyType(name="reason", type="STRING", description="Exemption cited, if any"),
                PropertyType(name="date", type="STRING"),
            ],
        ),
    ],
    relationship_types=[
        RelationshipType(
            label="MENTIONS", description="A document names an entity anywhere in its text"
        ),
        RelationshipType(
            label="DESCRIBES_EVENT", description="A document is an account of an event"
        ),
        RelationshipType(
            label="HAS_OBSERVATION", description="An event includes a recorded observation"
        ),
        RelationshipType(
            label="DESCRIBES_OBJECT", description="An observation is of this reported object"
        ),
        RelationshipType(
            label="REPORTED_BY", description="An observation was reported by this witness"
        ),
        RelationshipType(
            label="CAPTURED_BY", description="An observation was recorded by this sensor"
        ),
        RelationshipType(label="OCCURRED_AT", description="An event happened at this location"),
        RelationshipType(
            label="INVESTIGATED_BY", description="An event was investigated by this agency"
        ),
        RelationshipType(label="CREATED_BY", description="An agency authored a document"),
        RelationshipType(
            label="PART_OF_RELEASE", description="A document was published in this release"
        ),
        RelationshipType(label="SUPPORTED_BY", description="A claim rests on this evidence"),
        RelationshipType(
            label="SAME_AS",
            description="Two records are stated by the source to be the same thing",
        ),
        RelationshipType(
            label="POSSIBLY_SAME_AS",
            description=(
                "Two records may be the same thing. Use only where the source itself "
                "raises the possibility — never to assert an identification."
            ),
        ),
    ],
    patterns=[
        # Provenance: everything is reachable from the document that says it.
        ("Document", "MENTIONS", "Person"),
        ("Document", "MENTIONS", "Witness"),
        ("Document", "MENTIONS", "Agency"),
        ("Document", "MENTIONS", "Location"),
        ("Document", "MENTIONS", "Facility"),
        ("Document", "MENTIONS", "Event"),
        ("Document", "MENTIONS", "Observation"),
        ("Document", "MENTIONS", "UAP_Object"),
        ("Document", "MENTIONS", "Vehicle"),
        ("Document", "MENTIONS", "Sensor"),
        ("Document", "MENTIONS", "MediaAsset"),
        ("Document", "MENTIONS", "Claim"),
        ("Document", "MENTIONS", "Evidence"),
        ("Document", "MENTIONS", "Redaction"),
        ("Document", "DESCRIBES_EVENT", "Event"),
        ("Document", "PART_OF_RELEASE", "Release"),
        ("Document", "PART_OF_RELEASE", "CaseFile"),
        ("Agency", "CREATED_BY", "Document"),
        # The sighting chain: event -> observation -> object, with who and what saw it.
        ("Event", "HAS_OBSERVATION", "Observation"),
        ("Observation", "DESCRIBES_OBJECT", "UAP_Object"),
        ("Observation", "REPORTED_BY", "Witness"),
        ("Observation", "CAPTURED_BY", "Sensor"),
        ("Event", "OCCURRED_AT", "Location"),
        ("Event", "INVESTIGATED_BY", "Agency"),
        # Claims and their support.
        ("Claim", "SUPPORTED_BY", "Evidence"),
        # Identity, asserted and merely suspected.
        ("UAP_Object", "POSSIBLY_SAME_AS", "UAP_Object"),
        ("UAP_Object", "SAME_AS", "UAP_Object"),
        ("Event", "POSSIBLY_SAME_AS", "Event"),
        ("Event", "SAME_AS", "Event"),
        ("Person", "SAME_AS", "Witness"),
    ],
    # Hold the extractor to the labels the graph already uses. Without this it
    # invents "Sighting" and "Phenomenon" next to Event and Observation, and the
    # POLE grouping — along with every saved query — stops covering the graph.
    additional_node_types=False,
    additional_relationship_types=False,
    additional_patterns=False,
)
