from uuid import UUID, uuid4
from dataclasses import dataclass
from typing import Dict
@dataclass
class Course:
    id: str
    code: str
    name: str
    department: str

COURSES = {
    "CS5589": {
        "id": UUID("123e4567-e89b-12d3-a456-426614174000"),
        "department": "Engineering",
        "name": "Advanced Topics in Computer Science",
    },
    "ENGR-301": {
        "id": UUID("223e4567-e89b-12d3-a456-426614174001"),
        "department": "Engineering",
        "name": "Thermodynamics",
    },
}

_COURSE_REGISTRY: Dict[str, Course] = {
    "CS5589": Course(
        id=str(uuid4()),
        code="CS5589",
        name="Knowledge Representation",
        department="Computer Science",
    ),
    "CS5300": Course(
        id=str(uuid4()),
        code="CS5300",
        name="Advanced Operating Systems",
        department="Computer Science",
    ),
}

def get_all_courses():
    # today
    return list(_COURSE_REGISTRY.values())

    # later
    return db.query(Course).all()


def get_course_by_code(course_code: str):
    course = COURSES.get(course_code.upper())
    if not course:
        raise ValueError(f"Unknown course code: {course_code}")
    return course