"""Threaded TCP port scanner."""
from __future__ import annotations

import socket
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, asdict
from typing import List, Tuple

COMMON_SERVICES = {
    21: "ftp", 22: "ssh", 23: "telnet", 25: "smtp", 53: "dns",
    80: "http", 110: "pop3", 143: "imap", 443: "https", 445: "smb",
    465: "smtps", 587: "smtp-tls", 993: "imaps", 995: "pop3s",
    3306: "mysql", 3389: "rdp", 5432: "postgres", 5900: "vnc",
    6379: "redis", 8080: "http-proxy", 8443: "https-alt", 27017: "mongodb",
}


@dataclass
class PortResult:
    port: int
    status: str  # "open" | "closed"
    service: str


@dataclass
class ScanReport:
    target: str
    ip: str
    started_at: float
    duration: float
    total: int
    open_count: int
    results: List[dict]


def _service_for(port: int) -> str:
    return COMMON_SERVICES.get(port, "unknown")


def _resolve(target: str) -> str:
    return socket.gethostbyname(target)


def _check_port(ip: str, port: int, timeout: float) -> PortResult:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((ip, port))
            status = "open" if result == 0 else "closed"
            return PortResult(port=port, status=status, service=_service_for(port))
    except OSError:
        return PortResult(port=port, status="closed", service=_service_for(port))


def scan_ports(
    target: str,
    start_port: int,
    end_port: int,
    timeout: float = 0.5,
    threads: int = 100,
    max_ports: int = 1024,
) -> ScanReport:
    """Scan a range of TCP ports on the target host."""
    if not target or len(target) > 253:
        raise ValueError("Invalid target")
    if not (1 <= start_port <= 65535 and 1 <= end_port <= 65535):
        raise ValueError("Ports must be between 1 and 65535")
    if start_port > end_port:
        raise ValueError("start_port must be <= end_port")
    if (end_port - start_port + 1) > max_ports:
        raise ValueError(f"Port range exceeds maximum of {max_ports}")
    timeout = max(0.1, min(float(timeout), 3.0))
    threads = max(1, min(int(threads), 200))

    ip = _resolve(target)
    started = time.time()
    results: List[PortResult] = []

    with ThreadPoolExecutor(max_workers=threads) as pool:
        futures = [
            pool.submit(_check_port, ip, p, timeout)
            for p in range(start_port, end_port + 1)
        ]
        for fut in as_completed(futures):
            results.append(fut.result())

    results.sort(key=lambda r: r.port)
    duration = round(time.time() - started, 3)
    open_count = sum(1 for r in results if r.status == "open")

    return ScanReport(
        target=target,
        ip=ip,
        started_at=started,
        duration=duration,
        total=len(results),
        open_count=open_count,
        results=[asdict(r) for r in results],
    )
