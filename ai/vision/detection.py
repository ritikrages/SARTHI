# ai/vision/detection.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import cv2
import time
from threading import Thread
from ai.voice import say

# Load Haar cascades
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

def detect_faces_and_eyes():
    print("🟢 detect_faces_and_eyes() started")
    say("Eye monitoring activated.")
    cap = cv2.VideoCapture(0)
    eye_closed_start = None
    EYE_CLOSED_THRESHOLD = 2  # seconds

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to read frame from webcam.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        eyes_detected = False

        for (x, y, w, h) in faces:
            roi_gray = gray[y:y + h, x:x + w]
            eyes = eye_cascade.detectMultiScale(roi_gray)

            if len(eyes) >= 1:
                eyes_detected = True
                break

        if eyes_detected:
            eye_closed_start = None
        else:
            if eye_closed_start is None:
                eye_closed_start = time.time()
            elif time.time() - eye_closed_start >= EYE_CLOSED_THRESHOLD:
                say("Warning: Your eyes seem closed for too long.")
                print("⚠️ Drowsiness Detected!")
                eye_closed_start = None

        cv2.imshow("Face & Eye Monitor - Press Q to quit", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def monitor_face_and_eyes():
    print("🟢 monitor_face_and_eyes() thread launching")
    Thread(target=detect_faces_and_eyes, daemon=True).start()
