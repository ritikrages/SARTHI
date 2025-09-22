# ai/navigation.py

from ai.voice import say

# ✅ Expanded offline navigation routes
OFFLINE_DIRECTIONS = {
    "home to school": [
        "Start from your home.",
        "Take a left onto MG Road.",
        "Continue straight for 1 kilometer.",
        "Turn right at the petrol pump.",
        "You’ll reach the school in 300 meters."
    ],
    "station to hospital": [
        "Exit the station towards west gate.",
        "Cross the signal and take a right.",
        "Follow the road for 2 kilometers.",
        "The hospital will be on your left."
    ],
    "home to market": [
        "Start from your home gate.",
        "Go straight for 500 meters.",
        "Turn left at the main road.",
        "The market will be on your right."
    ],
    "college to hostel": [
        "Exit the college gate.",
        "Walk towards the north road.",
        "Turn right after the library.",
        "The hostel is 200 meters ahead."
    ]
}

def offline_navigate(route_key):
    steps = OFFLINE_DIRECTIONS.get(route_key.lower())
    if not steps:
        say("Sorry, I don't have offline directions for that route.")
        return

    say("Starting offline navigation.")
    for step in steps:
        say(step)
