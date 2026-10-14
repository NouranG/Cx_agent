from agents.technical_agent import TechnicalAgent


class FakeDatabase:
    def get_network_status(self, customer_id):
        return {"internet_status": "offline", "router_status": "online",
                "signal_strength": 40, "outage": 0}


def test_technical_agent_uses_network_and_retrieval(monkeypatch):
    agent = TechnicalAgent()
    agent.db = FakeDatabase()
    monkeypatch.setattr(agent.llm, "generate", lambda *_: "Try restarting your router.")
    response = agent.answer(1001, "My internet is slow")
    assert response.success is True
    assert response.agent == "technical"
    assert response.message == "Try restarting your router."
    assert response.data["network"]["internet_status"] == "offline"
    assert response.data["sources"] == ["test-guide.md"]
