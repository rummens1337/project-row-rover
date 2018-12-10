#Libraries
from src.common.log import *
import time

if config["RangeSensor"].getboolean("simulate_rangesensor") is False:
    import RPi.GPIO as GPIO
else:
    import src.dummy.GPIOdummy as GPIO

class DistanceSensor():

    def __init__(self,TRIGGER,ECHO):
        self.distance = 0
        self.startTime = time.time()
        self.stopTime = time.time()
        self.sonicSpeed = 34300

        #GPIO Mode (BOARD / BCM)
        GPIO.setmode(GPIO.BOARD)

        #set GPIO Pins
        self.GPIO_TRIGGER = TRIGGER
        self.GPIO_ECHO = ECHO

        #set GPIO direction (IN / OUT)
        GPIO.setup(self.GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO, GPIO.IN)

        # Define an ISR for when an ECHO is received on the sensor.
        GPIO.add_event_detect(self.GPIO_ECHO, GPIO.RISING, callback=self.echoInterruptHandler())

        # Send pulse to initialize the loop
        self.sendPulse()

    def sendPulse(self):
        # set Trigger to HIGH
        GPIO.output(self.GPIO_TRIGGER, True)

        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(self.GPIO_TRIGGER, False)

        # Save the starttime of pulse sent
        self.startTime = time.time()

        #
        # # save StartTime
        # while GPIO.input(self.GPIO_ECHO) == 0:
        #     StartTime = time.time()
        #
        # # save time of arrival
        # while GPIO.input(self.GPIO_ECHO) == 1:
        #     StopTime = time.time()
        #
        # # time difference between start and arrival
        # TimeElapsed = StopTime - StartTime
        # # multiply with the sonic speed (34300 cm/s)
        # # and divide by 2, because there and back
        # distance = (TimeElapsed * self.sonicSpeed) / 2


    def echoInterruptHandler(self):
        # Save time of arrival
        self.stopTime = time.time()

        # Time difference between start and arrival
        self.timeElapsed = (self.stopTime - self.startTime)

        # Multiply with the sonic speed (34300 cm/s)
        # Divide by two because it travels to and back
        self.distance = (self.timeElapsed * self.sonicSpeed) / 2
        self.sendPulse()

    def getDistanceCM(self) -> float:
        return self.distance


