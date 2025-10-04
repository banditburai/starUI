from collections.abc import Callable
from typing import Any
import json
from uuid import uuid4
from starhtml import Div

try:
    from starmerge import merge
except ImportError:
    def merge(*classes: str) -> str:
        return " ".join(c for c in classes if c)

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


def inject_signal_recursively(element, signal, *args):
    """Recursively inject signals into factory functions within nested HTML structures."""
    match element:
        case _ if callable(element) and not hasattr(element, 'children'):
            return element(signal, *args)
        case _ if hasattr(element, 'children') and element.children:                        
            children = [
                child(signal, *args) if callable(child) else child 
                for child in element.children
            ]
            attrs = getattr(element, 'attrs', {}).copy()
            return Div(*children, **attrs)
        case _:
            return element


def gen_id(prefix: str) -> str:
    """Generate a short, unique id with a given prefix."""
    return f"{prefix}_{uuid4().hex[:8]}"


def ensure_signal(signal: str | None, prefix: str) -> str:
    """Return the provided signal or generate one with the prefix."""
    return signal or gen_id(prefix)


def js_literal(value: str) -> str:
    """Return a JSON-encoded JS string literal for safe embedding in JS expressions."""
    return json.dumps(value)

