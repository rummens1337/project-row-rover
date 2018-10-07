from src.processing.api import Api
from src.processing.webserver import WebServer
from flask import Flask
from src.common.log import *
import os


class Server:
    path = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
    # log.debug(template_dir)
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
        self.api = Api(self.server, api_key)
        # Added statement below
        self.webServer = WebServer(self.server)
        # TODO fixen dat de server normaal afsluit.
        self.server.run(debug=config["General"].getint("DEBUG"), port=self.PORT, host='0.0.0.0')

    def __del__(self):
        """
        Destroys the server and api.
        """
        self.api = 0
        self.server = 0
