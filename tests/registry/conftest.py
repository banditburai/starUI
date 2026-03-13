import json

from starui.registry.checksum import compute_checksum
from starui.registry.client import RegistryClient


def make_component_entry(name: str, source: str, *, deps: list[str] | None = None) -> dict:
    return {
        "name": name,
        "description": f"Test {name}",
        "file": f"components/{name}.py",
        "dependencies": deps or [],
        "packages": [],
        "css_imports": [],
        "handlers": [],
        "checksum": compute_checksum(source),
    }


def make_block_entry(
    name: str,
    source: str,
    *,
    deps: list[str] | None = None,
    install_name: str | None = None,
) -> dict:
    return {
        "name": name,
        "description": f"Test block {name}",
        "file": f"blocks/{name}/{install_name or name}.py",
        "dependencies": deps or [],
        "install_name": install_name or name,
        "packages": [],
        "css_imports": [],
        "handlers": [],
        "checksum": compute_checksum(source),
    }


def make_test_client(
    tmp_path,
    version: str,
    index: dict,
    sources: dict[str, str],
    block_sources: dict[str, tuple[str, str]] | None = None,
) -> RegistryClient:
    cache_dir = tmp_path / ".starui" / "cache" / "registry" / version
    cache_dir.mkdir(parents=True)
    (cache_dir / "index.json").write_text(json.dumps(index))
    (cache_dir / "index.meta.json").write_text(json.dumps({"fetched_at": 9999999999}))

    comp_dir = cache_dir / "components"
    comp_dir.mkdir()
    for name, source in sources.items():
        (comp_dir / f"{name}.py").write_text(source)

    if block_sources:
        blocks_dir = cache_dir / "blocks"
        blocks_dir.mkdir()
        for _name, (install_name, source) in block_sources.items():
            (blocks_dir / f"{install_name}.py").write_text(source)

    client = RegistryClient(version=version)
    client.cache_dir = cache_dir
    return client
