from src.common.log import *
import atexit
if config["Audio"].getboolean("simulate_audio") is False:
    from pygame import mixer
    from espeak import espeak
else:
    from src.dummy.audiodummy import mixer
    from src.dummy.audiodummy import espeak


class Audio:
    shutdownCount = 0

    def __init__(self, volume=100):
        mixer.init()
        self.volume = volume
        atexit.register(self.shutdown)

    def shutdown(self):
        if Audio.shutdownCount is 0:
            Audio.shutdownCount = 1
            log.error("PLAYING SHUTDOWN")
            if config["Audio"].getboolean("simulate_audio") is False:
                self.play("/app/jams/Shutdown.mp3", 0)
                while mixer.music.get_busy():
                    pass

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

