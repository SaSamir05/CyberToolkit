"""Hash generation service."""
from __future__ import annotations

import hashlib
from typing import Dict, List

SUPPORTED_ALGORITHMS: List[str] = [
    "md5", "sha1", "sha224", "sha256", "sha384", "sha512",
]


def generate_hash(text: str, algorithm: str) -> str:
    """Generate a hex digest for the given text using the chosen algorithm."""
    algorithm = algorithm.lower().strip()
    if algorithm not in SUPPORTED_ALGORITHMS:
        raise ValueError(f"Unsupported algorithm: {algorithm}")
    if not isinstance(text, str):
        raise ValueError("Input must be a string")
    hasher = hashlib.new(algorithm)
    hasher.update(text.encode("utf-8"))
    return hasher.hexdigest()


def generate_all(text: str) -> Dict[str, str]:
    """Return hashes for all supported algorithms."""
    return {alg: generate_hash(text, alg) for alg in SUPPORTED_ALGORITHMS}
