from flask import Flask, render_template, Response, redirect, request
import flask_login
from src.processing.User import User
# Raspberry Pi camera module (requires picamera package, developed by Miguel Grinberg)
from src.hardware.camera_pi import Camera
import time
from src.common.log import *
import threading

class WebServer:

    current_user = User()

    def __init__(self, server):
        # TODO is het verstandig dat dit in een thread zit?
        # TODO deze thead werkt niet eens omdat het geen `run()` functie heeft.
        # threading.Thread.__init__(self)
        # self.daemon = True
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
        return render_template('index.html')

    def video_feed(self):
        if not self.current_user.is_authenticated:
            return self.server.login_manager.unauthorized()
        """

        @returns frame -
        """
        # TODO camera lag fixen, comment hieronder kan daarbij helpen
        #time.sleep(0.03)
        """Video streaming route. Put this in the src attribute of an img tag."""
        return Response(self.gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

    def gen(self):
        if not self.current_user.is_authenticated:
            return self.server.login_manager.unauthorized()
        """Video streaming generator function."""
        while True:
            frame = self.camera.get_frame()
            yield (b'--frame\r\n'
                #    TODO crashed in emulated mode
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
