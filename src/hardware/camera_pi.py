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

import cv2
if config["Lamp"].getboolean("simulate_camera") is False:
    import picamera


class Camera(object):
    """
    Declares variables to be used later on.
    """
    thread = None  # background thread that reads frames from camera
    frame = None  # current frame is stored here by background thread
    last_access = 0  # time of last client access to the camera

    def initialize(self):
        """
        Checks if there is a thread, if not creates and starts one.
        """
        if Camera.thread is None:
            # start background frame thread
            Camera.thread = threading.Thread(target=self._thread)
            Camera.thread.start()

            # wait until frames start to be available
            while self.frame is None:
                time.sleep(0)

    # TODO Check how to implement this functionality (class) better, maybe via the singleton pattern??
    def get_frame(self):
        """
        Is called to get frames
        @return frame as jpeg
        """
        if config["Camera"].getboolean("simulate_camera"):
            return cv2.imread("cam_emulate.jpg", 0)
        Camera.last_access = time.time()
        self.initialize()
        return self.frame

    # TODO merge this function's output (currently jpegs, should be something else in the future)
    # with Noeël's OpenCV project.
    @classmethod
    def _thread(cls):
        """
        Initializes and starts camera, then keeps putting jpeg's in frames.
        Frames get caught by get_frame function.
        """
        with picamera.PiCamera() as camera:
            # camera setup
            camera.resolution = (320, 140)
            camera.hflip = False
            camera.vflip = False

            # let camera warm up
            camera.start_preview()
            time.sleep(2)

            stream = io.BytesIO()
            for foo in camera.capture_continuous(stream, 'jpeg',
                                                 use_video_port=True):
                # store frame
                stream.seek(0)
                cls.frame = stream.read()

                # reset stream for next frame
                stream.seek(0)
                stream.truncate()

                # if there hasn't been any clients asking for frames in
                # the last 10 seconds stop the thread
                if time.time() - cls.last_access > 10:
                    break
        cls.thread = None
