# using cv2, write a program that takes the first frame of a video, and allows the user to use the mouse to find hsv values

# Path: imageanalysis.py

import cv2
import numpy as np
import imutils


def mouse_position(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        # get color value from gray
        color = hsv[y, x]
        # print color
        print(color)
        print(x/hsv.shape[1], y/hsv.shape[0])


def extract_first_frame(video_path):
    first = get_first_video_frame(video_path)
    cv2.imwrite('assets/first.png', first)


def get_first_video_frame(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print('Error opening video stream or file')
        return None
    ret, frame = cap.read()
    cap.release()
    return frame


frame = get_first_video_frame('assets/new.MOV')
# resize frame to width = 700
frame = imutils.resize(frame, width=1000)
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
cv2.namedWindow('frame')
cv2.setMouseCallback('frame', mouse_position)
cv2.imshow('frame', frame)
cv2.waitKey(0)
