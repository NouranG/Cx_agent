from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


VECTOR_DB = Path("vector_store")


class Retriever:

    def __init__(self):

        embeddings = HuggingFaceEmbeddings(
            model_name="BAAI/bge-small-en-v1.5"
        )

        self.db = FAISS.load_local(
            str(VECTOR_DB),
            embeddings,
            allow_dangerous_deserialization=True
        )

    def search(self, query, k=3):

        return self.db.similarity_search(query, k=k)