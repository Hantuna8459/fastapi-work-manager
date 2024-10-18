from passlib.context import CryptContext
from backend.app.core.config import settings


pwd_context= CryptContext(schemes=[settings.CRYPTCONTEXT_SCHEME], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_hashed_password(password: str) -> str:
    return pwd_context.hash(password)