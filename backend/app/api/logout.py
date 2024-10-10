from fastapi import Request
from fastapi.responses import JSONResponse
from backend.app.api.exception import NotLogin

from backend.app.api.routes import auth_router

@auth_router.get("logout")
async def auth_logout(request: Request):

    token = request.cookies.get("token")
    if not token:
        raise NotLogin
    
    response = JSONResponse({"message": "Logout!"})
    response.delete_cookie("token")
    response.delete_cookie("refresh_token")
    return response
