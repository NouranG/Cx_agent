from pathlib import Path

from langchain_community.document_loaders import (
    DirectoryLoader,
    TextLoader,
    PyPDFLoader,
)


class KnowledgeLoader:

    def __init__(self, knowledge_path="knowledge_base"):
        self.knowledge_path = Path(knowledge_path)

    def load_documents(self):

        documents = []

        text_loader = DirectoryLoader(
            self.knowledge_path,
            glob="**/*.md",
            loader_cls=TextLoader
        )

        pdf_loader = DirectoryLoader(
            self.knowledge_path,
            glob="**/*.pdf",
            loader_cls=PyPDFLoader
        )

        documents.extend(text_loader.load())

        try:
            documents.extend(pdf_loader.load())
        except Exception:
            pass

        return documents