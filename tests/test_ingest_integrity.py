"""Ingestion control flow without model or database calls."""

import asyncio
from pathlib import Path
from unittest.mock import Mock

import pytest
from neo4j_graphrag.components.lexical_graph import LexicalGraphBuilder

from graphrag_kit import ingest
from graphrag_kit.prepare import PreparedFileLoader
from graphrag_kit.project import load_project


def test_failed_attempt_cleanup_uses_its_id_and_keeps_successful_attempt(monkeypatch):
    metadata = []

    class Pipeline:
        async def run_async(self, *, file_path, document_metadata):
            metadata.append(document_metadata)
            if len(metadata) == 2:
                raise RuntimeError("partial write")

    cleanup = Mock(return_value={"chunks": 1, "entities": 1})
    monkeypatch.setattr(ingest, "get_embedder", lambda: object())
    monkeypatch.setattr(ingest, "build_pipeline", lambda *args: Pipeline())
    monkeypatch.setattr(ingest, "remove_source", cleanup)
    driver = Mock()
    spec = load_project("projects.example")
    result = asyncio.run(
        ingest.ingest_files(
            spec,
            [Path("old/report.md"), Path("new/report.md")],
            driver,
            object(),
            "neo4j",
            continue_on_error=True,
            resolve_entities=False,
            report=lambda _: None,
        )
    )

    assert result["succeeded"] == 1
    assert len(result["failed"]) == 1
    assert metadata[0]["ingestion_id"] != metadata[1]["ingestion_id"]
    assert metadata[0]["source"] == metadata[1]["source"] == "report.md"
    cleanup.assert_called_once_with(spec, driver, "neo4j", ingestion_id=metadata[1]["ingestion_id"])
    # --no-resolve must not normalize the whole graph as an unrelated side effect.
    driver.execute_query.assert_not_called()


def test_cleanup_refuses_missing_attempt_id():
    driver = Mock()
    with pytest.raises(ValueError, match="ingestion_id"):
        ingest.remove_source(load_project(), driver, "neo4j", ingestion_id="")
    driver.execute_query.assert_not_called()


def test_attempt_id_survives_loader_and_lexical_document_creation(tmp_path):
    path = tmp_path / "report.md"
    path.write_text("A synthetic report.", encoding="utf-8")
    metadata = {"source": path.name, "project": "example", "ingestion_id": "attempt-123"}
    document = asyncio.run(PreparedFileLoader().run(str(path), metadata=metadata))
    node = LexicalGraphBuilder().create_document_node(document.document_info)
    assert node.properties.items() >= metadata.items()
