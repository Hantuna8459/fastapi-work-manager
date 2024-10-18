# api end point here
from fastapi import APIRouter

from . import register, email_test, login, logout

api_router = APIRouter()
api_router.include_router(register.router, tags=["accounts"])
api_router.include_router(login.router, tags=["accounts"])
api_router.include_router(logout.router, tags=["accounts"])
api_router.include_router(email_test.router, tags=["mailing"])