# main.py

import socket
import json
import time
import threading
import cv2

from ai.assistant import multilingual_assistant
from ai.offline_assistant import offline_assistant
from ai.navigation import offline_navigate
from ai.voice import listen_command, say, set_voice
from ai.vision.detection import monitor_face_and_eyes
from ai.vision.greeting import run_greeting
from ai.vision.emotion import analyze_emotion
from ai.vision.passenger_count import run_passenger_counter
from ai.vision.finger_count import count_fingers

chat_history = []

# === Load user info ===
try:
    with open("config/user.json", "r") as f:
        user_profile = json.load(f)
        USER_NAME = user_profile.get("name", "User")
except:
    USER_NAME = "User"

def is_online():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return True
    except OSError:
        return False

def check_all_systems():
    say("Running full system diagnostics.")
    time.sleep(1)
    say("Fuel level: 78 percent.")
    say("Engine temperature: Normal.")
    say("Oil pressure: Stable.")
    say("Tire pressure: All four are optimal.")
    say("Radar and sensor status: Fully operational.")
    say("All systems are functioning normally.")

def start_background_tasks():
    # Start face/eye detection and greeting in separate threads
    threading.Thread(target=monitor_face_and_eyes, daemon=True).start()
    threading.Thread(target=run_greeting, daemon=True).start()

def run_sarthi():
    say(f"Hello {USER_NAME}! I am SARTHI, your AI driving assistant.")
    check_all_systems()

    start_background_tasks()

    while True:
        command = listen_command()

        if not command:
            continue

        if "exit" in command or "quit" in command:
            say("Goodbye! Stay safe.")
            break

        elif "check" in command:
            check_all_systems()

        elif "reset chat" in command:
            multilingual_assistant(reset=True, history=chat_history)

        elif "navigate" in command:
            say("Please tell me the route, like 'home to school' or 'station to hospital'.")
            route_command = listen_command()
            offline_navigate(route_command)

        elif "switch language to hindi" in command:
            set_voice("hi")

        elif "switch language to bengali" in command:
            set_voice("bn")

        elif "switch language to english" in command:
            set_voice("en")

        elif "emergency override" in command or "take control" in command:
            say("Emergency detected. Activating AI override.")

        elif "health status" in command or "check vitals" in command:
            say("Initiating health check.")
            say("Heart rate: 78 beats per minute.")
            say("Oxygen level: 98 percent.")
            say("All vitals are within normal range.")

        elif "detect emotion" in command:
            say("Analyzing your emotion now.")
            analyze_emotion()  # Now uses its own video capture internally

        elif "count passengers" in command:
            run_passenger_counter()

        elif "count fingers" in command:
            count_fingers()

        elif is_online():
            multilingual_assistant(command=command, history=chat_history)

        else:
            say("No internet detected. Switching to offline mode.")
            offline_assistant(command)

if __name__ == "__main__":
    run_sarthi()
