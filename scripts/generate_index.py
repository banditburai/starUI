#!/usr/bin/env python3
"""Generate registry/index.json from component files.

Derives dependencies from relative imports via AST, and reads non-derivable
metadata (description, handlers, packages, css_imports) from each component's
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


def extract_dependencies(file_path: Path) -> list[str]:
    """Derive component dependencies from relative imports."""
    tree = ast.parse(file_path.read_text())
    deps = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.level == 1 and node.module:
            deps.add(node.module)
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


def generate_index() -> dict:
    components = {}
    for file_path in sorted(COMPONENTS_DIR.glob("*.py")):
        if file_path.name.startswith("_"):
            continue
        entry = load_component(file_path)
        components[entry["name"]] = entry

    with open(PROJECT_ROOT / "pyproject.toml", "rb") as f:
        version = tomllib.load(f)["project"]["version"]

    return {"version": version, "schema_version": 1, "components": components}


def main():
    index = generate_index()
    output_path = REGISTRY_DIR / "index.json"
    output_path.write_text(json.dumps(index, indent=2) + "\n")
    print(f"Generated {output_path} with {len(index['components'])} components (v{index['version']})")


if __name__ == "__main__":
    main()
