from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from agent import main_async
import threading
import sys
from io import StringIO

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class ConnectionManager:
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

@app.post("/start-analysis")
async def start_analysis():
    # Redirect stdout to a string buffer
    old_stdout = sys.stdout
    sys.stdout = redirected_output = StringIO()

    # Run the analysis in a separate thread
    thread = threading.Thread(target=asyncio.run, args=(main_async(),))
    thread.start()

    # Periodically send the output to the client
    while thread.is_alive():
        await asyncio.sleep(0.1)
        output = redirected_output.getvalue()
        if output:
            await manager.broadcast(output)
            redirected_output.truncate(0)
            redirected_output.seek(0)

    # Restore stdout
    sys.stdout = old_stdout

    # Get the final output and broadcast it
    output = redirected_output.getvalue()
    await manager.broadcast(output)

    return {"status": "success"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast("Client left the chat")

if __name__ == "__main__":
    import uvicorn
    import subprocess
    import os

    # Start the live-server as a subprocess
    frontend_dir = os.path.join(os.path.dirname(__file__), "frontend")
    live_server_command = ["live-server", frontend_dir]
    
    try:
        print("Starting live-server...")
        subprocess.Popen(live_server_command, shell=True)
    except FileNotFoundError:
        print("live-server command not found. Please ensure it is installed and in your PATH.")
        print("You can install it with: npm install -g live-server")
    except Exception as e:
        print(f"Failed to start live-server: {e}")

    # Start the uvicorn server
    uvicorn.run(app, port=8000)
