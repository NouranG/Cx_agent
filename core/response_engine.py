from agents.billing_agent import BillingAgent
from agents.knowledge_agent import KnowledgeAgent
from agents.technical_agent import TechnicalAgent
from agents.triage import TriageAgent

from core.request import SupportRequest
from core.response import ResponseFactory


class ResponseEngine:

    def __init__(self):

        self.triage = TriageAgent()

        self.billing = BillingAgent()

        self.technical = TechnicalAgent()

        self.knowledge = KnowledgeAgent()

    def process(
        self,
        request: SupportRequest,
    ):

        route = self.triage.route(request.message)

        if route == "billing":
            return self.billing.answer(
                request.customer_id,
                request.message,
            )

        elif route == "technical":
            return self.technical.answer(
                request.customer_id,
                request.message,
            )

        elif route == "knowledge":
            return self.knowledge.answer(
                request.message,
            )

        return ResponseFactory.failure(
            agent="response_engine",
            message=f"Unknown route: {route}",
        )