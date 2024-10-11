from fastapi import Depends, Request, APIRouter

from backend.app.core.auth import make_new_access_token
from backend.app.core.database import get_db

refresh_token_router = APIRouter()
@refresh_token_router.post("/refresh-token")
def refresh_access_token (request: Request, db = Depends(get_db)):
    new_access_token = make_new_access_token(request, db)
    return new_access_token