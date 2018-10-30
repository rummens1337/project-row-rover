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
        self.look_for_faces_timeout = config["FaceDetection"].getint("look_for_faces_timeout")
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
        photodata = []
        cf = 0
        while True:
            time.sleep(1.0 / self.framerate)
            frame = camera.get_frame()
            cf+=1

            if cf == (self.framerate / self.look_for_faces_timeout):
                cf = 0
                photodata = list(image.get_faces(frame))

            for face, conf in photodata:
                frame = image.draw_rectangle(frame, face)


            frame = cv2.imencode('.jpg', frame)[1].tostring()


            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

