"""
FastAPI server for FRC Video Referee application.
"""

from pathlib import Path
import logging

from fastapi import FastAPI, Depends, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import uvicorn
from pydantic import BaseModel

logger = logging.getLogger(__name__)

# Simple password-based authentication
security = HTTPBasic()
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password"  # TODO: Move to environment variable


class ServerSettings(BaseModel, use_attribute_docstrings=True):
    """Settings for the web server."""

    host: str = "0.0.0.0"
    port: int = 8000


def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    """Simple password-based authentication."""
    if credentials.username != ADMIN_USERNAME or credentials.password != ADMIN_PASSWORD:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


def get_static_directory() -> Path:
    """Get the static directory for serving assets."""
    # For development, serve from workspace static folder
    dev_static = Path(__file__).parent.parent.parent / "static"
    if dev_static.exists():
        return dev_static

    # For installed package, serve from package static folder
    package_static = Path(__file__).parent / "static"
    if package_static.exists():
        return package_static

    # If neither exists, raise an error
    raise RuntimeError(
        "Static assets directory not found. "
        "For development, ensure 'static/' directory exists in workspace. "
        "For installed package, static assets should be embedded."
    )


# Create FastAPI app
app = FastAPI(
    title="FRC Video Referee",
    description="Video analysis and referee assistance for FRC competitions",
    version="0.1.0",
)

# Set up static files
static_dir = get_static_directory()
app.mount("/static", StaticFiles(directory=static_dir), name="static")


class ConnectionManager:
    """Manages WebSocket connections."""

    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main application page."""
    index_file = static_dir / "index.html"
    return HTMLResponse(content=index_file.read_text(encoding="utf-8"))


@app.get("/api/status")
async def get_status(current_user: str = Depends(get_current_user)):
    """Get application status (requires authentication)."""
    return {"status": "running", "user": current_user}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates."""
    await manager.connect(websocket)
    try:
        while True:
            # Wait for messages from client
            data = await websocket.receive_text()

            # Echo the message back (placeholder functionality)
            await manager.send_personal_message(f"Echo: {data}", websocket)

            # Broadcast to all connected clients
            await manager.broadcast(f"Broadcast: {data}")

    except WebSocketDisconnect:
        manager.disconnect(websocket)


async def run(settings: ServerSettings) -> None:
    """Run the FastAPI server."""
    config = uvicorn.Config(
        "frc_video_referee.server:app",
        host=settings.host,
        port=settings.port,
    )
    server = uvicorn.Server(config)
    await server.serve()
