from core.message_bus import MessageBus
from core.response_engine import ResponseEngine
from core.api_gateway import APIGateway


# --------------------------------------------------
# Mock Triage Agent
# --------------------------------------------------

class MockTriageAgent:

    def handle_request(self, request):

        return ResponseEngine.success(
            agent="MockTriageAgent",
            message=f"Received request: {request['message']}",
            confidence=0.95,
            data={
                "customer_id": request["customer_id"]
            }
        )


# --------------------------------------------------
# Message Bus Test
# --------------------------------------------------

print("=" * 60)
print("MESSAGE BUS TEST")
print("=" * 60)

bus = MessageBus()


def billing_listener(data):
    print("Billing Listener:", data)


def technical_listener(data):
    print("Technical Listener:", data)


bus.subscribe("billing", billing_listener)
bus.subscribe("technical", technical_listener)

bus.publish(
    "billing",
    {
        "customer_id": 1,
        "issue": "Refund"
    }
)

bus.publish(
    "technical",
    {
        "customer_id": 2,
        "issue": "Internet down"
    }
)


# --------------------------------------------------
# Response Engine Test
# --------------------------------------------------

print("\n" + "=" * 60)
print("RESPONSE ENGINE TEST")
print("=" * 60)

response = ResponseEngine.success(
    agent="BillingAgent",
    message="Refund approved.",
    confidence=0.98,
    data={
        "amount": 30
    }
)

print(response.to_dict())


failure = ResponseEngine.failure(
    agent="TechnicalAgent",
    message="Customer not found."
)

print(failure.to_dict())


# --------------------------------------------------
# API Gateway Test
# --------------------------------------------------

print("\n" + "=" * 60)
print("API GATEWAY TEST")
print("=" * 60)

gateway = APIGateway(MockTriageAgent())

request = {
    "customer_id": 101,
    "message": "My internet is slow."
}

result = gateway.process_request(request)

print(result.to_dict())


# --------------------------------------------------
# Invalid Request Test
# --------------------------------------------------

print("\n" + "=" * 60)
print("INVALID REQUEST TEST")
print("=" * 60)

bad_request = {
    "message": "Refund please"
}

result = gateway.process_request(bad_request)

print(result.to_dict())