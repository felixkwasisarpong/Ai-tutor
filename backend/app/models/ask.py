from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    question: str = Field(..., example="What is the capital of France?")
    course_code: Optional[str] = None
