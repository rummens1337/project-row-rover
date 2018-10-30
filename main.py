import cv2
import platform
from src.common.log import *
from src.processing.server import Server
from src.hardware.motor import motor
from src.hardware.lamp import lamp
import time
import sys
import atexit


def main():
    log.info("David de ROW-rover! Version: %s", config["General"]["version"])
    motor.getInstance()
    lamp.getInstance()
    server = Server()
    server.start()
    while True:
        loop()


def loop():
    time.sleep(1000)


@atexit.register
def close():
    log.info("Closing down...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt as e:
        sys.exit(0)
