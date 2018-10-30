from src.common.log import *


class SMBus(object):
    lastBlockData = None
    lastCMD = None

    def __init__(self, bus=None, force=False):
        log.debug("I2C bus created on /dev/i2c-" + str(bus))

    def write_byte_data(self, addr, cmd, data):
        self.lastCMD = cmd
        log.debug("I2C send data to adres " + str(addr)+" data: "+str(data)+" command: "+str(cmd))

    def write_byte(self, addr, cmd):
        self.lastCMD = cmd
        log.debug("I2C send data to adres " + str(addr) + "command: " + str(cmd))

    def write_i2c_block_data(self, addr, offset, motor_data):
        self.lastBlockData = motor_data
        log.debug("I2C send data to adres " + str(addr)+" data: "+str(motor_data)+" offset: "+str(offset))

    def read_byte(self, addres):
        log.debug("I2C read byte from "+ str(addres))
        return self.lastBlockData

    def read_byte_data(self, addres, cmd):
        log.debug("I2C read byte from "+ str(addres)+" with command "+str(cmd))
        return self.lastBlockData

    def read_block_data(self, addres, cmd):
        log.debug("I2C read byte from "+ str(addres)+" with command "+str(cmd))
        return self.lastBlockData

    def close(self):
        log.debug("I2C bus closed")
