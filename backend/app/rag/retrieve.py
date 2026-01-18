from app.rag.store import vector_store
from typing import Optional


def retrieve_context(query: str, course_code: str | None = None):
    if course_code:
        print(f"RAG: filtered to course={course_code}")
        return vector_store.search(
            query,
            filters={"course_code": course_code},
        )

    return vector_store.search(query)