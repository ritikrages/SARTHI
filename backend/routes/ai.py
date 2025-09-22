from flask import Blueprint, request, jsonify
from ...ai.voice import say
from ...ai.assistant import multilingual_assistant
from ...ai.offline_assistant import offline_assistant
from ...ai.navigation import offline_navigate
from ...ai.vision.emotion import analyze_emotion
from ...ai.vision.passenger_count import run_passenger_counter
from ...ai.vision.finger_count import count_fingers
from ...ai.vision.detection import monitor_face_and_eyes

bp = Blueprint("ai", __name__)


@bp.post("/speak")
def tts():
    data = request.get_json(force=True) or {}
    text = (data.get("text") or "").strip()
    if not text:
        return jsonify({"error": "text is required"}), 400
    say(text)
    return ("", 204)


@bp.post("/chat")
def chat():
    data = request.get_json(force=True) or {}
    command = (data.get("message") or "").strip()
    mode = (data.get("mode") or "online").strip()
    history = []
    if not command:
        return jsonify({"error": "message is required"}), 400
    if mode == "offline":
        offline_assistant(command)
        return jsonify({"mode": "offline"})
    multilingual_assistant(command=command, history=history)
    return jsonify({"mode": "online"})


@bp.post("/navigate")
def navigate():
    data = request.get_json(force=True) or {}
    route = (data.get("route") or "").strip()
    if not route:
        return jsonify({"error": "route is required"}), 400
    offline_navigate(route)
    return ("", 204)


@bp.post("/vision/drowsiness/start")
def start_drowsiness():
    monitor_face_and_eyes()
    return jsonify({"status": "started"})


@bp.post("/vision/emotion")
def vision_emotion():
    analyze_emotion()
    return ("", 204)


@bp.post("/vision/passengers")
def vision_passengers():
    run_passenger_counter()
    return ("", 204)


@bp.post("/vision/fingers")
def vision_fingers():
    count_fingers()
    return ("", 204)


