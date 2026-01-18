from typing import TypedDict, Literal, Optional

class AgentState(TypedDict):
    question: str
    use_rag: bool
    context: Optional[str]
    decision_reason: Optional[str]
    answer: Optional[str]
    course_hint: Optional[str]