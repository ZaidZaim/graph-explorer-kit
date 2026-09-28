"""The question's two routes into a hybrid retriever.

One `query_text` goes both to the embedder and to the fulltext index, and only
the second reads it as a query language. The retrievers here split the two:
the embedder sees the question as typed, the index sees it with Lucene's
operators escaped. No database or model is needed to check that.
"""

from __future__ import annotations

from graphrag_kit.retrievers import FACTS_PER_ENTITY, _FulltextSafe


class _Embedder:
    def embed_query(self, text):
        return [len(text)]


class _Library:
    """Stands in for the neo4j-graphrag class: records what it was handed."""

    def __init__(self):
        self.embedder = _Embedder()
        self.calls = []

    def get_search_results(self, query_text, query_vector=None, **kwargs):
        self.calls.append((query_text, query_vector, kwargs))
        return "result"


class Safe(_FulltextSafe, _Library):
    pass


def test_the_index_gets_the_escaped_question_and_the_embedder_the_plain_one():
    retriever = Safe()
    question = "Which Phase I/II studies (NSCLC) did BMS run?"
    assert retriever.get_search_results(question, top_k=3) == "result"
    ((query_text, query_vector, kwargs),) = retriever.calls
    assert query_text == r"Which Phase I\/II studies \(NSCLC\) did BMS run\?"
    # The vector was computed from the unescaped text.
    assert query_vector == [len(question)]
    assert kwargs == {"top_k": 3}


def test_a_supplied_vector_is_passed_through():
    retriever = Safe()
    retriever.get_search_results("a/b", query_vector=[1.0])
    ((_, query_vector, _),) = retriever.calls
    assert query_vector == [1.0]


def test_the_fact_cap_is_a_sane_number():
    # A hub node in an adopted graph can carry hundreds of edges; the cap has
    # to sit well above an ordinary record and well below a hub.
    assert 10 <= FACTS_PER_ENTITY <= 100
