from datetime import datetime
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from typing import Literal


DocumentType = Literal["lecture", "slides", "notes", "exam", "other"]    
class DocumentBase(BaseModel):
    title: str = Field(..., example="Lecture 1 - Entropy")
    type: DocumentType = Field(default="lecture", example="lecture")


class DocumentCreate(DocumentBase):
    course_id: UUID


class Document(DocumentBase):
    id: UUID = Field(default_factory=uuid4)
    course_id: UUID
    filename: str
    uploaded_at: datetime | None = None

    class Config:
        from_attributes = True
