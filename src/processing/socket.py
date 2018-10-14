from flask_sockets import Sockets
from src.common.log import *
import json
from json import JSONDecodeError
from src.processing.api import Api
from enum import Enum
import src.hardware.motor as motor
from src.hardware.display import lcd
import src.hardware.lamp as lamp
import atexit


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
        # TODO waarom als de socket aangaat word er tekst op de LCD geprint. Deze twee zijn toch onrelevant van elkaar? @michel
        self.lcdInstance.lcd_display_string("Team: David", 1)
        self.lcdInstance.lcd_display_string("\"RescueDavid\"", 2)
        lamp.lampoff()
        atexit.register(self.__del__)

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
                        if "data" in recieved:
                            if "left" in recieved["data"]:
                                motor.left(int(recieved["data"]["left"]))
                            if "right" in recieved["data"]:
                                motor.right(int(recieved["data"]["right"]))
                            ws.send(json.dumps(Api.print()))
                        else:
                            ws.send(json.dumps(Api.print(200, Api.Motor.get_motor_status())))

                    elif recieved["request"] == Socket.Request.status.name:
                        version = {"version": config["General"]["version"]}
                        ws.send(json.dumps(Api.print(200, version)))

                    elif recieved["request"] == Socket.Request.lamp.name:
                        if "data" not in recieved:
                            ws.send(json.dumps(Api.print(200, lamp.get_status())))
                        elif recieved["data"] == 1:
                            lamp.lampon()
                            ws.send(json.dumps(Api.print()))
                        elif recieved["data"] == 0:
                            lamp.lampoff()
                            ws.send(json.dumps(Api.print()))


                    elif recieved["request"] == Socket.Request.displayMsg.name:
                        # TODO displayMsg status opvragen
                        self.lcdInstance.lcd_clear()
                        self.lcdInstance.lcd_display_string(str(recieved["data"][0:15]), 1)
                        self.lcdInstance.lcd_display_string(str(recieved["data"][15:31]), 1)
                        ws.send(json.dumps(Api.print()))


                    else:
                        raise AttributeError("Request not found")
                except (AttributeError, JSONDecodeError, KeyError, ValueError) as err:
                    msg = Api.print(400, str(err))
                    ws.send(json.dumps(msg))
                    ws.close()

                except Exception as err:
                    if ws.closed is not True:
                        ws.send(json.dumps(Api.print(500)))
                        ws.close()
                        log.error("Internal Server Error", exc_info=True)


    # TODO wanneer de socket word gesloten (door de server of client) moeten de motors uitgaan en het lampje knipperen of uitgaan (om aantegeven dat er geen connectie is)
    def __del__(self):
        # TODO
        pass
