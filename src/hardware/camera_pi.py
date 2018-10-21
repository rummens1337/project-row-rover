#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  camera_pi.py
#
#
#
import time
import io
import threading
from src.common.log import *
import atexit

import cv2

if config["Camera"].getboolean("simulate_camera") is False:
    import picamera
    from picamera.array import PiRGBArray

"""
Declares variables to be used later on.
"""
thread = None  # background thread that reads frames from camera
frame = None  # current frame is stored here by background thread
last_access = 0  # time of last client access to the camera

frame = cv2.imread("cam_emulate.jpg", 0)

def initialize():
    """
    Checks if there is a thread, if not creates and starts one.
    """
    global thread, frame
    if thread is None:
        # start background frame thread
        log.debug("new camera thread")
        # thread = threading.Thread(target=_thread)
        thread = thready_boy()
        thread.start()

        # wait until frames start to be available
        # while frame is None:
        #     time.sleep(0)


# TODO Check how to implement this functionality (class) better, maybe via the singleton pattern??
def get_frame():
    """
    Is called to get frames
    @return frame as jpeg
    """
    global thread, frame, last_access
    # if config["Camera"].getboolean("simulate_camera"):
    #     return cv2.imread("cam_emulate.jpg", 0)
    # last_access = time.time()
    # initialize()
    return frame


# TODO merge this function's output (currently jpegs, should be something else in the future)
# with Noeël's OpenCV project.
def _thread():
    """
    Initializes and starts camera, then keeps putting jpeg's in frames.
    Frames get caught by get_frame function.
    """
    global thread, frame, last_access

    camera = picamera.PiCamera()
    # with picamera.PiCamera() as camera:
    # camera setup
    # TODO lezen uit .conf
    log.debug("camera startup")
    camera.resolution = (320, 240)
    camera.framerate = 24
    rawCapture = PiRGBArray(camera, size=camera.resolution)
    camera.hflip = False
    camera.vflip = False

    # let camera warm up
    time.sleep(2)

    # while True:
    #     # camera.capture(rawCapture, format="bgr", use_video_port=True)
    #     # frame = rawCapture.array
    #     frame = cv2.imread("cam_emulate.jpg", 0)
    #     # log.debug("frame update")
    #     rawCapture.truncate(0)

    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        rawCapture.truncate(0)
        frame = frame.array

        # if there hasn't been any clients asking for frames in
        # the last 10 seconds stop the thread
        if time.time() - last_access > 10:
            break

    thread = None


# @atexit.register
def close(self):
    # TODO kijken of dit wel werkt @michel
    # self.thread.close()
    pass


class thready_boy(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.camera = picamera.PiCamera()
        # with picamera.PiCamera() as camera:
        # camera setup
        # TODO lezen uit .conf
        log.debug("camera startup")
        self.camera.resolution = (320, 240)
        self.camera.framerate = 24
        self.rawCapture = PiRGBArray(self.camera, size=self.camera.resolution)
        self.camera.hflip = False
        self.camera.vflip = False

    def run(self):
        global frame
        while True:
            self.camera.capture(self.rawCapture, format="bgr", use_video_port=True)
            frame = self.rawCapture.array
            # frame = cv2.imread("cam_emulate.jpg", 0)
            log.debug("frame update")
            # time.sleep(0.0001)
            self.rawCapture.truncate(0)
