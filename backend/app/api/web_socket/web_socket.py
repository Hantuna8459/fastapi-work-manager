from fastapi import (APIRouter, WebSocket, WebSocketDisconnect, Depends)

from ...core.ws_manager import user_ws
from ...core.auth import get_current_user
from ...schema.user import UserPrivate


web_socket_router = APIRouter()


@web_socket_router.websocket("")
async def ws_endpoint(ws: WebSocket,
                      user: UserPrivate = Depends(get_current_user)):

    user_id = user.id
    try:
        await ws.accept()
        user_ws.update({user_id: ws})

    except WebSocketDisconnect:
        print("Client disconnected")
        user_ws.pop(user_id)

    except Exception as e:
        print(f"An error occurred: {e}")
        await ws.close()
        user_ws.pop(user_id)