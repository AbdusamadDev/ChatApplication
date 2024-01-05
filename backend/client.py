import websockets



class ClientHandler:
    def __init__(self, channel: websockets.ClientProtocol) -> None:
        self.channel = channel
