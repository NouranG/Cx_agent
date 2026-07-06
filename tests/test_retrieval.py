from utils.retrieval import Retriever

retriever = Retriever()

results = retriever.search(
    "How do I restart my router?"
)

for i, doc in enumerate(results, 1):
    print(f"\nResult {i}")
    print("-" * 40)
    print(doc.page_content[:500])
    print(doc.metadata)