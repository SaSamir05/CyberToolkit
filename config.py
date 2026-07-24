"""Application configuration."""
from __future__ import annotations

import os
import secrets


class Config:
    """Flask config."""
    SECRET_KEY: str = os.getenv("SECRET_KEY", secrets.token_hex(32))
    WTF_CSRF_ENABLED: bool = True
    MAX_CONTENT_LENGTH: int = 2 * 1024 * 1024  # 2 MB

    # Scanner limits
    SCANNER_MAX_PORTS: int = 1024
    SCANNER_DEFAULT_TIMEOUT: float = 0.5
    SCANNER_MAX_THREADS: int = 200

    # WHOIS
    WHOIS_TIMEOUT: int = 10
