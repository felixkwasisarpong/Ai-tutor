from sqlalchemy.orm import Session
from app.db.models.department import Department
from app.db.models.course import Course


def create_department_service(db: Session, payload):
    existing = db.query(Department).filter_by(code=payload.code).first()
    if existing:
        return existing

    department = Department(
        code=payload.code,
        name=payload.name,
        faculty=payload.faculty,
    )

    db.add(department)
    db.commit()
    db.refresh(department)
    return department


def create_course_service(db: Session, payload):
    department = db.query(Department).filter_by(
        code=payload.department_code
    ).first()

    if not department:
        raise ValueError("Department not found")

    existing = db.query(Course).filter_by(code=payload.code).first()
    if existing:
        return existing

    course = Course(
        code=payload.code,
        name=payload.name,
        department_id=department.id,
    )

    db.add(course)
    db.commit()
    db.refresh(course)
    return course