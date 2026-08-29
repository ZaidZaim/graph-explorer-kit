"""Graph schema handed to the extraction LLM.

An explicit schema is the single biggest lever on extraction quality: it tells the
LLM which labels are allowed, which properties to fill, and which triples are
legal. Without it (`schema="FREE"` / `"EXTRACTED"`) the model invents labels and
the graph fragments.
"""

from __future__ import annotations

from neo4j_graphrag.components.schema import (
    GraphSchema,
    NodeType,
    PropertyType,
    RelationshipType,
)

DEMO_SCHEMA = GraphSchema(
    node_types=[
        NodeType(
            label="Person",
            description="A named individual mentioned in the source documents.",
            properties=[
                PropertyType(name="name", type="STRING", description="Full name"),
                PropertyType(name="role", type="STRING", description="Job title or role"),
            ],
        ),
        NodeType(
            label="Organization",
            description="A company, university, research lab, or public body.",
            properties=[
                PropertyType(name="name", type="STRING", description="Official name"),
                PropertyType(name="industry", type="STRING"),
            ],
        ),
        NodeType(
            label="Product",
            description="A commercial product, platform, or robot model.",
            properties=[
                PropertyType(name="name", type="STRING"),
                PropertyType(name="category", type="STRING"),
            ],
        ),
        NodeType(
            label="Technology",
            description="A technique, standard, or component used to build a product.",
            properties=[
                PropertyType(name="name", type="STRING"),
            ],
        ),
        NodeType(
            label="Location",
            description="A city, region, or country.",
            properties=[
                PropertyType(name="name", type="STRING"),
            ],
        ),
    ],
    relationship_types=[
        RelationshipType(label="WORKS_AT", description="A person is employed by an organization."),
        RelationshipType(label="LOCATED_IN", description="An organization is based in a location."),
        RelationshipType(label="PRODUCES", description="An organization builds or sells a product"),
        RelationshipType(label="USES", description="A product is built on a technology."),
        RelationshipType(
            label="PARTNERS_WITH",
            description="Two organizations have a stated commercial or research partnership.",
        ),
        RelationshipType(
            label="COMPETES_WITH",
            description="Two organizations are described as competitors.",
        ),
    ],
    patterns=[
        ("Person", "WORKS_AT", "Organization"),
        ("Organization", "LOCATED_IN", "Location"),
        ("Organization", "PRODUCES", "Product"),
        ("Product", "USES", "Technology"),
        ("Organization", "PARTNERS_WITH", "Organization"),
        ("Organization", "COMPETES_WITH", "Organization"),
    ],
    # Refuse anything outside the lists above — keeps the graph queryable.
    additional_node_types=False,
    additional_relationship_types=False,
    additional_patterns=False,
)

#: Entity labels produced by extraction (i.e. everything except the lexical layer).
ENTITY_LABELS = [node.label for node in DEMO_SCHEMA.node_types]
