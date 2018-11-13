import cv2
import platform
from src.common.log import *
from src.processing.server import Server
import src.hardware.motor as motor
import src.hardware.lamp as lamp
import src.hardware.camera as camera
import time, subprocess
import sys
import atexit


def main():
    # TODO cores en ram printen
    # cores = subprocess.call("nproc")
    # mem = subprocess.call("cat /proc/meminfo | grep MemTotal")
    log.info("David de ROW-rover! Version: %s", config["General"]["version"])
    # log.info("Container running on %s cores and %s", cores, mem)
    camera.start()
    motor.start()  # motor in api class.
    lamp.start()
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
