from typing import List, Dict, Optional
from app.rag.store import vector_store



from typing import Optional, List, Dict


def retrieve_context(
    query: str,
    course_code: Optional[str] = None,
    k: int = 3,
) -> Dict:
    """
    Retrieve relevant RAG chunks for a query.

    Returns:
    {
        "chunks": List[Dict],
        "confidence": str
    }
    """

    filters = None
    if course_code:
        filters = {"course_code": course_code}
        print(f"RAG: filtered to course={course_code}")

    # NOTE: vector_store.search does NOT support top_k
    results = vector_store.search(
        query=query,
        k=k,
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

    # 🔢 Deterministic confidence heuristic
    if len(context) >= 3:
        confidence = "high"
    elif len(context) == 2:
        confidence = "medium"
    elif len(context) == 1:
        confidence = "low"
    else:
        confidence = "none"

    if context:
        sample = context[0].get("metadata", {}).get("course_code")
        print(f"RAG: retrieved {len(context)} chunks; sample course_code={sample!r}")

    return {
        "chunks": context,
        "confidence": confidence,
    }
