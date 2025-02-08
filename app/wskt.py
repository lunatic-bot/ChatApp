from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from transformers import pipeline
from typing import List
import wikipediaapi

# Initialize FastAPI router
websocket_router = APIRouter()

# Load a small, efficient chatbot model from Hugging Face
chat_model = pipeline("text-generation", model="distilgpt2")

class ConnectionManager:
    """Handles WebSocket connections and broadcasting."""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """Accept and store WebSocket connections."""
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        """Remove disconnected WebSocket connections."""
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        """Send messages to all active WebSocket clients."""
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except WebSocketDisconnect:
                self.disconnect(connection)

    async def send_message(self, websocket: WebSocket, message: str):
        """Send a message to a specific WebSocket client."""
        await websocket.send_text(message)

manager = ConnectionManager()

# Initialize Wikipedia API
wiki_wiki = wikipediaapi.Wikipedia("en")

def search_wikipedia(query: str) -> str:
    """Search Wikipedia for the given query and return the summary."""
    page = wiki_wiki.page(query)
    if page.exists():
        return page.summary[:500]  # Return the first 500 characters
    return None  # Return None if no page is found

async def get_ai_response(user_message: str) -> str:
    """Generate response using Wikipedia if possible, otherwise use AI model."""
    
    # Check if the message is a factual question
    if "who is" in user_message.lower() or "what is" in user_message.lower():
        wiki_answer = search_wikipedia(user_message)
        if wiki_answer:
            return wiki_answer  # Return Wikipedia answer if found
    
    # If Wikipedia search fails, use AI model
    response = chat_model(user_message, max_length=50, do_sample=True)
    return response[0]["generated_text"]

# async def get_ai_response(user_message: str) -> str:
#     """Generate AI response using a local Hugging Face model."""
#     response = chat_model(user_message, max_length=50, do_sample=True)
#     return response[0]["generated_text"]

@websocket_router.websocket("/chat/{room_id}")
async def chat_websocket(websocket: WebSocket, room_id: int):
    """WebSocket endpoint for chat with AI bot."""
    await manager.connect(websocket)
    print(f"New connection to room {room_id}")

    try:
        while True:
            user_message = await websocket.receive_text()
            print(f"Received: {user_message}")

            # Broadcast user message to all clients
            await manager.broadcast(f"User: {user_message}")

            # Generate AI response
            ai_response = await get_ai_response(user_message)

            # Send AI response to the user
            await manager.send_message(websocket, f"Bot: {ai_response}")

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print(f"Disconnected from room {room_id}")


# from fastapi import APIRouter, WebSocket, WebSocketDisconnect
# from typing import List

# # Create a FastAPI router specifically for WebSocket connections
# websocket_router = APIRouter()

# class ConnectionManager:
#     """Manages WebSocket connections and broadcasting messages to connected clients."""
    
#     def __init__(self):
#         self.active_connections: List[WebSocket] = []  # List to store active WebSocket connections

#     async def connect(self, websocket: WebSocket):
#         """Accepts a new WebSocket connection and adds it to the active connections list."""
#         await websocket.accept()
#         self.active_connections.append(websocket)

#     def disconnect(self, websocket: WebSocket):
#         """Removes a WebSocket connection from the active connections list when it disconnects."""
#         self.active_connections.remove(websocket)

#     async def broadcast(self, message: str):
#         """
#         Sends a message to all active WebSocket connections.
#         If a connection is disconnected, it removes it from the active connections list.
#         """
#         disconnected_clients = []
#         for connection in self.active_connections:
#             try:
#                 await connection.send_text(message)
#             except WebSocketDisconnect:
#                 disconnected_clients.append(connection)

#         # Remove disconnected clients
#         for client in disconnected_clients:
#             self.disconnect(client)

#     async def send_message(self, websocket: WebSocket, message: str):
#         """Sends a message to a specific WebSocket client."""
#         await websocket.send_text(message)

# # Instantiate the connection manager to handle WebSocket connections
# manager = ConnectionManager()

# @websocket_router.websocket("/chat/{room_id}")
# async def chat_websocket(websocket: WebSocket, room_id: int):
#     """
#     WebSocket endpoint for a chat room.
    
#     - Each client connects to a specific chat room using `room_id`.
#     - Messages received from one client are broadcasted to all connected clients.
#     - The application replies with the same message.
#     """
#     await manager.connect(websocket)
#     print(f"New connection to room {room_id}")  

#     try:
#         while True:
#             data = await websocket.receive_text()  # Receive message from the client
#             print(f"Received message in room {room_id}: {data}")

#             # Broadcast the user's message to all clients
#             await manager.broadcast(f"User: {data}")

#             # Application replies with the same message after a short delay (simulating an AI bot)
#             bot_response = f"Bot: {data}"  # Simulated chatbot response
#             await manager.send_message(websocket, bot_response)  

#     except WebSocketDisconnect:
#         manager.disconnect(websocket)  # Handle client disconnection
#         print(f"Disconnected from room {room_id}")  
