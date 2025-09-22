# ai/vision/finger_count.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import cv2
import numpy as np
from ai.voice import say

def count_fingers():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        say("Camera not accessible.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        roi = frame[100:400, 100:400]  # Define region of interest
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        lower_skin = np.array([0, 20, 70], dtype=np.uint8)
        upper_skin = np.array([20, 255, 255], dtype=np.uint8)
        mask = cv2.inRange(hsv, lower_skin, upper_skin)

        kernel = np.ones((3,3), np.uint8)
        mask = cv2.dilate(mask, kernel, iterations=4)
        mask = cv2.GaussianBlur(mask, (5,5), 100)

        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            cnt = max(contours, key=lambda x: cv2.contourArea(x))
            hull = cv2.convexHull(cnt, returnPoints=False)

            if hull is not None and len(hull) > 3:
                defects = cv2.convexityDefects(cnt, hull)
                if defects is not None:
                    finger_count = 0
                    for i in range(defects.shape[0]):
                        s, e, f, d = defects[i, 0]
                        start = tuple(cnt[s][0])
                        end = tuple(cnt[e][0])
                        far = tuple(cnt[f][0])

                        a = np.linalg.norm(np.array(end) - np.array(start))
                        b = np.linalg.norm(np.array(far) - np.array(start))
                        c = np.linalg.norm(np.array(end) - np.array(far))

                        angle = np.arccos((b**2 + c**2 - a**2)/(2*b*c))

                        if angle <= np.pi / 2:
                            finger_count += 1
                    say(f"You are showing {finger_count + 1} fingers.")

        key = cv2.waitKey(3000)
        if key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    count_fingers()
