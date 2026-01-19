from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.models.course import Course


COURSES = [
    {
        "code": "CS5589",
        "name": "Knowledge Representation",
        "department": "Computer Science",
    },
    {
        "code": "CS5300",
        "name": "Advanced Algorithms",
        "department": "Computer Science",
    },
    {
        "code": "PHY510",
        "name": "Thermodynamics",
        "department": "Physics",
    },
]


def seed_courses():
    db: Session = SessionLocal()

    try:
        for course_data in COURSES:
            existing = (
                db.query(Course)
                .filter(Course.code == course_data["code"])
                .first()
            )

            if existing:
                continue  # idempotent

            course = Course(**course_data)
            db.add(course)

        db.commit()
        print("Courses seeded successfully")

    finally:
        db.close()


if __name__ == "__main__":
    seed_courses()