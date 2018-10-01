from flask_sockets import Sockets
from src.common.log import *


class Socket:
    def __init__(self, server):
        socket = Sockets(server)

        @socket.route('/')
        def handle_test(ws):
            # log.debug("test!")
            ws.send("hello world!")

    def __del__(self):
        # TODO
        pass
