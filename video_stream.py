import sys, time, atexit, subprocess, websockets, asyncio, threading
from src.common.log import *
import src.hardware.camera as camera
import src.processing.image as image
import numpy as np



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
    log.debug("new video object")
    current_frame = None
    last_frame = None
    while True:
        # TODO alleen de 1e client die verbonden is heeft verbinding met de socket.
        try:
            current_frame = image.get_processed_frame()
            # TODO uitzoeken of deze equal functie niet teveel tijd kost.
            if not np.array_equal(current_frame, last_frame):
                log.debug("new info!")
                await websocket.send(image.to_base64(image.frame2jpg(current_frame)))
                last_frame = current_frame
            websocket.recv()
        #     TODO deze exception werkt niet
        except websockets.exceptions.ConnectionClosed:
            log.debug("connection closed")
            break



def main():
    # TODO cores en ram printen
    # cores = subprocess.call("nproc")
    # meminfo = dict((i.split()[0].rstrip(':'),int(i.split()[1])) for i in open('/proc/meminfo').readlines())
    # mem_kib = meminfo['MemTotal']  # e.g. 3921852
    # mem = subprocess.call(["cat", "/proc/meminfo", "grep", "MemTotal"])
    # log.info("Container running on %s cores and %s", cores, mem)
    log.info("video stream start")
    camera.start()
    # TODO beter als we multiprocessing gebruiken
    pf = threading.Thread(target = image.process_frames_forever)
    pf.daemon = True
    pf.start()
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
