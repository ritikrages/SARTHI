from flask import Blueprint, request, jsonify
from ..services.env_services import get_weather, get_air_quality, get_disaster_alerts

bp = Blueprint("env", __name__)


@bp.get("/weather")
def weather():
    city = request.args.get("city", "Kolkata")
    data = get_weather(city)
    return jsonify(data)


@bp.get("/aqi")
def aqi():
    city = request.args.get("city", "Kolkata")
    data = get_air_quality(city)
    return jsonify(data)


@bp.get("/disasters")
def disasters():
    data = get_disaster_alerts()
    return jsonify(data)


