from llm.ollama_provider import OllamaProvider
from llm.prompt_builder import TRIAGE_SYSTEM_PROMPT


class TriageAgent:

    VALID_AGENTS = {
        "knowledge",
        "billing",
        "technical",
    }

    def __init__(self):

        self.llm = OllamaProvider()

    def route(self, question: str) -> str:

        agent = self.llm.generate(
            TRIAGE_SYSTEM_PROMPT,
            question,
        ).strip().lower()

        if agent not in self.VALID_AGENTS:
            return "knowledge"

        return agent