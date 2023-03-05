
import cv2
import imutils

GREEN1 = (55, 100, 60)
GREEN2 = (75, 255, 255)

"""
Steps:
1. load video
2. analyze frame -- select section (of the tube (green liquid)) || you can train network to recognize
    a. since this is specific use case as well
3. find the separated sections of the green
    a. but gotta move the stupid clamp somewhere else (higher or lower) -- except hte heated liquid so im not too sure
4. find min + max height of greens
5. scale images by using scaleing method lmao
    a. get a ruler or smth and stick into frame :D
6. ez??
7. can find height -- volume calculations are just approx so
    a. either go with vol of cylinder
    b. OR go with volume of ellipsoid
8. volume calculated per frame --> data sent to file?? 
    a. or just print to console
    b. OR only pick up max volume for each (BUBBLING sequence)
"""

# # loop through all frames in assets/sample.mov, mask out green color and display it
# cap = cv2.VideoCapture('assets/sample.mov')

# while cap.isOpened():
#     ret, frame = cap.read()
#     if not ret:
#         break
#     # lower frame size
#     frame = imutils.resize(frame, height=800)
#     # gaussian blur frame
#     frame = cv2.blur(frame, (10, 10))
#     hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
#     mask = cv2.inRange(hsv, GREEN1, GREEN2)
#     # show oroginal as well
#     cv2.imshow('frame1', frame)
#     cv2.imshow('frame2', mask)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()

# exit()


# load assets/test.jpg
img = cv2.imread('assets/clip1.jpg')

img = imutils.resize(img, height=800)
# blur frame
img = cv2.blur(img, (10, 10))

# convert to hsv and mask only green
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, GREEN1, GREEN2)

# mouse positino func


def mouse_position(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        # get color value from gray
        color = hsv[y, x]
        # print color
        print(color)


# show image
cv2.imshow('image', hsv)
cv2.setMouseCallback('image', mouse_position)
cv2.imshow('edges', mask)
# show hsv gray
# cv2.imshow('hsv gray', hsv_gray)
cv2.waitKey(0)
