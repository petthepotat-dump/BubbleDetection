# this file is for configuring the points of the selected image
import cv2
import json
import time
import numpy as np
import imutils

# load config
data = json.load(open("config.json", "r"))

POINTS = data["points"]
DIAMETER = data["diameter"]
DPOINTS = data["dpts"]

# now to take in sample image
# and select the points
path = "assets/clip2.jpg"
# imput_image = input("Enter the path to the image: ")
imput_image = path
buf = cv2.imread(imput_image)
height = 720
image = imutils.resize(buf, height=height)
# create empty cv2 mask of same size as image
mask = np.zeros(image.shape, dtype=np.uint8)

pts = POINTS.copy()
change = True

# diamter stuff
d_pts = DPOINTS.copy()
dchange = True


# mouse input handler
def mouse_handler(event, x, y, flags, param):
    global change, dchange
    # if left press
    if event == cv2.EVENT_LBUTTONDOWN:
        print(len(pts), x / image.shape[1], y / image.shape[0])
        change = True
        pts.append(x / image.shape[1])
        pts.append(y / image.shape[0])
        if len(pts) > 8:
            pts.pop(0)
            pts.pop(0)
    elif event == cv2.EVENT_RBUTTONDOWN:
        dchange = True
        d_pts.append(x / image.shape[1])
        d_pts.append(y / image.shape[0])
        if len(d_pts) > 4:
            d_pts.pop(0)
            d_pts.pop(0)


# display image
cv2.imshow("image", image)
cv2.setMouseCallback("image", mouse_handler)

while True:
    if change:
        change = False
        mask = np.zeros(image.shape, dtype=np.uint8)
        # render points
        for i in range(4):
            cv2.circle(
                mask,
                (
                    int(pts[i * 2] * image.shape[1]),
                    int(pts[i * 2 + 1] * image.shape[0]),
                ),
                5,
                (0, 0, 255),
                -1,
            )
        # render diameter
        i = 0
        cv2.line(
            mask,
            (
                int(d_pts[i * 2] * image.shape[1]),
                int(d_pts[i * 2 + 1] * image.shape[0]),
            ),
            (
                int(d_pts[(i + 1) * 2] * image.shape[1]),
                int(d_pts[(i + 1) * 2 + 1] * image.shape[0]),
            ),
            (255, 0, 0),
            2,
        )

    # display image
    cv2.imshow("image", cv2.bitwise_or(image, mask))

    # check if user wants to exit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

    # zoom in on image
    if cv2.waitKey(1) & 0xFF == ord("z"):
        height += 100
        image = imutils.resize(buf, height=height)
        change = True
        print("zoom")

    # save
    if cv2.waitKey(1) & 0xFF == ord("s"):
        data["points"] = pts
        # find distance between 2 dpoints
        d = (
            np.sqrt((d_pts[0] - d_pts[2]) ** 2 + (d_pts[1] - d_pts[3]) ** 2)
            * image.shape[1]
        )
        data["diameter"] = d
        data["dpts"] = d_pts
        json.dump(data, open("config.json", "w"), indent=3)
        print("saved")
