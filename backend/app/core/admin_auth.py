from fastapi import HTTPException,Header,status
import os
ADMIN_API_KEY = os.getenv("ADMIN_API_KEY")

def require_admin(x_admin_api_key: str = Header(...)):
    if ADMIN_API_KEY is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Admin API key is not configured.",
        )
    if x_admin_api_key != ADMIN_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Admin API key.",
        )
    return x_admin_api_key
