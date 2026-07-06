from pathlib import Path

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

VECTOR_STORE = Path("vector_store")


class EmbeddingBuilder:

    def __init__(self):

        self.embedding_model = HuggingFaceEmbeddings(
            model_name="BAAI/bge-small-en-v1.5"
        )

    def build(self, chunks):

        db = FAISS.from_documents(
            chunks,
            self.embedding_model,
        )

        VECTOR_STORE.mkdir(exist_ok=True)

        db.save_local(str(VECTOR_STORE))