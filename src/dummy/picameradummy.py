import time

from src.common.log import *


class PiCamera:
    testImage = "cam_emulate.jpg"
    use_video_port = False
    _resolution = (0, 0)

    def _init_defaults(self):
        self.sharpness = 0
        self.contrast = 0
        self.brightness = 50
        self.saturation = 0
        self.iso = 0 # auto
        self.video_stabilization = False
        self.exposure_compensation = 0
        self.exposure_mode = 'auto'
        self.meter_mode = 'average'
        self.awb_mode = 'auto'
        self.image_effect = 'none'
        self.color_effects = None
        self.rotation = 0
        self._hflip = self._vflip = False
        self.zoom = (0.0, 0.0, 1.0, 1.0)

    def _get_resolution(self):
        return self._resolution

    def _set_resolution(self, value):
        log.debug("Camera resolution set to "+str(value))
        self._resolution = value

    resolution = property(_get_resolution, _set_resolution, doc="""
        Retrieves or sets the resolution at which image captures, video
        recordings, and previews will be captured.""")

    def _get_hflip(self):
        return self._hflip

    def _set_hflip(self, value):
        log.debug("Camera hflip set to "+str(value))
        self._hflip = value

    hflip = property(_get_hflip, _set_hflip, doc="""\
        Retrieves or sets whether the camera's output is horizontally flipped.
        """)

    def _get_vflip(self):
        return self._vflip

    def _set_vflip(self, value):
        log.debug("Camera vflip set to "+str(value))
        self._vflip = value

    vflip = property(_get_vflip, _set_vflip, doc="""\
            Retrieves or sets whether the camera's output is horizontally flipped.
            """)

    def start_preview(self, **options):
        log.debug("Camera preview started")

    def capture_continuous(
            self, output, format=None, use_video_port=False, resize=None,
            splitter_port=0, burst=False, bayer=False, **options):
        log.debug("Video capture started, streaming to: "+str(output)+" In format: "+str(format)+" Using video port: "+str(use_video_port))
        yield None  # return camera stream instead?

    def __enter__(self):
        log.debug("Camera object entered ;) ")
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        log.debug("Camera object exit")
        del self

    def __init__(
            self, camera_num=0, stereo_mode='none', stereo_decimate=False,
            resolution=None, framerate=None, sensor_mode=0, led_pin=None,
            clock_mode='reset', framerate_range=None):
        self._init_defaults()
        self.resolution = resolution
        log.debug("Camera object created")
