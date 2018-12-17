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
        """
        initializes the audio object
        @param volume: Ranges from 0 to 100, standard is 100
        """
        mixer.init()
        self.volume = volume

    def __del__(self):
        """
        Shuts the audio down. Plays music only once
        """
        if Audio.shutdownCount is 0:
            Audio.shutdownCount = 1
            if config["Audio"].getboolean("simulate_audio") is False:
                self.play("/app/jams/Shutdown.mp3", 0)
                while mixer.music.get_busy():
                    pass

    def say(self, text):
        """
        Says a line of text
        @param text: The sentence to say
        """
        espeak.synth(text)

    def pause(self):
        """
        Pause music
        """
        mixer.music.pause()

    def unpause(self):
        """
        Unpause music
        """
        mixer.music.unpause()

    def setVolume(self, volume):
        """
        Sets the volume to a specific percentage
        @param volume: Ranges from 0 to 100, the percentage of the volume
        @raises: Error when volume value is invalid
        """
        if volume <= 100 and volume >= 0:
            amp = volume/100
            mixer.music.set_volume(amp)
            self._volume = volume
        else:
            log.error("Volume "+str(volume)+" is an invalid volume")

    def getVolume(self):
        """
        Get the current volume
        @return: The volume
        """
        return self._volume

    def delVolume(self):
        """
        Delete the volume property
        """
        del self._volume

    volume = property(getVolume, setVolume, delVolume, "Volume property")

    def volumeMasterUP(self):
        """
        Increases the volume by 10 percent
        """
        self.volume += 10

    def volumeMasterDOWN(self):
        """
        Decreases the volume by 10 percent
        """
        self.volume -= 10

    def play(self, path, loops=-1):
        """
        Play a local MP3 on the rover
        @param path: Path to the MP3 file
        @param loops: Number of times to repeat the song. -1 = unlimited 0 = play once 1 = play twice etc.
        """
        mixer.music.load(path)
        mixer.music.play(loops)

