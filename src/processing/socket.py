from flask import Flask, render_template
from flask_socketio import SocketIO
from src.common.log import *


class Socket:
    def __init__(self, server):
        self.socket = SocketIO(server)
        self.socket.run(server)

        self.socket.on_event('test', self.handle_test)

    def __del__(self):
        # TODO
        pass

    def handle_test(self):
        log.debug("test!")
