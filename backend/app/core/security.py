
import hashlib
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def _normalize_password(password: str) -> str:
    password_bytes = password.encode("utf-8")
    if len(password_bytes) <= 72:
        return password
    return hashlib.sha256(password_bytes).hexdigest()

def hash_password(password: str) -> str:
    return pwd_context.hash(_normalize_password(password))

def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(_normalize_password(password), password_hash)
