"""Hash tool routes."""
from __future__ import annotations

from flask import Blueprint, jsonify, render_template, request

from services.hash_service import SUPPORTED_ALGORITHMS, generate_all, generate_hash

hash_bp = Blueprint("hash", __name__)


@hash_bp.route("/", methods=["GET"])
def page():
    return render_template("hash.html", algorithms=SUPPORTED_ALGORITHMS)


@hash_bp.route("/api", methods=["POST"])
def api():
    payload = request.get_json(silent=True) or {}
    text = payload.get("text", "")
    algorithm = payload.get("algorithm", "sha256")
    if len(text) > 100_000:
        return jsonify({"error": "Input too large"}), 400
    try:
        if algorithm == "all":
            digests = generate_all(text)
        else:
            digests = {algorithm: generate_hash(text, algorithm)}
        return jsonify({"ok": True, "digests": digests, "length": len(text)})
    except ValueError as e:
        return jsonify({"ok": False, "error": str(e)}), 400
