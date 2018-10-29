from src.common.log import *
import atexit
if config["Lamp"].getboolean("simulate_lamp") is False:
    import RPi.GPIO as GPIO
else:
    import src.dummy.GPIOdummy as GPIO

LAMPPIN1 = 7
status = 0

def start():
    """
    Set the pi to use the BCM numbers for GPIO pins
    Configure pins to their required modes
    """
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(LAMPPIN1, GPIO.OUT)


def lampon() -> bool:
    """
    Turns the lamp on
    @return returns a bool based on success
    """
    GPIO.output(LAMPPIN1, GPIO.HIGH)
    global status
    status = 1
    # TODO vind een manier om te checken of hij echt aan staat
    return True


def lampoff() -> bool:
    """
    Turns the lamp off
    @return returns a bool based on success
    """
    GPIO.output(LAMPPIN1, GPIO.LOW)
    global status
    status = 0
    # TODO vind een manier om te checken of hij echt uit staat
    return True


def get_status() -> dict:
    """
    Generates the current state of the lamp
    @return returns a dictionary with the status
    """
    return {
        "lampmode": status,
        "lamppin": LAMPPIN1
    }


@atexit.register
def close():
    GPIO.cleanup()
