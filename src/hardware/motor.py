from time import sleep
from src.common.log import *
import threading
import math
if config["Motor"].getboolean("simulate_motor") is False:
    import smbus2 as smbus
    import RPi.GPIO as GPIO
else:
    import src.dummy.smbus2dummy as smbus
    import src.dummy.GPIOdummy as GPIO


class motor(threading.Thread):
    __Instance = None
    OFFSET = 0  # offset in the array
    ADDRESS = 0x32  # I2c address of the motorcontroller
    # variables for the Wheelencoder
    INTERVALSPEED = 0.5  # seconds
    ENCODERPIN1 = 12
    ENCODERHOLES = 20
    ENCODERCIRCUMFERENCE = (math.pi*24.0)/1000.0  # meters
    ENCODERHOLEDISTANCE = ENCODERCIRCUMFERENCE/ENCODERHOLES  # meters
    encoderPulses = 0
    encoderSpeed = 0  # meters/second
    # speed from 4 to 250
    speedl = 0
    speedr = 0
    # 0 = stilstaan 1 = vooruit 2 = achteruit
    richtingl = 0
    richtingr = 0

    def interruptPulse(self, channel):
        """
        Called by the wheel encoder when it creates a pulse, count the number of pulses
        @param channel: The pin of the interrupt
        """
        self.encoderPulses += 1

    def __init__(self):
        """
        Initilizes a motor object, but only one. To use this class, use getInstance instead.
        @raises: exception when a instance of this class already exists
        """
        if motor.__Instance is not None:
            raise Exception("Instance already exists")
        else:
            threading.Thread.__init__(self)
            self.start()
            motor.__Instance = self
            self.bus = smbus.SMBus(1)  # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(self.ENCODERPIN1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(self.ENCODERPIN1, GPIO.FALLING, callback=self.interruptPulse)
            self.left(0)
            self.right(0)

    @staticmethod
    def getInstance():
        """
        Initializes a compas object, but only one
        @return: The single only instance of this class
        """
        if motor.__Instance is None:
            motor()
        return motor.__Instance

    def __del__(self):
        """
        Closes the i2c bus.
        """
        self.left(0)
        self.right(0)
        self.bus.close()
        GPIO.cleanup()

    def run(self):
        while True:
            self.encoderSpeed = (self.encoderPulses*self.ENCODERHOLEDISTANCE)/self.INTERVALSPEED
            self.encoderPulses = 1
            #log.debug(str(self.encoderSpeed)+" "+str(self.encoderPulses)+" "+str(self.ENCODERHOLEDISTANCE)+" " +str(self.INTERVALSPEED))
            sleep(self.INTERVALSPEED)

    def left(self, speed: int) -> bool:
        """
        Speed and direction of the left wheels
        @param speed: Range from -255 to 255
        @return: returns a bool based on success
        @raises: Value error when speed is out of the range
        """
        if speed > -256 and speed < 256:
            if speed == 0:
                self.speedl = 0
                self.richtingl = 0
            if speed > 0:
                self.speedl = speed
                self.richtingl = 2
            if speed < 0:
                self.speedl = -speed
                self.richtingl = 1
        else:
            raise ValueError("{0} is not in the range of -255 to 255".format(speed))
        if self._send_data():
            return True
        else:
            return False

    def right(self, speed: int) -> bool:
        """
        Speed and direction of the right wheels
        @param speed: Range from -255 to 255
        @return: returns a bool based on success
        @raises: Value error when speed is out of the range
        """
        if speed > -256 and speed < 256:
            if speed == 0:
                self.speedr = 0
                self.richtingr = 0
            if speed > 0:
                self.speedr = speed
                self.richtingr = 2
            if speed < 0:
                self.speedr = -speed
                self.richtingr = 1
        else:
            raise ValueError("{0} is not in the range of -255 to 255".format(speed))
        if self._send_data():
            return True
        else:
            return False

    def status(self) -> dict:
        """
        Generates the current state of the motor
        @return: returns a dictionary with the status
        """
        return {
            "speedl": self.speedl,
            "richtingl": self.richtingl,
            "speedr": self.speedr,
            "richtingr": self.richtingr
        }

    def get_speed(self) -> float:
        """
        @return: returns a dictionary with the speeds
        """
        return self.encoderSpeed

    def get_value_left(self) -> int:
        """
        Get left speed value
        @return (int): value
        """
        return self.speedl

    def get_value_right(self) -> int:
        """
        Get right speed value
        @return (int): value
        """
        return self.speedr

    def _send_data(self) -> bool:
        """
        generate an array of data for the motorcontroller and sends it over the I2C bus
        @return: returns a bool based on success
        """
        try:
            motor_data = [7, 3, self.speedl, self.richtingl, 3, self.speedr, self.richtingr]
            self.bus.write_i2c_block_data(self.ADDRESS, self.OFFSET, motor_data)
        except IOError as e:
            print("I/O error({0}): {1}".format(e.errno, e.strerror))
            return False
        else:
            return True
