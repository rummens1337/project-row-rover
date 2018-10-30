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
        self.photodata = zip()
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
        cf = 0
        # face = None
        # conf = 0.0
        while True:
            log.debug(list(self.photodata))

            time.sleep(1.0 / self.framerate)

            frame = camera.get_frame()
            cf+=1

            if cf == (self.framerate / self.look_for_faces_timeout):
                cf = 0
                # TODO het ouwe vierkantje van het vorige herkende gezicht zou nog zichtbaar moeten zijn in de nieuwe frame.
                self.photodata = image.get_faces(frame)

            log.debug(list(self.photodata))
            log.debug(range(len(list(self.photodata))))
            # for i in range(len(list(self.photodata))):
            #     face, conf = list(self.photodata)
            #     log.debug(conf)
            #     log.debug("data: %s", conf[i])
            #     frame = image.draw_rectangle(frame, face[i])
            # else:
            #     log.debug("failed")


            frame = cv2.imencode('.jpg', frame)[1].tostring()
            log.debug(list(self.photodata))


            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

