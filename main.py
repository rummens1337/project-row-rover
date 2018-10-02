import cv2
import platform
from src.common.log import *
from src.processing.server import Server
import src.hardware.motor as motor


def main():
    log.info("David de ROW-rover! Version: %s", config["General"]["version"])
    motor.start()
    Server()

if __name__ == "__main__":
    main()
