import cv2
import imutils
from imutils import contours
from imutils.perspective import four_point_transform

import numpy as np


# ------------------ data ------------------
DIGITS_LOOKUP = {
    (1, 1, 1, 0, 1, 1, 1): 0,
    (0, 0, 1, 0, 0, 1, 0): 1,
    (1, 0, 1, 1, 1, 1, 0): 2,
    (1, 0, 1, 1, 0, 1, 1): 3,
    (0, 1, 1, 1, 0, 1, 0): 4,
    (1, 1, 0, 1, 0, 1, 1): 5,
    (1, 1, 0, 1, 1, 1, 1): 6,
    (1, 0, 1, 0, 0, 1, 0): 7,
    (1, 1, 1, 1, 1, 1, 1): 8,
    (1, 1, 1, 1, 0, 1, 1): 9
}

# black background
NUM_RANGE = [
    [(0, 0, 0), (180, 255, 10)],
]

POINTS = [
    [0.5407407407407407, 0.3972222222222222],
    [0.8777777777777778, 0.39166666666666666],
    [0.8740740740740741, 0.6652777777777777],
    [0.516666666666666, 0.6569444444444444]
]

LEVEL2 = [
    [0.425, 0.1773049645390071],
    [0.7791666666666667, 0.24680851063829787],
    [0.46111111111111114, 0.5276595744680851],
    [0.8208333333333333, 0.5219858156028369],
]
# --------------------------------- #


def get_abs_screen_coords(screen_size, rel_points):
    p = [
        int(rel_points[0][0]*screen_size[1]
            ), int(rel_points[0][1]*screen_size[0]),
        int(rel_points[1][0]*screen_size[1]
            ), int(rel_points[1][1]*screen_size[0]),
        int(rel_points[2][0]*screen_size[1]
            ), int(rel_points[2][1]*screen_size[0]),
        int(rel_points[3][0]*screen_size[1]
            ), int(rel_points[3][1]*screen_size[0])
    ]
    return np.ndarray(shape=(4, 2), dtype=np.int32, buffer=np.array(p))


def get_mouse_position(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, y)


image = cv2.imread("assets/sample2.jpg")
# image = imutils.resize(image, height=720)
# buf = image.copy()
# ------------------ pre-process ------------------
# extract display
# translate points from relative to abs image coords

r = get_abs_screen_coords(image.shape, POINTS)
output = four_point_transform(image, r)
output = imutils.resize(output, height=720)

# cv2.imshow('test', output)
# cv2.setMouseCallback('test', get_mouse_position)
# cv2.waitKey(0)
# exit()
# extract text box :D
r = get_abs_screen_coords(output.shape, LEVEL2)
output = four_point_transform(output, r)
output = imutils.resize(output, height=720)

# contours


cv2.imshow('image', output)
cv2.waitKey(0)
exit()


# ------------------ find contours ------------------
cv2.imshow('image', result)
cv2.setMouseCallback('image', get_mouse_position)
cv2.waitKey(0)
