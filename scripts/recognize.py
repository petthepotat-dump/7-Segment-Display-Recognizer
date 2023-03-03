import cv2
import imutils
from imutils import contours
from imutils.perspective import four_point_transform

import numpy as np
import math

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

DIGITS_LOCATION = [
    (0.5, 0.1), # top
    (0.2, 0.3), # topleft
    (0.8, 0.3), # topright
    (0.5, 0.5), # middle
    (0.2, 0.7), # bottomleft
    (0.8, 0.7), # bottomright
    (0.5, 0.9), # bottom
]

DIST_LIM = 0.15
POINTS = [
    0.7358280423280423, 0.46106150793650796,
    0.7755121693121693, 0.4615575396825397,
    0.7753677248677249, 0.477390873015873,
    0.734457671957672, 0.4776388888888889
]

def init(points, dist_limit):
    global POINTS, DIST_LIM
    POINTS = points
    DIST_LIM = dist_limit

# --------------------------------- #

def get_abs_screen_coords(screen_size, rel_points):
    p = [
        int(rel_points[0]*screen_size[1]), 
        int(rel_points[1]*screen_size[0]),
        int(rel_points[2]*screen_size[1]), 
        int(rel_points[3]*screen_size[0]),
        int(rel_points[4]*screen_size[1]), 
        int(rel_points[5]*screen_size[0]),
        int(rel_points[6]*screen_size[1]), 
        int(rel_points[7]*screen_size[0])
    ]
    return np.array(p)

