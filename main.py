from core.api_gateway import APIGateway


gateway = APIGateway()

customer_id = 1001

print("ISP Customer Support")
print("Type 'exit' to quit.\n")

while True:

    question = input("> ")

    if question.lower() == "exit":
        break

    response = gateway.process_request(
    {
        "customer_id": customer_id,
        "message": question,
    }
)

    print("\nAssistant:\n")

    print(response.message)

    print("\n" + "=" * 80 + "\n")