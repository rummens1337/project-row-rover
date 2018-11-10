from src.common.log import *
from flask import Flask, request
from flask_restful import Resource, reqparse, Api as fapi
import json
from http_status import Status
from src.hardware.motor import motor
import atexit

class Api:
    API_KEY = 0
    PORT = 0
    api = 0

    parser = reqparse.RequestParser()

    def __init__(self, server, api_key=str(config["Server"]["api_key"])):
        """
        Api class, create an api endpoint to controll the motors of the rover. Accesable from "./api/".
        @param server: Flask server object to attach to.
        @param api_key: key to access the api. Defaults to config>server>api_key
        """
        Api.API_KEY = api_key

        self.api = fapi(server)

        self.api.add_resource(self.Motor, "/api/motor")
        self.api.add_resource(self.Root, '/api')
        self.api.add_resource(self.Stream, '/api/stream')

        self.parser.add_argument('right', type=int, help='motor value must be between -255 and 255')
        self.parser.add_argument('left', type=int, help='motor value must be between -255 and 255')
        self.parser.add_argument('key', help='key invalid')

        atexit.register(self.__del__)

    def __del__(self):
        """
        destroy motor and closes the server
        """
        self.motor = 0
        self.api = 0

    @staticmethod
    def print(status: int = 200, data: str = "") -> json:
        """
        Makes a json object to return to send.
        @param status (int): HTTP status code: https://nl.wikipedia.org/wiki/Lijst_van_HTTP-statuscodes. Default = 200
        @param data (json): object what has to be send back. Default = ""
        @return formatted json.

        input:
        @code
            Api.print(200, {
                "result": 1
            })
        @endcode

        Result:
        @code
            {
                "description": "Request was successful.",
                "status": 200,
                "data": {
                    "result": 1
                },
                "message": "OK"
            }
        @endcode

        """
        return {
            "status": Status(status).code,
            "message": Status(status).name,
            "description": Status(status).description,
            "data": data
        }

    class Motor(Resource):
        @staticmethod
        def get_motor_status() -> json:
            """
            get the motor status (speed value and actual speed)
            @return json object
            """
            lv, rv, s = 0, 0, 0
            s = motor.getInstance().get_speed()
            # invert value if negative
            if motor.richtingl == 1:
                lv -= motor.getInstance().get_value_left()
            else:
                lv = motor.getInstance().get_value_left()
            if motor.richtingr == 1:
                rv -= motor.getInstance().get_value_right()
            else:
                rv = motor.getInstance().get_value_right()
            return {
                "motor": [
                    {
                        "side": "left",
                        "value": lv,
                        "speed": s
                    },
                    {
                        "side": "right",
                        "value": rv,
                        "speed": s
                    }
                ]
            }

        def get(self):
            """
            get motor information from `self.get_motor_status()`
            @return json to sender.
            """
            args = Api.parser.parse_args()
            if args["key"] != Api.API_KEY:
                return Api.print(401), 401
            try:
                motor_status = self.get_motor_status()
            except Exception as err:
                return Api.print(500, str(err))
            else:
                return Api.print(200, motor_status)

        def put(self):
            """
            Set motor left and right speed. (-255 to 255)
            @param left: left speed.
            @param right: right speed.
            @return json to sender
            """
            args = Api.parser.parse_args()
            if args["key"] != Api.API_KEY:
                return Api.print(401), 401
            try:
                if type(args["left"]) is int:
                    motor.getInstance().left(args["left"])
                if type(args["right"]) is int:
                    motor.getInstance().right(args["right"])
            except ValueError as error:
                return Api.print(422, {
                    "message": str(error)
                }), 422
            except Exception as error:
                return Api.print(500, {
                    "message": str(error)
                }), 500
            else:
                return Api.print()

    class Root(Resource):
        def get(self):
            """
            get rover version.
            @return json to sender
            """
            args = Api.parser.parse_args()
            if args["key"] != Api.API_KEY:
                return Api.print(401), 401
            return Api.print(200, {
                "version": str(config["General"]["version"])
            })

    class Stream(Resource):
        def get(self):
            """
            get video stream.
            Not implemeted.
            @return json to sender
            """
            args = Api.parser.parse_args()
            if args["key"] != Api.API_KEY:
                return Api.print(401), 401
            return Api.print(501), 501
