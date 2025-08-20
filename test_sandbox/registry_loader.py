"""Registry component loader for testing."""

import importlib.util
import sys
from pathlib import Path
from typing import Any


def load_registry_components() -> dict[str, Any]:
    """Load all components from the registry for testing."""
    # Add parent directory to path
    parent_dir = Path(__file__).parent.parent
    sys.path.insert(0, str(parent_dir))

    registry_path = parent_dir / "src" / "starui" / "registry" / "components"

    if not registry_path.exists():
        return {}

    components = {}

    for py_file in registry_path.glob("*.py"):
        if py_file.name.startswith("_") or py_file.name == "utils.py":
            continue

        module_name = f"src.starui.registry.components.{py_file.stem}"

        try:
            module = importlib.import_module(module_name)

            # Get all callable, uppercase attributes (components)
            for name in dir(module):
                attr = getattr(module, name)
                if name[0].isupper() and callable(attr):
                    components[name] = attr

        except Exception as e:
            print(f"Failed to load {module_name}: {e}")
            continue

    return components


# Load all components and make them available
_components = load_registry_components()
globals().update(_components)

# Export for * imports
__all__ = list(_components.keys())
