import numpy as np
from src.common.log import *
import cv2, time, base64, asyncio
import src.hardware.camera as camera

DEBUG = config['General'].getint('DEBUG')

framerate = config["Camera"].getint("framerate")
look_for_faces_timeout = config["FaceDetection"].getfloat("look_for_faces_timeout")
# TODO getter en setter voor photodata is wel netjes
photodata = []
color = (0, 0, 255)


def get_faces(photo: np.array):
    """
    Geeft alle gezichten terug die door opencv gevonden worden in de foto, met de confidence score voor elk gezicht

    Args:
       photo: De foto met gezichten

    Returns:
       Een list met de coordinaten van de gezichten en een lijst met confidence scores
    """
    if DEBUG >= 2:
        log.debug("Opencv Input image size:" + str(photo.shape))

    img_gray = cv2.cvtColor(photo, cv2.COLOR_BGR2GRAY)

    face_cascade = cv2.CascadeClassifier(config['FaceDetection']['HAAR_CASCADE_PATH'])

    if face_cascade is None:
        message = "Face cascade failed to load!"
        log.error(message)
        raise FileNotFoundError(message)

    opencv_min_face_size = config['FaceDetection'].getint('OPENCV_MIN_FACE_SIZE')
    faces, _, confidences = face_cascade.detectMultiScale3(
        img_gray,
        scaleFactor=config['FaceDetection'].getfloat('OPENCV_SCALE_FACTOR'),
        minNeighbors=config['FaceDetection'].getint('OPENCV_MIN_NEIGHBORS'),
        minSize=(opencv_min_face_size, opencv_min_face_size),
        outputRejectLevels=True
    )

    if len(confidences) and DEBUG >= 2:
        log.debug("face confidence " + str(confidences[0]))

    if DEBUG >= 2 and len(faces):
        log.debug("got " + str(len(faces)) + " faces! (in one foto)")

    return zip(faces, confidences)


def crop_image(img: np.array, rect: list, padding: int) -> np.array:
    """
    Knip een vierkant uit een array zoals aangegeven in rect, met padding in pixels

    Args:
       img: foto
       rect: (x,y,w,h) (top left xt coordinates, width and height)

    Returns:
       De uitgeknipte foto.
    """

    x, y, w, h = rect
    x -= padding
    y -= padding
    w += (padding * 2)
    h += (padding * 2)

    # prevent face cutout being out of image range
    photo_w, photo_h, _ = img.shape

    if x < 0:
        x = 0
    if y < 0:
        y = 0

    if x + w > photo_w:
        w = photo_w - x

    if y + h > photo_h:
        h = photo_h - y

    return img[y:(y + h), x:(x + w)]


def cut_out_head(face, photo: np.array, cut_out_paddign: float) -> np.array:
    """
    Haalt een gezicht uit de foto en geeft die weer terug als een aparte foto

    Args:
        face: Het gezicht met locatie
        photo: De volledige foto waaruit je het gezicht wilt knippen

    Returns:
        Het gezicht als een aparte foto
    """
    x, y, w, h = face.pos

    padding = int(round(w * cut_out_paddign))
    cutout = _crop_image(photo, face.pos, padding)

    return cutout


def draw_rectangle(frame, rect, texts=(""), color=(0, 0, 255)):
    """
    draws a rectangle at rect (x, y, w, h) position
    @param frame: image to draw on
    @param rect: x,y,w,h
    @param texts: text to display
    @param color: bgr color uint8 tuple (255, 0, 0) = blue
    @return frame with rectangle
    """
    try:
        height, width, _ = frame.shape
    except ValueError:
        height, width = frame.shape

    x, y, w, h = rect
    letter_size_px = 11
    text_margin_px = 2

    # float text left or right of rect, based on the longest text

    longest_text = 0
    for text in texts:
        if len(text) > longest_text:
            longest_text = len(text)

    text_size = letter_size_px * longest_text
    text_offset = int(x + w + text_margin_px)
    if width - text_offset < text_size:
        text_offset = int(x - text_size - text_margin_px)

    text_nr = 1
    for text in texts:
        frame = draw_text(frame, text, (text_offset, int(y + (text_nr * letter_size_px))))
        text_nr += 1

    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

    return frame


def draw_image(img) -> None:
    """
    Laat het plaatje zien.

    @param Plaatje
    """
    cv2.imshow("FYS", img)
    cv2.waitKey()


def draw_text(img, text, pos, size=1):
    """
    draw text on an image
    @param img: image to draw on
    @param text: text to display
    @param pos: position
    @param size: size of the text. Default 1
    @return image with text
    """
    font = cv2.FONT_HERSHEY_DUPLEX
    thickness = 1
    cv2.putText(img, text, pos, font, size, (0, 0, 255), thickness, cv2.LINE_AA)
    return img


def get_processed_frame():
    """
    get the current frame from the camera with face detection.
    @return: frame with rectangles on the faces
    @rtype: cv2 numpy array
    """
    global framerate, photodata, color
    time.sleep((1.0 / framerate))
    frame = camera.get_frame()
    log.debug("get fd: %s", photodata)
    for face, conf in photodata:
        frame = draw_rectangle(frame, face, color=color)

    return frame


def process_frames_forever():
    """
    get new frame from camera and processes this. Stores result in `photodata`
    """
    global look_for_faces_timeout, photodata
    current_frame = camera.get_frame()
    last_frame = None
    while True:
        time.sleep(look_for_faces_timeout)
        if not (np.array_equal(current_frame, last_frame)):
            current_frame = camera.get_frame()
            photodata = list(get_faces(current_frame))
            log.debug("set photodata: %s", photodata)
            last_frame = current_frame


def frame2jpg(frame):
    """
    turn an numpy array into a jpg
    @return jpg image
    @rtype: jpg
    """
    return cv2.imencode('.jpg', frame)[1].tostring()


def to_base64(object):
    """
    encode object into base64
    @return: base64 string of object
    @rtype: base64 string
    """
    return (base64.b64encode(object)).decode("utf-8")


if __name__ == "__main__":
    log.warn("Running as main")
    frame = cv2.imread("cam_emulate.jpg", 0)
    for face, conf in get_faces(frame):
        log.debug("conf: %s", conf)
        frame = draw_rectangle(frame, face)
    cv2.imwrite("./out/FaceFrame.jpg", frame)
