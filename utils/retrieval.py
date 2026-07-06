from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

VECTOR_STORE = Path("vector_store")


class Retriever:

    def __init__(self):

        embeddings = HuggingFaceEmbeddings(
            model_name="BAAI/bge-small-en-v1.5"
        )

        self.db = FAISS.load_local(
            str(VECTOR_STORE),
            embeddings,
            allow_dangerous_deserialization=True,
        )

    def retrieve(self, query: str, k: int = 4):

        docs = self.db.similarity_search(query, k=k)

        return docs

    def build_context(self, docs):

        context = ""

        for i, doc in enumerate(docs, 1):

            context += (
                f"\nDocument {i}\n"
                f"Source: {doc.metadata.get('source')}\n\n"
                f"{doc.page_content}\n\n"
            )

        return context