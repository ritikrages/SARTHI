import os
import requests


def get_weather(city: str):
    # TODO: Set OPENWEATHER_API_KEY in environment
    api_key = os.getenv("OPENWEATHER_API_KEY", "")
    if not api_key:
        return {"city": city, "temp_c": None, "description": None, "note": "Set OPENWEATHER_API_KEY"}
    try:
        url = (
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        )
        resp = requests.get(url, timeout=10)
        data = resp.json()
        return {
            "city": city,
            "temp_c": data.get("main", {}).get("temp"),
            "description": data.get("weather", [{}])[0].get("description"),
        }
    except Exception as exc:
        return {"city": city, "error": str(exc)}


def get_air_quality(city: str):
    # Placeholder: different providers often require lat/lon; we keep a stub
    return {"city": city, "aqi": None, "note": "Implement with preferred provider"}


def get_disaster_alerts():
    # TODO: Integrate GDACS feed; stubbed for demo
    try:
        return {"alerts": []}
    except Exception as exc:
        return {"error": str(exc), "alerts": []}


