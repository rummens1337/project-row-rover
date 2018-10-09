from src.common.log import *

if config["Lamp"].getboolean("simulate_lamp") is False:
    import RPi.GPIO as GPIO
import threading
import atexit

class Lamp(threading.Thread):
    # TODO van lamp (net als alles in hardware) mogen geen meerdere instances van bestaan, het moet dus een module worden en geen class.
    LAMPPIN1 = 7
    status = 0

    def __init__(self):
        """
        Set the pi to use the BCM numbers for GPIO pins
        Configure pins to their required modes
        """
        threading.Thread.__init__(self)
        # TODO dit is een thread object zonder `run()` dus het doet niks.
        if config["Lamp"].getboolean("simulate_lamp") is False:
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(self.LAMPPIN1, GPIO.OUT)

        atexit.register(self.close)


    def lampon(self) -> bool:
        """
        Turns the lamp on
        @return returns a bool based on success
        """
        if config["Lamp"].getboolean("simulate_lamp") is False:
            GPIO.output(self.LAMPPIN1, GPIO.HIGH)
        self.status = 1
        # TODO vind een manier om te checken of hij echt aan staat
        return True

    def lampoff(self) -> bool:
        """
        Turns the lamp off
        @return returns a bool based on success
        """
        if config["Lamp"].getboolean("simulate_lamp") is False:
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

    def close(self):
        # TODO GPIO sluiten @robin1
        pass