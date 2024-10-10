from passlib.context import CryptContext
from backend.app.core.config import settings


pwd_context= CryptContext(schemes=[settings.CRYPTCONTEXT_SCHEME], deprecated="auto")


def get_hashed_password(password:str):
    return pwd_context.hash(password)

def verify_password(password:str, user_password:str):
    return pwd_context.verify(password, user_password)   