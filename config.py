
# this file is for configuring the points of the selected image
import cv2
import json

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

# mouse input handler
def mouse_handler(event, x, y, flags, param):
    # if left press
    if event == cv2.EVENT_LBUTTONDOWN:
        pts.append((x/image.shape[1],y/image.shape[0]))
        if len(pts) > 4:
            pts.pop(0)
        cv2.circle(mask, (x, y), 5, (0, 0, 255), -1)

# display image
cv2.imshow("image", image)
cv2.setMouseCallback("image", mouse_handler)

while True:
    # display image
    cv2.imshow("image", image)
    # render points
    
    key = cv2.waitKey(1)
    if key == ord("q"):
        break

