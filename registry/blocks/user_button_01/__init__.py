"""Bridge relative imports to the components package for dev/docs contexts.

When installed via `star add`, the block file lives alongside component files
in `components/ui/`, so relative imports resolve naturally. In the registry
layout (where blocks live in their own subdirectory), this __init__.py maps
relative imports to the `components` package so the block can be imported
directly during development and docs builds.
"""

import importlib
import sys

_COMPONENT_DEPS = ['avatar', 'dropdown_menu', 'utils']

for _name in _COMPONENT_DEPS:
    _key = f"{__name__}.{_name}"
    if _key not in sys.modules:
        try:
            sys.modules[_key] = importlib.import_module(f"components.{_name}")
        except ModuleNotFoundError:
            pass  # Not in a context where components package is on the path
