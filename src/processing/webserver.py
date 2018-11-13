from flask import Flask, render_template, Response
# Raspberry Pi camera module (requires picamera package, developed by Miguel Grinberg)
import src.hardware.camera as camera
import time
from src.common.log import *
import threading
import src.processing.image as image

import cv2


class WebServer:

    def __init__(self, server):
        self.server = server
        server.add_url_rule('/', 'index', self.index)
        server.add_url_rule('/video_feed', 'video_feed', self.video_feed)

    def index(self):
        """Video streaming home page."""
        return render_template('index.html')

    def video_feed(self):
        """

        @returns frame -
        """
        """Video streaming route. Put this in the src attribute of an img tag."""
        return Response(self.gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

    def gen(self):
        """Video streaming generator function."""
        while True:
            # TODO testen
            frame = image.frame2jpg(image.get_processed_frame())

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
