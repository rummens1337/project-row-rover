from src.common.log import *
if config["Lamp"].getboolean("simulate_lamp") is False:
    import RPi.GPIO as GPIO
import atexit

LAMPPIN1 = 7
status = 0


def start():
    """
    Set the pi to use the BCM numbers for GPIO pins
    Configure pins to their required modes
    """
    if config["Lamp"].getboolean("simulate_lamp") is False:
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(LAMPPIN1, GPIO.OUT)


def lampon() -> bool:
    """
    Turns the lamp on
    @return returns a bool based on success
    """
    if config["Lamp"].getboolean("simulate_lamp") is False:
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
    if config["Lamp"].getboolean("simulate_lamp") is False:
        GPIO.output(LAMPPIN1, GPIO.LOW)
    global status
    status = 0
    # TODO vind een manier om te checken of hij echt uit staat
    return True

def status() -> dict:
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
    # TODO GPIO sluiten @robin1
    pass
