from core.response import ResponseFactory

from llm.prompt_builder import KNOWLEDGE_SYSTEM_PROMPT
from utils.singletons import retriever
from utils.singletons import llm


class KnowledgeAgent:

    def __init__(self):

        self.retriever = retriever
        self.llm = llm

    def answer(
        self,
        question: str,
        k: int = 4,
    ):

        docs = self.retriever.retrieve(
            question,
            k=k,
        )

        if not docs:

            return ResponseFactory.failure(
                agent="knowledge",
                message="I couldn't find any relevant information.",
            )

        context = self.retriever.build_context(
            docs
        )

        user_prompt = f"""
Context:
{context}

Question:
{question}

Answer:
"""

        answer = self.llm.generate(
            KNOWLEDGE_SYSTEM_PROMPT,
            user_prompt,
        )

        sources = list(
            dict.fromkeys(
                doc.metadata.get("source", "Unknown")
                for doc in docs
            )
        )

        return ResponseFactory.success(
            agent="knowledge",
            message=answer,
            data={
                "sources": sources,
                "documents": len(docs),
            },
        )