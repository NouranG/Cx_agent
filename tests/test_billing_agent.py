from agents.billing_agent import BillingAgent

agent = BillingAgent()

response = agent.answer(
    customer_id=1003,
    question="Why is my account suspended and how much do I owe?"
)

print(response.answer)