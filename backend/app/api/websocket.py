from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from backend.app.core.connectionmanager import manager
router = APIRouter()

@router.websocket("/ws/{client-id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket)
    try:
        while True:
            # lang nghe tu websocket (client co the gui thong bao hoac message cho phia server)
            data = await websocket.receive_text()
            await manager.send_message(f"Client {client_id} says: {data}", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"client {client_id} disconnected")