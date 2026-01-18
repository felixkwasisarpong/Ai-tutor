from pydantic import BaseModel, Field
from uuid import UUID,uuid4


class DepartmentBase(BaseModel):
    name: str = Field (..., example="Engineering")
    description: str | None = Field (..., example="School of Engineering")


class DepartmentCreate(DepartmentBase):
    pass


class Department(DepartmentBase):
    id: UUID = Field (default_factory=uuid4)

    class Config:
        from_attributes = True