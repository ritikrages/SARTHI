from flask import Blueprint, request, jsonify

# TODO: Wire to serial/Bluetooth service when hardware available

bp = Blueprint("arduino", __name__)


@bp.post("/command")
def send_command():
    data = request.get_json(force=True) or {}
    cmd = (data.get("command") or "").strip().upper()
    if cmd not in {"FLASH", "HORN", "SOS", "IMMOBILIZE"}:
        return jsonify({"error": "invalid command"}), 400
    # Placeholder: route to hardware layer
    print(f"[ARDUINO] Command requested: {cmd}")
    return jsonify({"status": "queued", "command": cmd})


