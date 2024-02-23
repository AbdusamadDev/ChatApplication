from websockets.server import WebSocketServerProtocol
from typing import AsyncIterable, Iterable
from websockets.typing import Data

from .exceptions import DisconnectClientException
from database.manager import GroupMessageManager

import logging
import json


class Client(WebSocketServerProtocol):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.group_id = None  # Initialize group_id to None

    def to_json(self, message):
        loaded_message = json.dumps(message)
        return loaded_message

    def to_dict(self, message) -> dict:
        loaded_message = json.loads(message)
        return loaded_message

    # async def save_and_send(
    #     self, message: Data | Iterable[Data] | AsyncIterable[Data]
    # ) -> None:

    #     if self.group_id is None:
    #         logging.warning("Client does not have a group_id set.")
    #         return

    #     table_name = self.group_id
    #     database = GroupMessageManager(table_name=table_name)
    #     msg = self.to_dict(message).get("message")
    #     database.add(message=msg, user_id=self.client_id)
    #     logging.info(f"CURRENT CLIENT STATUS: {self.open}")
    #     return await self.send(message)

    async def set_client_id(self):
        uri = self.path
        parts = uri.split("/")
        if len(parts) >= 4 and parts[1] == "chat":
            client_id = parts[2]
            group_id = parts[3]
            self.group_id = group_id
            self.client_id = client_id
        else:
            logging.warning("Invalid URI format. Expected '/chat/<client_id>/<token>'.")
            raise DisconnectClientException("Invalid token or id provided")
