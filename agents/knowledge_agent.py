from dataclasses import dataclass
from typing import List

from llm.ollama_provider import OllamaProvider
from llm.prompt_builder import KNOWLEDGE_SYSTEM_PROMPT
from utils.retrieval import Retriever


@dataclass
class KnowledgeResponse:
    question: str
    answer: str
    sources: List[str]
    success: bool


class KnowledgeAgent:

    def __init__(self):

        self.retriever = Retriever()
        self.llm = OllamaProvider()

    def answer(
        self,
        question: str,
        k: int = 4,
    ) -> KnowledgeResponse:

        docs = self.retriever.retrieve(question, k=k)

        if not docs:
            return KnowledgeResponse(
                question=question,
                answer="I couldn't find any relevant information.",
                sources=[],
                success=False,
            )

        context = self.retriever.build_context(docs)

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

        return KnowledgeResponse(
            question=question,
            answer=answer,
            sources=sources,
            success=True,
        )