import sys, time, atexit, subprocess, websockets, asyncio
from src.common.log import *
import src.hardware.camera as camera
import src.processing.image as image


def loop():
    time.sleep(1000)


@atexit.register
def close():
    log.info("Closing down...")


def startServer():
    asyncio.get_event_loop().run_until_complete(
        websockets.serve(video, '0.0.0.0', config["Server"].getint("video_port")))
    asyncio.get_event_loop().run_forever()


async def video(websocket, path):
    await websocket.send(image.to_base64(image.frame2jpg(image.get_processed_frame())))


def main():
    # TODO cores en ram printen
    # cores = subprocess.call("nproc")
    # meminfo = dict((i.split()[0].rstrip(':'),int(i.split()[1])) for i in open('/proc/meminfo').readlines())
    # mem_kib = meminfo['MemTotal']  # e.g. 3921852
    # mem = subprocess.call(["cat", "/proc/meminfo", "grep", "MemTotal"])
    # log.info("Container running on %s cores and %s", cores, mem)
    log.info("video stream start")
    camera.start()
    startServer()
    while True:
        loop()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt as e:
        sys.exit(0)
else:
    log.crit("must be run as main, exiting")
    sys.exit(1)
