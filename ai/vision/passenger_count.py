# ai/vision/passenger_count.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import cv2
from threading import Thread
from ai.voice import say

class PassengerCounter:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.running = True

    def count_faces(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            say("Camera not accessible.")
            return

        try:
            while self.running:
                ret, frame = cap.read()
                if not ret:
                    continue
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
                passenger_count = len(faces)
                say(f"Detected {passenger_count} passengers.")
                cv2.waitKey(3000)  # Wait 3 seconds before next check
        finally:
            cap.release()
            cv2.destroyAllWindows()

    def stop(self):
        self.running = False


def run_passenger_counter():
    counter = PassengerCounter()
    Thread(target=counter.count_faces).start()
    return counter

