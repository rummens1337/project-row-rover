import cv2
import platform
from src.common.log import *
from src.processing.server import Server
import src.hardware.motor as motor
import time
import sys
import atexit


server = Server()

def main():
    log.info("David de ROW-rover! Version: %s", config["General"]["version"])
    motor.start()  # motor in api class.

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
