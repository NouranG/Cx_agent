from dataclasses import dataclass
from typing import Optional

from database.db import Database
from llm.ollama_provider import OllamaProvider
from llm.prompt_builder import BILLING_SYSTEM_PROMPT


@dataclass
class BillingResponse:
    customer_id: int
    answer: str
    success: bool


class BillingAgent:

    def __init__(self):
        self.db = Database()
        self.llm = OllamaProvider()

    def answer(
        self,
        customer_id: int,
        question: str,
    ) -> BillingResponse:

        customer = self.db.get_customer(customer_id)

        if customer is None:
            return BillingResponse(
                customer_id,
                "Customer not found.",
                False,
            )

        bill = self.db.get_bill(customer_id)

        prompt = f"""
Customer

Name:
{customer['first_name']} {customer['last_name']}

Plan:
{customer['internet_plan']}

AutoPay:
{customer['autopay']}

Status:
{customer['account_status']}

Bill

Amount:
{bill['amount']}

Due Date:
{bill['due_date']}

Bill Status:
{bill['status']}

Last Payment:
{bill['last_payment_date']}

Customer Question

{question}
"""

        answer = self.llm.generate(
            BILLING_SYSTEM_PROMPT,
            prompt,
        )

        return BillingResponse(
            customer_id,
            answer,
            True,
        )