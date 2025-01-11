from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from database import Base, async_engine

# from database import init_db
from auth import auth_router
from websocket import websocket_router
from pathlib import Path

app = FastAPI(debug=True)

# Database Initialization
# Base.metadata.create_all(bind=engine)

# async def init_db():
#     # Run create_all within an async context
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

# init_db()


# Set the correct path to your 'static' and 'templates' directories
current_dir = Path(__file__).resolve().parent
static_path = current_dir / "static"
templates_path = current_dir / "templates"

# Mount static files
app.mount("/static", StaticFiles(directory=static_path), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory=templates_path)
# Mount Static Files and Templates
# app.mount("/static", StaticFiles(directory="/static"), name="static")
# templates = Jinja2Templates(directory="/templates")

# Include Routers
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(websocket_router, prefix="/ws", tags=["WebSocket"])
