from typing import Dict, List, TypedDict, Literal, Optional
from pydantic import BaseModel


class VerifiedContext(BaseModel):
    course_code: str
    chunks: list[Dict]
    expires_at: float

class AgentState(BaseModel):
    question: str
    course_code: Optional[str] = None

    # Routing
    force_rag: bool = False
    use_rag: Optional[bool] = None
    decision_reason: Optional[str] = None

    # RAG output
    context: Optional[List[Dict]] = None
    confidence: Optional[str] = None

    # ✅ NEW: follow-up safe memory
    verified_context: Optional[VerifiedContext] = None

    # Final output
    answer: Optional[str] = None
    citations: Optional[List[Dict]] = None
    source: Optional[str] = None
