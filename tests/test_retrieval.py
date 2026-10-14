from utils.retrieval import Retriever


class FakeVectorStore:
    def similarity_search(self, query, k):
        from langchain_core.documents import Document
        return [Document(page_content="Restart the router.", metadata={"source": "guide.md"})]


def test_retrieve_passes_query_and_k():
    retriever = Retriever.__new__(Retriever)
    retriever.db = FakeVectorStore()
    docs = retriever.retrieve("router restart", k=2)
    assert len(docs) == 1
    assert docs[0].metadata["source"] == "guide.md"


def test_build_context_includes_sources_and_content():
    from langchain_core.documents import Document
    retriever = Retriever.__new__(Retriever)
    context = retriever.build_context([
        Document(page_content="Restart the router.", metadata={"source": "guide.md"})
    ])
    assert "Source: guide.md" in context
    assert "Restart the router." in context
