from websockets.exceptions import ConnectionClosedOK, ConnectionClosedError
from datetime import datetime
import websockets
import asyncio

# import logging


class WebSocketServer:
    def __init__(self, addr: tuple) -> None:
        # logging.basicConfig(level=logging.DEBUG)
        self.addr = addr
        self.clients = set()

    async def connect(self, client):
        self.clients.add(client)

    async def recieve(self, client):
        return await client.recv()

    async def disconnect(self, websocket):
        self.clients.remove(websocket)

    async def communicate(self, input_client):
        while True:
            try:
                data = await input_client.recv()
                # print("Number of clients: ", len(self.clients))
                for client in self.clients:
                    # if client.remote_address[0] != input_client.remote_address[0]:
                    # if client.open:
                        await client.send()
                        print(client.open, client.remote_address)
                    # else:
                        # await self.disconnect(client)
                    # break
            except RuntimeError as error:
                print(error)
                print("Number of clients: ", len(self.clients))

    async def handle_server(self, websocket, path):
        await self.connect(websocket)
        while True:
            try:
                print("Keeping alive: [%s]" % datetime.now())
                print("Number of clients: ", len(self.clients))
                print("Client addresses: ", self.clients)
                for i in self.clients:
                    print(i.open, i.remote_address)
                await self.communicate(websocket)
            except (ConnectionClosedError, ConnectionClosedOK):
                continue

    def run(self):
        # websockets.WebSocketServerProtocol.
        run_server = websockets.serve(self.handle_server, *self.addr)
        # logging.info(f"Websocket server started running on {self.addr}")
        # logging.info("Ctrl+c to get out of loop")
        asyncio.get_event_loop().run_until_complete(run_server)
        asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    server = WebSocketServer(addr=("0.0.0.0", 8000))
    server.run()
