from gevent import monkey
monkey.patch_all()

from src.processing.api import Api
from src.processing.socket import Socket
from src.processing.webserver import WebServer
from src.processing.tracker import Tracker
from flask import Flask
from src.common.log import *
import os
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
import threading
import atexit

class Server(threading.Thread):
    path = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
    path = os.path.join(path, 'web')
    template_dir = os.path.join(path, 'templates')
    static_dir = os.path.join(path, 'static')
    PORT = 0
    flask = Flask(__name__, template_folder = template_dir, static_url_path='/static', static_folder= static_dir)
    api = 0

    #TODO research on secure key and moving to config file
    flask.secret_key = 'hasdku786*&^%*&^5dsa'

    def __init__(self, port=config["Server"].getint("port"), api_key=str(config["Server"]["api_key"])):
        """
        Start flask server. And API server.
        @param port: port to run the server on. Defaults to config>server>port.
        @param api_key: key to access the api. Defaults to config>server>api_key
        """
        threading.Thread.__init__(self)
        self.daemon = True
        self.PORT = port
        self.api_key = api_key

        # Start classes depending on servers, giving this instance as parameter.
        Api(self.flask, self.api_key)
        WebServer(self.flask)
        Socket(self.flask, self.api_key)
        self.server = pywsgi.WSGIServer(('', self.PORT), self.flask, handler_class=WebSocketHandler)
        atexit.register(self.close)


    def run(self):
        """
        Called when thread is started
        """
        log.info("Started server on port: %s, api_key: %s", self.PORT, self.api_key)
        self.server.serve_forever()

    def __del__(self):
        """
        Destroys the server.
        """
        self.close()


    def close(self):
        # TODO, server uitzetten.
        # self.server.stop()
        pass

# TODO moeten nog een serve(), en stop() functie bij komen zodat het nog een beetje bestuurbaar is.
