from src.common.log import *
if config["Lamp"].getboolean("simulate_lamp") is False:
    import RPi.GPIO as GPIO
else:
    import src.dummy.GPIOdummy as GPIO


class lamp:
    LAMPPIN1 = 7
    status = 0
    __Instance = None

    def __init__(self):
        """
        Initilizes a lamp object, but only one. To use this class, use getInstance instead.
        @raises: exception when a instance of this class already exists
        """
        if lamp.__Instance is not None:
            raise Exception("Instance already exists")
        else:
            lamp.__Instance = self
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(self.LAMPPIN1, GPIO.OUT)

    @staticmethod
    def getInstance():
        """
        Initializes a lamp object, but only one
        @return: The single only instance of this class
        """
        if lamp.__Instance is None:
            lamp()
        return lamp.__Instance

    def lampon(self) -> bool:
        """
        Turns the lamp on
        @return returns a bool based on success
        """
        GPIO.output(self.LAMPPIN1, GPIO.HIGH)
        self.status = 1
        # TODO vind een manier om te checken of hij echt aan staat
        return True

    def lampoff(self) -> bool:
        """
        Turns the lamp off
        @return returns a bool based on success
        """
        GPIO.output(self.LAMPPIN1, GPIO.LOW)
        self.status = 0
        # TODO vind een manier om te checken of hij echt uit staat
        return True

    def get_status(self) -> dict:
        """
        Generates the current state of the lamp
        @return returns a dictionary with the status
        """
        return {
            "lampmode": self.status,
            "lamppin": self.LAMPPIN1
        }

    def __del__(self):
        GPIO.cleanup()
