"""Password generator routes."""
from __future__ import annotations

from flask import Blueprint, jsonify, render_template, request

from services.password_service import (
    PasswordOptions,
    entropy_bits,
    generate_multiple,
    strength_label,
)

password_bp = Blueprint("password", __name__)


@password_bp.route("/", methods=["GET"])
def page():
    return render_template("password.html")


@password_bp.route("/api", methods=["POST"])
def api():
    p = request.get_json(silent=True) or {}
    try:
        opts = PasswordOptions(
            length=int(p.get("length", 16)),
            uppercase=bool(p.get("uppercase", True)),
            lowercase=bool(p.get("lowercase", True)),
            numbers=bool(p.get("numbers", True)),
            symbols=bool(p.get("symbols", True)),
            exclude_similar=bool(p.get("exclude_similar", False)),
        )
        count = int(p.get("count", 1))
        passwords = generate_multiple(opts, count)
        analyzed = [
            {
                "password": pw,
                "entropy": entropy_bits(pw),
                "strength": strength_label(entropy_bits(pw)),
            }
            for pw in passwords
        ]
        return jsonify({"ok": True, "passwords": analyzed})
    except ValueError as e:
        return jsonify({"ok": False, "error": str(e)}), 400
