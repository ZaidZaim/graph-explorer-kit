"""POLE+O graph schema for the GTA VI corpus. See the package docstring for why."""
from __future__ import annotations

from neo4j_graphrag.components.schema import (
    GraphSchema,
    NodeType,
    PropertyType,
    RelationshipType,
)

_STATUS = PropertyType(
    name="status",
    type="STRING",
    description=(
        "Evidence level. 'confirmed' = stated by Rockstar, Take-Two, or a court "
        "record. 'reported' = credible press reporting. 'rumored' = fan "
        "speculation, datamining, or unverified leak chatter."
    ),
)

POLE_SCHEMA = GraphSchema(
    node_types=[
        NodeType(
            label="Person",
            description=(
                "A named individual: in-game characters, and real people such as "
                "executives, developers, and convicted hackers."
            ),
            properties=[
                PropertyType(name="name", type="STRING", description="Full name"),
                PropertyType(
                    name="role",
                    type="STRING",
                    description="e.g. 'protagonist', 'CEO', 'hacker', 'record label owner'",
                ),
                PropertyType(
                    name="fictional",
                    type="BOOLEAN",
                    description="True for in-game characters, false for real people",
                ),
                PropertyType(name="description", type="STRING"),
                _STATUS,
            ],
        ),
        NodeType(
            label="Object",
            description=(
                "A thing: a trailer or marketing asset, a hardware platform, a game "
                "edition or bonus pack, a vehicle, or an item of evidence in a criminal case."
            ),
            properties=[
                PropertyType(name="name", type="STRING"),
                PropertyType(
                    name="kind",
                    type="STRING",
                    description="e.g. 'trailer', 'platform', 'edition', 'vehicle', 'evidence'",
                ),
                PropertyType(name="description", type="STRING"),
                _STATUS,
            ],
        ),
        NodeType(
            label="Location",
            description=(
                "A place: fictional in-game regions and cities, and real-world places "
                "relevant to the game's production or the criminal case around it."
            ),
            properties=[
                PropertyType(name="name", type="STRING"),
                PropertyType(
                    name="fictional",
                    type="BOOLEAN",
                    description="True for in-game places, false for real-world places",
                ),
                PropertyType(
                    name="inspiration",
                    type="STRING",
                    description="Real-world place the fictional location is modelled on",
                ),
                PropertyType(name="description", type="STRING"),
                _STATUS,
            ],
        ),
        NodeType(
            label="Event",
            description=(
                "Something that happened at a point in time: a trailer premiere, a "
                "delay announcement, a hack, a court sentencing, preorders opening."
            ),
            properties=[
                PropertyType(name="name", type="STRING"),
                PropertyType(
                    name="date",
                    type="STRING",
                    description=(
                        "ISO-8601 where known, e.g. '2026-08-27'; "
                        "otherwise a month or year"
                    ),
                ),
                PropertyType(
                    name="kind",
                    type="STRING",
                    description="e.g. 'announcement', 'release', 'delay', 'crime', 'legal'",
                ),
                PropertyType(name="description", type="STRING"),
                _STATUS,
            ],
        ),
        NodeType(
            label="Organization",
            description=(
                "A company, label, agency, criminal group, or in-game faction: "
                "Rockstar Games, Take-Two, Lapsus$, Only Raw Records, street gangs."
            ),
            properties=[
                PropertyType(name="name", type="STRING"),
                PropertyType(
                    name="kind",
                    type="STRING",
                    description="e.g. 'developer', 'publisher', 'record label', 'gang', 'platform'",
                ),
                PropertyType(
                    name="fictional",
                    type="BOOLEAN",
                    description="True for in-game organizations, false for real companies",
                ),
                PropertyType(name="description", type="STRING"),
                _STATUS,
            ],
        ),
    ],
    relationship_types=[
        RelationshipType(
            label="INVOLVED_IN",
            description="A person, organization, or object took part in or featured in an event",
            properties=[
                PropertyType(name="role", type="STRING", description="How they were involved"),
            ],
        ),
        RelationshipType(label="MEMBER_OF", description="A person belongs to an organization"),
        RelationshipType(
            label="ASSOCIATE_OF",
            description="Two people are connected — partners, friends, family, accomplices",
            properties=[PropertyType(name="nature", type="STRING")],
        ),
        RelationshipType(
            label="APPEARS_IN", description="A person or organization is present at a location"
        ),
        RelationshipType(
            label="BASED_IN",
            description="An organization is headquartered somewhere",
        ),
        RelationshipType(label="OCCURRED_AT", description="An event happened at a location"),
        RelationshipType(
            label="PRECEDED_BY", description="An event follows an earlier event in a timeline"
        ),
        RelationshipType(
            label="PART_OF",
            description="A location or organization sits inside another",
        ),
        RelationshipType(label="OWNS", description="A person or organization owns something"),
        RelationshipType(
            label="DEPICTS",
            description="An object such as a trailer shows a location",
        ),
    ],
    patterns=[
        ("Person", "INVOLVED_IN", "Event"),
        ("Organization", "INVOLVED_IN", "Event"),
        ("Object", "INVOLVED_IN", "Event"),
        ("Person", "MEMBER_OF", "Organization"),
        ("Person", "ASSOCIATE_OF", "Person"),
        ("Person", "APPEARS_IN", "Location"),
        ("Organization", "APPEARS_IN", "Location"),
        ("Organization", "BASED_IN", "Location"),
        ("Event", "OCCURRED_AT", "Location"),
        ("Event", "PRECEDED_BY", "Event"),
        ("Location", "PART_OF", "Location"),
        ("Organization", "PART_OF", "Organization"),
        ("Person", "OWNS", "Object"),
        ("Organization", "OWNS", "Object"),
        ("Organization", "OWNS", "Organization"),
        ("Object", "DEPICTS", "Location"),
    ],
    # Hold the model to POLE+O. Without this the extractor invents labels like
    # "Game" and "Feature" and the four-quadrant structure stops being useful.
    additional_node_types=False,
    additional_relationship_types=False,
    additional_patterns=False,
)

