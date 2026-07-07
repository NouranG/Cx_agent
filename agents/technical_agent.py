from core.response import ResponseFactory

from database.db import Database
from llm.prompt_builder import TECHNICAL_SYSTEM_PROMPT
from utils.singletons import retriever
from utils.singletons import llm


class TechnicalAgent:

    def __init__(self):

        self.db = Database()
        self.retriever = retriever
        self.llm = llm

    def answer(
        self,
        customer_id: int,
        question: str,
    ):

        network = self.db.get_network_status(customer_id)

        if network is None:
            return ResponseFactory.failure(
                agent="technical",
                message="Customer not found.",
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

        return ResponseFactory.success(
            agent="technical",
            message=answer,
            data={
                "customer_id": customer_id,
                "network": network,
                "sources": [
                    doc.metadata.get("source", "")
                    for doc in docs
                ],
            },
        )