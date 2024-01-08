from websockets.exceptions import ConnectionClosedOK, ConnectionClosedError
from database.models import GlobalChatManager
from .exceptions import ValidationError
from datetime import datetime
from .client import Client
import websockets
import asyncio
import logging
import json


class WebSocketServer:
    def __init__(self, addr: tuple) -> None:
        self.addr = addr
        self.clients = set()
        self.database = GlobalChatManager()

    async def connect(self, client):
        logging.info(("Client connected: ", client))
        self.clients.add(client)

    async def recieve(self, client):
        return await client.recv()

    async def disconnect(self, websocket):
        self.clients.remove(websocket)

    async def communicate(self, input_client):
        while True:
            try:
                print("Target client life: ", input_client.open)
                print("Target client address: ", input_client.remote_address)
                print("Keeping alive: [%s]" % datetime.now())
                print("Number of clients: ", len(self.clients))
                print("Client addresses: ", self.clients)
                data = await input_client.recv()
                if "message" not in input_client.dict_message(data).keys():
                    error_message = {
                        "error": "validation_error",
                        "message": "The 'message' key is required.",
                    }
                    await input_client.send(json.dumps(error_message))
                    continue
                for client in self.clients:
                    await client.send_and_save(data)

            except RuntimeError as error:
                print(error)
                print("Number of clients: ", len(self.clients))

    async def handle_server(self, websocket: Client, path):
        await self.connect(websocket)
        while True:
            try:
                if websocket.open:
                    # Main and simple way to pass user to conversation
                    await self.communicate(websocket)
                else:
                    await self.disconnect(websocket)

            except (ConnectionClosedError, ConnectionClosedOK):
                if websocket in self.clients:
                    await self.disconnect(websocket)
                continue

    def run(self):
        run_server = websockets.serve(self.handle_server, *self.addr, klass=Client)
        logging.info(f"Websocket server started running on {self.addr}")
        logging.info("Ctrl+c to get out of loop")
        asyncio.get_event_loop().run_until_complete(run_server)
        asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    server = WebSocketServer(addr=("0.0.0.0", 8000))
    server.run()
