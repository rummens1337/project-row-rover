import RPi.GPIO as GPIO
import threading

class Lamp(threading.Thread):
    LAMPPIN1 = 7
    status = 0

    def __init__(self):
        """
        Set the pi to use the BCM numbers for GPIO pins
        Configure pins to their required modes
        """
        # if config["Lamp"].getboolean("simulate_lamp") == False:
        threading.Thread.__init__(self)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.LAMPPIN1, GPIO.OUT)

    def lampon(self) -> bool:
        """
        Turns the lamp on
        @return returns a bool based on success
        """
        # if config["Lamp"].getboolean("simulate_lamp") == False:
        GPIO.output(self.LAMPPIN1, GPIO.HIGH)
        self.status = 1
        # TODO vind een manier om te checken of hij echt aan staat
        return True

    def lampoff(self) -> bool:
        """
        Turns the lamp off
        @return returns a bool based on success
        """
        # if config["Lamp"].getboolean("simulate_lamp") == False:
        GPIO.output(self.LAMPPIN1, GPIO.LOW)
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
