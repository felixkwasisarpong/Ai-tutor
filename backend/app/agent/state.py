from typing import TypedDict, Optional

class AgentState(TypedDict):
    question: str
    use_rag: bool
    context: Optional[str]
    answer: Optional[str]