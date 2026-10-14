from agents.billing_agent import BillingAgent


class FakeDatabase:
    def get_customer(self, customer_id):
        return {"first_name": "Test", "last_name": "Customer", "internet_plan": "Basic",
                "autopay": 0, "account_status": "active"}

    def get_bill(self, customer_id):
        return {"amount": 45.0, "due_date": "2026-10-20", "status": "pending",
                "last_payment_date": "2026-09-20"}


def test_billing_agent_returns_structured_success(monkeypatch):
    agent = BillingAgent()
    agent.db = FakeDatabase()
    monkeypatch.setattr(agent.llm, "generate", lambda *_: "Your bill is 45.")
    response = agent.answer(1001, "How much is my bill?")
    assert response.success is True
    assert response.agent == "billing"
    assert response.message == "Your bill is 45."
    assert response.data["bill"]["amount"] == 45.0


def test_billing_agent_handles_missing_customer():
    agent = BillingAgent()
    class MissingDatabase:
        def get_customer(self, customer_id):
            return None
    agent.db = MissingDatabase()
    response = agent.answer(9999, "Check my bill")
    assert response.success is False
    assert response.message == "Customer not found."
