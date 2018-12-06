from src.common.log import *
import atexit
from espeak import espeak
if config["Audio"].getboolean("simulate_audio") is False:
    import pygame
else:
    import src.dummy.audiodummy as pygame

class Audio:
    def __init__(self, volume=0):
        self._volume = volume
        pygame.mixer.init()

    def __del__(self):
        self.play("Jams/Shutdown.mp3", 0)

    def say(self, text):
        log.debug("Saying: "+str(text))
        espeak.synth(text)

    def setVolume(self, volume):
        if volume <= 100 and volume >= 0:
            amp = volume/100
            pygame.mixer.music.set_volume(amp)
            self._volume = volume
        else:
            log.error("Volume "+str(volume)+" is an invalid volume")

    def getVolume(self):
        return self._volume

    def delVolume(self):
        del self._volume

    volume = property(getVolume, setVolume, delVolume, "Volume property")

    def volumeMasterUP(self):
        self.volume += 10

    def volumeMasterDOWN(self):
        self.volume -= 10

    def play(self, path, loops=-1):
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(loops)

