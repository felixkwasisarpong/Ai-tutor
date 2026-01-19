from pydantic import BaseModel, Field
from uuid import UUID,uuid4
from app.db.base import Base

class CourseBase(Base):
    code: str = Field(..., example="ENG-301")
    name: str = Field(..., example="Thermodynamics")
    semester: str = Field(..., example="Fall 2024")


class CourseCreate(CourseBase):
    department_id: str = UUID

class Course(CourseBase):
    id: UUID = Field(default_factory=uuid4)

    class Config:
        from_attributes = True