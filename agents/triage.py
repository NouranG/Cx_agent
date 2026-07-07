from llm.prompt_builder import TRIAGE_SYSTEM_PROMPT
from utils.singletons import llm



class TriageAgent:

    VALID_AGENTS = {
        "knowledge",
        "billing",
        "technical",
    }

    def __init__(self):

        self.llm = llm

    def route(self, question: str) -> str:

        agent = self.llm.generate(
            TRIAGE_SYSTEM_PROMPT,
            question,
        ).strip().lower()

        if agent not in self.VALID_AGENTS:
            return "knowledge"

        return agent