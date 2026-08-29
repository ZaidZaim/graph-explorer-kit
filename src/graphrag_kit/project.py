"""Project specification — the seam between the reusable engine and one corpus.

Everything in `graphrag_kit` is domain-agnostic. Everything that makes a demo
*about something* lives in a project package under `projects/`, which exposes a
single `PROJECT: ProjectSpec`.

Select one with the GRAPHRAG_PROJECT environment variable:

    GRAPHRAG_PROJECT=projects.vicecity

To start a new demo, copy `projects/example`, swap the schema and the corpus,
and point GRAPHRAG_PROJECT at it. No engine code changes.
"""

from __future__ import annotations

import importlib
import os
from dataclasses import dataclass, field
from functools import cache
from pathlib import Path

from neo4j_graphrag.components.schema import GraphSchema

DEFAULT_PROJECT = "projects.example"

#: Evidence levels, strongest first. The order is the precedence used when an
#: entity is asserted at more than one level across the corpus.
DEFAULT_EVIDENCE_LEVELS = ("confirmed", "reported", "rumored")


@dataclass(frozen=True)
class ProjectSpec:
    """Everything the engine needs to know about one corpus."""

    key: str
    title: str
    subtitle: str
    schema: GraphSchema
    data_dir: Path

    #: Extra rules appended to the extraction prompt. This is where corpus-specific
    #: instructions go ("status is stated explicitly as Status: confirmed", etc.).
    extraction_rules: str = ""

    #: How the answering model should describe itself.
    rag_persona: str = "You are an analyst answering questions from a knowledge graph."

    #: Few-shot NL->Cypher pairs for Text2CypherRetriever.
    text2cypher_examples: list[str] = field(default_factory=list)

    #: Seed questions surfaced as chips in the explorer UI.
    example_questions: list[str] = field(default_factory=list)

    #: Node colour per schema label, used by the explorer.
    palette: dict[str, str] = field(default_factory=dict)

    evidence_levels: tuple[str, ...] = DEFAULT_EVIDENCE_LEVELS

    @property
    def labels(self) -> list[str]:
        return [node.label for node in self.schema.node_types]


@cache
def load_project(dotted_path: str | None = None) -> ProjectSpec:
    """Import the configured project package and return its PROJECT."""
    target = dotted_path or os.getenv("GRAPHRAG_PROJECT", DEFAULT_PROJECT)
    try:
        module = importlib.import_module(target)
    except ImportError as exc:
        raise ImportError(
            f"Could not import project {target!r}. Set GRAPHRAG_PROJECT to a "
            f"package exposing PROJECT, e.g. 'projects.vicecity'."
        ) from exc
    try:
        spec = module.PROJECT
    except AttributeError as exc:
        raise AttributeError(f"{target!r} does not define PROJECT") from exc
    if not isinstance(spec, ProjectSpec):
        raise TypeError(f"{target}.PROJECT must be a ProjectSpec, got {type(spec)!r}")
    return spec
