from typing import List
from app.memory.models import MemoryEntry



def summarize_intent(memory: List[MemoryEntry]) -> str | None:
    if not memory:
        return None
    last = memory[-1]

    if last.follow_up == "clarify_or_general":
        return "User is seeking clarification on a previous concept"
    
    return None