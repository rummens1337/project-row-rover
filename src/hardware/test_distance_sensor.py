import time
from src.common.log import *
# from src.hardware.distance_sensor import DistanceSensor

# distSensorLeft = DistanceSensor(config["RangeSensor"].getint("TRIGGER"), config["RangeSensor"].getint("ECHO_LEFT"))
# distSensorRight = DistanceSensor(config["RangeSensor"].getint("TRIGGER"), config["RangeSensor"].getint("ECHO_RIGHT"))
distSensorFront = (config["RangeSensor"].getint("TRIGGER"), config["RangeSensor"].getint("ECHO_FRONT"))
# lalala
while False:
    # distanceLeft = distSensorLeft.getDistanceCM()
    # time.sleep(50)
    # distanceRight = distSensorRight.getDistanceCM()
    # time.sleep(50)
    distSensorFront.sendPulse()
    time.sleep(0.06)
    distanceFront = distSensorFront.getDistanceCM()

    # print("Measured DistanceLEFT = %.1f cm" % distanceLeft)
    # print("Measured DistanceRIGHT = %.1f cm" % distanceRight)
    print("Measured DistanceFRONT = %.1f cm" % distanceFront)
    time.sleep(1)

# End of file
