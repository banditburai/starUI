"""Python-first UI component library for StarHTML applications."""

__version__ = "0.1.0"

from .registry.components.button import Button
from .registry.components.theme_toggle import ThemeToggle
from .registry.components.utils import (
    cn,
    cva,
    gen_id,
    inject_context,
    with_signals,
    DEFAULT_THEME,
    ALT_THEME,
)
from .registry.local import discover_components

_components = discover_components()
globals().update(_components)

__all__ = [
    "__version__",
    "cn",
    "cva",
    "gen_id",
    "inject_context",
    "with_signals",
    "DEFAULT_THEME",
    "ALT_THEME",
    "Button",
    "ThemeToggle",
    *list(_components.keys()),
]


def __getattr__(name: str):
    if name in _components:
        return _components[name]

    components = discover_components()
    if name in components:
        _components[name] = components[name]
        return components[name]

    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
