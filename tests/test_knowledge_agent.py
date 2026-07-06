from agents.knowledge_agent import KnowledgeAgent

agent = KnowledgeAgent()

response = agent.answer(
    "How do I restart my router?"
)

print("=" * 80)
print("QUESTION")
print(response.question)

print("=" * 80)
print("ANSWER")
print(response.answer)

print("=" * 80)
print("SOURCES")
for source in response.sources:
    print(source)