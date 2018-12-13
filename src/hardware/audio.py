from src.common.log import *
import atexit
import subprocess
from espeak import espeak
if config["Audio"].getboolean("simulate_audio") is False:
    from pygame import mixer
else:
    from src.dummy.audiodummy import mixer

class Audio:
    def __init__(self, volume=100):
        self._volume = volume
        mixer.init()
        atexit.register(self.shutdown)

    def shutdown(self):
        log.debug("BYE BYE AUDIO")
        subprocess.Popen(["mpg123", "-q", "/app/jams/Shutdown.mp3"]).wait()

    def __del__(self):
        self.shutdown()

    def say(self, text):
        espeak.synth(text)

    def pause(self):
        mixer.music.pause()

    def unpause(self):
        mixer.music.unpause()

    def setVolume(self, volume):
        if volume <= 100 and volume >= 0:
            amp = volume/100
            mixer.music.set_volume(amp)
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
        mixer.music.load(path)
        mixer.music.play(loops)

