from app.rag.store import VectorStore

vector_store = VectorStore()

def retrieve_context(query: str) -> list[str]:
    results = vector_store.search(query)
    return "\n\n".join(results)