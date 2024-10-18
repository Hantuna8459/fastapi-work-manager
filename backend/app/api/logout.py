from fastapi import APIRouter
from fastapi.responses import JSONResponse

from backend.app.core.exception import NotLogin

router = APIRouter()

@router.post("/logout")
async def logout():
    response = JSONResponse({"message": "Logout!"})
    return response