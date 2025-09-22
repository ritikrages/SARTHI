from flask import Blueprint, request, jsonify
from ..db import get_db

bp = Blueprint("alerts", __name__)


@bp.get("")
def list_alerts():
    db = get_db()
    rows = db.execute(
        "SELECT id, type, message, severity, resolved, created_at FROM alerts ORDER BY id DESC"
    ).fetchall()
    return jsonify([dict(r) for r in rows])


@bp.post("")
def create_alert():
    data = request.get_json(force=True) or {}
    alert_type = (data.get("type") or "generic").strip()
    message = (data.get("message") or "").strip()
    severity = (data.get("severity") or "info").strip()
    db = get_db()
    cur = db.execute(
        "INSERT INTO alerts(type, message, severity) VALUES(?,?,?)",
        (alert_type, message, severity),
    )
    db.commit()
    return jsonify({
        "id": cur.lastrowid,
        "type": alert_type,
        "message": message,
        "severity": severity,
        "resolved": 0,
    }), 201


@bp.post("/<int:alert_id>/resolve")
def resolve_alert(alert_id: int):
    db = get_db()
    db.execute("UPDATE alerts SET resolved=1 WHERE id=?", (alert_id,))
    db.commit()
    return jsonify({"id": alert_id, "resolved": True})


