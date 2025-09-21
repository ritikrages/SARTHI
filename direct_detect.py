# detect_direct.py

import cv2
import time
import pyttsx3

# TTS engine
tts = pyttsx3.init()
tts.setProperty('rate', 170)

def speak(text):
    print(f"SARTHI: {text}")
    tts.say(text)
    tts.runAndWait()

# Load Haar cascades
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

def detect_faces_and_eyes():
    print("🟢 Starting continuous drowsiness monitoring...")
    cap = cv2.VideoCapture(0)

    eye_closed_start = None
    last_alert_time = 0
    ALERT_INTERVAL = 3     # seconds between repeated alerts
    EYE_CLOSED_THRESHOLD = 2  # time to first trigger

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Camera failure.")
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
            print("👁️ Eyes detected.")
            eye_closed_start = None
            last_alert_time = 0
        else:
            if eye_closed_start is None:
                eye_closed_start = time.time()
                print("⏳ Eyes not detected. Timer started...")
            else:
                duration = time.time() - eye_closed_start
                if duration >= EYE_CLOSED_THRESHOLD:
                    if time.time() - last_alert_time >= ALERT_INTERVAL:
                        print("⚠️ Drowsiness detected. Speaking alert.")
                        speak("Warning! You appear drowsy. Please stay alert.")
                        last_alert_time = time.time()

        cv2.imshow("Face & Eye Monitor - Press Q to quit", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("🛑 Stopped by user.")
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    detect_faces_and_eyes()
