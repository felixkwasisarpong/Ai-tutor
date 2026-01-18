from typing import List, Dict, Optional
from app.rag.store import vector_store



def retrieve_context(
    query: str,
    course_code: Optional[str] = None,
) -> List[Dict]:
    """
    Retrieve relevant RAG chunks for a query.

    Returns a list of dicts:
    {
        "text": str,
        "metadata": dict
    }
    """

    filters = None
    if course_code:
        filters = {"course_code": course_code}
        print(f"RAG: filtered to course={course_code}")

    # NOTE: vector_store.search does NOT support top_k
    results = vector_store.search(
        query=query,
        filters=filters,
    )

    context: List[Dict] = []
    for r in results:
        context.append(
            {
                "text": r["text"],
                "metadata": r.get("metadata", {}),
            }
        )

    return context