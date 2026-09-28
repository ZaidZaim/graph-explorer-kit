"""Conversations the agent can continue, and the memory they leave behind.

One question, one answer, no history — that is how `ask.py` and the explorer's
first version worked, and it is the wrong shape for an analyst. The second
question is always a follow-up: "and in 1949?", "which of those had radar?",
"show me the other document". Answering it needs the conversation so far, and a
demo that forgets between restarts needs it written somewhere durable.

This module keeps conversations in the same Neo4j instance as the knowledge
graph, through `neo4j-agent-memory` — a Neo4j Labs package that stores
messages, sessions and reasoning traces as nodes. Three things come from that:

  * **Follow-up questions.** Each conversation is an Agent Framework session
    whose history provider reads and writes Neo4j, so the agent sees every
    earlier turn, and a restarted server picks the conversation up where it
    was.
  * **A transcript that outlives the tab.** `GET /api/conversations/{id}`
    rebuilds the thread the browser shows; the CLI resumes one with
    `--session`.
  * **State history.** Every agent turn is recorded as a reasoning trace —
    the question, the tools it called in order, the answer — next to the
    messages, queryable in Cypher like everything else.

The fixed retrievers get follow-ups too, by a cheaper route: before a
`hybrid-cypher` question is embedded, the recent turns are used to rewrite
"and in 1949?" into a question that stands on its own, and the rewrite is
shown so nothing is done silently.

What memory deliberately does *not* do here is extract entities from the
conversation into long-term memory. The package can, but its POLE+O labels
(`Person`, `Location`, `Event`) are this project's schema labels too, and a
question mentioning Roswell must not create a `Location` next to the ones the
documents produced. Messages and traces are the memory; the knowledge graph
stays the documents'.

Memory is optional. `AGENT_MEMORY=off` runs without it (history then lives
in process memory for the server's lifetime), and `NAMS_API_KEY` switches the
store from this Neo4j instance to the hosted Neo4j Agent Memory Service.
"""

from __future__ import annotations

import asyncio
import os
import uuid
from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Any

from graphrag_kit.config import EMBEDDING_DIMENSIONS, Neo4jSettings, get_embedder

#: How many recent turns a follow-up is read against. Enough for "the other
#: document" three questions back; few enough that the rewrite stays cheap.
FOLLOWUP_CONTEXT_TURNS = 6

#: How much history the agent is shown per turn. Older turns are still stored
#: and searchable through `recall_conversations`; they are not all replayed
#: into every prompt.
HISTORY_WINDOW = 40


def memory_mode() -> str:
    """auto (default): on when the package is installed. on: required. off: never."""
    value = os.getenv("AGENT_MEMORY", "auto").strip().lower()
    if value not in ("auto", "on", "off"):
        raise ValueError(f"AGENT_MEMORY must be auto, on or off, got {value!r}")
    return value


def memory_available() -> bool:
    try:
        import neo4j_agent_memory  # noqa: F401
    except ImportError:
        return False
    return True


def memory_wanted() -> bool:
    mode = memory_mode()
    if mode == "off":
        return False
    if mode == "on" and not memory_available():
        raise RuntimeError(
            "AGENT_MEMORY=on but neo4j-agent-memory is not installed. Run: uv sync --extra memory"
        )
    return memory_available()


def new_session_id() -> str:
    return uuid.uuid4().hex


