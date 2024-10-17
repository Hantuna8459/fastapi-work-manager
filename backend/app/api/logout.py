from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from backend.app.core.exception import NotLogin

logout_router = APIRouter()

@logout_router.post("/logout")
async def auth_logout(request: Request):

    response = JSONResponse({"message": "Logout!"})
    return response