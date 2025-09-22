# vision_runner.py
# Main vision orchestrator
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from ai.vision.detection import detect_faces_and_eyes
from ai.vision.emotion import analyze_emotion
from ai.vision.greeting import check_and_greet
from ai.vision.passenger_count import count_passengers
from ai.vision.finger_count import count_fingers
from ai.voice import say
import cv2
import threading


def vision_main():
    say("Initializing SARTHI Vision AI module.")
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        faces = detect_faces_and_eyes(frame)
        count_passengers(frame, faces)
        count_fingers(frame)
        check_and_greet(frame, faces)
        analyze_emotion(frame, faces)

        cv2.imshow("SARTHI Vision", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    vision_main()
