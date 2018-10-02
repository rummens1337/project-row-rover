from src.common.log import *
import smbus2 as smbus

OFFSET = 0  # offset in the array
ADDRESS = 0x32  # I2c address of the motorcontroller
# speed from 4 to 250
speedl = 0
speedr = 0
# 0 = stilstaan 1 = vooruit 2 = achteruit
richtingl = 0
richtingr = 0
global bus

def start():
    """
    Create a bus connection over I2C and sets the speed at 0
    """
    global bus
    log.debug("init motor")
    if config["Motor"].getboolean("simulate_motor") == False:
        bus = smbus.SMBus(
            1)  # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1) <- found on internet, hope it makes sense to you
    else:
        bus = 0

    left(0)
    right(0)


def __del__():
    """
    closes the i2c bus.
    """
    stop()


def stop() -> bool:
    """
    Stop the motors and stop the I2c bus connection
    :return: returns a bool based on success
    """
    left(0)
    right(0)
    try:
        bus.close()
    except AttributeError as er:
        log.error("failed to access bus %s, normal if in fake env", er)
    # TODO dit returnt altijd true, moet natuurlijk op basis van de uitkomst. @robin1
    return True


def left(speed: int) -> bool:
    """
    Speed and direction of the left wheels
    :param speed: Range from -255 to 255
    :return: returns a bool based on success
    :raises: Value error when speed is out of the range
    """
    global speedl
    global richtingl
    if speed > -256 and speed < 256:
        if speed == 0:
            speedl = 0
            richtingl = 0
        if speed > 0:
            speedl = speed
            richtingl = 1
        if speed < 0:
            speedl = -speed
            richtingl = 2
    else:
        raise ValueError("{0} is not in the range of -255 to 255".format(speed))

    if _send_data():
        return True
    else:
        return False


def right(speed: int) -> bool:
    """
    Speed and direction of the right wheels
    :param speed: Range from -255 to 255
    :return: returns a bool based on success
    :raises: Value error when speed is out of the range
    """
    global speedr
    global richtingr
    if speed > -256 and speed < 256:
        if speed == 0:
            speedr = 0
            richtingr = 0
        if speed > 0:
            speedr = speed
            richtingr = 1
        if speed < 0:
            speedr = -speed
            richtingr = 2
    else:
        raise ValueError("{0} is not in the range of -255 to 255".format(speed))

    if _send_data():
        return True
    else:
        return False


def status() -> dict:
    """
    Generates the current state of the motor
    :return: returns a dictionary with the status
    """
    return {
        "speedl": speedl,
        "richtingl": richtingl,
        "speedr": speedr,
        "richtingr": richtingr
    }


def get_speed() -> int:
    """
    :return: returns a dictionary with the speeds
    """
    # TODO return speed gemeten door sensor @robin1
    return 0


def get_value_left() -> int:
    """
    Get left speed value
    :return (int): value
    """
    return speedl


def get_value_right() -> int:
    """
    Get right speed value
    :return (int): value
    """
    return speedr


def _send_data() -> bool:
    """
    generate an array of data for the motorcontroller and sends it over the I2C bus
    :return: returns a bool based on success
    """
    global bus
    if config["Motor"].getboolean("simulate_motor") == False:
        try:
            motor_data = [7, 3, speedl, richtingl, 3, speedr, richtingr]
            bus.write_i2c_block_data(ADDRESS, OFFSET, motor_data)
        except IOError as e:
            print("I/O error({0}): {1}".format(e.errno, e.strerror))
            return False
        else:
            return True
    else:
        return True
