import contextlib
import json
import os
import tempfile
from pathlib import Path
from typing import Any, Literal

from .checksum import compute_checksum

ItemKind = Literal["component", "block"]


SECTIONS: dict[ItemKind, str] = {"component": "components", "block": "blocks"}


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

    def record_install(
        self, name: str, version: str, checksum: str, file_path: str, kind: ItemKind = "component"
    ) -> None:
        """In-memory only — call save() to persist."""
        self._load()[SECTIONS[kind]][name] = {
            "version": version,
            "checksum": checksum,
            "file": file_path,
        }

    def get_installed(self, kind: ItemKind = "component") -> dict[str, dict[str, str]]:
        return self._load()[SECTIONS[kind]]

    def _is_modified(self, record: dict[str, str] | None, name: str, component_dir: Path) -> bool:
        if not record:
            return False
        recorded = record.get("file")
        local_file = self.project_root / recorded if recorded else component_dir / f"{name}.py"
        return not local_file.exists() or compute_checksum(local_file) != record.get("checksum", "")

    def is_modified(self, name: str, component_dir: Path, kind: ItemKind = "component") -> bool:
        return self._is_modified(self.get_installed(kind).get(name), name, component_dir)

    def exists(self) -> bool:
        return self.path.exists()
