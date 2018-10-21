from flask import Flask, render_template, Response
# Raspberry Pi camera module (requires picamera package, developed by Miguel Grinberg)
import src.hardware.camera_pi as camera
import time
from src.common.log import *
import threading
import src.processing.image as image
import cv2

class WebServer:

    def __init__(self, server):
        # TODO is het verstandig dat dit in een thread zit?
        # TODO deze thead werkt niet eens omdat het geen `run()` functie heeft.
        # threading.Thread.__init__(self)
        # self.daemon = True
        self.server = server
        camera.initialize()
        # self.camera = Camera()
        server.add_url_rule('/', 'index', self.index)
        server.add_url_rule('/video_feed', 'video_feed', self.video_feed)

    def index(self):
        """Video streaming home page."""
        return render_template('index.html')

    def video_feed(self):
        """

        @returns frame -
        """
        #time.sleep(0.03)
        """Video streaming route. Put this in the src attribute of an img tag."""
        return Response(self.gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

    def gen(self):
        """Video streaming generator function."""
        while True:
            # self.video_feed()
            # log.debug("gen loop")
            frame = camera.get_frame()
            time.sleep(0.0001)
            for face, conf in image.get_faces(frame):
                # log.debug("conf: %s", conf)
                frame = image.draw_rectangle(frame, face)
            frame = cv2.imencode('.jpg', frame)[1].tostring()
            yield (b'--frame\r\n'
                   #    TODO crashed in emulated mode
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
