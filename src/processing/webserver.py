from flask import Flask, render_template, Response, redirect, request
import flask_login
from src.processing.User import User
# Raspberry Pi camera module (requires picamera package, developed by Miguel Grinberg)
import src.hardware.camera as camera
import time
from src.common.log import *
import threading
import src.processing.image as image
import cv2


class WebServer:

    current_user = User()

    def __init__(self, server):
        self.server = server
        self.camera = Camera()
        self.login_manager = flask_login.LoginManager()

        self.login_manager.init_app(self.server)

        self.server.add_url_rule('/', 'login', self.login)
        self.server.add_url_rule('/login', 'post', self.post, methods=['POST'])
        self.server.add_url_rule('/login', 'login', self.login, methods=['GET'])
        self.server.add_url_rule('/logout', 'logout', self.logout)
        self.server.add_url_rule('/rover', 'index', self.index)
        self.server.add_url_rule('/video_feed', 'video_feed', self.video_feed)

        self.framerate = config["Camera"].getint("framerate")
        self.look_for_faces_timeout = config["FaceDetection"].getint("look_for_faces_timeout")

    def post(self):
        # TODO make somekind of central database for users?
        if(request.form['username'] == 'robin' and request.form['password'] == 'qpzn'):
            self.current_user.is_authenticated = True
        return redirect("/")

    def login(self):
        if self.current_user.is_authenticated:
            return redirect("/rover")
        return render_template('login.html')

    def logout(self):
        self.current_user = User()
        return redirect("/")

    def index(self):
        if not self.current_user.is_authenticated:
            return redirect("/")

        """Video streaming home page."""
        return render_template('operator.html')

    def video_feed(self):
        if not self.current_user.is_authenticated:
            return self.server.login_manager.unauthorized()
        """

        @returns frame -
        """
        """Video streaming route. Put this in the src attribute of an img tag."""
        return Response(self.gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

    def gen(self):
        if not self.current_user.is_authenticated:
            return self.server.login_manager.unauthorized()
        """Video streaming generator function."""
        photodata = []
        cf = 0
        while True:
            time.sleep((1.0 / self.framerate))
            frame = camera.get_frame()
            cf += 1
            color = (0, 0, 255)

            if cf == (self.framerate / self.look_for_faces_timeout):
                cf = 0
                color = (0, 255, 0)
                photodata = list(image.get_faces(frame))

            for face, conf in photodata:
                frame = image.draw_rectangle(frame, face, color=color)

            frame = cv2.imencode('.jpg', frame)[1].tostring()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
