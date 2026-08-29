"""Run one question through every retriever and print the results side by side.

This is the demo's argument for GraphRAG: on a question whose answer is spread
across documents, `vector` returns the chunks that *sound* like the question,
while `hybrid-cypher` returns those chunks plus the graph facts around them.
"""

from __future__ import annotations

import argparse
import sys
import textwrap
import time

from neo4j_graphrag.generation import GraphRAG

from graphrag_demo.ask import RAG_TEMPLATE
from graphrag_demo.config import get_driver, get_llm
from graphrag_demo.retrievers import RETRIEVERS

DEFAULT_ORDER = ["vector", "hybrid", "vector-cypher", "hybrid-cypher", "text2cypher"]


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare retrievers on one question.")
    parser.add_argument("question", nargs="+", help="The question to ask.")
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument(
        "--only",
        nargs="+",
        choices=sorted(RETRIEVERS),
        default=DEFAULT_ORDER,
        help="Subset of retrievers to run.",
    )
    args = parser.parse_args()
    question = " ".join(args.question)

    driver = get_driver()
    llm = get_llm()
    try:
        print(f"Question: {question}\n")
        for name in [n for n in DEFAULT_ORDER if n in args.only]:
            print("=" * 78)
            print(name)
            print("=" * 78)
            config = {} if name == "text2cypher" else {"top_k": args.top_k}
            rag = GraphRAG(
                retriever=RETRIEVERS[name](driver), llm=llm, prompt_template=RAG_TEMPLATE
            )
            started = time.monotonic()
            try:
                result = rag.search(
                    query_text=question,
                    retriever_config=config,
                    return_context=True,
                    response_fallback="(retriever returned no context)",
                )
            except Exception as exc:  # noqa: BLE001 - a failing retriever shouldn't stop the comparison
                print(f"  failed: {type(exc).__name__}: {exc}\n")
                continue
            elapsed = time.monotonic() - started

            items = result.retriever_result.items if result.retriever_result else []
            print(f"  {len(items)} context item(s) in {elapsed:.1f}s\n")
            print(textwrap.indent(textwrap.fill(result.answer, width=76), "  "))
            print()
    finally:
        llm.close()
        driver.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
