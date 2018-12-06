from src.common.log import *

if config["Battery"].getboolean("simulate_Battery") is False:
    import smbus2 as smbus
else:
    import src.dummy.smbus2dummy as smbus


def start():
    """
    Join the I²C bus as master
    """
    global bus
    bus = smbus.SMBus(1)


def get_batteryStatus():
    """
    get the battery percentage.
    @return: int 0-100
    """
    global bus
    return bus.read_byte_data(int(config["Battery"]["I2C_slave_address"], 16), 0)
