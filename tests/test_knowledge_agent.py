from agents.knowledge_agent import KnowledgeAgent

agent = KnowledgeAgent()

response = agent.answer(
    "How do I restart my router?"
)

print(response["context"])