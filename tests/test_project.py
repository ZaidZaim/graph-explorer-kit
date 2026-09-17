"""The engine/corpus seam: ProjectSpec, LexicalSpec, and the safety it carries.

The interesting cases here are the ones that protect data. `owns_graph` decides
whether entity resolution is allowed to run across a whole graph, and a
relationship field holding a read-time alternation must never be written as-is.
"""

from __future__ import annotations

from graphrag_kit.ingest import lexical_graph_config, resolution_filter
from graphrag_kit.project import LexicalSpec, load_project


def test_example_project_loads_and_every_label_has_a_colour():
    spec = load_project("projects.example")
    assert spec.labels
    colors = spec.label_colors
    assert set(colors) == set(spec.labels)
    assert all(value.startswith("#") or value.startswith("rgb") for value in colors.values())


def test_a_project_without_groups_is_still_valid():
    # The explorer falls back to a flat label list; nothing here should require
    # a grouping to exist.
    spec = load_project("projects.example")
    if not spec.groups:
        assert spec.ungrouped_labels() == spec.labels
        assert all(spec.group_of(label) is None for label in spec.labels)


def test_write_relationship_names_take_the_first_alternative():
    # The read pattern matches both conventions; a write has to pick one, and
    # writing the literal "A|B" would create a relationship type called "A|B".
    lex = LexicalSpec(
        entity_to_chunk="FROM_CHUNK|__NODE_TO_CHUNK__",
        chunk_to_source="FROM_DOCUMENT|__CHUNK_TO_DOCUMENT__",
    )
    assert lex.entity_to_chunk_write == "FROM_CHUNK"
    assert lex.chunk_to_source_write == "FROM_DOCUMENT"


def test_write_names_pass_a_plain_relationship_through():
    lex = LexicalSpec()
    assert lex.entity_to_chunk_write == "FROM_CHUNK"
    assert lex.chunk_to_source_write == "FROM_DOCUMENT"


def test_the_writer_is_configured_from_the_lexical_spec():
    spec = load_project("projects.example")
    config = lexical_graph_config(spec)
    lex = spec.lexical
    assert config.document_node_label == lex.source_label
    assert config.chunk_node_label == lex.chunk_label
    assert config.chunk_embedding_property == lex.embedding_property
    # Never the alternation: this one goes into a CREATE.
    assert "|" not in config.node_to_chunk_relationship_type
    assert "|" not in config.chunk_to_document_relationship_type


def test_resolution_is_unscoped_only_where_the_project_owns_the_graph():
    owner = load_project("projects.example")
    assert owner.owns_graph is True
    assert resolution_filter(owner, ["a.md"]) is None


def test_resolution_is_scoped_for_an_adopted_graph():
    import dataclasses

    adopted = dataclasses.replace(load_project("projects.example"), owns_graph=False)
    clause = resolution_filter(adopted, ["new.md"])
    assert clause is not None
    assert clause.startswith("WHERE EXISTS {")
    # It has to confine the merge to the document just ingested — an unscoped
    # run merges same-named records the other tool kept apart, irreversibly.
    assert "'new.md'" in clause
    assert adopted.lexical.entity_to_chunk in clause
