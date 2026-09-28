"""Conversations and memory: the parts that need no database.

What is pinned here is the behaviour a follow-up question depends on — when a
question is rewritten against the conversation, what the model is shown, and
what happens when the rewrite cannot be trusted — plus the embedder adapter's
two-protocol shape, because the memory package picks a protocol by attribute
and a wrong guess there surfaces as vectors of the wrong width at connect time.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass

import pytest

from graphrag_kit.memory import (
    FOLLOWUP_CONTEXT_TURNS,
    GraphRAGEmbedder,
    Turn,
    memory_mode,
    needs_rewrite,
    rewrite_prompt,
    standalone_question,
)


@dataclass
class _Reply:
    content: str


class _LLM:
    def __init__(self, reply: str, fail: bool = False):
        self.reply, self.fail, self.prompts = reply, fail, []

    def invoke(self, prompt: str):
        self.prompts.append(prompt)
        if self.fail:
            raise RuntimeError("model down")
        return _Reply(self.reply)


TURNS = [
    ("user", "What did witnesses report over New Mexico in 1949?"),
    ("assistant", "Green fireballs were reported near Los Alamos and Sandia."),
]


def test_a_first_question_is_never_rewritten():
    llm = _LLM("should not be called")
    question = "What did witnesses report?"
    assert standalone_question(llm, [], question) == question
    assert llm.prompts == []
    assert not needs_rewrite([])
    assert needs_rewrite(TURNS)


def test_a_follow_up_is_rewritten_against_the_conversation():
    llm = _LLM("What did witnesses report over New Mexico in 1950?")
    assert standalone_question(llm, TURNS, "and in 1950?") == (
        "What did witnesses report over New Mexico in 1950?"
    )
    prompt = llm.prompts[0]
    assert "Analyst: What did witnesses report over New Mexico in 1949?" in prompt
    assert "Assistant: Green fireballs" in prompt
    assert prompt.rstrip().endswith("Latest question: and in 1950?")


def test_a_failed_or_runaway_rewrite_falls_back_to_the_question():
    # The model is down: the question goes through as asked.
    assert standalone_question(_LLM("", fail=True), TURNS, "and in 1950?") == "and in 1950?"
    # The model answered instead of rewriting: far too long to be a question.
    essay = "Green fireballs " * 60
    assert standalone_question(_LLM(essay), TURNS, "and in 1950?") == "and in 1950?"
    # Empty and quoted replies are handled too.
    assert standalone_question(_LLM("  "), TURNS, "and in 1950?") == "and in 1950?"
    assert standalone_question(_LLM('"In 1950?"'), TURNS, "and in 1950?") == "In 1950?"


def test_the_rewrite_reads_only_the_recent_turns_and_trims_long_answers():
    long_answer = "x" * 5000
    turns = [("user", f"q{i}") if i % 2 == 0 else ("assistant", long_answer) for i in range(40)]
    prompt = rewrite_prompt(turns, "and then?")
    # At most FOLLOWUP_CONTEXT_TURNS exchanges, each answer cut to a paragraph.
    assert prompt.count("Analyst:") <= FOLLOWUP_CONTEXT_TURNS
    assert "x" * 700 not in prompt
    assert "…" in prompt


def test_the_embedder_adapter_serves_both_protocols():
    class Fake:
        def embed_query(self, text):
            return [float(len(text))] * 3

    adapter = GraphRAGEmbedder(Fake())
    # New protocol: model + dimensions + batch embed + embed_one.
    assert adapter.model
    assert isinstance(adapter.dimensions, int)
    assert asyncio.run(adapter.embed_one("abc")) == [3.0, 3.0, 3.0]
    assert asyncio.run(adapter.embed(["a", "bb"])) == [[1.0] * 3, [2.0] * 3]
    # Old protocol: embed(str) returns one vector, embed_batch a list.
    assert asyncio.run(adapter.embed("abcd")) == [4.0] * 3
    assert asyncio.run(adapter.embed_batch(["a"])) == [[1.0] * 3]


def test_memory_mode_rejects_nonsense(monkeypatch):
    monkeypatch.setenv("AGENT_MEMORY", "maybe")
    with pytest.raises(ValueError):
        memory_mode()
    monkeypatch.setenv("AGENT_MEMORY", "OFF")
    assert memory_mode() == "off"


def test_turns_serialise_with_their_retriever():
    turn = Turn("user", "hello", "2026-09-28T10:00:00", {"retriever": "agent"})
    assert turn.as_dict() == {
        "role": "user",
        "content": "hello",
        "at": "2026-09-28T10:00:00",
        "retriever": "agent",
    }
