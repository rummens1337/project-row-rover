from flask import Flask, render_template, Response, redirect, request
import flask_login
from src.processing.User import User
import time
from src.common.log import *
import threading
import src.processing.image as image
import cv2


class WebServer:

    current_user = User()

    def __init__(self, server):
        self.server = server
        self.login_manager = flask_login.LoginManager()

        self.login_manager.init_app(self.server)

        self.server.add_url_rule('/', 'login', self.login)
        self.server.add_url_rule('/login', 'post', self.post, methods=['POST'])
        self.server.add_url_rule('/login', 'login', self.login, methods=['GET'])
        self.server.add_url_rule('/logout', 'logout', self.logout)
        self.server.add_url_rule('/rover', 'index', self.index)


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
        return render_template('communicator.html')

