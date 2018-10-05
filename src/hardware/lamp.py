import RPi.GPIO as GPIO


class Lamp:
    LAMPPIN1 = 7
    status = 0

    def __init__(self):
        """
        Set the pi to use the BCM numbers for GPIO pins
        Configure pins to their required modes
        """
        if config["Lamp"].getboolean("simulate_lamp") == False:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.LAMPPIN1, GPIO.OUT)

    def lampon(self) -> bool:
        """
        Turns the lamp on
        @return returns a bool based on success
        """
        if config["Lamp"].getboolean("simulate_lamp") == False:
            GPIO.output(self.LAMPPIN1, 1)
        self.status = 1
        # TODO vind een manier om te checken of hij echt aan staat
        return True

    def lampoff(self) -> bool:
        """
        Turns the lamp off
        @return returns a bool based on success
        """
        if config["Lamp"].getboolean("simulate_lamp") == False:
            GPIO.output(self.LAMPPIN1, 0)
        self.status = 0
        # TODO vind een manier om te checken of hij echt uit staat
        return True

    def status(self) -> dict:
        """
        Generates the current state of the lamp
        @return returns a dictionary with the status
        """
        return {
            "lampmode": self.status,
            "lamppin": self.LAMPPIN1
        }
