import cv2
import platform
from src.common.log import *
from src.processing.server import Server


def main():
    log.debug("python version: %s", platform.python_version())
    log.debug("OpenCV version: %s", cv2.__version__)

    server = Server()


#    mot = Motor()
#    mot.left(0)


if __name__ == "__main__":
    main()
