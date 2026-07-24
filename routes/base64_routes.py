"""Base64 tool routes."""
from __future__ import annotations

import base64

from flask import Blueprint, jsonify, render_template, request

base64_bp = Blueprint("base64", __name__)


@base64_bp.route("/", methods=["GET"])
def page():
    return render_template("base64.html")


@base64_bp.route("/api", methods=["POST"])
def api():
    payload = request.get_json(silent=True) or {}
    mode = payload.get("mode", "encode")
    text = payload.get("text", "")
    if len(text) > 500_000:
        return jsonify({"ok": False, "error": "Input too large"}), 400
    try:
        if mode == "encode":
            out = base64.b64encode(text.encode("utf-8")).decode("ascii")
        elif mode == "decode":
            out = base64.b64decode(text.encode("ascii"), validate=True).decode(
                "utf-8", errors="replace"
            )
        else:
            return jsonify({"ok": False, "error": "Invalid mode"}), 400
        return jsonify({"ok": True, "result": out})
    except Exception as e:  # noqa: BLE001
        return jsonify({"ok": False, "error": f"Invalid input: {e}"}), 400
