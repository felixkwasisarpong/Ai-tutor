from typing import TypedDict, Literal, Optional

class AgentState(TypedDict):
    question: str
    force_rag: bool
    course_code: Optional[str]
    course_id: Optional[str]
    use_rag: Optional[bool]
    decision_reason: Optional[str]
    answer: Optional[str]
    source: Optional[str]
    citations: Optional[list[dict]]
