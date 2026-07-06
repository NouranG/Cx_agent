from utils.retrieval import Retriever


class KnowledgeAgent:

    def __init__(self):

        self.retriever = Retriever()

    def answer(self, question: str):

        docs = self.retriever.retrieve(question)

        context = self.retriever.build_context(docs)

        return {
            "question": question,
            "context": context,
            "sources": [
                doc.metadata.get("source")
                for doc in docs
            ]
        }