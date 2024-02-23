from websockets.exceptions import WebSocketException


class ValidationError(WebSocketException):
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code


class DisconnectClientException(Exception):
    """Disconnection label of Client"""
