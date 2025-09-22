import os
import threading
from flask import Flask
from flask_cors import CORS

# Local imports
from .db import init_db


def create_app() -> Flask:
    app = Flask(__name__)

    # Basic config
    app.config["JSON_SORT_KEYS"] = False
    app.config["DATABASE_PATH"] = os.path.join(os.path.dirname(__file__), "database.sqlite")

    # CORS for local dev and future frontend
    CORS(app)

    # Initialize SQLite database and tables
    init_db(app)

    # Register blueprints
    from .routes.health import bp as health_bp
    from .routes.contacts import bp as contacts_bp
    from .routes.alerts import bp as alerts_bp
    from .routes.sensors import bp as sensors_bp
    from .routes.env import bp as env_bp
    from .routes.ai import bp as ai_bp
    from .routes.arduino import bp as arduino_bp

    app.register_blueprint(health_bp)
    app.register_blueprint(contacts_bp, url_prefix="/contacts")
    app.register_blueprint(alerts_bp, url_prefix="/alerts")
    app.register_blueprint(sensors_bp, url_prefix="/sensors")
    app.register_blueprint(env_bp, url_prefix="/env")
    app.register_blueprint(ai_bp, url_prefix="/ai")
    app.register_blueprint(arduino_bp, url_prefix="/arduino")

    return app


app = create_app()


if __name__ == "__main__":
    # Single-process dev server
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)


