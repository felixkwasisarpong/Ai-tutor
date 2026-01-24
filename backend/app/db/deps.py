from fastapi.security import OAuth2PasswordBearer
from app.db.session import SessionLocal
from fastapi import Depends, HTTPException, status
from app.core.jwt import decode_access_token

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload


def require_student(user=Depends(get_current_user)):
    if user["role"] not in {"student", "admin"}:
        raise HTTPException(status_code=403, detail="Forbidden")
    return user


def require_admin(user=Depends(get_current_user)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    return user