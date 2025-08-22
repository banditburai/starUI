"""Component metadata registry."""

from typing import Any

from pydantic import BaseModel, Field


class ComponentMetadata(BaseModel):
    """StarUI component metadata."""

    name: str
    description: str = ""
    dependencies: list[str] = Field(default_factory=list)
    packages: list[str] = Field(default_factory=list)
    css_files: list[str] = Field(default_factory=list)
    css_imports: list[str] = Field(default_factory=list)
    options: dict[str, Any] = Field(default_factory=dict)

    model_config = {"extra": "ignore"}


def _component(name: str, desc: str, deps: list[str] = None, **kwargs):
    """Helper to create component metadata."""
    return ComponentMetadata(
        name=name, description=desc, dependencies=deps or [], **kwargs
    )


COMPONENT_REGISTRY = {
    "code_block": _component(
        "code_block",
        "Code block with syntax highlighting",
        ["utils"],
        packages=["starlighter"],
        options={
            "available_themes": [
                "github",
                "monokai",
                "dracula",
                "catppuccin",
                "vscode",
            ],
            "default_theme": "github",
        },
    ),
    "theme_toggle": _component(
        "theme_toggle", "Theme toggle button", ["utils", "button"]
    ),
    "sheet": _component("sheet", "Slide-out panel", ["utils", "button"]),
    "dialog": _component("dialog", "Modal dialog", ["utils", "button"]),
    "button": _component("button", "Button with variants", ["utils"]),
    "alert": _component("alert", "Alert notifications", ["utils"]),
    "badge": _component("badge", "Badge for labels", ["utils"]),
    "breadcrumb": _component("breadcrumb", "Breadcrumb navigation", ["utils"]),
    "card": _component("card", "Card container", ["utils"]),
    "checkbox": _component("checkbox", "Checkbox input", ["utils"]),
    "input": _component("input", "Form input", ["utils"]),
    "label": _component("label", "Form label", ["utils"]),
    "tabs": _component("tabs", "Tabbed interface", ["utils"]),
    "utils": _component("utils", "Class name utilities"),
}


def get_component_metadata(component_name: str) -> ComponentMetadata | None:
    """Get metadata for a component."""
    return COMPONENT_REGISTRY.get(component_name)
