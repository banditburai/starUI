import json
import logging
import time
from pathlib import Path
from typing import Any

import requests

from .checksum import compute_checksum
from .manifest import SECTIONS, ItemKind

logger = logging.getLogger(__name__)

GITHUB_RAW_BASE = "https://raw.githubusercontent.com/banditburai/starUI"
INDEX_TTL_SECONDS = 3600


class RegistryClient:
    def __init__(self, version: str = "main") -> None:
        self.version = version
        self.cache_dir = Path.home() / ".starui" / "cache" / "registry" / version
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._index: dict[str, Any] | None = None

    @property
    def _is_immutable(self) -> bool:
        return self.version.startswith("v") and self.version[1:2].isdigit()

    @property
    def _base_url(self) -> str:
        return f"{GITHUB_RAW_BASE}/{self.version}/registry"

    def _fetch_url(self, url: str) -> str:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        return resp.text

    def _set_index(self, data: dict[str, Any]) -> dict[str, Any]:
        for key in ("components", "blocks"):
            data.setdefault(key, {})
        self._index = data
        return data

    def _get_index(self) -> dict[str, Any]:
        if self._index is not None:
            return self._index

        cached = self.cache_dir / "index.json"
        meta = self.cache_dir / "index.meta.json"

        if cached.exists():
            cache_valid = self._is_immutable
            if not cache_valid and meta.exists():
                try:
                    fetched_at = json.loads(meta.read_text()).get("fetched_at", 0)
                    cache_valid = (time.time() - fetched_at) < INDEX_TTL_SECONDS
                except (json.JSONDecodeError, KeyError):
                    pass

            if cache_valid:
                try:
                    return self._set_index(json.loads(cached.read_text()))
                except (json.JSONDecodeError, OSError):
                    pass

        url = f"{self._base_url}/index.json"
        try:
            text = self._fetch_url(url)
            cached.write_text(text)
            meta.write_text(json.dumps({"fetched_at": time.time()}))
            return self._set_index(json.loads(text))
        except requests.RequestException as e:
            if cached.exists():
                try:
                    logger.warning("Network error fetching index, using cached version: %s", e)
                    return self._set_index(json.loads(cached.read_text()))
                except (json.JSONDecodeError, OSError):
                    pass
            raise ConnectionError(
                f"Cannot fetch registry index from {url}. Check your network connection or try again later."
            ) from e

    def _fetch_source(self, entry: dict[str, Any], cache_subdir: str, cache_name: str, label: str) -> str:
        cached_file = self.cache_dir / cache_subdir / f"{cache_name}.py"

        if cached_file.exists():
            data = cached_file.read_bytes()
            if compute_checksum(data) == entry.get("checksum"):
                return data.decode("utf-8")

        url = f"{self._base_url}/{entry['file']}"
        try:
            source = self._fetch_url(url)
            cached_file.parent.mkdir(parents=True, exist_ok=True)
            cached_file.write_bytes(source.encode("utf-8"))
            return source
        except requests.RequestException as e:
            if cached_file.exists():
                logger.warning("Network error fetching %s, using cached version: %s", label, e)
                return cached_file.read_bytes().decode("utf-8")
            raise ConnectionError(
                f"Cannot fetch {label} from {url}. Check your network connection or try again later."
            ) from e

    def _get_entry(self, name: str, kind: ItemKind) -> dict[str, Any]:
        entry = self._get_index()[SECTIONS[kind]].get(name)
        if not entry:
            raise FileNotFoundError(f"{kind.title()} '{name}' not found in registry")
        return entry

    def list_items(self, kind: ItemKind) -> list[str]:
        names = self._get_index()[SECTIONS[kind]]
        return sorted(n for n in names if n != "utils") if kind == "component" else sorted(names)

    def get_source(self, name: str, kind: ItemKind = "component") -> str:
        entry = self._get_entry(name, kind)
        cache_name = entry.get("install_name", name) if kind == "block" else name
        return self._fetch_source(entry, SECTIONS[kind], cache_name, f"{kind} '{name}'")

    def get_metadata(self, name: str, kind: ItemKind = "component") -> dict[str, Any]:
        return self._get_entry(name, kind)

    def _visit_dep(self, name: str, resolved: list[str], visiting: set[str], visited: set[str]) -> None:
        if name in visiting:
            raise ValueError(f"Circular dependency: {name}")
        if name in visited:
            return
        visiting.add(name)
        for dep in self.get_metadata(name).get("dependencies", []):
            self._visit_dep(dep, resolved, visiting, visited)
        visiting.remove(name)
        visited.add(name)
        resolved.append(name)

    def resolve_dependencies(self, name: str, kind: ItemKind = "component") -> list[str]:
        resolved: list[str] = []
        visiting: set[str] = set()
        visited: set[str] = set()
        roots = self._get_entry(name, kind).get("dependencies", []) if kind == "block" else [name]
        for dep in roots:
            self._visit_dep(dep, resolved, visiting, visited)
        return resolved

    def get_with_dependencies(self, name: str, kind: ItemKind = "component") -> tuple[dict[str, str], str]:
        """For components, deps excludes self. For blocks, deps are component dependencies."""
        deps = {n: self.get_source(n) for n in self.resolve_dependencies(name, kind) if n != name}
        return deps, self.get_source(name, kind)

    def lookup(self, name: str) -> tuple[ItemKind, dict[str, Any]]:
        index = self._get_index()
        for kind, section in SECTIONS.items():
            if name in index[section]:
                return kind, index[section][name]
        # Fallback: match by install_name so `star add user-button` resolves
        for entry in index[SECTIONS["block"]].values():
            if entry.get("install_name") == name:
                return "block", entry
        raise FileNotFoundError(f"'{name}' not found in registry (checked components and blocks)")
