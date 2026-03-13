import json
import logging
import time
from pathlib import Path
from typing import Any

import requests

from .checksum import compute_checksum

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
                    self._index = json.loads(cached.read_text())
                    return self._index
                except (json.JSONDecodeError, OSError):
                    pass

        url = f"{self._base_url}/index.json"
        try:
            text = self._fetch_url(url)
            self._index = json.loads(text)
            cached.write_text(text)
            meta.write_text(json.dumps({"fetched_at": time.time()}))
            return self._index
        except requests.RequestException as e:
            if cached.exists():
                try:
                    self._index = json.loads(cached.read_text())
                    logger.warning("Network error fetching index, using cached version: %s", e)
                    return self._index
                except (json.JSONDecodeError, OSError):
                    pass
            raise ConnectionError(
                f"Cannot fetch component registry from {url}. Check your network connection or try again later."
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

    # ── Components ──────────────────────────────────────────────────────

    def _get_component_entry(self, name: str) -> dict[str, Any]:
        comp = self._get_index()["components"].get(name)
        if not comp:
            raise FileNotFoundError(f"Component '{name}' not found in registry")
        return comp

    def list_components(self) -> list[str]:
        index = self._get_index()
        return sorted(name for name in index["components"] if name != "utils")

    def get_component_source(self, component_name: str) -> str:
        return self._fetch_source(
            self._get_component_entry(component_name),
            "components",
            component_name,
            f"component '{component_name}'",
        )

    def get_component_metadata(self, component_name: str) -> dict[str, Any]:
        return self._get_component_entry(component_name)

    def _visit_component(self, name: str, resolved: list[str], visiting: set[str], visited: set[str]) -> None:
        if name in visiting:
            raise ValueError(f"Circular dependency: {name}")
        if name in visited:
            return
        visiting.add(name)
        for dep in self.get_component_metadata(name).get("dependencies", []):
            self._visit_component(dep, resolved, visiting, visited)
        visiting.remove(name)
        visited.add(name)
        resolved.append(name)

    def resolve_dependencies(self, component_name: str) -> list[str]:
        resolved: list[str] = []
        self._visit_component(component_name, resolved, set(), set())
        return resolved

    def get_component_with_dependencies(self, component_name: str) -> dict[str, str]:
        return {n: self.get_component_source(n) for n in self.resolve_dependencies(component_name)}

    # ── Blocks ──────────────────────────────────────────────────────────

    def _get_block_entry(self, name: str) -> dict[str, Any]:
        block = self._get_index()["blocks"].get(name)
        if not block:
            raise FileNotFoundError(f"Block '{name}' not found in registry")
        return block

    def list_blocks(self) -> list[str]:
        return sorted(self._get_index()["blocks"])

    def get_block_source(self, name: str) -> str:
        block = self._get_block_entry(name)
        install_name = block.get("install_name", name)
        return self._fetch_source(block, "blocks", install_name, f"block '{name}'")

    def get_block_metadata(self, name: str) -> dict[str, Any]:
        return self._get_block_entry(name)

    def resolve_block_dependencies(self, name: str) -> list[str]:
        block = self._get_block_entry(name)
        resolved: list[str] = []
        visiting: set[str] = set()
        visited: set[str] = set()
        for dep in block.get("dependencies", []):
            self._visit_component(dep, resolved, visiting, visited)
        return resolved

    def get_block_with_dependencies(self, name: str) -> tuple[dict[str, str], str]:
        comp_deps = {n: self.get_component_source(n) for n in self.resolve_block_dependencies(name)}
        block_source = self.get_block_source(name)
        return comp_deps, block_source

    # ── Unified lookup ──────────────────────────────────────────────────

    def lookup(self, name: str) -> tuple[str, dict[str, Any]]:
        index = self._get_index()
        if name in index["components"]:
            return ("component", index["components"][name])
        blocks = index["blocks"]
        if name in blocks:
            return ("block", blocks[name])
        # Fallback: match by install_name so `star add user-button` resolves
        for entry in blocks.values():
            if entry.get("install_name") == name:
                return ("block", entry)
        raise FileNotFoundError(f"'{name}' not found in registry (checked components and blocks)")
