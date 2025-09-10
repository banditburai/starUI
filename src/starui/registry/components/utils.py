from collections.abc import Callable
from typing import Any


def cn(*classes: Any) -> str:
    result_classes: list[str] = []

    for cls in classes:
        if not cls:
            continue

        if isinstance(cls, str):
            result_classes.append(cls)
        elif isinstance(cls, dict):
            for class_name, condition in cls.items():
                if condition:
                    result_classes.append(str(class_name))
        elif isinstance(cls, list | tuple):
            result_classes.append(cn(*cls))
        else:
            result_classes.append(str(cls))

    return " ".join(result_classes)


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
    """
    Recursively inject signals into factory functions within nested HTML structures.
    
    This utility handles the common pattern where factory functions (like SelectItem, 
    DropdownMenuItem, etc.) are nested inside HTML elements (like Div) with conditional 
    visibility or grouping.
    
    Args:
        element: Either a factory function or HTML element to process
        signal: The signal to inject into factory functions
        *args: Additional arguments to pass to factory functions (e.g., for tabs)
    
    Returns:
        - If element is a factory function: calls element(signal, *args)
        - If element is HTML with children: creates new element with processed children
        - Otherwise: returns element unchanged
    """
    # Check if it's a factory function (callable but not an HTML element)
    if callable(element) and not hasattr(element, 'children'):
        return element(signal, *args) if args else element(signal)
    elif hasattr(element, 'children') and element.children:
        # This is an HTML element with children - process its children recursively
        processed_children = []
        for child in element.children:
            if callable(child):
                processed_children.append(child(signal, *args) if args else child(signal))
            else:
                processed_children.append(child)
        
        # Create a new element with the processed children and same attributes
        from starhtml import Div
        # Extract attributes from the original element
        attrs = {}
        if hasattr(element, 'attrs'):
            attrs = element.attrs.copy()
        
        return Div(*processed_children, **attrs)
    else:
        return element


