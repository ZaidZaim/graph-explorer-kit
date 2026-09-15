"""Cypher fragments built from the active project.

Three things vary per corpus and appear in nearly every query the engine runs:
what an entity is *called*, which label to show it under, and how the lexical
layer is named. Generating those fragments in one place keeps the difference
between two corpora down to a ProjectSpec, and stops the same coalesce chain
being spelled slightly differently in five files.

Everything here returns a Cypher expression as a string. Nothing here
interpolates user input — only names taken from the project spec. The one
function that *does* touch user input is `lucene_escape`, which escapes it.
"""

from __future__ import annotations

import re

from graphrag_kit.project import RESERVED_LABELS, ProjectSpec

#: Longest display name taken from a free-text property. A Claim's identity is
#: its text, but a whole paragraph is not a node label.
NAME_EXCERPT = 80


def _reserved_list() -> str:
    return "[" + ", ".join(f"'{label}'" for label in RESERVED_LABELS) + "]"


def label_expr(var: str) -> str:
    """The node's schema label — the first one that is not reserved.

    Label order on a node is not guaranteed, so the reserved ones are filtered
    rather than skipped by position.
    """
    return f"head([l IN labels({var}) WHERE NOT l IN {_reserved_list()}])"


def name_expr(var: str, spec: ProjectSpec, excerpt: int = NAME_EXCERPT) -> str:
    """Display name for an entity, from the first property it actually has.

    Long free text is truncated: a Claim is identified by what it says, and the
    first line of it is the readable form of that.
    """
    parts = []
    for prop in spec.name_properties:
        # `description` and `text` are prose; the rest are already short labels.
        if prop in ("text", "description", "summary"):
            parts.append(f"left({var}.{prop}, {excerpt})")
        else:
            parts.append(f"{var}.{prop}")
    return f"coalesce({', '.join(parts)})"


def source_name_expr(var: str, spec: ProjectSpec) -> str:
    """Display name for a source file."""
    props = spec.lexical.source_name_properties
    return f"coalesce({', '.join(f'{var}.{p}' for p in props)})"


def evidence_expr(var: str, spec: ProjectSpec) -> str:
    """The entity's evidence level, or a literal null where the corpus has none."""
    if not spec.grades_evidence:
        return "null"
    weakest = spec.evidence_levels[-1]
    return f"coalesce({var}.{spec.evidence_property}, '{weakest}')"


def fact_expr(subject: str, rel: str, obj: str, spec: ProjectSpec) -> str:
    """One graph fact rendered for an LLM: `A -[REL]-> B`, with B's grading.

    This is what turns an edge into something a language model can use. Without
    the evidence tag a reader cannot tell an asserted fact from a rumoured one;
    where the corpus has no grading the tag is left off entirely rather than
    printed as "unrated" on every line, which reads like missing data.
    """
    arrow = f"{name_expr(subject, spec)} + ' -[' + type({rel}) + ']-> ' + {name_expr(obj, spec)}"
    if not spec.grades_evidence:
        return arrow
    return f"{arrow} + ' (' + {evidence_expr(obj, spec)} + ')'"


#: Lucene operators that make a half-typed search term a syntax error rather
#: than a search. The explorer searches on every keystroke and the agent passes
#: entity names straight through, so an unescaped ":" or "(" must not be a 500.
LUCENE_SPECIAL = re.compile(r'([+\-!(){}\[\]^"~*?:\\/]|&&|\|\|)')


def lucene_escape(term: str) -> str:
    """Escape a user-supplied term for a fulltext index query."""
    return LUCENE_SPECIAL.sub(r"\\\1", term.strip())
