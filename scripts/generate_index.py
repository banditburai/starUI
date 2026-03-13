#!/usr/bin/env python3
"""Generate registry/index.json from component and block files.

Derives dependencies from relative imports via AST, and reads non-derivable
metadata (description, handlers, packages, css_imports) from each file's
__metadata__ dict. No separate registry file needed.
"""

import ast
import json
import sys
import tomllib
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from starui.registry.checksum import compute_checksum  # noqa: E402

REGISTRY_DIR = PROJECT_ROOT / "registry"
COMPONENTS_DIR = REGISTRY_DIR / "components"
BLOCKS_DIR = REGISTRY_DIR / "blocks"


def extract_dependencies(file_path: Path) -> list[str]:
    """Derive component dependencies from relative and absolute imports."""
    tree = ast.parse(file_path.read_text())
    deps = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            if node.level == 1:
                deps.add(node.module)
            elif node.level == 0 and node.module.startswith("components."):
                deps.add(node.module.removeprefix("components."))
    return sorted(deps)


def extract_metadata(file_path: Path) -> dict:
    """Read __metadata__ dict from a component file via AST."""
    tree = ast.parse(file_path.read_text())
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Assign)
            and len(node.targets) == 1
            and isinstance(node.targets[0], ast.Name)
            and node.targets[0].id == "__metadata__"
        ):
            return ast.literal_eval(node.value)
    return {}


def load_component(file_path: Path) -> dict:
    """Build index entry for a single component file."""
    meta = extract_metadata(file_path)
    deps = extract_dependencies(file_path)

    entry = {
        "name": file_path.stem,
        "description": meta.get("description", ""),
        "file": f"components/{file_path.name}",
        "dependencies": deps,
        "packages": meta.get("packages", []),
        "css_imports": meta.get("css_imports", []),
        "handlers": meta.get("handlers", []),
        "checksum": compute_checksum(file_path),
    }

    return entry


def load_block(block_dir: Path) -> dict | None:
    """Build index entry for a block subdirectory."""
    py_files = [f for f in block_dir.glob("*.py") if not f.name.startswith("_")]
    if not py_files:
        return None

    file_path = py_files[0]
    meta = extract_metadata(file_path)
    deps = extract_dependencies(file_path)

    return {
        "name": block_dir.name,
        "install_name": file_path.stem,
        "description": meta.get("description", ""),
        "file": f"blocks/{block_dir.name}/{file_path.name}",
        "dependencies": deps,
        "packages": meta.get("packages", []),
        "css_imports": meta.get("css_imports", []),
        "handlers": meta.get("handlers", []),
        "checksum": compute_checksum(file_path),
    }


def generate_index() -> dict:
    components = {}
    for file_path in sorted(COMPONENTS_DIR.glob("*.py")):
        if file_path.name.startswith("_"):
            continue
        entry = load_component(file_path)
        components[entry["name"]] = entry

    blocks = {}
    if BLOCKS_DIR.exists():
        for block_dir in sorted(BLOCKS_DIR.iterdir()):
            if not block_dir.is_dir() or block_dir.name.startswith("_"):
                continue
            entry = load_block(block_dir)
            if entry:
                blocks[entry["name"]] = entry

    with open(PROJECT_ROOT / "pyproject.toml", "rb") as f:
        version = tomllib.load(f)["project"]["version"]

    return {"version": version, "schema_version": 2, "components": components, "blocks": blocks}


def main():
    index = generate_index()
    output_path = REGISTRY_DIR / "index.json"
    output_path.write_text(json.dumps(index, indent=2) + "\n")
    parts = [f"{len(index['components'])} components"]
    if index["blocks"]:
        parts.append(f"{len(index['blocks'])} blocks")
    print(f"Generated {output_path} with {', '.join(parts)} (v{index['version']})")


if __name__ == "__main__":
    main()
