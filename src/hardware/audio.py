from espeak import espeak


class Audio:
    def __init__(self):
        pass

    def say(self, text):
        espeak.synth(text)

    def run(self):
        pass
