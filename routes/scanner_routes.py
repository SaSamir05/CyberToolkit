"""Port scanner routes."""
from __future__ import annotations

import csv
import io
import json
import logging
import re

from flask import Blueprint, Response, current_app, jsonify, render_template, request

from services.scanner_service import scan_ports

scanner_bp = Blueprint("scanner", __name__)
log = logging.getLogger(__name__)

_TARGET_RE = re.compile(r"^[A-Za-z0-9.\-]{1,253}$")


def _validate_target(target: str) -> str:
    target = (target or "").strip()
    if not _TARGET_RE.match(target):
        raise ValueError("Invalid target host")
    return target


@scanner_bp.route("/", methods=["GET"])
def page():
    return render_template("scanner.html")


@scanner_bp.route("/api", methods=["POST"])
def api():
    p = request.get_json(silent=True) or {}
    try:
        target = _validate_target(p.get("target", ""))
        start_port = int(p.get("start_port", 1))
        end_port = int(p.get("end_port", 1024))
        timeout = float(p.get("timeout", current_app.config["SCANNER_DEFAULT_TIMEOUT"]))
        threads = int(p.get("threads", 100))
        report = scan_ports(
            target=target,
            start_port=start_port,
            end_port=end_port,
            timeout=timeout,
            threads=threads,
            max_ports=current_app.config["SCANNER_MAX_PORTS"],
        )
        return jsonify({"ok": True, "report": report.__dict__})
    except ValueError as e:
        return jsonify({"ok": False, "error": str(e)}), 400
    except Exception as e:  # noqa: BLE001
        log.exception("Scanner failed")
        return jsonify({"ok": False, "error": f"Scan failed: {e}"}), 500


@scanner_bp.route("/export/<fmt>", methods=["POST"])
def export(fmt: str):
    data = request.get_json(silent=True) or {}
    results = data.get("results", [])
    if fmt == "json":
        return Response(
            json.dumps(data, indent=2),
            mimetype="application/json",
            headers={"Content-Disposition": "attachment; filename=scan.json"},
        )
    if fmt == "csv":
        buf = io.StringIO()
        writer = csv.DictWriter(buf, fieldnames=["port", "status", "service"])
        writer.writeheader()
        for r in results:
            writer.writerow({k: r.get(k, "") for k in ("port", "status", "service")})
        return Response(
            buf.getvalue(),
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment; filename=scan.csv"},
        )
    return jsonify({"ok": False, "error": "Unsupported format"}), 400
