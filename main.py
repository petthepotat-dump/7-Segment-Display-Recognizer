from scripts import recognize
import cv2
import json

data = json.load(open("config.json", "r"))

POINTS = data["points"]
DIST_LIM = data["dist_lim"]

# ------------------ data ------------------ #

recognize.init(POINTS, DIST_LIM)

# ------------------------------------------ #

image = cv2.imread("image.jpg")
recognize.find_digits(image)

# ------------------------------------------ #
# video loading
# ------------------------------------------ #
video_path = input("input video path: ")
cap = cv2.VideoCapture(video_path)

data = []

while True:
	ret, frame = cap.read()
	if not ret:
		break
	nums = recognize.find_digits(frame)

	# insert formatting code

	# --
	# TODO - change this
	data.append(num)

	cv2.imshow("frame", frame)
	if cv2.waitKey(1) == ord("q"):
		break

cap.release()
cv2.destroyAllWindows()
# save data to file
result_path = input("where save file?: ")
with open(result_path, "w") as f:
	f.write("\n".join(data))

