from src.common.log import *
import atexit
import math
if config["Compas"].getboolean("simulate_compas") is False:
    import smbus2 as smbus
else:
    import src.dummy.smbus2dummy as smbus


class Compas:
    __Instance = None
    bus = None

    ADDRESS = 0x1e  # I2c address of the compass

    # some MPU6050 Registers and their Address
    Register_A = 0          # Address of Configuration register A
    Register_B = 0x01       # Address of configuration register B
    Register_mode = 0x02    # Address of mode register

    X_axis_H = 0x03         # Address of X-axis MSB data register
    Z_axis_H = 0x05         # Address of Z-axis MSB data register
    Y_axis_H = 0x07         # Address of Y-axis MSB data register
    declination = -0.00669  # define declination angle of location where measurement going to be done

    north = 0
    northeast = 45
    east = 90
    southeast = 135
    south = 180
    southwest = 225
    west = 270
    northwest = 315

    directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']

    def __init__(self):
        """
        Initilizes a Compas object, but only one. To use this class, use getInstance instead.
        @raises: exception when a instance of this class already exists
        """
        if Compas.__Instance is not None:
            raise Exception("Instance already exists")
        else:
            Compas.__Instance = self
            self.bus = smbus.SMBus(1)
            # write to Configuration Register A
            self.bus.write_byte_data(self.ADDRESS, self.Register_A, 0x70)
            # Write to Configuration Register B for gain
            self.bus.write_byte_data(self.ADDRESS, self.Register_B, 0xa0)
            # Write to mode Register for selecting mode
            self.bus.write_byte_data(self.ADDRESS, self.Register_mode, 0)

    @staticmethod
    def getInstance():
        """
        Initializes a compas object, but only one
        @return: The single only instance of this class
        """
        if Compas.__Instance is None:
            Compas()
        return Compas.__Instance

    def __convert(self, data, offset):
        # to get signed value from module
        value = ((int(data[offset]) << 8) | int(data[offset+1]))
        if value > 32768:
            value = value - 65536
        return value

    def read_raw_data(self):
        """
        Read data from a register in the compas
        @param addr: The address of the register to read
        @return: The data in the register in 16 bit
        """
        data = self.bus.read_i2c_block_data(self.ADDRESS, 0x00)
        #log.debug(str(data))
        x = self.__convert(data, 3)
        y = self.__convert(data, 7)
        z = self.__convert(data, 5)
        return x, y, z
        #Read raw 16-bit value
        # high = self.bus.read_byte_data(self.ADDRESS, addr)
        # low = self.bus.read_byte_data(self.ADDRESS, addr+1)

        #concatenate higher and lower value
        # value = ((high << 8) | low)
        #
        # #to get signed value from module
        # if(value > 32768):
        #     value = value - 65536
        # return value

    def getDegree(self) -> float:
        """
        Calculate the degree of the rover based on X and Y of the compas
        @return: The degree the rover is pointing at, range 0 to 360
        """
        # Read Accelerometer raw value
        # x = self.read_raw_data(self.X_axis_H)
        # z = self.read_raw_data(self.Z_axis_H)
        # y = self.read_raw_data(self.Y_axis_H)
        (x, y, z) = self.read_raw_data()
        # Calculate direction
        heading = math.atan2(y, x) + self.declination
        if heading > (2*math.pi):
            heading = heading - 2*math.pi
        # check for sign
        if heading < 0:
            heading = heading + 2*math.pi

        heading_angle = heading * 180/math.pi
        return heading_angle

    def getDirection(self) -> str:
        """
        Calculates the direction based on the degree
        @return: A direction in N, NE, E... based on the degree
        """
        degree = self.getDegree()
        number = round((degree/360.0)*8.0)
        if number > 7:
            number = 1
        return self.directions[number]

    @atexit.register
    def stop(self):
        """
        Stop the compas
        """
        self.bus.close()
