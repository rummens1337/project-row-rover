from src.processing.api import Api
from src.processing.socket import Socket
from src.processing.webserver import WebServer
from flask import Flask
from src.common.log import *
import os
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
from threading import Thread
from src.hardware.lamp import Lamp


class Server:
    path = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
    path = os.path.join(path, 'web')
    template_dir = os.path.join(path, 'templates')
    static_dir = os.path.join(path, 'static')
    PORT = 0
    server = Flask(__name__, template_folder = template_dir, static_url_path='/static', static_folder= static_dir)
    api = 0

    def __init__(self, port=config["Server"].getint("port"), api_key=str(config["Server"]["api_key"])):
        """
        Start flask server. And API server.
        @param port: port to run the server on. Defaults to config>server>port.
        @param api_key: key to access the api. Defaults to config>server>api_key
        """
        self.PORT = port

        # Start classes depending on servers, giving this instance as parameter.
        Api(self.server, api_key)
        _lamp = Lamp()
        _lamp.start()
        _lamp.lampoff()
        _webServer = WebServer(self.server)
        _webServer.start()
        Socket(self.server, api_key)
        self.server = pywsgi.WSGIServer(('', self.PORT), self.server, handler_class=WebSocketHandler)
        # TODO dit grapje moet in een thread, anders houd het de main op.
        self.server.serve_forever()
        log.info("Started server on port: %s, api_key: %s", self.PORT, api_key)

    def __del__(self):
        """
        Destroys the server.
        """
        self.server.stop()

# TODO moeten nog een serve(), en stop() functie bij komen zodat het nog een beetje bestuurbaar is.