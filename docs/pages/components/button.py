"""
Button component documentation - Interactive triggers and actions.
"""

TITLE = "Button"
DESCRIPTION = "Displays a button or a component that looks like a button."
CATEGORY = "ui"
ORDER = 10
STATUS = "stable"

from starhtml import Div, Icon
from starui.registry.components.button import Button
from utils import auto_generate_page, Prop, Component, build_api_reference, with_code


@with_code
def hero_button_example():
    return Div(
        Button("Default"),
        Button("Secondary", variant="secondary"),
        Button("Destructive", variant="destructive"),
        Button("Outline", variant="outline"),
        Button("Ghost", variant="ghost"),
        Button("Link", variant="link"),
        cls="flex flex-wrap gap-2 justify-center"
    )


@with_code
def button_sizes_example():
    return Div(
        Button("Small", size="sm"),
        Button("Default"),
        Button("Large", size="lg"),
        Button(
            Icon("lucide:chevron-right", cls="h-4 w-4"),
            variant="outline",
            size="icon",
            aria_label="Next"
        ),
        cls="flex items-center gap-2"
    )


@with_code
def with_icons_button_example():
    return Div(
        Button(Icon("lucide:log-in", cls="h-4 w-4"), "Sign in"),
        Button(
            "Export",
            Icon("lucide:download", cls="h-4 w-4"),
            variant="outline"
        ),
        Button(
            Icon("lucide:loader-2", cls="h-4 w-4 animate-spin"),
            "Deploying...",
            disabled=True,
        ),
        cls="flex gap-2 flex-wrap"
    )


@with_code
def icon_toolbar_example():
    return Div(
        Div(
            Button(Icon("lucide:bold", cls="h-4 w-4"), size="icon", variant="ghost", aria_label="Bold"),
            Button(Icon("lucide:italic", cls="h-4 w-4"), size="icon", variant="ghost", aria_label="Italic"),
            Button(Icon("lucide:underline", cls="h-4 w-4"), size="icon", variant="ghost", aria_label="Underline"),
            cls="flex gap-1"
        ),
        Div(
            Button(Icon("lucide:align-left", cls="h-4 w-4"), size="icon", variant="ghost", aria_label="Align left"),
            Button(Icon("lucide:align-center", cls="h-4 w-4"), size="icon", variant="ghost", aria_label="Align center"),
            Button(Icon("lucide:align-right", cls="h-4 w-4"), size="icon", variant="ghost", aria_label="Align right"),
            cls="flex gap-1"
        ),
        cls="flex gap-4"
    )


@with_code
def action_patterns_example():
    return Div(
        Button("Cancel", variant="outline"),
        Button("Save changes"),
        Button(
            Icon("lucide:trash-2", cls="h-4 w-4"),
            "Delete repository",
            variant="destructive"
        ),
        cls="flex flex-wrap gap-2"
    )


EXAMPLES_DATA = [
    {"fn": hero_button_example, "title": "Variants", "description": "The six built-in variants — default, secondary, destructive, outline, ghost, and link"},
    {"fn": button_sizes_example, "title": "Sizes", "description": "Four size options including icon-only buttons — always pair size='icon' with aria_label"},
    {"fn": with_icons_button_example, "title": "With Icons", "description": "Place icons before or after text as children — the built-in gap handles spacing, no manual margin needed"},
    {"fn": icon_toolbar_example, "title": "Icon Toolbar", "description": "Ghost icon buttons composed as a text formatting toolbar with accessible labels"},
    {"fn": action_patterns_example, "title": "Action Patterns", "description": "Mixing variants to convey intent — outline for cancel, default for confirm, destructive for danger"},
]

API_REFERENCE = build_api_reference(
    main_props=[
        Prop("variant", "Literal['default', 'secondary', 'destructive', 'outline', 'ghost', 'link']",
             "Visual style variant", "'default'"),
        Prop("size", "Literal['default', 'sm', 'lg', 'icon']",
             "Button size. Use 'icon' for square icon-only buttons", "'default'"),
        Prop("disabled", "bool",
             "Disables the button — adds opacity and blocks pointer events", "False"),
        Prop("type", "Literal['button', 'submit', 'reset']",
             "HTML button type. Defaults to 'button' (not 'submit' as in native HTML)", "'button'"),
        Prop("cls", "str",
             "Additional CSS classes", "''"),
    ],
    components=[
        Component("Button", "Renders a <button> element. Accepts arbitrary children — text, icons, or both. All extra keyword arguments (data_on_click, aria_label, id, etc.) are passed through to the underlying element"),
    ]
)


def create_button_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)
