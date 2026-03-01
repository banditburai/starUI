"""
Toggle component documentation — A two-state button that can be on or off.
"""

# Component metadata for auto-discovery
TITLE = "Toggle"
DESCRIPTION = "A two-state button that can be either on or off."
CATEGORY = "ui"
ORDER = 80
STATUS = "stable"

from starhtml import Div, Span, Icon, Signal
from starui.registry.components.toggle import Toggle
from utils import auto_generate_page, with_code, Prop, build_api_reference


@with_code
def default_example():
    bookmarked = Signal("bookmarked", False)
    return Div(
        bookmarked,
        Toggle(
            Icon("lucide:bookmark", fill=bookmarked),
            "Bookmark",
            signal=bookmarked,
            aria_label="Toggle bookmark",
        ),
    )


@with_code
def outline_example():
    return Div(
        Toggle(
            Icon("lucide:pin"),
            variant="outline",
            aria_label="Toggle pin",
        ),
        Toggle(
            Icon("lucide:star"),
            variant="outline",
            aria_label="Toggle star",
        ),
        cls="flex items-center gap-2",
    )


@with_code
def with_text_example():
    muted = Signal("notif_muted", False)
    return Div(
        muted,
        Toggle(
            Icon("lucide:bell", data_show=~muted),
            Icon("lucide:bell-off", data_show=muted),
            Span("Mute", data_text=muted.if_("Muted", "Mute")),
            signal=muted,
            aria_label="Toggle notifications",
        ),
    )


@with_code
def sizes_example():
    return Div(
        Toggle(Icon("lucide:star", cls="size-3.5"), size="sm", variant="outline", aria_label="Small"),
        Toggle(Icon("lucide:heart"), variant="outline", aria_label="Default"),
        Toggle(Icon("lucide:bell", cls="size-5"), size="lg", variant="outline", aria_label="Large"),
        cls="flex items-center gap-2",
    )


@with_code
def disabled_example():
    return Div(
        Toggle(
            Icon("lucide:lock"),
            variant="outline",
            aria_label="Toggle lock",
            disabled=True,
        ),
        Toggle(
            Icon("lucide:lock"),
            variant="outline",
            pressed=True,
            aria_label="Toggle lock",
            disabled=True,
        ),
        cls="flex items-center gap-2",
    )


EXAMPLES_DATA = [
    {
        "title": "Default",
        "description": "Default variant with a bookmark icon that fills when pressed. Uses Icon's fill parameter with the toggle signal for reactive fill.",
        "fn": default_example,
        "preview_class": "min-h-[150px]",
    },
    {
        "title": "Outline",
        "description": "Outline variant with a visible border and shadow. Hover shows a muted preview while pressed uses the full accent.",
        "fn": outline_example,
        "preview_class": "min-h-[150px]",
    },
    {
        "title": "With Text",
        "description": "Icon and label both react to the same signal. The icon swaps and the button text changes from Mute to Muted when pressed.",
        "fn": with_text_example,
        "preview_class": "min-h-[150px]",
    },
    {
        "title": "Sizes",
        "description": "Three size variants: sm (h-8), default (h-9), and lg (h-10). Icons default to size-4 — pass an explicit size class to scale with the button.",
        "fn": sizes_example,
        "preview_class": "min-h-[150px]",
    },
    {
        "title": "Disabled",
        "description": "Disabled toggles in unpressed and pressed states. Both are non-interactive with reduced opacity.",
        "fn": disabled_example,
        "preview_class": "min-h-[150px]",
    },
]

API_REFERENCE = build_api_reference(
    main_props=[
        Prop("variant", "Literal['default', 'outline']", "Visual style — default is transparent, outline adds border and shadow", "'default'"),
        Prop("size", "Literal['default', 'sm', 'lg']", "Button size controlling height, padding, and min-width", "'default'"),
        Prop("pressed", "bool", "Initial pressed state (maps to data-[state=on])", "False"),
        Prop("signal", "str | Signal", "Datastar signal for pressed state — auto-generated if omitted", "''"),
        Prop("disabled", "bool", "Disable interaction and reduce opacity", "False"),
        Prop("aria_label", "str | None", "Accessible label — required for icon-only toggles", "None"),
    ]
)


def create_toggle_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)
