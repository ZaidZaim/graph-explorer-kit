"""Ask a question against the active project's knowledge graph.

    graphrag-ask "who was involved in the breach?"
    graphrag-ask --retriever text2cypher "how many claims are only rumored?"
    graphrag-ask --show-context "what do we actually know?"
    graphrag-ask --chat
"""

from __future__ import annotations

import argparse
import sys

from neo4j_graphrag.generation import GraphRAG
from neo4j_graphrag.generation.prompts import RagTemplate
from neo4j_graphrag.message_history import InMemoryMessageHistory

from graphrag_kit.config import get_driver, get_llm, use_utf8_stdout
from graphrag_kit.project import load_project
from graphrag_kit.retrievers import RETRIEVERS, build_rag_prompt


def main() -> int:
    use_utf8_stdout()
    parser = argparse.ArgumentParser(description="Query the project knowledge graph.")
    parser.add_argument("question", nargs="*", help="The question to ask.")
    parser.add_argument(
        "--retriever",
        choices=sorted(RETRIEVERS),
        default="hybrid-cypher",
        help="Retrieval strategy (default: hybrid-cypher).",
    )
    parser.add_argument("--top-k", type=int, default=5, help="Chunks to retrieve (default: 5).")
    parser.add_argument("--show-context", action="store_true", help="Print retrieved context.")
    parser.add_argument("--chat", action="store_true", help="Multi-turn REPL keeping history.")
    args = parser.parse_args()

    question = " ".join(args.question).strip()
    if not question and not args.chat:
        parser.error("provide a question, or pass --chat")

    spec = load_project()
    driver = get_driver()
    llm = get_llm()
    try:
        rag = GraphRAG(
            retriever=RETRIEVERS[args.retriever](driver),
            llm=llm,
            prompt_template=RagTemplate(
                template=build_rag_prompt(spec),
                expected_inputs=["context", "query_text", "examples"],
            ),
        )
        # Text2CypherRetriever generates Cypher and takes no top_k.
        config = {} if args.retriever == "text2cypher" else {"top_k": args.top_k}

        def answer(q: str, history=None) -> None:
            result = rag.search(
                query_text=q,
                message_history=history,
                retriever_config=config,
                return_context=args.show_context,
                response_fallback="Nothing in the graph covers that.",
            )
            if args.show_context and result.retriever_result:
                print("\n--- retrieved context ---")
                for i, item in enumerate(result.retriever_result.items, start=1):
                    print(f"[{i}] {item.content}")
                print("--- end context ---\n")
            print(result.answer)

        if args.chat:
            history = InMemoryMessageHistory()
            if question:
                answer(question, history)
            print("\n(empty line or Ctrl-D to exit)")
            while True:
                try:
                    line = input("\n> ").strip()
                except EOFError:
                    break
                if not line:
                    break
                answer(line, history)
        else:
            answer(question)
    finally:
        llm.close()
        driver.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
