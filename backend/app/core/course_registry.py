from uuid import UUID, uuid4

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


def get_course_by_code(course_code: str):
    course = COURSES.get(course_code.upper())
    if not course:
        raise ValueError(f"Unknown course code: {course_code}")
    return course