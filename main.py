import cv2
import platform
from src.common.log import *
from src.hardware.motor import *
from src.hardware.camWebServer.appCam import *


def main():
    log.info("hello, world!")
    log.debug("python version: %s", platform.python_version())
    log.debug("OpenCV version: %s", cv2.__version__)


#    mot = Motor()
#    mot.left(0)




if __name__ == "__main__":
    main()
