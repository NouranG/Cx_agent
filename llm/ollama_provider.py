from ollama import Client

from llm.provider import LLMProvider


class OllamaProvider(LLMProvider):

    def __init__(
        self,
        model: str = "llama3.1:8b",
        host: str = "http://localhost:11434",
    ):
        self.client = Client(host=host)
        self.model = model

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> str:

        response = self.client.chat(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
        )

        return response["message"]["content"]