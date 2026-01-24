from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.models.user import User
from app.core.security import hash_password





def seed():
    db: Session = SessionLocal()

    admin = User(
        email="admin@aitutor.dev",
        password_hash=hash_password("admin123"),
        role="admin",
    )

    db.add(admin)
    db.commit()
    db.close()

if __name__ == "__main__":
    seed()