import cv2
import imutils
import json
from scripts import recognize
from scripts import config

# ------------------ constants ------------------ #
GREEN1 = (65, 150, 100)
GREEN2 = (80, 255, 255)

# ------------------ functions ------------------ #

def get_first_video_frame(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error opening video stream or file")
        return None
    ret, frame = cap.read()
    cap.release()
    return frame

# load video
video_path = input("video path: ")
OUTPUT = "results/" + input("project name? (no extensions please): ")

# ------------------ configuration ------------------ #
# get first frame + setup config

_first = get_first_video_frame(video_path)
if not config.configuration_handler(_first):
    exit()

# ------------------ setup ------------------ #

cap = cv2.VideoCapture(video_path)

# load data
data = json.load(open("config.json", "r"))
POINTS = data["points"]
DIA_TO_PIX = data["diameter"]
REAL = data["real"]

recognize.init(POINTS)

# ------------------ find bubble ------------------ #
ret, frame = cap.read()
locations = recognize.get_abs_screen_coords(frame.shape, POINTS).reshape((4, 2))


def preprocess(fullframe) -> "image":
    image = recognize.four_point_transform(fullframe, locations)
    # hsv image
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # blur hsv
    hsv = cv2.blur(hsv, (10, 10))
    # filter out green
    mask = cv2.inRange(hsv, GREEN1, GREEN2)
    return mask


def find_area(mask) -> "area":
    # find area of white
    return cv2.countNonZero(mask)


# initial white area - in frame
masked = preprocess(frame)
# find initial white area in mask
initial_white_area = find_area(masked)
# print(initial_white_area, initial_white_area / (DIA_TO_PIX**2) * REAL, "mm^2")

# recognize.display(masked)
# exit()

# ------------------ file io ------------------ #

# open file
TFILEOUTPUT = open(f"{OUTPUT}-time", "w")
AFILEOUTPUT = open(f"{OUTPUT}-area", "w")
LFILEOUTPUT = open(f"{OUTPUT}-length", "w")
VFILEOUTPUT = open(f"{OUTPUT}-volume", "w")
# data output type

# ------------------ watch video + bubbles please  ------------------ #

while True:
    ret, frame = cap.read()
    if not ret:
        break

    mask = preprocess(frame)
    area = find_area(mask)
    # find difference from initial
    dif = initial_white_area - area if initial_white_area - area > 0 else 0
    area = dif / (DIA_TO_PIX**2) * REAL
    length = area / REAL
    volume = length*(REAL/2)*3.14
    # file output
    TFILEOUTPUT.write(f"{cap.get(cv2.CAP_PROP_POS_MSEC)}\n")
    AFILEOUTPUT.write(f"{area}\n")
    LFILEOUTPUT.write(f"{length}\n")
    VFILEOUTPUT.write(f"{volume}\n")
    print(dif, f"{area:4f}mm^2", f"{length:4f}mm", f"{volume:4f}mm^3", sep="\t")

    output = mask
    # scale output up
    output = imutils.resize(output, height=800)
    # show oroginal as well
    cv2.imshow("video", output)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# close files
TFILEOUTPUT.close()
AFILEOUTPUT.close()
LFILEOUTPUT.close()
VFILEOUTPUT.close()
