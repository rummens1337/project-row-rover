import cv2
import platform
from src.common.log import *
from src.processing.server import Server
import src.hardware.motor as motor
import src.hardware.lamp as lamp
import time


def main():
    log.info("David de ROW-rover! Version: %s", config["General"]["version"])
    motor.start() #motor in api class.
    lamp.start()
    Server()


if __name__ == "__main__":
    main()
