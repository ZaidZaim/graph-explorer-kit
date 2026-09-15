"""Project specification — the seam between the reusable engine and one corpus.

Everything in `graphrag_kit` is domain-agnostic. Everything that makes a demo
*about something* lives in a project package under `projects/`, which exposes a
single `PROJECT: ProjectSpec`.

Select one with the GRAPHRAG_PROJECT environment variable:

    GRAPHRAG_PROJECT=projects.example

To start a new demo, copy `projects/example`, swap the schema and the corpus,
and point GRAPHRAG_PROJECT at it. No engine code changes.

Three things beyond the schema are worth knowing about:

`groups` places a lens over the labels — POLE (Person, Object, Location, Event)
in the projects here. The engine groups filters and colours nodes by it, so the
model the analyst is taught is the model the picture shows.

`name_properties` exists because not every entity has a `name`. A Claim is
identified by its text and a Document by its title, and a graph that renders
both as "(unnamed)" is useless.

`lexical` describes how the chunk/embedding layer is *named* in this particular
graph. The defaults are what `neo4j-graphrag` writes itself; a graph built by
another tool — Neo4j Document Intelligence, say — uses its own names, and this
is what lets the engine read it without rewriting anyone's data.
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
#: entity is asserted at more than one level across the corpus. A project whose
#: corpus carries no evidence grading sets this to () and the engine drops the
#: facet rather than inventing a level for every node.
DEFAULT_EVIDENCE_LEVELS = ("confirmed", "reported", "rumored")

RESERVED_LABELS = ("__Entity__", "__KGBuilder__")


@dataclass(frozen=True)
class LexicalSpec:
    """How the lexical layer — chunks, embeddings, source files — is named.

    Defaults match what `SimpleKGPipeline` writes. Override them to point the
    engine at a graph some other tool built.
    """

    #: Label on chunk nodes. A vector index is fixed to exactly one label, so
    #: this is the one label every chunk must end up carrying.
    chunk_label: str = "Chunk"

    #: Label the chunks already carry in a graph some other tool built.
    #: `graphrag-adopt` adds `chunk_label` alongside it — the one write needed to
    #: put a vector index over chunks this engine did not create.
    adopted_chunk_label: str | None = None

    #: Label on source-file nodes. Deliberately separate from any domain label:
    #: in the UAP corpus `Document` is an extracted *entity* with a title and
    #: classification markings, which is not the same thing as the file on disk.
    source_label: str = "Document"

    #: Properties to try, in order, for a source file's display name.
    source_name_properties: tuple[str, ...] = ("source", "path")

    #: Chunk property holding the embedding vector. Worth overriding when the
    #: graph already has an `embedding` written by a different model: two models
    #: cannot share one property, and a vector index is fixed to one width.
    embedding_property: str = "embedding"

    #: Chunk property holding the text.
    text_property: str = "text"

    #: (entity)-[:?]->(chunk). Cypher alternation is allowed, so a graph with
    #: two conventions can be read through one pattern.
    entity_to_chunk: str = "FROM_CHUNK"

    #: (chunk)-[:?]->(source file).
    chunk_to_source: str = "FROM_DOCUMENT"

    #: Entity properties worth putting in the explorer's fulltext index.
    entity_text_properties: tuple[str, ...] = ("name", "description")

    @property
    def entity_to_chunk_write(self) -> str:
        """The single relationship type to *write*. Reading may match several."""
        return self.entity_to_chunk.split("|")[0]

    @property
    def chunk_to_source_write(self) -> str:
        return self.chunk_to_source.split("|")[0]


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

    #: Node colour per schema label, used by the explorer. Labels left out fall
    #: back to the colour of the group they belong to.
    palette: dict[str, str] = field(default_factory=dict)

    #: A lens over the labels: group name -> labels, in display order.
    groups: dict[str, tuple[str, ...]] = field(default_factory=dict)

    #: Colour per group.
    group_colors: dict[str, str] = field(default_factory=dict)

    #: Properties tried in order for an entity's display name.
    name_properties: tuple[str, ...] = ("name",)

    #: Entity property holding a date, for the timeline view. None disables it.
    date_property: str | None = "date"

    #: Property holding the evidence level, and the levels themselves.
    evidence_property: str = "status"
    evidence_levels: tuple[str, ...] = DEFAULT_EVIDENCE_LEVELS

    #: False when the graph was built by something else and this project only
    #: reads and extends it. It makes the engine cautious in the two places that
    #: change data it did not write:
    #:
    #:   * entity resolution is not run across the whole graph. Resolution merges
    #:     same-named nodes, and a graph built by another tool may hold
    #:     same-named nodes on purpose — merging them destroys distinctions the
    #:     other tool made deliberately, and the merge cannot be undone.
    #:   * `graphrag-reset` refuses without an explicit extra flag.
    owns_graph: bool = True

    lexical: LexicalSpec = field(default_factory=LexicalSpec)

    @property
    def labels(self) -> list[str]:
        return [node.label for node in self.schema.node_types]

    @property
    def relationship_labels(self) -> list[str]:
        return [rel.label for rel in self.schema.relationship_types]

    @property
    def grades_evidence(self) -> bool:
        """Whether this corpus carries an evidence level at all."""
        return bool(self.evidence_levels)

    def group_of(self, label: str) -> str | None:
        for group, members in self.groups.items():
            if label in members:
                return group
        return None

    @property
    def label_colors(self) -> dict[str, str]:
        """Colour for every schema label: its own, else its group's, else grey."""
        colors = {}
        for label in self.labels:
            group = self.group_of(label)
            colors[label] = self.palette.get(label) or self.group_colors.get(group or "", "#8894a8")
        return colors

    def ungrouped_labels(self) -> list[str]:
        """Labels no group claims — a spec typo, surfaced rather than swallowed."""
        return [label for label in self.labels if self.group_of(label) is None]


@cache
def load_project(dotted_path: str | None = None) -> ProjectSpec:
    """Import the configured project package and return its PROJECT."""
    target = dotted_path or os.getenv("GRAPHRAG_PROJECT", DEFAULT_PROJECT)
    try:
        module = importlib.import_module(target)
    except ImportError as exc:
        raise ImportError(
            f"Could not import project {target!r}. Set GRAPHRAG_PROJECT to a "
            f"package exposing PROJECT, e.g. 'projects.example'."
        ) from exc
    try:
        spec = module.PROJECT
    except AttributeError as exc:
        raise AttributeError(f"{target!r} does not define PROJECT") from exc
    if not isinstance(spec, ProjectSpec):
        raise TypeError(f"{target}.PROJECT must be a ProjectSpec, got {type(spec)!r}")
    return spec
