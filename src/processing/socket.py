from flask_sockets import Sockets
from src.common.log import *
import json
from json import JSONDecodeError
from src.processing.api import Api
from enum import Enum
from src.hardware.motor import motor
from src.hardware.display import lcd
from src.hardware.lamp import lamp
import atexit
import src.hardware.camera as camera
import src.processing.image as image
import base64, time, cv2
import src.hardware.battery as battery


class Socket:
    class Request(Enum):
        motor = 0,
        status = 1,
        lamp = 2,
        displayMsg = 3,
        tagclicked = 4,
        compass = 5,
        battery = 6

    def __init__(self, server, api_key):
        socket = Sockets(server)
        self.api_key = api_key
        atexit.register(self.__del__)

        @socket.route('/')
        def handle(ws):
            """
            handle the incomming websocket connection. Do not call this function.
            @param ws: websocket object, supplied by flask_sockets
            """
            # TODO exit if not a websocket request
            while not ws.closed:
                try:
                    recieved = json.loads(ws.receive())
                    if recieved["key"] != self.api_key:
                        msg = Api.print(401)
                        ws.send(json.dumps(msg) + json.dumps(recieved))
                        ws.close()

                    if recieved["request"] == Socket.Request.motor.name:
                        if "data" in recieved:
                            if "left" in recieved["data"] and "right" in recieved["data"]:
                                motor.getInstance().leftright(int(recieved["data"]["left"]),
                                                              int(recieved["data"]["right"]))
                            else:
                                if "left" in recieved["data"]:
                                    motor.getInstance().left(int(recieved["data"]["left"]))
                                if "right" in recieved["data"]:
                                    motor.getInstance().right(int(recieved["data"]["right"]))
                            ws.send(json.dumps(Api.print()))
                        else:
                            ws.send(json.dumps(Api.print(200, Api.Motor.get_motor_status())))

                    elif recieved["request"] == Socket.Request.tagclicked.name:
                        motor.getInstance().moveBack()

                    elif recieved["request"] == Socket.Request.status.name:
                        version = {"version": config["General"]["version"]}
                        ws.send(json.dumps(Api.print(200, version)))

                    elif recieved["request"] == Socket.Request.lamp.name:
                        if "data" not in recieved:
                            ws.send(json.dumps(Api.print(200, lamp.getInstance().get_status())))
                        elif recieved["data"] == 1:
                            lamp.getInstance().lampon()
                            ws.send(json.dumps(Api.print()))
                        elif recieved["data"] == 0:
                            lamp.getInstance().lampoff()
                            ws.send(json.dumps(Api.print()))
                    #         TODO er moet hier een `else` voor error handeling

                    elif recieved["request"] == Socket.Request.displayMsg.name:
                        # TODO displayMsg status opvragen
                        self.lcdInstance.lcd_clear()
                        self.lcdInstance.lcd_display_string(str(recieved["data"][0:16]), 1)
                        self.lcdInstance.lcd_display_string(str(recieved["data"][16:33]), 2)
                        ws.send(json.dumps(Api.print()))

                    elif recieved["request"] == Socket.Request.compass.name:
                        # TODO: Toevoegen van actuele compasdata.
                        direction = 180
                        data = {"compass": {"dir": direction}}
                        # TODO dit houd zich niet aan de API spec, hij moet api.print(htmlco, data) doen
                        ws.send(json.dumps(data))

                    elif recieved["request"] == Socket.Request.battery.name:
                        ws.send(json.dumps(Api.print(200,
                            {"battery": battery.get_batteryStatus()}
                        )))

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

            self.close()

    def close(self):
        """
        when the socket connection is closed, stop all the motors and turn the flashlight off.
        """
        # TODO wanneer er nog een andre connectie open is gaat alles ook uit, zou eigenlijk alleen moeten gebeuren als er 0 connecties zijn.

    def __del__(self):
        self.close()
