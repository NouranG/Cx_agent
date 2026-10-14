from agents.triage import TriageAgent


def test_triage_normalizes_valid_route(monkeypatch):
    agent = TriageAgent()
    monkeypatch.setattr(agent.llm, "generate", lambda *_: " BILLING\n")
    assert agent.route("How much is my bill?") == "billing"


def test_triage_falls_back_for_invalid_route(monkeypatch):
    agent = TriageAgent()
    monkeypatch.setattr(agent.llm, "generate", lambda *_: "unexpected")
    assert agent.route("An ambiguous question") == "knowledge"
