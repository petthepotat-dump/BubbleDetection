import cv2


def get_first_video_frame(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cv2.isOpened():
        print('Error opening video stream or file')
        return None
    ret, frame = cap.read()
    cap.release()
    return frame


# get first frame and save
cv2.imwrite('assets/first.png', get_first_video_frame('assets/sample.mov'))
