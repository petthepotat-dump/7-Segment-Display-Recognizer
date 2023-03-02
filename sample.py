import cv2
import imutils
from imutils import contours
from imutils.perspective import four_point_transform

import numpy as np


# ------------------ data ------------------
DIGITS_LOOKUP = {
    (1, 1, 1, 0, 1, 1, 1): 0,
    (0, 0, 1, 0, 0, 1, 0): 1,
    (1, 0, 1, 1, 1, 0, 1): 2,
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

    [0.7305785123966942, 0.4606323620582765],
    [0.7759537190082644, 0.4606323620582765],
    [0.7760330578512397, 0.47489150650960943],
    [0.7322314049586777, 0.47489150650960943],


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


image = cv2.imread("sample2.jpg")
# image = imutils.resize(image, height=720)
# buf = image.copy()
# ------------------ pre-process ------------------
# extract display
# translate points from relative to abs image coords

r = get_abs_screen_coords(image.shape, POINTS)
output = four_point_transform(image, r)
output = imutils.resize(output, height=720)

# ------------------------------------
# contours
# threshold the warped image, then apply a series of morphological
# operations to cleanup the thresholded image
gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)

# cv2.imshow('image', gray)
# img = cv2.resize(image, (0, 0), fx=0.4, fy=0.4)
# cv2.imshow('image', img)
# print(img.shape)
# cv2.setMouseCallback('image', get_mouse_position)
# cv2.waitKey(0)
# exit()
# ------------------ numbers  ------------------

thresh = cv2.threshold(gray, 0, 255,
                       cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 5))
thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

# cv2.imshow('image', thresh)
# cv2.waitKey(0)


# eat nums
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
digitCnts = []
# loop over the digit area candidates
for c in cnts:
    # compute the bounding box of the contour
    (x, y, w, h) = cv2.boundingRect(c)
    # if the contour is sufficiently large, it must be a digit
    if w >= 200 and (h >= 200 and h <= 290):
        digitCnts.append(c)
        # draw box around figit
        cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 1)

cv2.imshow('image', thresh)
cv2.waitKey(0)


digitCnts = contours.sort_contours(digitCnts, method="left-to-right")[0]


cv2.imshow('image', output)
cv2.setMouseCallback('image', get_mouse_position)
cv2.waitKey(0)

# =============
# figure out a way to fix small error

digits = []
# loop over each of the digits
for c in digitCnts:
    # extract the digit ROI
    (x, y, w, h) = cv2.boundingRect(c)

    # cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 1)

    roi = thresh[y:y + h, x:x + w]
    # compute the width and height of each of the 7 segments
    # we are going to examine
    (roiH, roiW) = roi.shape
    (dW, dH) = (int(roiW * 0.25), int(roiH * 0.2))
    dHC = int(roiH * 0.05)
    # define the set of 7 segments
    segments = [
        ((0, 0), (w, dH)),  # top
        ((0, 0), (dW, h // 2)),  # top-left
        ((w - dW, 0), (w, h // 2)),  # top-right
        ((0, (h // 2) - dHC), (w, (h // 2) + dHC)),  # center
        ((0, h // 2), (dW, h)),  # bottom-left
        ((w - dW, h // 2), (w, h)),  # bottom-right
        ((0, h - dH), (w, h))  # bottom
    ]
    on = [0] * len(segments)

    # loop over the segments
    for (i, ((xA, yA), (xB, yB))) in enumerate(segments):
        # extract the segment ROI, count the total number of
        # thresholded pixels in the segment, and then compute
        # the area of the segment
        segROI = roi[yA:yB, xA:xB]
        total = cv2.countNonZero(segROI)
        area = (xB - xA) * (yB - yA)
        # if the total number of non-zero pixels is greater than
        # 50% of the area, mark the segment as "on"
        if total / float(area) > 0.5:
            on[i] = 1

    # lookup the digit and draw it on the image
    digit = DIGITS_LOOKUP[tuple(on)]
    print(digit)

    digits.append(digit)
    # draw a rectangle
    cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 1)
    cv2.putText(output, str(digit), (x - 10, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2)

print(digits)

cv2.imshow('image', thresh)
cv2.waitKey(0)
