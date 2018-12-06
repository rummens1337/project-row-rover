from flask import Flask, render_template, Response, redirect, request
import flask_login
from src.processing.UserManager import UserManager
# Raspberry Pi camera module (requires picamera package, developed by Miguel Grinberg)
import src.hardware.camera as camera
import time
from src.common.log import *
import threading
import src.processing.image as image
import cv2
from src.processing.database import *

class WebServer:

    current_user = UserManager()
    # db = Database()

    def __init__(self, server):
        self.server = server
        self.login_manager = flask_login.LoginManager()

        self.login_manager.init_app(self.server)

        self.server.add_url_rule('/', 'login', self.login)
        self.server.add_url_rule('/login', 'post', self.post, methods=['POST'])
        self.server.add_url_rule('/login', 'login', self.login, methods=['GET'])
        self.server.add_url_rule('/logout', 'logout', self.logout)
        self.server.add_url_rule('/operator', 'opp', self.operator)
        self.server.add_url_rule('/communicator', 'comm', self.communicator)
        self.server.add_url_rule('/video_feed', 'video_feed', self.video_feed)

        self.framerate = config["Camera"].getint("framerate")
        self.look_for_faces_timeout = config["FaceDetection"].getint("look_for_faces_timeout")

    def post(self):
        # With database
        # res = db.select(table = "user", columns = [Column("id"), Column("password"), Column("can_drive"), Column("can_speak")], joins = [], where = "`user_name` = '"+request.form['username']+"'")

        # if(request.form['password'] == res[0]['user_password']):
        #     self.current_user.is_authenticated = True
        #     self.current_user.can_drive = res[0]['user_can_drive'] == 1
        #     self.current_user.can_speak = res[0]['user_can_speak'] == 1
        # return redirect("/")
        
        # Without database
        if(request.form['password'] == 'qpzn'):
            self.current_user.is_authenticated = True
            self.current_user.can_drive = 1 == 1
            self.current_user.can_speak = 1 == 1
        return redirect("/")

    def login(self):
        if self.current_user.is_authenticated:
            if self.current_user.can_drive:
                return redirect("/operator")
            if self.current_user.can_speak:
                return redirect("/communicator")
            return self.server.login_manager.unauthorized()
        return render_template('login.html')

    def logout(self):
        self.current_user = User()
        return redirect("/")

    def operator(self):
        if not self.current_user.is_authenticated:
            return redirect("/")
        if not self.current_user.can_drive:
            return self.server.login_manager.unauthorized()

        return render_template('operator.html')

    def communicator(self):
        if not self.current_user.is_authenticated:
            return redirect("/")
        if not self.current_user.can_speak:
            return self.server.login_manager.unauthorized()

        return render_template('communicator.html')

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
