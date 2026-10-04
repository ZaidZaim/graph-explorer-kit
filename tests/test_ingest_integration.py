"""Optional Neo4j/APOC regressions. Every test rolls its transaction back.

Set GRAPHRAG_TEST_URI and GRAPHRAG_TEST_PASSWORD to a disposable Neo4j instance.
These tests never use the application's .env database or a model provider.
"""

import asyncio
import os
from dataclasses import replace
from pathlib import Path

import neo4j
import pytest

from graphrag_kit import ingest
from graphrag_kit.project import LexicalSpec, load_project


@pytest.fixture
def db():
    uri = os.getenv("GRAPHRAG_TEST_URI")
    if not uri:
        pytest.skip("Set GRAPHRAG_TEST_URI for disposable Neo4j/APOC integration tests")
    password = os.environ["GRAPHRAG_TEST_PASSWORD"]
    username = os.getenv("GRAPHRAG_TEST_USERNAME", "neo4j")
    database = os.getenv("GRAPHRAG_TEST_DATABASE", "neo4j")
    with neo4j.GraphDatabase.driver(uri, auth=(username, password)) as driver:
        with driver.session(database=database) as session:
            tx = session.begin_transaction()

            class TransactionDriver:
                def __getattr__(self, name):
                    # The library also sets the real driver's user-agent.
                    return getattr(driver, name)

                def execute_query(self, query, database_=None, **params):
                    result = tx.run(query, **params)
                    keys = result.keys()
                    records = list(result)
                    return records, result.consume(), keys

                def query(self, query, **params):
                    return [r.data() for r in self.execute_query(query, **params)[0]]

            try:
                # Owned-graph tests intentionally operate over all entities.
                # Refuse existing data even though the transaction is rolled back.
                assert tx.run("MATCH (n) RETURN count(n) AS n").single()["n"] == 0, (
                    "Integration tests require an empty disposable database"
                )
                yield TransactionDriver()
            finally:
                tx.rollback()


def add_entity(
    db,
    *,
    source="new.md",
    project="example",
    name="Ada",
    label="Person",
    grade="rumored",
    prop="status",
):
    return db.query(
        f"CREATE (d:Document {{source:$source, project:$project}}),"
        "(c:Chunk)-[:FROM_DOCUMENT]->(d),"
        f"(e:__Entity__:{label} {{name:$name}})-[:FROM_CHUNK]->(c) "
        "SET e += $props RETURN elementId(e) AS id",
        source=source,
        project=project,
        name=name,
        props={prop: grade},
    )[0]["id"]


def test_adopted_and_shared_records_survive_normalization_and_resolution(db):
    spec = replace(load_project(), owns_graph=False)
    foreign = add_entity(db, project=None, source="new.md")  # basename collision
    shared = add_entity(db, project=None, name="Shared")
    db.query(
        "MATCH (e) WHERE elementId(e)=$id "
        "CREATE (e)-[:FROM_CHUNK]->(:Chunk)-[:FROM_DOCUMENT]->"
        "(:Document {source:'new.md',project:'example'})",
        id=shared,
    )
    add_entity(db, grade="confirmed")
    add_entity(db, name="Shared", grade="confirmed")
    # A second own Ada really should merge with the first, without touching foreign Ada.
    add_entity(db)
    asyncio.run(ingest.resolve(spec, db, "neo4j", sources=[Path("new.md")], report=lambda _: None))
    assert db.query(
        "MATCH (e) WHERE elementId(e) IN $ids RETURN e.status AS status ORDER BY status",
        ids=[foreign, shared],
    ) == [{"status": "rumored"}, {"status": "rumored"}]
    assert db.query("MATCH (e:Person {name:'Ada'}) RETURN count(e) AS n") == [{"n": 2}]


@pytest.mark.parametrize("scope", ["run", "project", "document"])
def test_resolution_normalizes_custom_evidence_property_in_each_scope(db, scope):
    spec = replace(
        load_project(),
        owns_graph=False,
        evidence_property="confidence",
        evidence_levels=("high", "low"),
    )
    add_entity(db, prop="confidence", grade="low")
    add_entity(db, prop="confidence", grade="high")
    asyncio.run(
        ingest.resolve(
            spec,
            db,
            "neo4j",
            sources=[Path("new.md")],
            scope=scope,
            report=lambda _: None,
        )
    )
    assert db.query(
        "MATCH (e:Person) RETURN e.confidence AS grade, e.status AS old_property,"
        "e.evidence_levels AS levels"
    ) == [{"grade": "high", "old_property": None, "levels": ["high", "low"]}]


