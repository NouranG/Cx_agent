from agents.triage import TriageAgent

agent = TriageAgent()

questions = [

    "How much is my bill?",

    "Why is my internet slow?",

    "How do I restart my router?",

    "Can I enable autopay?",

    "There is no internet.",

    "How do I install my modem?"
]

for q in questions:

    print(q)

    print(agent.route(q))

    print("-" * 50)