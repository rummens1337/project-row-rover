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
        self.framerate = config["Camera"].getint("framerate")
        camera.start()
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
            frame = camera.get_frame()
            time.sleep(1.0 / self.framerate)
            for face, conf in image.get_faces(frame):
                frame = image.draw_rectangle(frame, face)
            frame = cv2.imencode('.jpg', frame)[1].tostring()
            yield (b'--frame\r\n'
                   #    TODO crashed in emulated mode
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
