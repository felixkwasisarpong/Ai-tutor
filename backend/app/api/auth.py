

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.jwt import create_access_token
from app.core.security import verify_password
from app.db.deps import get_db
from app.db.models.user import User


router = APIRouter(prefix="/auth", tags=["auth"])
@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
        )
    
    token = create_access_token(
        {"sub": str(user.id), "role": user.role}
    )
    return {"access_token": token, "token_type": "bearer", "user": user.role,}
