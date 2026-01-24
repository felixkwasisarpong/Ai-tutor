from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.models.user import User
from app.core.security import hash_password


def seed_student():
    db: Session = SessionLocal()

    email = "student@university.edu"

    exists = db.query(User).filter_by(email=email).first()
    if exists:
        print("Student already exists")
        return

    student = User(
        email=email,
        password_hash=hash_password("student123"),
        role="student",
    )

    db.add(student)
    db.commit()
    db.close()
    print("✅ Student seeded")


if __name__ == "__main__":
    seed_student()