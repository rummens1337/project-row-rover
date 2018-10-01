import cv2
import platform
from src.common.log import *
from src.processing.server import Server


def main():
    log.info("David de ROW-rover! Version: %s", config["General"]["version"])
    Server()

if __name__ == "__main__":
    main()
