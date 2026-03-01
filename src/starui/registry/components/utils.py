from collections.abc import Callable
from typing import Any
from uuid import uuid4

try:
    from starmerge import merge
except ImportError:

    def merge(*classes: str) -> str:
        return " ".join(c for c in classes if c)


def with_signals(component, **signals):
    """
    Attach signals as attributes to a component for IDE autocomplete and type hints.

    Usage:
        return with_signals(
            Div(...),
            selected=selected_sig,
            month=month_sig,
        )

    This allows users to access component.selected, component.month, etc.
    """
    for name, signal in signals.items():
        setattr(component, name, signal)
    return component


# Theme configuration
DEFAULT_THEME = "light"
ALT_THEME = "dark"


def cn(*classes: Any) -> str:
    """Merge Tailwind classes intelligently, resolving conflicts."""
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
    if config is None:
        config = {}

    variants = config.get("variants", {})
    compound_variants = config.get("compoundVariants", [])
    default_variants = config.get("defaultVariants", {})

    def variant_function(**props: Any) -> str:
        classes = [base] if base else []

        # Merge defaults with props
        final_props = {**default_variants, **props}

        # Apply variants
        for variant_key, variant_values in variants.items():
            prop_value = final_props.get(variant_key)
            if prop_value and prop_value in variant_values:
                classes.append(variant_values[prop_value])

        # Apply compound variants
        for compound in compound_variants:
            compound_class = compound.get("class", "")
            if not compound_class:
                continue

            matches = True
            for key, value in compound.items():
                if key == "class":
                    continue
                if final_props.get(key) != value:
                    matches = False
                    break

            if matches:
                classes.append(compound_class)

        return cn(*classes)

    return variant_function


def gen_id(prefix: str) -> str:
    """Generate a short, unique id with a given prefix."""
    return f"{prefix}_{uuid4().hex[:8]}"


def ensure_signal(signal: str | None, prefix: str) -> str:
    """Return the provided signal or generate one with the prefix."""
    return signal or gen_id(prefix)


def _flatten(*items: Any) -> list:
    result: list = []
    for item in items:
        if isinstance(item, list | tuple):
            result.extend(item)
        elif item is not None:
            result.append(item)
    return result


def merge_actions(*before: Any, kwargs: dict | None = None, after: Any = None) -> list:
    # Flattens so callers can pass single actions or lists of actions freely
    result = _flatten(*before)
    if kwargs is not None:
        result.extend(_flatten(kwargs.pop("data_on_click", None)))
    result.extend(_flatten(after))
    return result


def inject_context(element, **context):
    """Recursively inject context into callable children, preserving structure."""
    # FT elements are callable (__call__ merges kwargs as HTML attrs) — skip them
    if callable(element) and not hasattr(element, "tag"):
        element = element(**context)

    if hasattr(element, "children") and element.children:
        element.children = tuple(inject_context(c, **context) for c in element.children)

    return element
