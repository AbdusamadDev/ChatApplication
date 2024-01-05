from websockets.exceptions import ConnectionClosedOK, ConnectionClosedError
from datetime import datetime
import websockets
import asyncio
import logging


class WebSocketServer:
    def __init__(self, addr: tuple) -> None:
        self.addr = addr
        self.clients = set()

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
                if input_client.open:
                    data = await input_client.recv()
                else:
                    self.disconnect(input_client)
                for client in self.clients:
                    await client.send(data)
            except RuntimeError as error:
                print(error)
                print("Number of clients: ", len(self.clients))

    async def handle_server(self, websocket, path):
        await self.connect(websocket)
        while True:
            try:
                await self.communicate(websocket)
            except (ConnectionClosedError, ConnectionClosedOK):
                self.disconnect(websocket)
                # Save messages to database
                continue

    def run(self):
        run_server = websockets.serve(self.handle_server, *self.addr)
        logging.info(f"Websocket server started running on {self.addr}")
        logging.info("Ctrl+c to get out of loop")
        asyncio.get_event_loop().run_until_complete(run_server)
        asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    server = WebSocketServer(addr=("0.0.0.0", 8000))
    server.run()
