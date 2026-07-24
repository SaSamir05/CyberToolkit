"""Cybersecurity Toolkit - Flask application entry point."""
from __future__ import annotations

import logging
import os

from flask import Flask, render_template
from dotenv import load_dotenv

from config import Config
from routes.hash_routes import hash_bp
from routes.base64_routes import base64_bp
from routes.password_routes import password_bp
from routes.scanner_routes import scanner_bp
from routes.whois_routes import whois_bp


def create_app() -> Flask:
    """Application factory."""
    load_dotenv()

    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object(Config)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    # Register blueprints
    app.register_blueprint(hash_bp, url_prefix="/hash")
    app.register_blueprint(base64_bp, url_prefix="/base64")
    app.register_blueprint(password_bp, url_prefix="/password")
    app.register_blueprint(scanner_bp, url_prefix="/scanner")
    app.register_blueprint(whois_bp, url_prefix="/whois")

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/about")
    def about():
        return render_template("about.html")

    @app.errorhandler(404)
    def not_found(_e):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def server_error(_e):
        return render_template("500.html"), 500

    return app


if __name__ == "__main__":
    app = create_app()
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=os.getenv("FLASK_DEBUG", "0") == "1")
