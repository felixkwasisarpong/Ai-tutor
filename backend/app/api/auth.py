

from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Form, Request
from sqlalchemy.orm import Session

from app.core.jwt import create_access_token
from app.core.security import verify_password
from app.db.deps import get_db
from app.db.models.user import User
from app.core.refresh import generarte_refresh_token, hash_refresh_token, refresh_token_expiry, hash_refresh_token
from app.db.models.refresh_token import RefreshToken


router = APIRouter(prefix="/auth", tags=["auth"])
@router.post("/login")
async def login(
    request: Request,
    db: Session = Depends(get_db),
):
    content_type = request.headers.get("content-type", "")
    email = None
    password = None

    if "application/json" in content_type:
        payload = await request.json()
        email = payload.get("email")
        password = payload.get("password")
    else:
        try:
            form = await request.form()
            email = form.get("email")
            password = form.get("password")
        except Exception:
            email = None
            password = None

    if not email or not password:
        query = request.query_params
        email = email or query.get("email")
        password = password or query.get("password")

    if not email or not password:
        raise HTTPException(status_code=422, detail="Email and password required")


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


@router.post("/refresh")
async def refresh_access_token(
    request: Request,
    db: Session = Depends(get_db),
):
    content_type = request.headers.get("content-type", "")
    refresh_token = None

    if "application/json" in content_type:
        payload = await request.json()
        refresh_token = payload.get("refresh_token")
    else:
        try:
            form = await request.form()
            refresh_token = form.get("refresh_token")
        except Exception:
            refresh_token = None

    if not refresh_token:
        refresh_token = request.query_params.get("refresh_token")

    if not refresh_token:
        raise HTTPException(status_code=422, detail="Refresh token required")

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


@router.post("/logout")
async def logout(
    request: Request,
    db: Session = Depends(get_db),
):
    content_type = request.headers.get("content-type", "")
    refresh_token = None

    if "application/json" in content_type:
        payload = await request.json()
        refresh_token = payload.get("refresh_token")
    else:
        try:
            form = await request.form()
            refresh_token = form.get("refresh_token")
        except Exception:
            refresh_token = None

    if not refresh_token:
        refresh_token = request.query_params.get("refresh_token")

    if not refresh_token:
        raise HTTPException(status_code=422, detail="Refresh token required")

    token_hash = hash_refresh_token(refresh_token)

    record = (
        db.query(RefreshToken)
        .filter_by(token_hash=token_hash, revoked=False)
        .first()
    )

    if not record:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    record.revoked = True
    db.commit()

    return {"message": "Logged out successfully"}
