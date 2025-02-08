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
        disconnected_clients = []
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except WebSocketDisconnect:
                disconnected_clients.append(connection)

        # Remove disconnected clients
        for client in disconnected_clients:
            self.disconnect(client)

    async def send_message(self, websocket: WebSocket, message: str):
        """Sends a message to a specific WebSocket client."""
        await websocket.send_text(message)

# Instantiate the connection manager to handle WebSocket connections
manager = ConnectionManager()

@websocket_router.websocket("/chat/{room_id}")
async def chat_websocket(websocket: WebSocket, room_id: int):
    """
    WebSocket endpoint for a chat room.
    
    - Each client connects to a specific chat room using `room_id`.
    - Messages received from one client are broadcasted to all connected clients.
    - The application replies with the same message.
    """
    await manager.connect(websocket)
    print(f"New connection to room {room_id}")  

    try:
        while True:
            data = await websocket.receive_text()  # Receive message from the client
            print(f"Received message in room {room_id}: {data}")

            # Broadcast the user's message to all clients
            await manager.broadcast(f"User: {data}")

            # Application replies with the same message after a short delay (simulating an AI bot)
            bot_response = f"Bot: {data}"  # Simulated chatbot response
            await manager.send_message(websocket, bot_response)  

    except WebSocketDisconnect:
        manager.disconnect(websocket)  # Handle client disconnection
        print(f"Disconnected from room {room_id}")  
