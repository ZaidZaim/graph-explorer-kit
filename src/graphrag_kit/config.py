"""Shared configuration: environment loading and Neo4j / model factories.

Domain-agnostic. Corpus-specific settings live in a ProjectSpec — see project.py.

Two model providers are supported, selected with LLM_PROVIDER:

  azure   Microsoft Foundry / Azure OpenAI. Authenticates with Entra ID via
          DefaultAzureCredential — an `az login` is enough and no key is stored
          anywhere. Set AZURE_AUTH_MODE=key to use AZURE_OPENAI_API_KEY instead.
  openai  api.openai.com with OPENAI_API_KEY.
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import neo4j
from dotenv import load_dotenv
from neo4j_graphrag.embeddings.base import Embedder
from neo4j_graphrag.llm import LLMInterface

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

#: Scope for Entra tokens against Foundry / Azure OpenAI endpoints.
AZURE_COGNITIVE_SCOPE = "https://cognitiveservices.azure.com/.default"
DEFAULT_AZURE_API_VERSION = "2024-10-21"

# EMBEDDING_DIMENSIONS must match the embedding model actually deployed:
#   text-embedding-3-small -> 1536      text-embedding-3-large -> 3072
EMBEDDING_DIMENSIONS = int(os.getenv("EMBEDDING_DIMENSIONS", "1536"))


def use_utf8_stdout() -> None:
    """Force UTF-8 on stdout/stderr for CLI entry points.

    The Windows console defaults to cp1252, which turns the en-dashes and
    curly quotes that models happily emit into replacement characters. The
    text is fine; only the terminal rendering is broken.
    """
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            try:
                reconfigure(encoding="utf-8", errors="replace")
            except (ValueError, OSError):
                pass


class ConfigError(RuntimeError):
    """Raised when required configuration is missing or inconsistent."""


def _require(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ConfigError(
            f"Missing required environment variable {name!r}. "
            "Copy .env.example to .env and fill it in."
        )
    return value


def provider() -> str:
    value = os.getenv("LLM_PROVIDER", "azure").strip().lower()
    if value not in {"azure", "openai"}:
        raise ConfigError(f"LLM_PROVIDER must be 'azure' or 'openai', got {value!r}")
    return value


# --- Neo4j ------------------------------------------------------------------


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


# --- Azure auth -------------------------------------------------------------


@lru_cache(maxsize=1)
def _azure_token_provider():
    """Bearer-token callable backed by the ambient Azure identity.

    Cached because DefaultAzureCredential probes several sources on construction
    (az CLI, managed identity, env vars) and that is wasted work per client.
    The callable it returns handles refresh internally.
    """
    try:
        from azure.identity import DefaultAzureCredential, get_bearer_token_provider
    except ImportError as exc:  # pragma: no cover - dependency is declared
        raise ConfigError(
            "azure-identity is required for LLM_PROVIDER=azure. Run: uv sync"
        ) from exc
    return get_bearer_token_provider(DefaultAzureCredential(), AZURE_COGNITIVE_SCOPE)


def azure_auth_mode() -> str:
    value = os.getenv("AZURE_AUTH_MODE", "entra").strip().lower()
    if value not in {"entra", "key"}:
        raise ConfigError(f"AZURE_AUTH_MODE must be 'entra' or 'key', got {value!r}")
    return value


def _azure_client_kwargs(role: str = "chat") -> dict:
    """Connection kwargs for one Azure client.

    Chat and embedding deployments frequently live on different Foundry
    resources — quota, region and model availability are all per-resource — so
    the embedding endpoint can be overridden independently. It falls back to the
    chat endpoint when unset, which is the single-resource case.

    Auth mode is explicit rather than inferred from whether a key happens to be
    present. Developer machines routinely carry an ambient AZURE_OPENAI_API_KEY
    exported for some other resource; preferring it whenever it exists means the
    key for resource A gets sent to resource B, which fails as a 401 that looks
    like a broken endpoint rather than the wrong credential.
    """
    endpoint = os.getenv("AZURE_OPENAI_EMBEDDING_ENDPOINT") if role == "embedding" else None
    kwargs = {
        "azure_endpoint": endpoint or _require("AZURE_OPENAI_ENDPOINT"),
        "api_version": os.getenv("AZURE_OPENAI_API_VERSION", DEFAULT_AZURE_API_VERSION),
    }
    if azure_auth_mode() == "key":
        kwargs["api_key"] = _require("AZURE_OPENAI_API_KEY")
    else:
        kwargs["azure_ad_token_provider"] = _azure_token_provider()
    return kwargs


def azure_endpoint_for(role: str) -> str:
    if role == "embedding":
        override = os.getenv("AZURE_OPENAI_EMBEDDING_ENDPOINT")
        if override:
            return override
    return os.getenv("AZURE_OPENAI_ENDPOINT", "?")


# --- Models -----------------------------------------------------------------


def _model_params(temperature: float | None) -> dict:
    """Build model_params, omitting temperature unless one is actually wanted.

    Newer reasoning models (gpt-5-mini and friends) reject any temperature other
    than the default and return 400. Sending nothing is the portable choice, so
    temperature is opt-in via LLM_TEMPERATURE rather than hard-coded to 0.
    """
    if temperature is None:
        raw = os.getenv("LLM_TEMPERATURE", "").strip()
        if not raw:
            return {}
        try:
            temperature = float(raw)
        except ValueError as exc:
            raise ConfigError(f"LLM_TEMPERATURE must be a number, got {raw!r}") from exc
    return {"temperature": temperature}


def get_llm(temperature: float | None = None) -> LLMInterface:
    """Chat model used for entity extraction, answering, and text2cypher."""
    params = _model_params(temperature)
    if provider() == "azure":
        from neo4j_graphrag.llm import AzureOpenAILLM

        return AzureOpenAILLM(
            model_name=_require("AZURE_OPENAI_CHAT_DEPLOYMENT"),
            model_params=params,
            **_azure_client_kwargs(),
        )

    from neo4j_graphrag.llm import OpenAILLM

    _require("OPENAI_API_KEY")
    return OpenAILLM(
        model_name=os.getenv("LLM_MODEL", "gpt-4.1-mini"), model_params=params
    )


def get_embedder() -> Embedder:
    """Embedding model. Its output width must equal EMBEDDING_DIMENSIONS."""
    if provider() == "azure":
        from neo4j_graphrag.embeddings import AzureOpenAIEmbeddings

        return AzureOpenAIEmbeddings(
            # For Azure this is the deployment name, not the model name.
            model=_require("AZURE_OPENAI_EMBEDDING_DEPLOYMENT"),
            **_azure_client_kwargs("embedding"),
        )

    from neo4j_graphrag.embeddings import OpenAIEmbeddings

    _require("OPENAI_API_KEY")
    return OpenAIEmbeddings(model=os.getenv("EMBEDDING_MODEL", "text-embedding-3-small"))


def describe_models() -> str:
    """One-line summary of the active provider, for startup logging."""
    if provider() == "azure":
        auth = "api-key" if azure_auth_mode() == "key" else "Entra ID (az login)"
        host = lambda url: url.replace("https://", "").rstrip("/").split(".")[0]  # noqa: E731
        chat_host = host(azure_endpoint_for("chat"))
        embed_host = host(azure_endpoint_for("embedding"))
        chat = f"chat={os.getenv('AZURE_OPENAI_CHAT_DEPLOYMENT', '?')}@{chat_host}"
        embed = f"embed={os.getenv('AZURE_OPENAI_EMBEDDING_DEPLOYMENT', '?')}@{embed_host}"
        return f"azure {chat} {embed} ({EMBEDDING_DIMENSIONS}d, auth={auth})"
    return (
        f"openai chat={os.getenv('LLM_MODEL', 'gpt-4.1-mini')} "
        f"embed={os.getenv('EMBEDDING_MODEL', 'text-embedding-3-small')} "
        f"({EMBEDDING_DIMENSIONS}d)"
    )


# --- Agent Framework chat client --------------------------------------------

# The Agent Framework talks to Azure through the same `agent_framework.openai`
# clients as direct OpenAI — the AzureOpenAI* compatibility classes were removed
# from `agent_framework.azure` in the 2026 release. Azure routing is selected by
# passing `azure_endpoint`/`credential` explicitly, which also stops an ambient
# OPENAI_API_KEY from silently pulling the client back to api.openai.com.
#
# Two API surfaces are available. Responses is the framework's recommended
# client and the only one with hosted tools; Chat Completions is the fallback
# for deployments or regions where /responses is not available.
AGENT_CHAT_APIS = ("responses", "chat-completions")

# Deliberately NOT AZURE_OPENAI_API_VERSION. That variable is set for the
# neo4j-graphrag clients, which speak Chat Completions and Embeddings and are
# routinely pinned to a GA version like 2024-10-21 — a version with no
# /responses route at all. Sending it here turns a working deployment into an
# opaque 404, so the agent client keeps its own default and its own override.
AGENT_DEFAULT_API_VERSIONS = {
    "responses": "preview",
    "chat-completions": "2024-12-01-preview",
}


def agent_chat_api() -> str:
    value = os.getenv("AGENT_CHAT_API", "responses").strip().lower()
    if value not in AGENT_CHAT_APIS:
        raise ConfigError(
            f"AGENT_CHAT_API must be one of {', '.join(AGENT_CHAT_APIS)}, got {value!r}"
        )
    return value


def get_chat_client():
    """Agent Framework chat client for the active provider.

    Returns an ``OpenAIChatClient`` (Responses API) or ``OpenAIChatCompletionClient``,
    pointed at Foundry / Azure OpenAI or at api.openai.com to match LLM_PROVIDER.
    This is the agent's model; ``get_llm()`` remains the neo4j-graphrag one used by
    extraction, text2cypher and the single-shot RAG pipeline.
    """
    from agent_framework.openai import OpenAIChatClient, OpenAIChatCompletionClient

    api = agent_chat_api()
    client_cls = OpenAIChatClient if api == "responses" else OpenAIChatCompletionClient

    if provider() == "openai":
        _require("OPENAI_API_KEY")
        return client_cls(model=os.getenv("LLM_MODEL", "gpt-4.1-mini"))

    kwargs = {
        # On Azure this is the deployment name, not the model name.
        "model": _require("AZURE_OPENAI_CHAT_DEPLOYMENT"),
        "azure_endpoint": _require("AZURE_OPENAI_ENDPOINT"),
        "api_version": os.getenv("AGENT_AZURE_API_VERSION") or AGENT_DEFAULT_API_VERSIONS[api],
    }
    if azure_auth_mode() == "key":
        kwargs["api_key"] = _require("AZURE_OPENAI_API_KEY")
    else:
        # A plain callable returning a bearer token is one of the accepted
        # credential types, so the cached provider from get_llm() is reused
        # rather than probing DefaultAzureCredential's sources a second time.
        kwargs["credential"] = _azure_token_provider()
    return client_cls(**kwargs)


def describe_agent_model() -> str:
    """One-line summary of the agent's model, for startup logging."""
    api = agent_chat_api()
    if provider() == "azure":
        auth = "api-key" if azure_auth_mode() == "key" else "Entra ID (az login)"
        version = os.getenv("AGENT_AZURE_API_VERSION") or AGENT_DEFAULT_API_VERSIONS[api]
        return (
            f"azure {api} model={os.getenv('AZURE_OPENAI_CHAT_DEPLOYMENT', '?')} "
            f"api-version={version} (auth={auth})"
        )
    return f"openai {api} model={os.getenv('LLM_MODEL', 'gpt-4.1-mini')}"
