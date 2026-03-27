from collections.abc import Callable
from typing import Any
from uuid import uuid4

from fastcore.xml import FT

try:
    from starmerge import merge
except ImportError:

    def merge(*classes: str) -> str:
        return " ".join(c for c in classes if c)


__metadata__ = {"description": "Class name utilities"}


def with_signals(component, **signals):
    """Attach signals as attributes to a component."""
    for name, signal in signals.items():
        setattr(component, name, signal)
    return component


DEFAULT_THEME = "light"
ALT_THEME = "dark"


def cn(*classes: Any) -> str:
    """Merge class names and truthy class mappings."""
    processed: list[str] = []

    for cls in classes:
        if not cls:
            continue

        if isinstance(cls, str):
            processed.append(cls)
        elif isinstance(cls, dict):
            for class_name, condition in cls.items():
                if condition:
                    processed.append(str(class_name))
        elif isinstance(cls, list | tuple):
            processed.append(cn(*cls))
        else:
            processed.append(str(cls))

    return merge(*processed) if processed else ""


def cva(base: str = "", config: dict[str, Any] | None = None) -> Callable[..., str]:
    config = config or {}

    variants = config.get("variants", {})
    compound_variants = config.get("compoundVariants", [])
    default_variants = config.get("defaultVariants", {})

    def variant_function(**props: Any) -> str:
        classes = [base] if base else []

        final_props = {**default_variants, **props}

        for variant_key, variant_values in variants.items():
            prop_value = final_props.get(variant_key)
            if prop_value and prop_value in variant_values:
                classes.append(variant_values[prop_value])

        for compound in compound_variants:
            compound_class = compound.get("class", "")
            if compound_class and all(final_props.get(k) == v for k, v in compound.items() if k != "class"):
                classes.append(compound_class)

        return cn(*classes)

    return variant_function


def gen_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:8]}"


def _flatten(*items: Any) -> list:
    result: list = []
    for item in items:
        if isinstance(item, list | tuple):
            result.extend(item)
        elif item is not None:
            result.append(item)
    return result


def merge_actions(*before: Any, kwargs: dict | None = None, after: Any = None) -> list:
    result = _flatten(*before)
    if kwargs is not None:
        result.extend(_flatten(kwargs.pop("data_on_click", None)))
    result.extend(_flatten(after))
    return result


def inject_context(element, **context):
    """Recursively inject context into callable children."""
    if callable(element) and not isinstance(element, FT):
        element = element(**context)

    if isinstance(element, FT) and element.children:
        element.children = tuple(inject_context(c, **context) for c in element.children)

    return element
