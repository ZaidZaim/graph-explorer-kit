"""Minimal example project — copy this directory to start a new demo.

Two fictional companies and their shared customer, written so the interesting
answers span documents. Small on purpose: it exists to prove the pipeline runs
end to end, not to be impressive.

    GRAPHRAG_PROJECT=projects.example
"""

from __future__ import annotations

from pathlib import Path

from neo4j_graphrag.components.schema import (
    GraphSchema,
    NodeType,
    PropertyType,
    RelationshipType,
)

from graphrag_kit.project import ProjectSpec

_STATUS = PropertyType(
    name="status",
    type="STRING",
    description="Evidence level: 'confirmed', 'reported', or 'rumored'.",
)

SCHEMA = GraphSchema(
    node_types=[
        NodeType(
            label="Person",
            description="A named individual.",
            properties=[
                PropertyType(name="name", type="STRING"),
                PropertyType(name="role", type="STRING"),
                PropertyType(name="description", type="STRING"),
                _STATUS,
            ],
        ),
        NodeType(
            label="Organization",
            description="A company, university, or public body.",
            properties=[
                PropertyType(name="name", type="STRING"),
                PropertyType(name="industry", type="STRING"),
                PropertyType(name="description", type="STRING"),
                _STATUS,
            ],
        ),
        NodeType(
            label="Product",
            description="A commercial product or platform.",
            properties=[
                PropertyType(name="name", type="STRING"),
                PropertyType(name="kind", type="STRING"),
                PropertyType(name="description", type="STRING"),
                _STATUS,
            ],
        ),
        NodeType(
            label="Location",
            description="A city, region, or country.",
            properties=[
                PropertyType(name="name", type="STRING"),
                PropertyType(name="description", type="STRING"),
                _STATUS,
            ],
        ),
    ],
    relationship_types=[
        RelationshipType(label="WORKS_AT", description="A person is employed by an organization"),
        RelationshipType(label="BASED_IN", description="An organization is based somewhere"),
        RelationshipType(label="PRODUCES", description="An organization builds or sells a product"),
        RelationshipType(label="PARTNERS_WITH", description="A stated partnership"),
        RelationshipType(label="COMPETES_WITH", description="A stated competitive relationship"),
    ],
    patterns=[
        ("Person", "WORKS_AT", "Organization"),
        ("Organization", "BASED_IN", "Location"),
        ("Organization", "PRODUCES", "Product"),
        ("Organization", "PARTNERS_WITH", "Organization"),
        ("Organization", "COMPETES_WITH", "Organization"),
    ],
    additional_node_types=False,
    additional_relationship_types=False,
    additional_patterns=False,
)

PROJECT = ProjectSpec(
    key="example",
    title="Example Corpus",
    subtitle="Two vendors and their shared customer",
    schema=SCHEMA,
    data_dir=Path(__file__).resolve().parent / "data",
    extraction_rules="""
Corpus-specific rules:
- Every entity MUST get a `status` property, one of: confirmed, reported, rumored.
  The text states it explicitly in lines like "Status: confirmed". Where a
  sentence carries no explicit status, inherit the status of its section.
""",
    rag_persona="You are an analyst answering questions about a small corpus of company briefings.",
    text2cypher_examples=[
        "USER INPUT: 'Who works at Meridian Robotics?' "
        "QUERY: MATCH (p:Person)-[:WORKS_AT]->(o:Organization) "
        "WHERE o.name CONTAINS 'Meridian' RETURN p.name, p.role",
        "USER INPUT: 'How many organizations are there?' "
        "QUERY: MATCH (o:Organization) RETURN count(o) AS organizations",
    ],
    example_questions=[
        "Which terminal runs both vendors' systems?",
        "Who leads engineering at Meridian Robotics?",
        "How are Meridian and Kestrel connected?",
        "What is only rumored rather than confirmed?",
    ],
    palette={
        "Person": "#FF5A8C",
        "Organization": "#5AA9FF",
        "Product": "#FFC857",
        "Location": "#2BD9C4",
    },
)
