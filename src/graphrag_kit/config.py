"""Shared configuration: environment loading and Neo4j / OpenAI object factories.

Domain-agnostic. Corpus-specific settings live in a ProjectSpec — see project.py.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

import neo4j
from dotenv import load_dotenv
from neo4j_graphrag.embeddings import OpenAIEmbeddings
from neo4j_graphrag.llm import OpenAILLM

PROJECT_ROOT = Path(__file__).resolve().parents[2]

# override=True on purpose: a stale NEO4J_URI exported in the shell would otherwise
# silently shadow this project's .env and point the demo at the wrong instance.
load_dotenv(PROJECT_ROOT / ".env", override=True)

VECTOR_INDEX_NAME = "chunk_embedding"
FULLTEXT_INDEX_NAME = "chunk_fulltext"
ENTITY_FULLTEXT_INDEX_NAME = "entity_fulltext"
CHUNK_LABEL = "Chunk"
CHUNK_EMBEDDING_PROPERTY = "embedding"
CHUNK_TEXT_PROPERTY = "text"

# EMBEDDING_DIMENSIONS must match EMBEDDING_MODEL:
#   text-embedding-3-small -> 1536      text-embedding-3-large -> 3072
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
EMBEDDING_DIMENSIONS = int(os.getenv("EMBEDDING_DIMENSIONS", "1536"))
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4.1-mini")


class ConfigError(RuntimeError):
    """Raised when a required environment variable is missing."""


def _require(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ConfigError(
            f"Missing required environment variable {name!r}. "
            "Copy .env.example to .env and fill it in."
        )
    return value


@dataclass(frozen=True)
class Neo4jSettings:
    uri: str
    username: str
    password: str
    database: str

    @classmethod
    def from_env(cls) -> Neo4jSettings:
        return cls(
            uri=_require("NEO4J_URI"),
            username=os.getenv("NEO4J_USERNAME", "neo4j"),
            password=_require("NEO4J_PASSWORD"),
            database=os.getenv("NEO4J_DATABASE", "neo4j"),
        )


def get_driver() -> neo4j.Driver:
    """Return a verified Neo4j driver. Caller is responsible for closing it."""
    settings = Neo4jSettings.from_env()
    driver = neo4j.GraphDatabase.driver(settings.uri, auth=(settings.username, settings.password))
    driver.verify_connectivity()
    return driver


def get_database() -> str:
    return os.getenv("NEO4J_DATABASE", "neo4j")


def get_embedder() -> OpenAIEmbeddings:
    _require("OPENAI_API_KEY")
    return OpenAIEmbeddings(model=EMBEDDING_MODEL)


def get_llm(temperature: float = 0.0) -> OpenAILLM:
    _require("OPENAI_API_KEY")
    return OpenAILLM(model_name=LLM_MODEL, model_params={"temperature": temperature})
