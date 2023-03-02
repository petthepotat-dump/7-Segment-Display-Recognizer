
# this file is for configuring the points of the selected image
import cv2
import json
import time
import numpy as np

# load config
data = json.load(open("config.json", "r"))

POINTS = data["points"]
DIST_LIM = data["dist_lim"]

# now to take in sample image
# and select the points
imput_image = input("Enter the path to the image: ")
image = cv2.imread(imput_image)
# create empty cv2 mask of same size as image
mask = np.zeros(image.shape, dtype=np.uint8)

pts = POINTS.copy()
change = False

# mouse input handler
def mouse_handler(event, x, y, flags, param):
    # if left press
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, y)
        change = True
        pts.append(x/image.shape[1])
        pts.append(y/image.shape[0])
        if len(pts) > 8:
            pts.pop(0)
            pts.pop(0)
        cv2.circle(mask, (x, y), 5, (0, 0, 255), -1)

# display image
cv2.imshow("image", image)
cv2.setMouseCallback("image", mouse_handler)

while True:
    if change:
        mask = np.zeros(image.shape, dtype=np.uint8)
        # render points
        print(pts)
        for i in range(4):
            cv2.circle(mask, (
                int(pts[i*2]*image.shape[1]),
                int(pts[i*2+1]*image.shape[0])
            ), 10, (0, 0, 255), -1)
    
    # display image
    cv2.imshow("image", cv2.bitwise_or(image, mask))

    # check if user wants to exit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

    time.sleep(1/30)

