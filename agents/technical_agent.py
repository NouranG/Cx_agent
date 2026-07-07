from dataclasses import dataclass

from database.db import Database
from llm.ollama_provider import OllamaProvider
from llm.prompt_builder import TECHNICAL_SYSTEM_PROMPT
from utils.retrieval import Retriever


@dataclass
class TechnicalResponse:
    customer_id: int
    answer: str
    success: bool


class TechnicalAgent:

    def __init__(self):

        self.db = Database()
        self.retriever = Retriever()
        self.llm = OllamaProvider()

    def answer(
        self,
        customer_id: int,
        question: str,
    ) -> TechnicalResponse:

        network = self.db.get_network_status(customer_id)

        if network is None:

            return TechnicalResponse(
                customer_id,
                "Customer not found.",
                False,
            )

        docs = self.retriever.retrieve(question)

        context = self.retriever.build_context(docs)

        prompt = f"""
Customer Network

Internet Status:
{network['internet_status']}

Router:
{network['router_status']}

Signal Strength:
{network['signal_strength']}

Outage:
{network['outage']}

-----------------------

Knowledge Base

{context}

-----------------------

Customer Question

{question}
"""

        answer = self.llm.generate(
            TECHNICAL_SYSTEM_PROMPT,
            prompt,
        )

        return TechnicalResponse(
            customer_id,
            answer,
            True,
        )