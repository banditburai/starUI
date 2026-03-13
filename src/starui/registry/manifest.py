import contextlib
import json
import os
import tempfile
from pathlib import Path
from typing import Any

from .checksum import compute_checksum

MANIFEST_FILE = ".starui/manifest.json"


class Manifest:
    def __init__(self, project_root: Path | None = None) -> None:
        self.project_root = project_root or Path.cwd()
        self.path = self.project_root / MANIFEST_FILE
        self._data: dict[str, Any] | None = None

    def _load(self) -> dict[str, Any]:
        if self._data is not None:
            return self._data
        self._data = {"registry_version": "main", "components": {}, "blocks": {}}
        if self.path.exists():
            try:
                self._data = json.loads(self.path.read_text())
            except (json.JSONDecodeError, OSError):
                pass
        # Normalize: ensure required keys exist after loading from disk
        for key in ("components", "blocks"):
            self._data.setdefault(key, {})
        return self._data

    def save(self) -> None:
        data = self._load()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        # Atomic write to avoid partial writes on crash
        fd, tmp = tempfile.mkstemp(dir=self.path.parent, suffix=".tmp")
        try:
            with os.fdopen(fd, "w") as f:
                json.dump(data, f, indent=2)
                f.write("\n")
            os.replace(tmp, self.path)
        except BaseException:
            with contextlib.suppress(OSError):
                os.unlink(tmp)
            raise

    @property
    def registry_version(self) -> str:
        return self._load().get("registry_version", "main")

    def record_install(self, name: str, version: str, checksum: str, file_path: str) -> None:
        """Record a component installation in memory. Call save() to persist."""
        self._load()["components"][name] = {
            "version": version,
            "checksum": checksum,
            "file": file_path,
        }

    def get_installed(self) -> dict[str, dict[str, str]]:
        return self._load()["components"]

    def _is_modified(self, record: dict[str, str] | None, name: str, component_dir: Path) -> bool:
        if not record:
            return False
        recorded_file = record.get("file")
        local_file = self.project_root / recorded_file if recorded_file else component_dir / f"{name}.py"
        if not local_file.exists():
            return True
        return compute_checksum(local_file) != record.get("checksum", "")

    def is_modified(self, name: str, component_dir: Path) -> bool:
        return self._is_modified(self.get_installed().get(name), name, component_dir)

    # ── Blocks ──────────────────────────────────────────────────────────

    def record_block_install(self, name: str, version: str, checksum: str, file_path: str) -> None:
        """Record a block installation in memory. Call save() to persist."""
        self._load()["blocks"][name] = {
            "version": version,
            "checksum": checksum,
            "file": file_path,
        }

    def get_installed_blocks(self) -> dict[str, dict[str, str]]:
        return self._load()["blocks"]

    def is_block_modified(self, name: str, component_dir: Path) -> bool:
        return self._is_modified(self.get_installed_blocks().get(name), name, component_dir)

    def exists(self) -> bool:
        return self.path.exists()
