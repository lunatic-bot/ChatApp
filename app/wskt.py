from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List

# Create a FastAPI router specifically for WebSocket connections
websocket_router = APIRouter()

class ConnectionManager:
    """Manages WebSocket connections and broadcasting messages to connected clients."""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []  # List to store active WebSocket connections

    async def connect(self, websocket: WebSocket):
        """Accepts a new WebSocket connection and adds it to the active connections list."""
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        """Removes a WebSocket connection from the active connections list when it disconnects."""
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        """
        Sends a message to all active WebSocket connections.
        If a connection is disconnected, it removes it from the active connections list.
        """
        disconnected_clients = []  # List to track disconnected clients
        for connection in self.active_connections:
            try:
                await connection.send_text(message)  # Send the message to the client
            except WebSocketDisconnect:
                disconnected_clients.append(connection)  # Mark disconnected clients
        
        # Remove all disconnected clients from the active connections list
        for client in disconnected_clients:
            self.disconnect(client)

# Instantiate the connection manager to handle WebSocket connections
manager = ConnectionManager()

@websocket_router.websocket("/chat/{room_id}")
async def chat_websocket(websocket: WebSocket, room_id: int):
    """
    WebSocket endpoint for a chat room.
    
    - Each client connects to a specific chat room using `room_id`.
    - Messages received from one client are broadcasted to all connected clients.
    """
    await manager.connect(websocket)  # Establish connection
    print(f"New connection to room {room_id}")  

    try:
        while True:
            data = await websocket.receive_text()  # Receive message from the client
            print(f"Received message in room {room_id}: {data}")  
            await manager.broadcast(f"Room {room_id}: {data}")  # Broadcast message to all clients
    except WebSocketDisconnect:
        manager.disconnect(websocket)  # Handle client disconnection
        print(f"Disconnected from room {room_id}")  
