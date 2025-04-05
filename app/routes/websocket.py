from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from ..websocket_manager import websocket_manager

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time notifications.
    
    Args:
        websocket: WebSocket connection instance
        
    Maintains an active WebSocket connection and handles disconnects.
    Used for broadcasting user registration notifications.
    """
    await websocket_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)