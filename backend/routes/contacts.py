from flask import Blueprint, request, jsonify
from ..db import get_db

bp = Blueprint("contacts", __name__)


@bp.get("")
def list_contacts():
    db = get_db()
    rows = db.execute("SELECT id, name, phone, email FROM contacts ORDER BY id DESC").fetchall()
    return jsonify([dict(r) for r in rows])


@bp.post("")
def add_contact():
    data = request.get_json(force=True) or {}
    name = (data.get("name") or "").strip()
    phone = (data.get("phone") or "").strip()
    email = (data.get("email") or "").strip()
    if not name:
        return jsonify({"error": "name is required"}), 400
    db = get_db()
    cur = db.execute("INSERT INTO contacts(name, phone, email) VALUES(?,?,?)", (name, phone, email))
    db.commit()
    return jsonify({"id": cur.lastrowid, "name": name, "phone": phone, "email": email}), 201


@bp.delete("/<int:contact_id>")
def delete_contact(contact_id: int):
    db = get_db()
    db.execute("DELETE FROM contacts WHERE id=?", (contact_id,))
    db.commit()
    return ("", 204)


