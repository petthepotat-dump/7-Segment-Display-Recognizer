from scripts import recognize
import cv2
import json

data = json.load(open("config.json", "r"))

POINTS = data["points"]
DIST_LIM = data["dist_lim"]
CHANGE_DIF = 5

# ------------------ data ------------------ #

recognize.init(POINTS, DIST_LIM)

# ------------------------------------------ #

image = cv2.imread("first_frame.jpg")
print(recognize.find_digits(image))
exit()

# ------------------------------------------ #
# video loading
# ------------------------------------------ #
# video_path = input("input video path: ")
video_path = "assets/sample.mp4"
cap = cv2.VideoCapture(video_path)

# save first frame to file
# ret, frame = cap.read()
# cv2.imwrite("first_frame.jpg", frame)
# exit()
data = []

def get_value(nums):
	return nums[0] * 100 + nums[1] * 10 + nums[2] + nums[3]/10

ret, frame = cap.read()
nums = recognize.find_digits(frame)
data.append((get_value(nums), nums[0], nums[1], nums[2], nums[3]))
print(get_value(nums))


while True:
	ret, frame = cap.read()
	if not ret:
		break
	nums = recognize.find_digits(frame)
	if nums[0] == -1:
		nums[0] = data[-1][1]
	if nums[1] == -1:
		nums[1] = data[-1][2]
	if nums[2] == -1:
		nums[2] = data[-1][3]
	if nums[3] == -1:
		nums[3] = data[-1][4]
	# insert formatting code
	# check with previous problem
	vv = get_value(nums)
	value = vv
	# check if value is off by too much lmao just in case
	if abs(data[-1][0] - vv) > CHANGE_DIF:
		value = data[-1][0] * 0.99 + nums[0] * 0.01

	print(vv, value, abs(data[-1][0] - vv))
	vv = value
	# --
	# TODO - change this
	data.append((value, nums[0], nums[1], nums[2], nums[3]))

	cv2.imshow("frame", frame)
	if cv2.waitKey(1) == ord("q"):
		break

cap.release()
cv2.destroyAllWindows()
# save data to file
result_path = input("where save file?: ")
with open(result_path, "w") as f:
	f.write("\n".join([f"{val[0]:.1f}" for val in data]))

