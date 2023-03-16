import cv2
import imutils

from scripts import utils

# ----------------------------
# getting first frame

# first = utils.get_first_video_frame('assets/new.MOV')
# cv2.imwrite('assets/first.png', first)


# ----------------------------
# examining first frame

GREEN1 = (55, 100, 60)
GREEN2 = (75, 255, 255)

RANGES = [
    [(40, 50, 10), (74, 180, 180)],
    [(15, 50, 10), (30, 180, 180)]

]

WHITE = (255, 255, 255)

# load video
cap = cv2.VideoCapture('assets/new.MOV')
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask1 = cv2.inRange(hsv, GREEN1, GREEN2)
    mask2 = cv2.inRange(hsv, RANGES[0][0], RANGES[0][1])
    mask3 = cv2.inRange(hsv, RANGES[1][0], RANGES[1][1])
    res1 = cv2.bitwise_and(frame, frame, mask=mask1)
    res2 = cv2.bitwise_and(frame, frame, mask=mask2)
    res3 = cv2.bitwise_and(frame, frame, mask=mask3)
    res = cv2.bitwise_or(res1, res2)
    res = cv2.bitwise_or(res, res3)
    # blur res
    res = cv2.GaussianBlur(res, (11, 11), 0)

    # # gray scale
    # gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    # # blur
    # blurred = cv2.GaussianBlur(gray, (11, 11), 0)
    # # threshold
    # thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
    # # dilate
    # dilated = cv2.dilate(thresh, None, iterations=2)
    # # erode
    # eroded = cv2.erode(dilated, None, iterations=2)

    res = res

    """
    TODO:
    - tryna filter out repeated rectangles from information lmao
    - find if min/max in range of 
    MIN = 0.73
    MAX = 0.39
    """

    # find contours
    cnts = cv2.findContours(
        mask2.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    # filter out countours if they are below 100px in size
    cnts = [c for c in cnts if cv2.contourArea(c) > 500]
    # filter out countours if they overlap
    r = []
    # low, high
    bounds = [-100, 1e9]
    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        bot = (y + h) / res.shape[0]
        top = y / res.shape[0]
        # find if within min/max range
        if bot > 0.39:
            bounds[0] = max(bounds[0], bot)
        if top < 0.73:
            bounds[1] = min(bounds[1], top)

    # draw some lines
    y1 = int(bounds[0]*res.shape[0])
    y2 = int(bounds[1]*res.shape[0])
    cv2.line(res, (0, y1), (800, y1), WHITE, 2)
    cv2.line(res, (0, y2), (800, y2), WHITE, 2)

    # for each contour, find min + max height and draw a line on screen
    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(res, (x, y), (x + w, y + h), WHITE, 2)
        cv2.line(res, (0, y), (800, y), WHITE, 2)
        cv2.line(res, (0, y + h), (800, y + h), WHITE, 2)

    # show at h alf reoslution
    cv2.imshow('frame', imutils.resize(res, width=800))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
