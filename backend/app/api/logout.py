from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse

from backend.app.core.exception import NotLogin

logout_router = APIRouter()

@logout_router.post("/logout")
async def auth_logout(request: Request):

    token = request.cookies.get("token")
    if not token:
        raise NotLogin

    response = JSONResponse({"message": "Logout!"})
    response.delete_cookie("token")
    response.delete_cookie("refresh_token")
    return response
