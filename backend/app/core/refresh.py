

import datetime
import hashlib
import secrets

REFRESH_TOKEN_TTL_DAYS = 7
def generarte_refresh_token() -> str:
    return secrets.token_urlsafe(32)

def hash_refresh_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()

def refresh_token_expiry() -> int:
    return datetime.datetime.utcnow() + datetime.timedelta(days=REFRESH_TOKEN_TTL_DAYS)