"""
API Gateway

Receives incoming support requests and forwards them
to the appropriate workflow.
"""

from core.response_engine import ResponseEngine


class APIGateway:
    def __init__(self, triage_agent):
        """
        Parameters
        ----------
        triage_agent : TriageAgent
            Main router for customer requests.
        """
        self.triage_agent = triage_agent

    def process_request(self, request: dict):
        """
        Process an incoming customer request.

        Expected format:
        {
            "customer_id": 101,
            "message": "Why is my internet slow?"
        }
        """

        customer_id = request.get("customer_id")
        message = request.get("message")

        if customer_id is None:
            return ResponseEngine.failure(
                agent="APIGateway",
                message="Missing customer_id."
            )

        if not message:
            return ResponseEngine.failure(
                agent="APIGateway",
                message="Message cannot be empty."
            )

        return self.triage_agent.handle_request(request)