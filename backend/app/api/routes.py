# api end point here
from fastapi import APIRouter

from . import login
from . import logout
from . import refresh_token

api_router = APIRouter()
api_router.include_router(login.login_router)
api_router.include_router(logout.logout_router)
api_router.include_router(refresh_token.refresh_token_router)

