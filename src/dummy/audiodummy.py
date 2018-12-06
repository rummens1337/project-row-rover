from src.common.log import *
import atexit


class espeak:
    def synth(self, text="No text given"):
        log.debug("Saying: " + str(text))


class Mixer:
    def __init__(self, outout="No output"):
        log.debug("Mixer init, output: " + str(outout))

    def setvolume(self, volume):
        log.debug("Volume set to " + str(volume))
