from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List

websocket_router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()


@websocket_router.websocket("/chat/{room_id}")
async def chat_websocket(websocket: WebSocket, room_id: int):
    await manager.connect(websocket)
    print(f"New connection to room {room_id}")  # Log for debugging
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received message in room {room_id}: {data}")  # Log for debugging
            await manager.broadcast(f"Room {room_id}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print(f"Disconnected from room {room_id}")  # Log for debugging


