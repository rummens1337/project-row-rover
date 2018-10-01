from flask import Flask, render_template, Response

# Raspberry Pi camera module (requires picamera package, developed by Miguel Grinberg)
from src.hardware.camera_pi import Camera

class WebServer:
    ###"""Not sure if this works properly, complains about type"""###

    def __init__(self, server):
        self.server = server

        server.add_url_rule('/', 'index', self.index)
        server.add_url_rule('/video_feed', 'video_feed', self.video_feed)

    def index(self):
        """Video streaming home page."""
        return render_template('index.html')

    def video_feed(self):
        """Video streaming route. Put this in the src attribute of an img tag."""
        return Response(self.gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')

    def gen(self, camera):
        """Video streaming generator function."""
        while True:
            frame = camera.get_frame()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')



    #app = Flask(__name__)
    #app.run(host='0.0.0.0', port =80, debug=True, threaded=True)