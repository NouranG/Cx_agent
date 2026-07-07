from agents.technical_agent import TechnicalAgent

agent = TechnicalAgent()

response = agent.answer(
    1002,
    "Why is my internet down?"
)

print(response.answer)