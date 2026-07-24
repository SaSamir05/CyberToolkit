"""WHOIS lookup service."""
from __future__ import annotations

import re
import socket
from typing import Any, Dict

import whois


_DOMAIN_RE = re.compile(
    r"^(?=.{1,253}$)([a-zA-Z0-9]([-a-zA-Z0-9]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,63}$"
)


def _normalize(value: Any) -> Any:
    if isinstance(value, list):
        # De-dup while preserving order
        seen = set()
        out = []
        for v in value:
            s = str(v)
            if s not in seen:
                seen.add(s)
                out.append(s)
        return out
    if value is None:
        return None
    return str(value)


def lookup(domain: str, timeout: int = 10) -> Dict[str, Any]:
    """Perform a WHOIS lookup."""
    domain = (domain or "").strip().lower()
    if not _DOMAIN_RE.match(domain):
        raise ValueError("Invalid domain name")

    socket.setdefaulttimeout(timeout)
    data = whois.whois(domain)

    return {
        "domain": domain,
        "registrar": _normalize(data.get("registrar")),
        "creation_date": _normalize(data.get("creation_date")),
        "expiration_date": _normalize(data.get("expiration_date")),
        "updated_date": _normalize(data.get("updated_date")),
        "country": _normalize(data.get("country")),
        "org": _normalize(data.get("org") or data.get("organization")),
        "status": _normalize(data.get("status")),
        "name_servers": _normalize(data.get("name_servers")),
        "dnssec": _normalize(data.get("dnssec")),
        "emails": _normalize(data.get("emails")),
    }
