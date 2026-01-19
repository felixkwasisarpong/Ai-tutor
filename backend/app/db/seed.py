from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.models.course import Course

COURSES = [
    {
        "code": "CS5589",
        "name": "Knowledge Representation",
        "department": "Computer Science",
    },
]

def seed():
    db: Session = SessionLocal()

    for c in COURSES:
        exists = db.query(Course).filter_by(code=c["code"]).first()
        if exists:
            continue

        db.add(Course(**c))

    db.commit()
    db.close()
    print("✅ Courses seeded")

if __name__ == "__main__":
    seed()