def find_digits(image):
    # ------------------ pre-process ------------------
    # extract display
    # translate points from relative to abs image coords
    r = get_abs_screen_coords(image.shape, POINTS).reshape((4, 2))
    output = four_point_transform(image, r)
    # output = imutils.resize(output, height=500)
    # make darker blobs darker
    hsv = cv2.cvtColor(output, cv2.COLOR_BGR2HSV)
    for i in range(hsv.shape[0]):
        for j in range(hsv.shape[1]):
            if hsv[i, j, 2] < 72:
                hsv[i, j, 2] *= 0
    # grayscale
    bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)


    # checkpoint 1
    # cv2.imshow("gray", imutils.resize(gray, height=500))
    # cv2.waitKey(0)

    # threshold
    thresh = cv2.threshold(gray, 77, 255, cv2.THRESH_BINARY_INV)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 5))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

    # checkpoint 2
    # cv2.imshow("thres", imutils.resize(thresh, height=500))
    # cv2.waitKey(0)

    # contours
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    digitCnts = []
    contour = cv2.Canny(thresh, 20, 200)
    # loop over the digit area candidates
    for c in cnts:
        # compute the bounding box of the contour
        (x, y, w, h) = cv2.boundingRect(c)
        # if the contour is sufficiently large, it must be a digit
        if w >= 40 and (h >= 40 and h <= 200):
            digitCnts.append(c)
            # draw rect around digit
            cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 1)
    
    # checkpoitn 3
    # cv2.imshow("output", imutils.resize(output, height=500))
    # cv2.waitKey(0)

    # TODO -- IMPORATN
    # split into 3 sections for 3 digits
    displays = []
    img0 = thresh[:, :thresh.shape[1]//4]
    img1 = thresh[:, thresh.shape[1]//4:thresh.shape[1]//4*2]
    img2 = thresh[:, thresh.shape[1]//2:thresh.shape[1]//4*3]
    img3 = thresh[:, thresh.shape[1]//4*3:]

    a = 0
    b = 0
    c = 0
    d = 0
    try:
        a = find_digit(img0)
    except: pass
    try:
        b = find_digit(img1)
    except: pass
    try:
        c = find_digit(img2)
    except: pass
    try:
        d = find_digit(img3)
    except: pass
    return [a, b, c, d]



def find_digit(image):
    """Find the digit in the image"""
    # display image
    img3 = image.copy()
    for i in range(len(DIGITS_LOCATION)):
        x = int(DIGITS_LOCATION[i][0] * img3.shape[1])
        y = int(DIGITS_LOCATION[i][1] * img3.shape[0])
        cv2.circle(img3, (x, y), 1, (255, 255, 255), -1)

    # cv2.imshow("image", imutils.resize(img3, height=500))
    # cv2.waitKey(0)

    # check if colored in certain radius around points
    blocks = [0] * 7
    for i, p in enumerate(DIGITS_LOCATION):
        x = int(p[0] * image.shape[1])
        y = int(p[1] * image.shape[0])
        # check if pixel is white
        if image[y, x] == 255:
            blocks[i] = 1

    # print(blocks)
    return DIGITS_LOOKUP[tuple(blocks)]







    cnts = cv2.findContours(image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    digitCnts = []
    # loop over digit area candidates
    for c in cnts:
        # compute the bounding box of the contour
        (x, y, w, h) = cv2.boundingRect(c)
        # if the contour is sufficiently large, it must be a digit
        if w >= 40 and (h >= 40 and h <= 200):
            digitCnts.append(c)

    # TODO - fix empty arr

    # sort contours
    # find bounding rect of segmnets
    brect = [1e9, 1e9, 0, 0]
    # draw contours onto image
    image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    legalConts = []
    for c in digitCnts:
        if cv2.contourArea(c) < 100:
            continue
        cv2.drawContours(image, [c], -1, (0, 255, 0), 1)
        (x, y, w, h) = cv2.boundingRect(c)
        brect[0] = min(brect[0], x)
        brect[1] = min(brect[1], y)
        brect[2] = max(brect[2], x+w)
        brect[3] = max(brect[3], y+h)
        legalConts.append(c)
    # remap texture again
    remap = image[brect[1]:brect[1]+brect[3], brect[0]:brect[0]+brect[2]]
    # check if digit is actually found
    if brect[0] == 1e9 or brect[1] == 1e9 or brect[2] == 0 or brect[3] == 0:
        return None

    # shift rectanlge
    brect[2] -= brect[0]
    brect[3] -= brect[1]
    shift = (brect[0], brect[1])
    brect[0] = 0
    brect[1] = 0

    # check if 1 (cuz diff)
    if brect[2] < 100: return 1

    # loop through each existing contour ==> figure outthere relative location.,
    # check if near center
    def find_distance(first, second):
        return math.sqrt((first[0] - second[0])**2 + (first[1] - second[1])**2)
    def find_rel(point, dimensions):
        return (point[0]/dimensions[0], point[1]/dimensions[1])
    # loop through segments
    active_segments = []
    for con in legalConts:
        # find center location
        rect = cv2.boundingRect(con)
        # print(rect)
        cx = (rect[0] + rect[0] + rect[2])//2
        cy = (rect[1] + rect[1] + rect[3])//2
        center = ((cx-shift[0])/remap.shape[1], (cy-shift[1])/remap.shape[0])
        
        # check if contour overalops with rectangle
        

        # find distance from position
        distance = find_distance(center, (brect[2]//2, brect[3]//2))
        closest_point = (-1, 1e9)
        
        
        for i, seg in enumerate(DIGITS_LOCATION):
            # find distance from center
            dist = find_distance(center, seg)
            if dist < DIST_LIM:
                closest_point = (i, dist)
        # print(closest_point)
        active_segments.append(closest_point[0])

        # draw center onto image
        cv2.rectangle(remap, (rect[0], rect[1]), (rect[0]+rect[2], rect[1]+rect[3]), (0, 0, 255), 1)
        cv2.circle(remap, (cx, cy), 5, (0, 0, 255), -1)
    # generate the array
    on =     [0] * 7
    for i in active_segments:
        on[i] = 1
    
    # draw segments onto mask
    mask = remap.copy()
    for i, seg in enumerate(DIGITS_LOCATION):
        if on[i]:
            cv2.circle(mask, 
                tuple(map(int, (seg[0] * mask.shape[1], seg[1] * mask.shape[0]))),
                5, (0, 255, 0), -1)
    
    # print(on)
    # draw mask on top of image
    
    cv2.imshow('img1', mask)
    cv2.waitKey(0)
    return DIGITS_LOOKUP[tuple(on)]




