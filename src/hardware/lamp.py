import RPi.GPIO as GPIO


class Lamp:
    LAMPPIN1 = 7

    def __init__(self):
        """
        Set the pi to use the BCM numbers for GPIO pins
        Configure pins to their required modes
        """
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.LAMPPIN1, GPIO.OUT)

    def lampon(self) -> bool:
        """
        Turns the lamp on
        :return: returns a bool based on success
        """
        GPIO.output(self.LAMPPIN1, 1)
        return True

    def lampoff(self) -> bool:
        """
        Turns the lamp off
        :return: returns a bool based on success
        """
        GPIO.output(self.LAMPPIN1, 0)
        return True

    def status(self) -> dict:
        """
        Generates the current state of the lamp
        :return: returns a dictionary with the status
        """
        pass
