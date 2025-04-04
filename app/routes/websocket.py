from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from ..websocket_manager import websocket_manager

router = APIRouter()



@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)