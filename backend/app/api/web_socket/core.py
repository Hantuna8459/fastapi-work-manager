from fastapi import APIRouter

from .web_socket import web_socket_router


ws_router = APIRouter(prefix="", tags=["web_socket"])
ws_router.include_router(web_socket_router)