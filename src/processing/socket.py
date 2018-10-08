from flask_sockets import Sockets
from src.common.log import *
import json
from json import JSONDecodeError
from src.processing.api import Api
from enum import Enum
import src.hardware.motor as motor
from src.hardware.lamp import Lamp
from src.hardware.display import lcd
from threading import Thread


class Socket:
    class Request(Enum):
        motor = 0,
        status = 1,
        lamp = 2,
        displayMsg = 3

    def __init__(self, server, api_key):
        socket = Sockets(server)
        self.api_key = api_key
        self.lcdInstance = lcd()
        self.lcdInstance.lcd_display_string("Team: David",1)
        self.lcdInstance.lcd_display_string("\"RescueDavid\"",2)
        self.lamp = Lamp()
        self.lamp.start()
        self.lamp.lampoff()

        @socket.route('/')
        def handle(ws):
            while not ws.closed:
                try:
                    recieved = json.loads(ws.receive())
                    if recieved["key"] != self.api_key:
                        msg = Api.print(401)
                        ws.send(json.dumps(msg) + json.dumps(recieved))
                        ws.close()

                    if recieved["request"] == Socket.Request.motor.name:
                        if "left" in recieved["data"]:
                            motor.left(int(recieved["data"]["left"]))
                        if "right" in recieved["data"]:
                            motor.right(int(recieved["data"]["right"]))
                        if "message" in recieved["data"]:
                            self.lcdInstance.lcd_display_string("Werkt hier :)",1)
                        ws.send(json.dumps(Api.print()))


                    elif recieved["request"] == Socket.Request.status.name:
                        # TODO versie moet ook meegestuurd worden.
                        # version = {"version": config["General"]["version"]}
                        ws.send(json.dumps(Api.print(200, Api.Motor.get_motor_status())))

                    elif recieved["request"] == Socket.Request.lamp.name:
                        if recieved["data"] == 1:
                            self.lamp.lampon()
                            ws.send(json.dumps(Api.print()))
                        elif recieved["data"] == 0:
                            self.lamp.lampoff()
                            ws.send(json.dumps(Api.print()))
                        ws.send(json.dumps(Api.print()))

                    elif recieved["request"] == Socket.Request.displayMsg.name:
                        # self.lcdInstance.lcd_display_string(recieved("Worksyeah"),1)
                            # recieved(["data"]["message"])
                        self.lcdInstance.lcd_display_string(str(recieved["data"]),1)
                        ws.send(json.dumps(Api.print()))


                    else:
                        raise AttributeError("Request not found")
                except (AttributeError, JSONDecodeError, KeyError, ValueError) as err:
                    msg = Api.print(400, str(err))
                    ws.send(json.dumps(msg))
                    ws.close()
                # except Exception as err:
                #     ws.send(json.dumps(Api.print(500, str(err))))
                #     ws.close()

    def __del__(self):
        # TODO
        pass