def test_rollup_does_not_combine_case_variants_labels_or_placeholders(db):
    spec = load_project()
    for name, label, grade in [
        ("Ada", "Person", "confirmed"),
        ("ada", "Person", "rumored"),
        (" Ada ", "Person", "rumored"),
        ("Ada", "Organization", "rumored"),
        ("unknown", "Person", "confirmed"),
        ("unknown", "Person", "rumored"),
    ]:
        add_entity(db, name=name, label=label, grade=grade)
    before = db.query(
        "MATCH (e:__Entity__) RETURN elementId(e) AS id, properties(e) AS props ORDER BY id"
    )
    db.execute_query(ingest.evidence_rollup_query(spec, ingest.resolution_filter(spec, None)))
    after = db.query(
        "MATCH (e:__Entity__) RETURN elementId(e) AS id, properties(e) AS props ORDER BY id"
    )
    assert [r["props"]["status"] for r in before] == [r["props"]["status"] for r in after]
    assert [r for r in before if r["props"]["name"] == "unknown"] == [
        r for r in after if r["props"]["name"] == "unknown"
    ]


@pytest.mark.parametrize("scope", ["run", "project"])
def test_cross_document_identity_rules_apply_to_rollup_too(db, scope):
    spec = replace(load_project(), owns_graph=False, cross_document_labels=("Organization",))
    ids = [
        add_entity(db, source="a.md", label="Product", name="Atlas"),
        add_entity(db, source="b.md", label="Product", name="Atlas", grade="confirmed"),
    ]
    asyncio.run(
        ingest.resolve(
            spec,
            db,
            "neo4j",
            sources=[Path("a.md"), Path("b.md")],
            scope=scope,
            report=lambda _: None,
        )
    )
    assert db.query(
        "MATCH (e) WHERE elementId(e) IN $ids RETURN e.status AS grade ORDER BY grade",
        ids=ids,
    ) == [{"grade": "confirmed"}, {"grade": "rumored"}]


def test_no_successful_sources_does_not_normalize_existing_graph(db):
    spec = load_project()
    add_entity(db)
    add_entity(db, grade="confirmed")
    asyncio.run(ingest.resolve(spec, db, "neo4j", sources=[], report=lambda _: None))
    assert db.query("MATCH (e:Person) RETURN e.status AS grade ORDER BY grade") == [
        {"grade": "confirmed"},
        {"grade": "rumored"},
    ]


def test_cleanup_removes_only_attempt_and_retains_shared_entities(db):
    # Two versions in the same project, an adopted source, and another project
    # all use the same name; only the failed attempt should disappear.
    db.query("""
        CREATE (old:Document {source:'same.md',project:'example',ingestion_id:'old'}),
               (failed:Document {source:'same.md',project:'example',ingestion_id:'failed'}),
               (:Document {source:'same.md'}),
               (:Document {source:'same.md',project:'other',ingestion_id:'failed'}),
               (a:Chunk)-[:FROM_DOCUMENT]->(old),
               (b:Chunk)-[:FROM_DOCUMENT]->(failed),
               (shared:__Entity__:Person {name:'Shared'})-[:FROM_CHUNK]->(a),
               (shared)-[:FROM_CHUNK]->(b),
               (:__Entity__:Person {name:'Only failed'})-[:FROM_CHUNK]->(b)
    """)
    assert ingest.remove_source(load_project(), db, "neo4j", ingestion_id="failed") == {
        "chunks": 1,
        "entities": 1,
    }
    assert db.query("MATCH (d:Document) RETURN count(d) AS n") == [{"n": 3}]
    assert db.query("MATCH (c:Chunk) RETURN count(c) AS n") == [{"n": 1}]
    assert db.query("MATCH (e:Person) RETURN e.name AS name") == [{"name": "Shared"}]
    assert ingest.remove_source(load_project(), db, "neo4j", ingestion_id="failed") == {
        "chunks": 0,
        "entities": 0,
    }


def test_cleanup_supports_adopted_lexical_names(db):
    spec = replace(
        load_project(),
        lexical=LexicalSpec(
            source_label="Source",
            chunk_label="Passage",
            entity_to_chunk="MENTIONED_IN",
            chunk_to_source="PART_OF",
            source_name_properties=("title",),
        ),
    )
    db.query("""
        CREATE (d:Source {title:'same.md',project:'example',ingestion_id:'failed'}),
               (c:Passage)-[:PART_OF]->(d),
               (:__Entity__:Person {name:'Ada'})-[:MENTIONED_IN]->(c),
               (:Source {title:'same.md'})
    """)
    assert ingest.remove_source(spec, db, "neo4j", ingestion_id="failed") == {
        "chunks": 1,
        "entities": 1,
    }
    assert db.query("MATCH (n) RETURN count(n) AS n") == [{"n": 1}]
