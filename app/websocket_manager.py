from typing import Set
from fastapi import WebSocket

class WebSocketManager:
    """
    Manages WebSocket connections and handles broadcasting messages to connected clients.
    """
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket):
        """
        Accept a new WebSocket connection and add it to the set of active connections.

        Args:
            websocket (WebSocket): The WebSocket connection to add
        """
        await websocket.accept()
        self.active_connections.add(websocket)

    def disconnect(self, websocket: WebSocket):
        """
        Remove a WebSocket connection from the set of active connections.

        Args:
            websocket (WebSocket): The WebSocket connection to remove
        """
        self.active_connections.remove(websocket)

    async def send_message(self, message: str):
        """
        Send a message to all connected clients.
        If sending fails for a client, that connection is removed.

        Args:
            message (str): The message to broadcast to all clients
        """
        for connection in list(self.active_connections):
            try: 
                await connection.send_text(message)
            except Exception:
                self.disconnect(connection)

    async def broadcast_new_user(self, message: str):
        """
        Broadcast a new user notification to all connected clients.

        Args:
            message (str): The notification message about the new user
        """
        await self.send_message(message)

websocket_manager = WebSocketManager()
