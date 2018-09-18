import smbus


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
        self.bus = smbus.SMBus(1)  # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1) <- found on internet, hope it makes sense to you
        self.bus.write_i2c_block_data(self.ADDRESS, self.OFFSET, self.MOTORST)  # Sets the motor to stop, just to be safe :P

    #  stop the motors and stop the I2c bus connection
    def stop(self) -> bool:
        self.left(0)
        self.right(0)
        self.bus.close()
        return True

    # change the speed of the left wheels range: -255 to 255
    def left(self, v: int) -> bool:
        if v > -256 and v < 256:
            if v == 0:
                self.speedl = 0
                self.richtingl = 0
            if v > 0:
                self.speedl = v
                self.richtingl = 1
            if v < 0:
                self.speedl = -v
                self.richtingl = 2
        else:
            return False
        self._send_data()
        return True

    # change the speed of the right wheels range: -255 to 255
    def right(self, v: int) -> bool:
        if v > -256 and v < 256:
            if v == 0:
                self.speedr = 0
                self.richtingr = 0
            if v > 0:
                self.speedr = v
                self.richtingr = 1
            if v < 0:
                self.speedr = -v
                self.richtingr = 2
        else:
            return False
        self._send_data()
        return True

    #  send help
    def status(self) -> dict:
        pass

    #  send help
    def get_speed(self) -> int:
        pass

    #  generate an array of data for the motorcontroller and send it over the I2C bus
    def _send_data(self) -> bool:
        motor_data = [7, 3, self.speedl, self.richtingl, 3, self.speedr, self.richtingr]
        self.bus.write_i2c_block_data(self.ADDRESS, self.OFFSET, motor_data)
        return True
