"""
Popover component documentation - Floating content triggered by a button.
"""

# Component metadata for auto-discovery
TITLE = "Popover"
DESCRIPTION = "Displays rich content in a portal, triggered by a button. Uses native HTML popover API for accessibility and performance."
CATEGORY = "overlay"
ORDER = 60
STATUS = "stable"

from starhtml import Div, P, H3, Icon, Ul, Li, Signal
from components.popover import (
    Popover, PopoverTrigger, PopoverContent, PopoverClose
)
from components.button import Button
from components.input import InputWithLabel
from components.label import Label
from utils import auto_generate_page, with_code, Component, build_api_reference


@with_code
def basic_popover_example():
    return Popover(
        PopoverTrigger("Open Popover", variant="outline"),
        PopoverContent(
            H3("Dimensions", cls="text-sm font-semibold"),
            P("Set the dimensions for the layer.", cls="text-sm text-muted-foreground"),
            cls="grid gap-2"
        )
    )


@with_code
def popover_placement_example():
    positions = [
        ("Top", "top"),
        ("Right", "right"),
        ("Bottom", "bottom"),
        ("Left", "left"),
    ]

    return Div(
        *[
            Popover(
                PopoverTrigger(label, variant="outline", size="sm"),
                PopoverContent(
                    P(f"Content positioned to the {side}.", cls="text-sm text-muted-foreground"),
                    side=side,
                    cls="w-48"
                )
            )
            for label, side in positions
        ],
        cls="flex flex-wrap justify-center gap-2"
    )


@with_code
def form_popover_example():
    return Div(
        (width_val := Signal("pop_width", "")),
        (height_val := Signal("pop_height", "")),
        (content_ref := Signal("dims_content", _ref_only=True)),
        Popover(
            PopoverTrigger("Open popover", variant="outline"),
            PopoverContent(
                H3("Dimensions", cls="text-sm font-semibold"),
                P("Set the dimensions for the layer.", cls="text-sm text-muted-foreground"),
                Div(
                    InputWithLabel(label="Width", placeholder="100%", signal=width_val),
                    InputWithLabel(label="Height", placeholder="25px", signal=height_val),
                    cls="grid gap-3"
                ),
                Div(
                    Button(
                        "Cancel",
                        variant="outline",
                        size="sm",
                        data_on_click=content_ref.hidePopover()
                    ),
                    Button(
                        "Apply",
                        size="sm",
                        data_on_click=content_ref.hidePopover()
                    ),
                    cls="flex justify-end gap-2"
                ),
                cls="grid w-64 gap-3",
            ),
            signal="dims"
        )
    )


@with_code
def inline_help_popover_example():
    return Div(
        Div(
            Label(
                "API Key",
                Popover(
                    PopoverTrigger(
                        Icon("lucide:help-circle", cls="size-3 text-muted-foreground"),
                        variant="ghost",
                        size="icon",
                        cls="size-5 p-0",
                        aria_label="API key help"
                    ),
                    PopoverContent(
                        H3("API Key", cls="text-sm font-semibold"),
                        P("Your API key authenticates requests to the service.", cls="text-sm text-muted-foreground"),
                        Ul(
                            Li("Keep it secret and secure"),
                            Li("Regenerate if compromised"),
                            cls="list-inside list-disc text-sm text-muted-foreground"
                        ),
                        cls="grid w-64 gap-2",
                        side="top"
                    )
                ),
                fr="api-key-help",
            ),
            cls="grid w-full max-w-sm gap-1.5"
        ),
    )


@with_code
def popover_with_close_button_example():
    return Popover(
        PopoverTrigger(
            Icon("lucide:info", cls="size-4"),
            "Notice",
            variant="outline"
        ),
        PopoverContent(
            PopoverClose(
                Icon("lucide:x", cls="size-3"),
                size="sm",
                variant="ghost"
            ),
            Div(
                Icon("lucide:alert-triangle", cls="size-5 shrink-0 text-amber-500"),
                Div(
                    H3("System Maintenance", cls="text-sm font-semibold"),
                    P("Scheduled maintenance tonight from 2:00 AM to 4:00 AM EST. Some features may be unavailable.",
                      cls="text-sm text-muted-foreground"),
                    cls="grid gap-1"
                ),
                cls="flex gap-3"
            ),
            PopoverClose("Got it", size="sm", variant="default", cls="static ml-auto"),
            cls="grid gap-3"
        )
    )


EXAMPLES_DATA = [
    {"title": "Basic Popover", "description": "Simple popover with a heading and description", "fn": basic_popover_example},
    {"title": "Placement", "description": "Control positioning with the side prop", "fn": popover_placement_example},
    {"title": "Form Popover", "description": "Form inputs inside a popover with programmatic close", "fn": form_popover_example},
    {"title": "Inline Help", "description": "Contextual help icon that opens a popover with guidance", "fn": inline_help_popover_example},
    {"title": "Close Button", "description": "Explicit close button using PopoverClose", "fn": popover_with_close_button_example},
]

API_REFERENCE = build_api_reference(
    components=[
        Component("Popover", "Container that wires a unique signal to trigger and content using the native popover API"),
        Component("PopoverTrigger", "Button that toggles the popover open/closed"),
        Component("PopoverContent", "Floating content positioned via data_position with side and align controls"),
        Component("PopoverClose", "Helper button that hides the popover; can be placed inside content"),
    ]
)


def create_popover_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)
