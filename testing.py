import cv2
import imutils
from imutils import contours

from scripts import recognize

# ------------------ data ------------------

# load assets/tets.jpg
image = cv2.imread("assets/2.jpg")

# make brighter -- increase v aspect o fhsv
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
for i in range(hsv.shape[0]):
    for j in range(hsv.shape[1]):
        if hsv[i, j, 2] > 70:
            hsv[i, j, 2] *= 1.5
image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

# show image
cv2.imshow("image", imutils.resize(image, height=500))
cv2.waitKey(0)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5, 5), 0)

thresh = cv2.threshold(gray, 66, 255, cv2.THRESH_BINARY_INV)[1]
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 5))
thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

#

# show thresh
cv2.imshow("thresh", imutils.resize(thresh, height=500))
cv2.waitKey(0)

x = recognize.find_digit(thresh)
print(x)

