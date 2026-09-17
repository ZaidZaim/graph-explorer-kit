"""The Cypher fragments the engine builds from a ProjectSpec.

These are strings spliced into queries, and a mistake in one is not a type
error — it is a query that runs and quietly returns the wrong thing, or a
half-typed search box that 500s. Hence tests over the fragments themselves,
which need no database.
"""

from __future__ import annotations

from neo4j_graphrag.components.schema import GraphSchema, NodeType, PropertyType

from graphrag_kit.cypher import (
    evidence_expr,
    fact_expr,
    label_expr,
    lucene_escape,
    name_expr,
    source_name_expr,
)
from graphrag_kit.project import LexicalSpec, ProjectSpec

SCHEMA = GraphSchema(
    node_types=[
        NodeType(label="Person", properties=[PropertyType(name="name", type="STRING")]),
        NodeType(label="Claim", properties=[PropertyType(name="text", type="STRING")]),
    ],
    relationship_types=[],
    patterns=[],
)


def spec(**overrides) -> ProjectSpec:
    defaults = dict(
        key="t",
        title="T",
        subtitle="",
        schema=SCHEMA,
        data_dir="/tmp",
        name_properties=("name", "title", "text"),
    )
    return ProjectSpec(**{**defaults, **overrides})


def test_label_expr_filters_the_reserved_labels():
    expr = label_expr("n")
    assert "labels(n)" in expr
    assert "'__Entity__'" in expr and "'__KGBuilder__'" in expr


def test_name_expr_prefers_properties_in_order_and_truncates_prose():
    expr = name_expr("n", spec())
    # `text` is prose, so it is excerpted rather than used whole; `name` is
    # already a short label and is used as-is.
    assert expr.index("n.name") < expr.index("n.title") < expr.index("left(n.text")
    assert expr == "coalesce(n.name, n.title, left(n.text, 80))"


def test_evidence_expr_is_null_when_the_corpus_has_no_grading():
    assert evidence_expr("n", spec(evidence_levels=())) == "null"


def test_evidence_expr_falls_back_to_the_weakest_level():
    expr = evidence_expr("n", spec(evidence_levels=("high", "low")))
    assert expr == "coalesce(n.status, 'low')"


def test_fact_expr_omits_the_grading_tag_for_an_ungraded_corpus():
    ungraded = fact_expr("a", "r", "b", spec(evidence_levels=()))
    graded = fact_expr("a", "r", "b", spec(evidence_levels=("confirmed",)))
    assert "type(r)" in ungraded
    assert "coalesce" not in ungraded.replace("coalesce(a.name", "").replace(
        "coalesce(b.name", "")
    assert "coalesce(b.status" in graded


def test_source_name_expr_follows_the_lexical_spec():
    expr = source_name_expr("d", spec(lexical=LexicalSpec(source_name_properties=("s", "p"))))
    assert expr == "coalesce(d.s, d.p)"


def test_lucene_escape_leaves_ordinary_words_alone():
    assert lucene_escape("New Mexico") == "New Mexico"


def test_lucene_escape_neutralises_operators():
    # A half-typed query must be a search, not a syntax error: the explorer
    # searches on every keystroke.
    assert lucene_escape("(x:y)") == r"\(x\:y\)"
    assert lucene_escape("a && b") == r"a \&\& b"
    assert lucene_escape("  padded  ") == "padded"
