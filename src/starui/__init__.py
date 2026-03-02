"""Python-first UI component library for StarHTML applications."""

from importlib.metadata import version

__version__ = version("starui")

from .utils import (
    ALT_THEME,
    DEFAULT_THEME,
    cn,
    cva,
    gen_id,
    inject_context,
    with_signals,
)

__all__ = [
    "__version__",
    "cn",
    "cva",
    "gen_id",
    "inject_context",
    "with_signals",
    "DEFAULT_THEME",
    "ALT_THEME",
]
