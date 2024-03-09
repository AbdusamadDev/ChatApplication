from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI

from backend.server import WebSocketServer
from api.router import router

import asyncio
import logging

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="./static"), name="static")
app.include_router(router)
if __name__ == "__main__":
    server = WebSocketServer(addr=("0.0.0.0", 8000))
    server.run()
