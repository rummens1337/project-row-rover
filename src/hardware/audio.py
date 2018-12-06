from src.common.log import *
import atexit
if config["Audio"].getboolean("simulate_audio") is False:
    from espeak import espeak
    from alsaaudio import *
else:
    from src.dummy.audiodummy import *



class Audio:
    def __init__(self):
        self.mixer = Mixer('Mono Output Select')
        pass

    def say(self, text):
        espeak.synth(text)

    def run(self):
        pass

    def setVolume(self, volume):
        self.mixer.setvolume(volume)

    def playFile(self, path):
        pass

