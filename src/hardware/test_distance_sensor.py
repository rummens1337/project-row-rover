import time
from src.common.log import *
from src.hardware.distance_sensor import DistanceSensor

distSensorLeft = DistanceSensor(config["RangeSensor"].getint("TRIGGER"), config["RangeSensor"].getint("ECHO_LEFT"))
distSensorRight = DistanceSensor(config["RangeSensor"].getint("TRIGGER"), config["RangeSensor"].getint("ECHO_RIGHT"))
distSensorFront = DistanceSensor(config["RangeSensor"].getint("TRIGGER"), config["RangeSensor"].getint("ECHO_FRONT"))

while True:
    distanceLeft = distSensorLeft.getDistanceCM()
    time.sleep(50)
    distanceRight = distSensorRight.getDistanceCM()
    time.sleep(50)
    distanceFront = distSensorFront.getDistanceCM()
    time.sleep(50)

    print("Measured DistanceLEFT = %.1f cm" % distanceLeft)
    print("Measured DistanceRIGHT = %.1f cm" % distanceRight)
    print("Measured DistanceFRONT = %.1f cm" % distanceFront)
    time.sleep(1)

# End of file
