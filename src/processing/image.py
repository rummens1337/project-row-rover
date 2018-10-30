import numpy as np
from src.common.log import *
import cv2

DEBUG = config['General'].getint('DEBUG')


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

    if DEBUG and len(faces):
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


if __name__ == "__main__":
    log.warn("Running as main")
    frame = cv2.imread("cam_emulate.jpg", 0)
    for face, conf in get_faces(frame):
        log.debug("conf: %s", conf)
        frame = draw_rectangle(frame, face)
    cv2.imwrite("./out/FaceFrame.jpg", frame)
