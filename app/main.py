from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from auth import auth_router
from websockets import websocket_router

app = FastAPI(debug=True)

# Set the correct path to your 'static' and 'templates' directories
current_dir = Path(__file__).resolve().parent
static_path = current_dir / "static"
templates_path = current_dir / "templates"

print(static_path)
print(templates_path)

# Mount static files
app.mount("/static", StaticFiles(directory=static_path), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory=templates_path)

# Include Routers
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(websocket_router, prefix="", tags=["WebSocket"])

# Home route to serve index.html
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

