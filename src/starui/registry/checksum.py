import hashlib
from pathlib import Path


def compute_checksum(source: str | bytes | Path) -> str:
    if isinstance(source, Path):
        data = source.read_bytes()
    elif isinstance(source, str):
        data = source.encode("utf-8")
    else:
        data = source
    return f"sha256:{hashlib.sha256(data).hexdigest()}"
