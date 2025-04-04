from typing import Set
from fastapi import WebSocket

class WebSocketManager:
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_message(self, message: str):
        for connection in list(self.active_connections):
            try: 
                await connection.send_text(message)
            except Exception:
                self.disconnect(connection)

    async def broadcast_new_user(self, message: str):
        await self.send_message(message)

websocket_manager = WebSocketManager()

