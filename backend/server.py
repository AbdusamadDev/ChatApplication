from websockets.exceptions import ConnectionClosedOK, ConnectionClosedError
from datetime import datetime
import websockets
import asyncio
import json


class WebSocketServer:
    def __init__(self, addr: tuple) -> None:
        self.addr = addr
        self.clients = set()

    async def connect(self, client):
        self.clients.add(client)

    async def recieve(self, client):
        return await client.recv()

    async def communicate(self, input_client):
        while True:
            for client in self.clients:
                print("Client: ", client)
                await client.send(str(await input_client.recv()))

    async def handle_server(self, websocket, path):
        await self.connect(websocket)
        while True:
            await websocket.send(
                json.dumps(
                    {
                        "chat_id": "chat id",
                        "messages": {"user a": "wassup", "user b": "nothin much"},
                    }
                )
            )
            try:
                # while True:
                print("Keeping alive: [%s]" % datetime.now())
                print("Number of clients: ", len(self.clients))
                print("Client addresses: ", self.clients)
                await self.communicate(websocket)
            except (ConnectionClosedError, ConnectionClosedOK):
                continue

    def run(self):
        run_server = websockets.serve(self.handle_server, "192.168.100.39", 8000)
        asyncio.get_event_loop().run_until_complete(run_server)
        asyncio.get_event_loop().run_forever()
        # websockets.WebSocketServer.


server = WebSocketServer(tuple())
server.run()
