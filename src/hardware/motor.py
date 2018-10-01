from src.common.log import *
import smbus2 as smbus


class Motor:
    OFFSET = 0  # offset in the array
    ADDRESS = 0x32  # I2c address of the motorcontroller
    # speed from 4 to 250
    speedl = 0
    speedr = 0
    # 0 = stilstaan 1 = vooruit 2 = achteruit
    richtingl = 0
    richtingr = 0

    def __init__(self):
        """
        Create a bus connection over I2C and sets the speed at 0
        """
        if config["Motor"].getboolean("simulate_motor") == False:
            self.bus = smbus.SMBus(
                1)  # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1) <- found on internet, hope it makes sense to you
        else:
            self.bus = 0

        self.left(0)
        self.right(0)

    def __del__(self):
        """
        closes the i2c bus.
        """
        self.stop()

    def stop(self) -> bool:
        """
        Stop the motors and stop the I2c bus connection
        :return: returns a bool based on success
        """
        self.left(0)
        self.right(0)
        try:
            self.bus.close()
        except AttributeError as er:
            log.error("failed to access bus %s, normal if in fake env", er)
        # TODO dit returnt altijd true, moet natuurlijk op basis van de uitkomst. @robin1
        return True

    def left(self, speed: int) -> bool:
        """
        Speed and direction of the left wheels
        :param speed: Range from -255 to 255
        :return: returns a bool based on success
        :raises: Value error when speed is out of the range
        """
        if speed > -256 and speed < 256:
            if speed > -4 and speed < 4:
                self.speedl = 0
                self.richtingl = 0
            if speed > 0:
                self.speedl = speed
                self.richtingl = 1
            if speed < 0:
                self.speedl = -speed
                self.richtingl = 2
        else:
            raise ValueError("{0} is not in the range of -255 to 255".format(speed))

        if self._send_data() :
            return True
        else:
            return False

    def right(self, speed: int) -> bool:
        """
        Speed and direction of the right wheels
        :param speed: Range from -255 to 255
        :return: returns a bool based on success
        :raises: Value error when speed is out of the range
        """
        if speed > -256 and speed < 256:
            if speed > -4 and speed < 4:
                self.speedr = 0
                self.richtingr = 0
            if speed > 4:
                self.speedr = speed
                self.richtingr = 1
            if speed < -4:
                self.speedr = -speed
                self.richtingr = 2
        else:
            raise ValueError("{0} is not in the range of -255 to 255".format(speed))

        if self._send_data():
            return True
        else:
            return False

    def status(self) -> dict:
        """
        Generates the current state of the motor
        :return: returns a dictionary with the status
        """
        return {
            "speedl": self.speedl,
            "richtingl": self.richtingl,
            "speedr": self.speedr,
            "richtingr": self.richtingr
        }

    def get_speed(self) -> dict:
        """
        :return: returns a dictionary with the speeds
        """
        return {
            "speedl": self.speedl,
            "speedr": self.speedr
        }

    def get_value_left(self) -> int:
        """
        Get left speed value
        :return (int): value
        """
        return self.speedl

    def get_value_right(self) -> int:
        """
        Get right speed value
        :return (int): value
        """
        return self.speedr

    def _send_data(self) -> bool:
        """
        generate an array of data for the motorcontroller and sends it over the I2C bus
        :return: returns a bool based on success
        """
        if config["Motor"].getboolean("simulate_motor") == False:
            try:
                motor_data = [7, 3, self.speedl, self.richtingl, 3, self.speedr, self.richtingr]
                self.bus.write_i2c_block_data(self.ADDRESS, self.OFFSET, motor_data)
            except IOError as e:
                print("I/O error({0}): {1}".format(e.errno, e.strerror))
                return False
            else:
                return True
        else:
            return True
