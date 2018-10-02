from flask_sockets import Sockets
from src.common.log import *
import json
from json import JSONDecodeError
from src.processing.api import Api
from enum import Enum
import src.hardware.motor as motor


class Socket:
    class Request(Enum):
        motor = 0,
        status = 1

    def __init__(self, server, api_key):
        socket = Sockets(server)
        self.api_key = api_key

        @socket.route('/')
        def handle(ws):
            while not ws.closed:
                try:
                    recieved = json.loads(ws.receive())
                    if recieved["key"] != self.api_key:
                        msg = Api.print(401)
                        ws.send(json.dumps(msg))
                        ws.close()
                    if recieved["request"] == Socket.Request.motor.name:
                        if "left" in recieved["data"]:
                            motor.left(int(recieved["data"]["left"]))
                        if "right" in recieved["data"]:
                            motor.right(int(recieved["data"]["right"]))
                        ws.send(json.dumps(Api.print()))
                    elif recieved["request"] == Socket.Request.status.name:
                        # TODO versie moet ook meegestuurd worden.
                        # version = {"version": config["General"]["version"]}
                        ws.send(json.dumps(Api.print(200, Api.Motor.get_motor_status())))

                    else:
                        raise AttributeError("Request not found")
                except (AttributeError, JSONDecodeError, KeyError, ValueError) as err:
                    msg = Api.print(400, str(err))
                    ws.send(json.dumps(msg))
                    ws.close()
                except Exception as err:
                    ws.send(json.dumps(Api.print(500, str(err))))
                    ws.close()

    def __del__(self):
        # TODO
        pass
