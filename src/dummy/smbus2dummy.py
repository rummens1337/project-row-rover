from src.common.log import *

# 0x3f = display
# 0x32 = 50 = motor
# 0x1e - compass


class SMBus(object):
    lastBlockData = 1
    lastCMD = 1

    def __init__(self, bus=None, force=False):
        log.debug("I2C bus created on /dev/i2c-" + str(bus))

    def write_byte_data(self, addr, cmd, data):
        self.lastCMD = cmd
        log.debug("I2C send data to adres " + str(addr)+" data: "+str(data)+" command: "+str(cmd))

    def write_byte(self, addr, cmd):
        self.lastCMD = cmd
        log.debug("I2C send data to adres " + str(addr) + " command: " + str(cmd))

    def write_i2c_block_data(self, addr, offset, motor_data):
        self.lastBlockData = motor_data
        log.debug("I2C send data to adres " + str(addr)+" data: "+str(motor_data)+" offset: "+str(offset))

    def write_block_data(self, addr, cmd, data):
        self.lastCMD = cmd
        log.debug("I2C send data to adres " + str(addr)+" data: "+str(data)+" command: "+str(cmd))

    def read_byte(self, addres):
        log.debug("I2C read byte from "+ str(addres))
        return self.lastBlockData

    def read_byte_data(self, addres, cmd):
        log.debug("I2C read byte from "+ str(addres)+" with command "+str(cmd))
        return self.lastBlockData

    def read_block_data(self, addres, cmd):
        log.debug("I2C read byte from "+ str(addres)+" with command "+str(cmd))
        return self.lastBlockData

    def read_i2c_block_data(self, addres, cmd):
        log.debug("I2C read byte from "+ str(addres)+" with command "+str(cmd))
        return [1, 2, 3, 4, 5, 6, 7, 8, 9]

    def close(self):
        log.debug("I2C bus closed")
