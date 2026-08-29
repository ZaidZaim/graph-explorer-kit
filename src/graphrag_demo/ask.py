"""Ask a question against the knowledge graph.

    graphrag-ask "Which technologies does the Atlas platform use?"
    graphrag-ask --retriever text2cypher "How many organizations are in the graph?"
    graphrag-ask --show-context "Who leads engineering at Meridian Robotics?"
    graphrag-ask --chat
"""

from __future__ import annotations

import argparse
import sys

from neo4j_graphrag.generation import GraphRAG
from neo4j_graphrag.generation.prompts import RagTemplate
from neo4j_graphrag.message_history import InMemoryMessageHistory

from graphrag_demo.config import get_driver, get_llm
from graphrag_demo.retrievers import RETRIEVERS

# The default RagTemplate is fine, but being explicit about grounding is what
# keeps a demo honest: no context, no answer.
RAG_TEMPLATE = RagTemplate(
    template="""You are answering questions about a small corpus of company briefings.

Use ONLY the context below. Each context item may contain the source text, the
entities extracted from it, and related facts drawn from the knowledge graph.
If the context does not contain the answer, say so plainly — do not guess.
Cite the source document for each claim.

Context:
{context}

Examples:
{examples}

Question: {query_text}

Answer:""",
    expected_inputs=["context", "query_text", "examples"],
)


def print_context(result) -> None:
    retriever_result = result.retriever_result
    if retriever_result is None:
        return
    print("\n--- retrieved context ---")
    for i, item in enumerate(retriever_result.items, start=1):
        print(f"[{i}] {item.content}")
    print("--- end context ---\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Query the GraphRAG demo.")
    parser.add_argument("question", nargs="*", help="The question to ask.")
    parser.add_argument(
        "--retriever",
        choices=sorted(RETRIEVERS),
        default="hybrid-cypher",
        help="Retrieval strategy (default: hybrid-cypher).",
    )
    parser.add_argument("--top-k", type=int, default=5, help="Chunks to retrieve (default: 5).")
    parser.add_argument(
        "--show-context", action="store_true", help="Print the retrieved context."
    )
    parser.add_argument(
        "--chat", action="store_true", help="Multi-turn REPL; follow-ups keep history."
    )
    args = parser.parse_args()

    question = " ".join(args.question).strip()
    if not question and not args.chat:
        parser.error("provide a question, or pass --chat")

    driver = get_driver()
    llm = get_llm()
    try:
        retriever = RETRIEVERS[args.retriever](driver)
        rag = GraphRAG(retriever=retriever, llm=llm, prompt_template=RAG_TEMPLATE)

        # Text2CypherRetriever generates Cypher and takes no top_k.
        retriever_config = {} if args.retriever == "text2cypher" else {"top_k": args.top_k}

        def answer(q: str, history=None) -> None:
            result = rag.search(
                query_text=q,
                message_history=history,
                retriever_config=retriever_config,
                return_context=args.show_context,
                response_fallback="I could not find anything relevant in the graph.",
            )
            if args.show_context:
                print_context(result)
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
