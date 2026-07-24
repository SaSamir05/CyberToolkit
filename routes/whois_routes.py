"""WHOIS routes."""
from __future__ import annotations

import logging

from flask import Blueprint, current_app, jsonify, render_template, request

from services.whois_service import lookup

whois_bp = Blueprint("whois", __name__)
log = logging.getLogger(__name__)


@whois_bp.route("/", methods=["GET"])
def page():
    return render_template("whois.html")


@whois_bp.route("/api", methods=["POST"])
def api():
    p = request.get_json(silent=True) or {}
    domain = p.get("domain", "")
    try:
        result = lookup(domain, timeout=current_app.config["WHOIS_TIMEOUT"])
        return jsonify({"ok": True, "result": result})
    except ValueError as e:
        return jsonify({"ok": False, "error": str(e)}), 400
    except Exception as e:  # noqa: BLE001
        log.exception("WHOIS failed")
        return jsonify({"ok": False, "error": f"Lookup failed: {e}"}), 500
