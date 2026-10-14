from agents.knowledge_agent import KnowledgeAgent


def test_knowledge_agent_returns_answer_and_source(monkeypatch):
    agent = KnowledgeAgent()
    monkeypatch.setattr(agent.llm, "generate", lambda *_: "Restart the router.")
    response = agent.answer("How do I restart my router?")
    assert response.success is True
    assert response.message == "Restart the router."
    assert response.data["sources"] == ["test-guide.md"]
    assert response.data["documents"] == 1


def test_knowledge_agent_handles_no_retrieved_documents(monkeypatch):
    agent = KnowledgeAgent()
    monkeypatch.setattr(agent.retriever, "retrieve", lambda *args, **kwargs: [])
    response = agent.answer("Unknown topic")
    assert response.success is False
    assert "couldn't find" in response.message.lower()
