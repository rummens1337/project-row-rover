from flask import Flask, render_template, Response
# Raspberry Pi camera module (requires picamera package, developed by Miguel Grinberg)
from src.hardware.camera_pi import Camera
import time
from src.common.log import *
import threading

class WebServer:

    def __init__(self, server):
        # TODO is het verstandig dat dit in een thread zit?
        # TODO deze thead werkt niet eens omdat het geen `run()` functie heeft.
        # threading.Thread.__init__(self)
        # self.daemon = True
        self.server = server
        self.camera = Camera()
        server.add_url_rule('/', 'index', self.index)
        server.add_url_rule('/video_feed', 'video_feed', self.video_feed)

    def index(self):
        """Video streaming home page."""
        return render_template('index.html')

    def video_feed(self):
        """

        @returns frame -
        """
        # TODO camera lag fixen, comment hieronder kan daarbij helpen
        #time.sleep(0.03)
        """Video streaming route. Put this in the src attribute of an img tag."""
        return Response(self.gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

    def gen(self):
        """Video streaming generator function."""
        while True:
            frame = self.camera.get_frame()
            yield (b'--frame\r\n'
                #    TODO crashed in emulated mode
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
