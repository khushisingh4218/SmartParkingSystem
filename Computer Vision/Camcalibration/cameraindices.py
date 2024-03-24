import cv2

for i in range(10):  # Check indices from 0 to 9
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        print(f"Camera index {i} is available")
        cap.release()
    else:
        print(f"Camera index {i} is not available")
