from websockets.server import WebSocketServerProtocol
from database.models import GlobalChatManager
from typing import AsyncIterable, Iterable
from websockets.typing import Data
import json


class Client(WebSocketServerProtocol):
    def __init__(self, *args, **kwargs) -> None:
        self.database = GlobalChatManager()
        super().__init__(*args, **kwargs)

    def dict_message(self, message) -> dict:
        loaded_message = json.loads(message)
        return loaded_message

    async def send_and_save(
        self, message: Data | Iterable[Data] | AsyncIterable[Data]
    ) -> None:
        msg = self.dict_message(message).get("message")
        print(self.dict_message(message))
        print(msg)
        self.database.add(message=msg)
        return await super().send(message)
