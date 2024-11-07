from fastapi import (APIRouter, WebSocket, WebSocketDisconnect, Depends, Query)

from backend.app.core.ws_manager import WSManager
from backend.app.core.database import get_db
from backend.app.core.exception import CredentialsException
from backend.app.core.auth import get_current_user
from backend.app.schema.user import UserPrivate


web_socket_router = APIRouter()


@web_socket_router.websocket("/ws")
async def ws_endpoint(ws: WebSocket, Authorization: str = Query(""),
                      db = Depends(get_db)):

    if Authorization == "":
        raise CredentialsException

    ws_manager = WSManager()
    token = Authorization.split(" ")[1]
    user = await get_current_user(token, db)
    user_id = user.id

    try:
        await ws.accept()
        await ws.send_text("helo")
        ws_manager.add_ws({user_id: ws})

        # Maintain WebSocket
        while True:
            print(await ws.receive_text())

    except WebSocketDisconnect:
        print("Client disconnected")
        await ws.close()
        ws_manager.remove_ws(user_id)

    except Exception as e:
        print(f"An error occurred: {e}")
        await ws.close()
        ws_manager.remove_ws(user_id)