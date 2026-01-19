from sqlalchemy.orm import Session
from app.db.models import Course


def get_course_by_code(db: Session, code: str) -> Course | None:
    return db.query(Course).filter(Course.code == code).first()

def list_courses(db: Session) -> list[Course]:
    return db.query(Course).order_by(Course.code).all()