from src.common.log import *

boardmode = None
BOARD = "BOARD"
BCM = "BCM"
IN = "INPUT"
OUT = "OUTPUT"
PUD_UP = "UP RESISTOR"
PUD_DOWN = "DOWN RESISTOR"
FALLING = "FALLING"
RISING = "RISING"
BOTH = "FALLING + RISING"
HIGH = "HIGH"
LOW = "LOW"


def setmode(board):
    global boardmode
    boardmode = board
    log.debug("GPIO Board mode set to " + str(board))


def setup(pin, config, pull_up_down=None):
    log.debug("GPIO Pin "+str(pin)+" set to "+str(config)+" with resistor "+str(pull_up_down))


def output(pin, mode):
    log.debug("GPIO pin "+str(pin)+" is now "+str(mode))


def add_event_detect(pin, edge, callback):
    log.debug("GPIO Interrupt created on pin "+str(pin)+" on " + str(edge) + " as callback " + str(callback))
    for i in range(10):
        callback(pin)

def cleanup():
    log.debug("GPIO is clean again")
