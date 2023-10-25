import socket
import uvicorn
import asyncio
import threading
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


class AuthRequest(BaseModel):
    teamName: str
    teamID: str
    apiKey: str


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

__auth_callback = None

@app.get('/')
def home():
    return "Hi!"

@app.post('/auth')
def auth(request: AuthRequest):
    __auth_callback(request.model_dump())
    return JSONResponse(content={})

def get_available_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))            # Bind to a port not in use
        return s.getsockname()[1]  # Return the port number
    
def start_server(auth_callback):
    global __auth_callback
    __auth_callback = auth_callback
    port = get_available_port()
    config = uvicorn.Config(
        app="banana_cli.server:app",
        host="0.0.0.0", 
        port=port,
        reload=False, 
        log_level="error", # error, warning, info, debug, trace
        workers=1,
        # limit_concurrency=1, 
        # limit_max_requests=1
    )

    server = ThreadedUvicorn(config)
    server.start()
    return server, port
    
# https://github.com/encode/uvicorn/discussions/1103
class ThreadedUvicorn:
    def __init__(self, config: uvicorn.Config):
        self.server = uvicorn.Server(config)
        self.thread = threading.Thread(daemon=True, target=self.server.run)

    def start(self):
        self.thread.start()
        asyncio.run(self.wait_for_started())

    async def wait_for_started(self):
        while not self.server.started:
            await asyncio.sleep(0.1)

    def stop(self):
        if self.thread.is_alive():
            self.server.should_exit = True
            while self.thread.is_alive():
                continue
