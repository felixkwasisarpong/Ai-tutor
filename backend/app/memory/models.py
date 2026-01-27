from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class MemoryEntry(BaseModel):
    question: str
    course_code: Optional[str]
    confidence: Optional[str]
    follow_up: Optional[str]
    timestamp: datetime
