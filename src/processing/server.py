from src.processing.api import Api
from src.processing.webServer import webServer

class Server:
    # TODO default port uit /config.ini halen.
    DEFAULT_PORT = 80

    def listen(self, port=DEFAULT_PORT):
        pass

    def _handle_connection(self):
        pass
