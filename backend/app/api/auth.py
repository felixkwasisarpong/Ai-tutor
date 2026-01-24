

from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.jwt import create_access_token
from app.core.security import verify_password
from app.db.deps import get_db
from app.db.models.user import User
from app.core.refresh import generarte_refresh_token, hash_refresh_token, refresh_token_expiry, hash_refresh_token
from app.db.models.refresh_token import RefreshToken


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
    refresh_token = generarte_refresh_token()

    db.add(
        RefreshToken(
            user_id=user.id,
            token_hash=hash_refresh_token(refresh_token),
            expires_at=refresh_token_expiry(),
        )
    )
    db.commit()
    return {
        "access_token": token,
        "refresh_token": refresh_token,
    }


@router.post("/auth/refresh")
def refresh_access_token(
    refresh_token: str,
    db: Session = Depends(get_db),
):
    token_hash = hash_refresh_token(refresh_token)

    record = (
        db.query(RefreshToken)
        .filter_by(token_hash=token_hash, revoked=False)
        .first()
    )

    if not record or record.expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    user = db.query(User).get(record.user_id)

    access_token = create_access_token({
        "sub": user.email,
        "role": user.role,
    })

    return {"access_token": access_token}