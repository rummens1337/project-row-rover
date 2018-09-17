import smbus


class Motor:
    MOTORR = [7, 3, 0xa5, 1, 3, 0xa5, 2]  # High speed left backwards + right forward
    MOTORL = [7, 3, 0xa5, 2, 3, 0xa5, 1]  # High speed left forwards + right backwards
    MOTORHF = [7, 3, 0xa5, 2, 3, 0xa5, 2]  # High speed forward left + right; add explanation
    MOTORST = [7, 0, 0, 0, 0, 0, 0]  # Stop left + right; add explanation
    MMOTORHR = [7, 3, 0xa5, 1, 3, 0xa5, 1]  # High speed reverse left + right; add explanation
    OFFSET = 0  # offset in the array
    ADDRESS = 0x32  # I2c address of the motorcontroller
    _speedLeft = 0
    _speedRight = 0

    def __init__(self):
        self.bus = smbus.SMBus(1)  # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1) <- found on internet, hope it makes sense to you
        self.bus.write_i2c_block_data(self.ADDRESS, self.OFFSET, self.MOTORST)  # Sets the motor to stop, just to be safe :P

    def stop(self) -> bool:
        self.bus.write_i2c_block_data(self.ADDRESS, self.OFFSET, self.MOTORST)
        self.bus.close()
        return True

    def left(self, v: int) -> bool:
        self.bus.write_i2c_block_data(self.ADDRESS, self.OFFSET, self.MOTORL)
        return True

    def right(self, v: int) -> bool:
        self.bus.write_i2c_block_data(self.ADDRESS, self.OFFSET, self.MOTORR)
        return True

    def status(self) -> dict:
        pass

    def get_speed(self) -> int:
        pass
