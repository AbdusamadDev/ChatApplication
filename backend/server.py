from websockets.exceptions import ConnectionClosedOK, ConnectionClosedError

from database.manager import GroupMessageManager, add_message_to_db
from backend.exceptions import DisconnectClientException
from backend.client import Client

from datetime import datetime
import websockets
import asyncio
import logging

logging.basicConfig(level=logging.INFO)


class WebSocketServer:
    STATE_ERROR = {
        "error": True,
        "description": "State of request is not provided."
        "Possible Values: connect/close",
    }
    ATTRIBUTE_ERROR = {
        "error": True,
        "description": "Group ID or Client ID not provided",
    }

    def __init__(self, addr: tuple) -> None:
        self.addr = addr
        self.clients: list = []
        self.chats = dict()

    async def connect(self, client):
        await client.set_client_id()
        # if client.group_id is None:
        #     raise DisconnectClientException("Group ID is not provided")
        # group_name = client.group_id
        # group_table = GroupMessageManager(table_name=group_name)
        # if group_name not in group_table.group_ids():
        #     await client.send(client.to_json({"error": "Group does not exist!"}))
        #     raise DisconnectClientException("Group does not exist")
        client_details = {"client_id": client.client_id, "connection": client}
        if str(client.client_id) not in [user.get("id") for user in self.clients]:
            self.clients.append(client_details)
        # if group_name not in self.chats.keys():
        #     self.chats[group_name] = {
        #         "database": group_table,
        #         "clients": [client_details],
        #     }
        # else:
        #     self.chats[group_name]["clients"].append(client_details)

    # async def remove_group(self, client_id):
    #     self.clients.remove

    async def broadcast(self, data, client):
        logging.info(f"The data to send --> {data}")
        # group_id = client.group_id
        data = client.to_json(data)
        for client in self.clients:
            if client["connection"].open:
                await client["connection"].send(data)
            else:
                await client["connection"].close()

    async def chat_in_group_handler(self, input_client):
        while True:
            if input_client.open:
                data = await input_client.recv()
                data = input_client.to_dict(data)
                content_data = data.get("message")
                group_id = data.get("group_id")
                data_type = data.get("type")
                current_time = datetime.now()
                formatted_time = current_time.strftime("%I:%M %p")
                data["sent_at"] = formatted_time
                await self.broadcast(data=data, client=input_client)
                add_message_to_db(
                    table_name=group_id,
                    message=content_data,
                    user_id=input_client.client_id,
                    type=data_type,
                    sent_at=formatted_time,
                )
            else:
                await input_client.close()
                return

    async def handle_server(self, websocket: Client, path):
        try:
            await self.connect(websocket)
        except DisconnectClientException:
            return await websocket.close()
        while True:
            if websocket.open:
                logging.info("Got into group chat room")
                await self.chat_in_group_handler(websocket)
            else:
                await websocket.close()
                break

    def run(self):
        run_server = websockets.serve(self.handle_server, *self.addr, klass=Client)
        logging.info(f"Websocket server started running on {self.addr}")
        logging.info("Ctrl+c to get out of loop")
        asyncio.get_event_loop().run_until_complete(run_server)
        asyncio.get_event_loop().run_forever()


# if __name__ == "__main__":
#     try:
#         logging.basicConfig(level=logging.INFO)
#         server = WebSocketServer(addr=("0.0.0.0", 8000))
#         server.run()
#     except KeyboardInterrupt:
#         logging.info(" Shutting down gracefully!")
