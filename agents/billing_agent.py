from core.response import ResponseFactory

from database.db import Database
from llm.prompt_builder import BILLING_SYSTEM_PROMPT
from utils.singletons import llm



class BillingAgent:

    def __init__(self):
        self.db = Database()
        self.llm = llm

    def answer(
        self,
        customer_id: int,
        question: str,
    ):

        customer = self.db.get_customer(customer_id)

        if customer is None:
            return ResponseFactory.failure(
                agent="billing",
                message="Customer not found.",
            )

        bill = self.db.get_bill(customer_id)

        if bill is None:
            return ResponseFactory.failure(
                agent="billing",
                message="No billing information found.",
            )

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

        return ResponseFactory.success(
            agent="billing",
            message=answer,
            data={
                "customer_id": customer_id,
                "customer": customer,
                "bill": bill,
            },
        )