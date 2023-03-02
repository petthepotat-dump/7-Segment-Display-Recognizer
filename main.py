from scripts import recognize
import cv2
import json

data = json.load(open("config.json", "r"))

POINTS = data["points"]
DIST_LIM = data["dist_lim"]

# ------------------ data ------------------ #

recognize.init(POINTS, DIST_LIM)

# ------------------------------------------ #

image = cv2.imread("sample2.jpg")
recognize.find_digits(image)
