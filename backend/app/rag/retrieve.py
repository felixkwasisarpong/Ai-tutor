from app.rag.store import vector_store
from typing import Optional


def retrieve_context(
    query: str,
    *,
    course: Optional[str] = None,
    k: int = 3,
) -> str:
    results = vector_store.search(query, k=k)

    if course:
        filtered = []
        for text, meta in zip(
            vector_store.texts, vector_store.metadatas
        ):
            if meta.get("course") == course:
                filtered.append(text)

        if filtered:
            print(f"RAG: filtered to course={course}")
            return "\n\n".join(filtered[:k])

    return "\n\n".join(r["text"] for r in results)
