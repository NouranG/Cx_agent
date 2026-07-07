#loading retreiver once
from utils.retrieval import Retriever

retriever = Retriever()

#loading ollama once
from llm.ollama_provider import OllamaProvider

llm = OllamaProvider()