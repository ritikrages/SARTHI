# ai/vision/greeting.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import cv2
import time
import threading
from ai.voice import say

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
greeted = False

def detect_face_stability():
    """Monitor for face presence ≥3 seconds."""
    global greeted
    cap = cv2.VideoCapture(0)
    face_visible_start = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(faces) > 0:
            if face_visible_start is None:
                face_visible_start = time.time()
            elif time.time() - face_visible_start >= 3 and not greeted:
                say("Hello there! I'm happy to see you.")
                greeted = True
        else:
            face_visible_start = None

        # Optional: show window for testing
        cv2.imshow("Greeting Monitor", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def run_greeting():
    """Launch greeting logic in a background thread."""
    thread = threading.Thread(target=detect_face_stability, daemon=True)
    thread.start()
