# ai/vision/emotion.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from deepface import DeepFace
import cv2
from ai.voice import say

def analyze_emotion():
    """Automatically detect emotion and age using webcam via DeepFace."""
    try:
        cap = cv2.VideoCapture(0)
        say("Analyzing your emotion now. Please look at the camera.")

        success = False
        frame_count = 0

        while frame_count < 50:
            ret, frame = cap.read()
            if not ret:
                say("Unable to access webcam.")
                break

            try:
                result = DeepFace.analyze(frame, actions=["emotion", "age"], enforce_detection=True)[0]
                emotion = result["dominant_emotion"]
                age = result["age"]

                say(f"You seem to be feeling {emotion}. Estimated age is {age} years.")
                print(f"[INFO] Emotion: {emotion} | Age: {age}")
                success = True
                break
            except:
                frame_count += 1
                continue

        cap.release()
        cv2.destroyAllWindows()

        if not success:
            say("Sorry, I couldn't detect your emotion.")

    except Exception as e:
        say("Sorry, there was an error during analysis.")
        print("DeepFace error:", e)
