from enum import Enum


class Api:
    # TODO api key uit /settings.conf halen
    API_KEY = 0

    class Request(Enum):
        SET_MOTOR_LEFT = 0
        SET_MOTOR_RIGHT = 1
        GET_STREAM = 2

    class Response(Enum):
        SUCCESS = 100
        UNKNOWN_ERROR = 200
        REQUEST_NOT_FOUND = 201
        ACTION_NOT_ALLOWED = 202

    def handle_request(self, req: Request) -> bool:
        pass
