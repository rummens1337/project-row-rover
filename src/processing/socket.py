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
import src.hardware.camera as camera
import src.processing.image as image
import base64, time, cv2

class Socket:
    class Request(Enum):
        motor = 0,
        status = 1,
        lamp = 2,
        displayMsg = 3

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
                        self.lcdInstance.lcd_display_string(str(recieved["data"][0:16]),1)
                        self.lcdInstance.lcd_display_string(str(recieved["data"][16:33]),2)
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

            self.close()

        @socket.route("/video")
        def get_video(ws):
            # TODO testen.
            frame = image.get_processed_frame()
            ws.send(image.to_base64(image.frame2jpg(frame)))

    def close(self):
        """
        when the socket connection is closed, stop all the motors and turn the flashlight off.
        """
        # TODO wanneer er nog een andre connectie open is gaat alles ook uit, zou eigenlijk alleen moeten gebeuren als er 0 connecties zijn.
        motor.left(0)
        motor.right(0)
        lamp.lampoff()

    def __del__(self):
        self.close()
        pass
