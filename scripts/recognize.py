import cv2
import imutils
from imutils import contours
from imutils.perspective import four_point_transform

import numpy as np
import math

# ------------------ data ------------------

POINTS = [
    0.7358280423280423,
    0.46106150793650796,
    0.7755121693121693,
    0.4615575396825397,
    0.7753677248677249,
    0.477390873015873,
    0.734457671957672,
    0.4776388888888889,
]


def init(points):
    global POINTS
    POINTS = points


# --------------------------------- #
# utils


def get_abs_screen_coords(screen_size, rel_points):
    p = [
        int(rel_points[0] * screen_size[1]),
        int(rel_points[1] * screen_size[0]),
        int(rel_points[2] * screen_size[1]),
        int(rel_points[3] * screen_size[0]),
        int(rel_points[4] * screen_size[1]),
        int(rel_points[5] * screen_size[0]),
        int(rel_points[6] * screen_size[1]),
        int(rel_points[7] * screen_size[0]),
    ]
    return np.array(p)


def color_picker(image, scale=1):
    image = imutils.resize(image, width=scale * image.shape[1])

    def mouse_event(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            print(image[y, x])

    cv2.namedWindow("image")
    cv2.setMouseCallback("image", mouse_event)
    cv2.imshow("image", image)
    cv2.waitKey(0)


def display(image, scale=1):
    image = imutils.resize(image, width=scale * image.shape[1])
    cv2.imshow("image", image)
    cv2.waitKey(0)


# --------------------------------- #
# bubble recognition
