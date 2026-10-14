"""Core smoke tests retained in the core package for compatibility."""
from core.message_bus import MessageBus
from core.response import ResponseFactory


def test_message_bus_dispatches_event():
    bus = MessageBus()
    received = []
    bus.subscribe("billing", received.append)
    bus.publish("billing", {"customer_id": 1001})
    assert received == [{"customer_id": 1001}]


def test_response_factory_success_and_failure():
    success = ResponseFactory.success("billing", "Bill retrieved")
    failure = ResponseFactory.failure("billing", "Customer not found")
    assert success.success is True
    assert failure.success is False
