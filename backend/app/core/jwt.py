from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
import os

JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret")
JWT_ALGORITHM = "HS256"
JWT_EXP_MINUTES = 60


def create_access_token(data: dict) -> str:
    """
    Create a signed JWT access token.

    Required fields in data:
    - sub: user identifier (email)
    - role: 'admin' | 'student'
    """
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(minutes=JWT_EXP_MINUTES)
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_access_token(token: str) -> Optional[dict]:
    """
    Decode and validate a JWT access token.
    Returns payload if valid, else None.
    """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

        # 🔐 Enforce required claims
        if "sub" not in payload or "role" not in payload:
            return None

        return payload

    except JWTError:
        return None