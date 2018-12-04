import pyttsx3


class Audio:
    def __init__(self):
        self.engine = pyttsx3.init()

    def say(self, text):
        self.engine.say(text)

    def run(self):
        self.engine.runAndWait()
