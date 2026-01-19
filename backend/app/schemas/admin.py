from pydantic import BaseModel


class DepartmentCreate(BaseModel):
    code: str
    name: str
    faculty: str    


class CourseCreate(BaseModel):
    code: str
    name: str
    department_code: str