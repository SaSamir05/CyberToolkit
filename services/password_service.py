"""Password generation and strength estimation."""
from __future__ import annotations

import math
import secrets
import string
from dataclasses import dataclass
from typing import List


SIMILAR = set("Il1O0o")


@dataclass
class PasswordOptions:
    length: int = 16
    uppercase: bool = True
    lowercase: bool = True
    numbers: bool = True
    symbols: bool = True
    exclude_similar: bool = False


def _alphabet(opts: PasswordOptions) -> str:
    chars = ""
    if opts.uppercase:
        chars += string.ascii_uppercase
    if opts.lowercase:
        chars += string.ascii_lowercase
    if opts.numbers:
        chars += string.digits
    if opts.symbols:
        chars += "!@#$%^&*()-_=+[]{};:,.<>/?~"
    if opts.exclude_similar:
        chars = "".join(c for c in chars if c not in SIMILAR)
    return chars


def generate_password(opts: PasswordOptions) -> str:
    if opts.length < 4 or opts.length > 128:
        raise ValueError("Length must be between 4 and 128")
    alphabet = _alphabet(opts)
    if not alphabet:
        raise ValueError("Select at least one character set")
    return "".join(secrets.choice(alphabet) for _ in range(opts.length))


def generate_multiple(opts: PasswordOptions, count: int = 5) -> List[str]:
    count = max(1, min(count, 25))
    return [generate_password(opts) for _ in range(count)]


def entropy_bits(password: str) -> float:
    pool = 0
    if any(c.islower() for c in password):
        pool += 26
    if any(c.isupper() for c in password):
        pool += 26
    if any(c.isdigit() for c in password):
        pool += 10
    if any(not c.isalnum() for c in password):
        pool += 30
    if pool == 0:
        return 0.0
    return round(len(password) * math.log2(pool), 2)


def strength_label(bits: float) -> str:
    if bits < 40:
        return "Weak"
    if bits < 60:
        return "Fair"
    if bits < 90:
        return "Strong"
    return "Excellent"