class GraphRAGEmbedder:
    """The project's embedder in the shape `neo4j-agent-memory` wants.

    Messages are embedded so past conversations can be searched semantically.
    They are embedded with the same deployment as the chunks, so `EMBEDDING_
    DIMENSIONS` is the width of the memory package's vector indexes too — and
    Entra auth, the embedding endpoint override and the retry handler all come
    along for free rather than being configured a second time.

    The package accepts two embedder protocols, one taking a single text and one
    taking a batch, and detects which by attribute shape. Both are satisfied
    here; `embed` looks at what it was handed.
    """

    def __init__(self, embedder=None):
        self._embedder = embedder or get_embedder()
        self.model = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT") or os.getenv(
            "EMBEDDING_MODEL", "text-embedding-3-small"
        )

    @property
    def dimensions(self) -> int:
        return EMBEDDING_DIMENSIONS

    async def embed_one(self, text: str) -> list[float]:
        return await asyncio.to_thread(self._embedder.embed_query, text)

    async def embed_batch(self, texts: Sequence[str]) -> list[list[float]]:
        return [await self.embed_one(text) for text in texts]

    async def embed(self, text_or_texts):
        if isinstance(text_or_texts, str):
            return await self.embed_one(text_or_texts)
        return await self.embed_batch(list(text_or_texts))


async def open_memory():
    """A connected `MemoryClient`, on this Neo4j instance or on NAMS.

    Extraction is switched off in the settings, not just unused: the package
    would otherwise try to load spaCy on the first message and, failing that,
    fall back to an LLM call per message to find entities nobody asked for.
    """
    from neo4j_agent_memory import MemoryClient, MemorySettings
    from neo4j_agent_memory.config.settings import (
        ExtractionConfig,
        MemoryConfig,
        NamsConfig,
        Neo4jConfig,
    )

    common: dict[str, Any] = {
        "extraction": ExtractionConfig(
            enable_spacy=False,
            enable_gliner=False,
            enable_llm_fallback=False,
            extract_relations=False,
            extract_preferences=False,
        ),
        "memory": MemoryConfig(message_embedding_enabled=True, trace_embedding_enabled=False),
    }
    nams_key = os.getenv("NAMS_API_KEY")
    if nams_key:
        settings = MemorySettings(backend="nams", nams=NamsConfig(api_key=nams_key), **common)
    else:
        neo = Neo4jSettings.from_env()
        settings = MemorySettings(
            backend="bolt",
            neo4j=Neo4jConfig(
                uri=neo.uri, username=neo.username, password=neo.password, database=neo.database
            ),
            **common,
        )
    client = MemoryClient(settings, embedder=GraphRAGEmbedder())
    await client.connect()
    return client


def describe_memory(client) -> str:
    if client is None:
        return "off (history kept in process only)"
    return "NAMS (memory.neo4jlabs.com)" if os.getenv("NAMS_API_KEY") else "Neo4j (same instance)"


# --- follow-up questions for the fixed retrievers ---------------------------

REWRITE_PROMPT = """Below is a conversation between an analyst and an assistant that answers
from a document collection, followed by the analyst's latest question.

Rewrite the latest question so it can be understood on its own, with no access
to the conversation: resolve "it", "they", "those", "the other one", "and in
1949?" and similar references using the conversation. Keep the analyst's
wording and intent; add nothing they did not ask. If the question already
stands on its own, return it exactly as written.

Return only the rewritten question, on one line, with no preamble.

Conversation:
__TURNS__

Latest question: __QUESTION__"""


def needs_rewrite(turns: Sequence[tuple[str, str]]) -> bool:
    return any(role == "user" for role, _ in turns)


def rewrite_prompt(turns: Sequence[tuple[str, str]], question: str) -> str:
    lines = []
    for role, content in turns[-FOLLOWUP_CONTEXT_TURNS * 2 :]:
        speaker = "Analyst" if role == "user" else "Assistant"
        text = " ".join(str(content).split())
        # An answer can be a page long; its first sentences carry what a
        # follow-up refers back to.
        if len(text) > 600:
            text = text[:600].rstrip() + "…"
        lines.append(f"{speaker}: {text}")
    return REWRITE_PROMPT.replace("__TURNS__", "\n".join(lines)).replace("__QUESTION__", question)


