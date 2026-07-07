from core.request import SupportRequest
from core.response import ResponseFactory
from core.response_engine import ResponseEngine


class APIGateway:

    def __init__(self):
        self.engine = ResponseEngine()

    def process_request(self, request: dict):

        customer_id = request.get("customer_id")
        message = request.get("message")

        if customer_id is None:
            return ResponseFactory.failure(
                "api_gateway",
                "Missing customer_id."
            )

        if not message:
            return ResponseFactory.failure(
                "api_gateway",
                "Message cannot be empty."
            )

        support_request = SupportRequest(
            customer_id=customer_id,
            message=message,
        )

        return self.engine.process(
            support_request
        )