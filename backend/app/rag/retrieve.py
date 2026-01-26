from typing import List, Dict, Optional
from app.rag.store import vector_store



from typing import Optional, List, Dict


from typing import Optional, List, Dict
import logging

logger = logging.getLogger(__name__)

def retrieve_context(
    query: str,
    course_code: Optional[str] = None,
) -> Dict:
    """
    Retrieve relevant RAG chunks for a query.

    Returns:
    {
        "chunks": List[Dict],
        "confidence": str
    }
    """

    # 🔒 Hard retrieval policy
    filters = {"active": True}

    if course_code:
        filters["course_code"] = course_code.upper()
        logger.info(
            "RAG filter applied",
            extra={"course_code": filters["course_code"], "active": True},
        )

    # 🚫 No k / top_k here — vector store controls retrieval size
    results = vector_store.search(
        query=query,
        filters=filters,
    )

    chunks: List[Dict] = [
        {
            "text": r["text"],
            "metadata": r.get("metadata", {}),
        }
        for r in results
    ]

    # 🔢 Deterministic confidence heuristic
    match len(chunks):
        case n if n >= 3:
            confidence = "high"
        case 2:
            confidence = "medium"
        case 1:
            confidence = "low"
        case _:
            confidence = "none"

    if chunks:
        sample_course = chunks[0]["metadata"].get("course_code")
        logger.info(
            "RAG retrieved",
            extra={
                "chunks": len(chunks),
                "confidence": confidence,
                "sample_course": sample_course,
            },
        )

    return {
        "chunks": chunks,
        "confidence": confidence,
    }
