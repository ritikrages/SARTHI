from flask import Blueprint, request, jsonify
from ..db import get_db

bp = Blueprint("sensors", __name__)


@bp.post("/log")
def log_sensor():
    data = request.get_json(force=True) or {}
    kind = (data.get("kind") or "").strip()
    value = data.get("value")
    if not kind:
        return jsonify({"error": "kind is required"}), 400
    db = get_db()
    db.execute("INSERT INTO sensor_logs(kind, value) VALUES(?,?)", (kind, str(value)))
    db.commit()
    return ("", 204)


@bp.get("/logs")
def list_logs():
    db = get_db()
    rows = db.execute(
        "SELECT id, kind, value, created_at FROM sensor_logs ORDER BY id DESC LIMIT 200"
    ).fetchall()
    return jsonify([dict(r) for r in rows])