def standalone_question(llm, turns: Sequence[tuple[str, str]], question: str) -> str:
    """The question rewritten to stand alone, or itself when there is no history
    or the model returns nothing usable. Synchronous: it is called from the
    streaming path, which runs on a worker thread."""
    if not needs_rewrite(turns):
        return question
    try:
        response = llm.invoke(rewrite_prompt(turns, question))
    except Exception:  # noqa: BLE001 - a failed rewrite must not cost the answer
        return question
    text = " ".join((response.content or "").split()).strip().strip('"')
    if not text or len(text) > 4 * max(len(question), 40):
        return question
    return text


# --- conversations ----------------------------------------------------------


@dataclass
class Turn:
    role: str
    content: str
    at: str | None = None
    meta: dict = field(default_factory=dict)

    def as_dict(self) -> dict:
        return {"role": self.role, "content": self.content, "at": self.at, **self.meta}


class Conversations:
    """Every conversation the server knows, each an agent session of its own.

    The tools are built once and shared — each retriever holds an embedder and
    the text2cypher one an LLM — and an `Agent` is built per session because the
    Neo4j history provider is bound to one session id at construction. Building
    the agent is cheap; the tools are the expensive part.
    """

    def __init__(self, driver, spec, memory=None):
        from graphrag_kit.agent import build_tools

        self.driver = driver
        self.spec = spec
        self.memory = memory
        self.tools = build_tools(driver, spec)
        self._agents: dict[str, Any] = {}
        self._sessions: dict[str, Any] = {}
        # In-process transcript, kept in both modes: without memory it is the
        # only record, with memory it saves a round trip for the common reads.
        self._transcripts: dict[str, list[Turn]] = {}

    # -- agents ---------------------------------------------------------------

    def _recall_tool(self):
        """A tool for reaching conversations the current one cannot see."""
        from typing import Annotated

        from agent_framework import tool
        from pydantic import Field

        memory = self.memory

        @tool
        async def recall_conversations(
            query: Annotated[str, Field(description="What to look for in earlier conversations.")],
            limit: Annotated[
                int, Field(description="How many past messages to return.", ge=1, le=10)
            ] = 5,
        ) -> str:
            """Search every earlier conversation with this analyst — other sessions
            included — for messages about a topic. Use when asked what was
            discussed, asked or concluded before, or when a question refers to
            something not in the current conversation."""
            hits = await memory.short_term.search_messages(query, limit=limit, threshold=0.4)
            if not hits:
                return "Nothing in earlier conversations matches."
            lines = []
            for message in hits:
                when = (
                    message.created_at.isoformat(timespec="minutes") if message.created_at else ""
                )
                role = message.role.value if hasattr(message.role, "value") else str(message.role)
                lines.append(f"[{when}] {role}: {' '.join(str(message.content).split())[:400]}")
            return "\n".join(lines)

        return recall_conversations

    def agent_for(self, session_id: str):
        """The agent and session for one conversation, built on first use."""
        from graphrag_kit.agent import build_agent

        if session_id not in self._agents:
            providers = []
            tools = list(self.tools)
            if self.memory is not None:
                from neo4j_agent_memory.integrations.microsoft_agent import Neo4jChatMessageStore

                providers.append(
                    Neo4jChatMessageStore(
                        memory_client=self.memory,
                        session_id=session_id,
                        max_messages=HISTORY_WINDOW,
                        extract_entities=False,
                    )
                )
                tools.append(self._recall_tool())
            agent = build_agent(self.driver, self.spec, tools=tools, context_providers=providers)
            self._agents[session_id] = agent
            self._sessions[session_id] = agent.create_session(session_id=session_id)
        return self._agents[session_id], self._sessions[session_id]

    async def ask(self, session_id: str, question: str):
        """One agent turn in a conversation, recorded as a reasoning trace."""
        from graphrag_kit.agent import ask_agent

        agent, session = self.agent_for(session_id)
        result = await ask_agent(agent, question, session)
        self._remember(session_id, "user", question, {"retriever": "agent"})
        self._remember(session_id, "assistant", result.answer, {"retriever": "agent"})
        await self._trace(session_id, question, result)
        return result

    async def _trace(self, session_id: str, question: str, result) -> None:
        """The turn as a reasoning trace: task, the tool calls in order, outcome.

        Best-effort. Memory is a record of the answer, never a condition of it,
        so a failure here is swallowed rather than surfaced to the asker.
        """
        if self.memory is None:
            return
        try:
            trace = await self.memory.reasoning.start_trace(
                session_id, task=question, generate_embedding=False
            )
            for call in result.trail.calls:
                await self.memory.reasoning.add_step(
                    trace.id, action=call, generate_embedding=False
                )
            await self.memory.reasoning.complete_trace(
                trace.id,
                outcome=" ".join(result.answer.split())[:300],
                success=True,
            )
        except Exception:  # noqa: BLE001
            pass

    # -- fixed retrievers -----------------------------------------------------

    async def record(self, session_id: str, question: str, answer: str, retriever: str) -> None:
        """A fixed-retriever exchange, written to the same thread the agent reads.

        The agent's history provider saves its own turns; these are the turns it
        did not see happen, so that switching retriever mid-conversation does
        not lose half the thread.
        """
        self._remember(session_id, "user", question, {"retriever": retriever})
        self._remember(session_id, "assistant", answer, {"retriever": retriever})
        if self.memory is None:
            return
        try:
            for role, content in (("user", question), ("assistant", answer)):
                await self.memory.short_term.add_message(
                    session_id,
                    role,
                    content,
                    extract_entities=False,
                    extract_relations=False,
                    metadata={"retriever": retriever},
                )
        except Exception:  # noqa: BLE001
            pass

    async def recent_turns(self, session_id: str) -> list[tuple[str, str]]:
        """(role, content) pairs, oldest first, for the follow-up rewrite."""
        turns = await self.history(session_id)
        return [(t.role, t.content) for t in turns[-FOLLOWUP_CONTEXT_TURNS * 2 :]]

    # -- transcripts ----------------------------------------------------------

    def _remember(self, session_id: str, role: str, content: str, meta: dict) -> None:
        from datetime import datetime, timezone

        self._transcripts.setdefault(session_id, []).append(
            Turn(role, content, datetime.now(timezone.utc).isoformat(timespec="seconds"), meta)
        )

    async def history(self, session_id: str) -> list[Turn]:
        """The conversation so far — from Neo4j when memory is on, so a reloaded
        page and a restarted server both get the thread back."""
        if self.memory is None:
            return list(self._transcripts.get(session_id, []))
        try:
            conversation = await self.memory.short_term.get_conversation(session_id)
        except Exception:  # noqa: BLE001
            return list(self._transcripts.get(session_id, []))
        turns = []
        for message in conversation.messages:
            role = message.role.value if hasattr(message.role, "value") else str(message.role)
            at = message.created_at.isoformat(timespec="seconds") if message.created_at else None
            meta = {k: v for k, v in (message.metadata or {}).items() if k == "retriever"}
            turns.append(Turn(role, str(message.content), at, meta))
        return turns

    async def sessions(self, limit: int = 30) -> list[dict]:
        if self.memory is None:
            return [
                {
                    "id": sid,
                    "title": next((t.content for t in turns if t.role == "user"), "")[:80],
                    "messages": len(turns),
                    "updated": turns[-1].at if turns else None,
                }
                for sid, turns in self._transcripts.items()
            ]
        infos = await self.memory.short_term.list_sessions(limit=limit)
        return [
            {
                "id": info.session_id,
                "title": (info.title or info.first_message_preview or "")[:80],
                "messages": info.message_count,
                "updated": info.updated_at.isoformat(timespec="seconds")
                if info.updated_at
                else None,
            }
            for info in infos
        ]

    async def forget(self, session_id: str) -> None:
        self._agents.pop(session_id, None)
        self._sessions.pop(session_id, None)
        self._transcripts.pop(session_id, None)
        if self.memory is not None:
            await self.memory.short_term.clear_session(session_id)

    async def close(self) -> None:
        if self.memory is not None:
            await self.memory.close()
