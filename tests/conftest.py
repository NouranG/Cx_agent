"""Test fixtures that keep unit tests independent of Ollama and FAISS."""
import sys
import types
from dataclasses import dataclass


class FakeLLM:
    def generate(self, system_prompt, user_prompt):
        return "Mock response"


@dataclass
class FakeDocument:
    page_content: str
    metadata: dict


class FakeRetriever:
    def retrieve(self, query, k=4):
        return [
            FakeDocument(
                page_content="Restart the router and wait two minutes.",
                metadata={"source": "test-guide.md"},
            )
        ][:k]

    def build_context(self, docs):
        return "\n".join(doc.page_content for doc in docs)


# Agent modules import these singletons at module-import time. Replace them
# before test modules import the agents so unit tests need no local model/index.
fake_singletons = types.ModuleType("utils.singletons")
fake_singletons.llm = FakeLLM()
fake_singletons.retriever = FakeRetriever()
sys.modules.setdefault("utils.singletons", fake_singletons)
