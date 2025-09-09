from typing import Optional, Tuple
from functools import lru_cache
from starhtml import Div, A, Span
from starui.registry.components.button import Button
from starui.registry.components.utils import cn
from component_registry import get_registry


@lru_cache(maxsize=1)
def _get_ordered_components() -> list[Tuple[str, str]]:
    registry = get_registry()
    components = sorted(registry.components.items(), key=lambda x: x[1].get("title", x[0]))
    return [(name, comp["title"]) for name, comp in components]


def _slug_to_registry_key(component_slug: str) -> Optional[str]:
    registry = get_registry()    
    if component_slug in registry.components:
        return component_slug    
    if (underscore_key := component_slug.replace("-", "_")) in registry.components:
        return underscore_key
    
    return None


def get_component_navigation(current_component: str) -> Tuple[Optional[Tuple[str, str]], Optional[Tuple[str, str]]]:
    if not (current_key := _slug_to_registry_key(current_component)):
        return None, None    
    components = _get_ordered_components()    
    try:
        current_index = [key for key, _ in components].index(current_key)
    except ValueError:
        return None, None    
    prev_comp = components[current_index - 1] if current_index > 0 else None
    next_comp = components[current_index + 1] if current_index < len(components) - 1 else None
    
    return prev_comp, next_comp


def TopNavigation(current_component: str, cls: str = "") -> Div:
    prev_comp, next_comp = get_component_navigation(current_component)
    
    prev_button = A(
        Button("←", variant="ghost", size="sm", cls="h-8 w-8 p-0"),
        href=f"/components/{prev_comp[0]}",
        cls="no-underline"
    ) if prev_comp else Div(cls="w-8 h-8")
    
    next_button = A(
        Button("→", variant="ghost", size="sm", cls="h-8 w-8 p-0"),
        href=f"/components/{next_comp[0]}",
        cls="no-underline"
    ) if next_comp else Div(cls="w-8 h-8")
    
    return Div(prev_button, next_button, cls=cn("flex items-center gap-2", cls))


def BottomNavigation(current_component: str, cls: str = "") -> Div:
    prev_comp, next_comp = get_component_navigation(current_component)
    
    prev_button = A(
        Button("←", Span(prev_comp[1], cls="ml-2"), variant="outline", cls="flex items-center"),
        href=f"/components/{prev_comp[0]}",
        cls="no-underline"
    ) if prev_comp else Span()
    
    next_button = A(
        Button(Span(next_comp[1], cls="mr-2"), "→", variant="outline", cls="flex items-center"),
        href=f"/components/{next_comp[0]}",
        cls="no-underline"
    ) if next_comp else Span()
    
    return Div(
        Div(prev_button, cls="flex-1"),
        Div(next_button, cls="flex-1 flex justify-end"),
        cls=cn("flex items-center justify-between pt-8 mt-8 border-t border-border/50", cls)
    )