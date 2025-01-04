from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.database import Base, engine
from app.auth import auth_router
from app.websocket import websocket_router

app = FastAPI()

# Database Initialization
Base.metadata.create_all(bind=engine)

# Mount Static Files and Templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Include Routers
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(websocket_router, prefix="/ws", tags=["WebSocket"])
