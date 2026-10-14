from core.api_gateway import APIGateway
from core.message_bus import MessageBus
from core.request import SupportRequest
from core.response import ResponseFactory
from core.response_engine import ResponseEngine


def test_response_factory_success_and_failure():
    success = ResponseFactory.success("knowledge", "Found an answer", data={"sources": ["guide.md"]})
    failure = ResponseFactory.failure("billing", "Customer not found.")
    assert success.success is True
    assert success.to_dict()["message"] == "Found an answer"
    assert success.data["sources"] == ["guide.md"]
    assert failure.success is False
    assert failure.confidence == 0.0


def test_api_gateway_rejects_missing_customer_id():
    response = APIGateway().process_request({"message": "Check my bill"})
    assert response.success is False
    assert response.agent == "api_gateway"
    assert response.message == "Missing customer_id."


def test_api_gateway_rejects_empty_message():
    response = APIGateway().process_request({"customer_id": 1001, "message": ""})
    assert response.success is False
    assert response.message == "Message cannot be empty."


def test_request_model():
    request = SupportRequest(customer_id=1001, message="Hello")
    assert request.customer_id == 1001
    assert request.message == "Hello"


def test_message_bus_dispatches_and_clear_removes_subscribers():
    bus = MessageBus()
    received = []
    bus.subscribe("billing", received.append)
    bus.publish("billing", {"amount": 25})
    assert received == [{"amount": 25}]
    bus.clear()
    bus.publish("billing", {"amount": 30})
    assert received == [{"amount": 25}]


def test_engine_routes_to_knowledge_agent(monkeypatch):
    engine = ResponseEngine()
    expected = ResponseFactory.success("knowledge", "Router instructions")
    monkeypatch.setattr(engine.triage, "route", lambda question: "knowledge")
    monkeypatch.setattr(engine.knowledge, "answer", lambda question: expected)
    response = engine.process(SupportRequest(1001, "How do I restart my router?"))
    assert response is expected
