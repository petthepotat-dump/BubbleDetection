import cv2


def get_first_video_frame(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print('Error opening video stream or file')
        return None
    ret, frame = cap.read()
    cap.release()
    return frame


def extract_first_frame(video_path):
    first = get_first_video_frame(video_path)
    cv2.imwrite('assets/first.png', first)
