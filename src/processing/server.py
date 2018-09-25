from src.processing.api import Api
# from src.processing.webServer import webServer
from flask import Flask
from src.common.log import *


class Server:
    PORT = 0
    server = Flask(__name__)
    api = 0

    def __init__(self, port=config["Server"].getint("port"), api_key=str(config["Server"]["api_key"])):
        """
        Start flask server. And API server.
        :param port: port to run the server on. Defaults to config>server>port.
        :param api_key: key to access the api. Defaults to config>server>api_key
        """
        self.PORT = port
        self.api = Api(self.server, api_key)
        # TODO fixen dat de server normaal afsluit.
        self.server.run(debug=config["General"].getint("DEBUG"), port=self.PORT, host='0.0.0.0')

    def __del__(self):
        """
        Destroys the server and api.
        """
        self.api = 0
        self.server = 0
