"""Port detection and management utilities for development tools."""

import re
import socket
from pathlib import Path


def detect_app_port(app_file: Path) -> int | None:
    """Detect port from common patterns in Python files."""
    try:
        content = app_file.read_text(encoding="utf-8")

        patterns = [
            r"WebApp\s*\(\s*.*?port\s*=\s*(\d+)",  # WebApp(port=8765)
            r"serve\s*\(\s*.*?port\s*=\s*(\d+)",  # serve(port=5000)
            r"uvicorn\.run\s*\(\s*.*?port\s*=\s*(\d+)",  # uvicorn.run(port=8000)
            r"app\.run\s*\(\s*.*?port\s*=\s*(\d+)",  # app.run(port=8000)
            r"\.run\s*\(\s*.*?port\s*=\s*(\d+)",  # *.run(port=8000)
        ]

        for pattern in patterns:
            if matches := re.findall(pattern, content, re.IGNORECASE | re.DOTALL):
                port = int(matches[-1])  # Last match likely in __main__
                if 1024 <= port <= 65535:
                    return port

        return None
    except (OSError, ValueError, re.error):
        return None


def port_available(port: int) -> bool:
    """Check if a port is available for binding."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("localhost", port))
            return True
    except OSError:
        return False


def find_port(start: int = 5000, max_tries: int = 100) -> int:
    """Find the next available port starting from a given port."""
    for port in range(start, start + max_tries):
        if port_available(port):
            return port
    raise RuntimeError(f"No ports available in {start}-{start + max_tries}")


def resolve_port(requested: int, strict: bool, app_file: Path | None = None) -> tuple[int, str | None]:
    """Resolve port: try detected → requested → auto-find.

    Returns (port, message) where message explains the choice if non-default.
    """
    # Try detected port from app file first
    if app_file and (detected := detect_app_port(app_file)):
        if port_available(detected):
            return detected, f"Using port {detected} from {app_file.name}"
        elif strict:
            raise RuntimeError(f"Port {detected} from {app_file.name} is already in use")

    # Try requested port
    if port_available(requested):
        return requested, None

    if strict:
        raise RuntimeError(f"Port {requested} is already in use")

    # Auto-find available port
    available = find_port(requested + 1)
    return available, f"Port {requested} in use, using {available}"
