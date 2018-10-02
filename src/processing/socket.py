from flask_sockets import Sockets
from src.common.log import *
import json
from src.processing.api import Api
from enum import Enum


class Socket:
    class Request(Enum):
        motor = 0,
        status = 1

    def __init__(self, server):
        socket = Sockets(server)

        @socket.route('/')
        def handle(ws):
            # log.debug("test!")
            while not ws.closed:
                code = 500
                try:
                    recieved = json.loads(ws.receive())
                    # TODO message escapen.

                    if recieved["request"] not in Socket.Request.__members__:
                        code = 400
                        msg = Api.print(code, "Request not found")
                        ws.send(json.dumps(msg))
                except (AttributeError) as err:
                    code = 400
                    msg = Api.print(code, "Wrong format")
                    ws.send(json.dumps(msg))


        @socket.route('/echo')
        def echo_socket(ws):
            while not ws.closed:
                message = ws.receive()
                ws.send(message)

    def __del__(self):
        # TODO
        pass
