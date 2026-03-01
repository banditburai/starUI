TITLE = "Skeleton"
DESCRIPTION = "Display a placeholder preview of your content before the data gets loaded to reduce load-time frustration."
CATEGORY = "ui"
ORDER = 25
STATUS = "stable"

from starhtml import Div, Signal
from starui.registry.components.skeleton import Skeleton
from starui.registry.components.button import Button
from starui.registry.components.card import Card, CardContent, CardHeader
from utils import auto_generate_page, with_code, Prop, build_api_reference


@with_code
def default_example():
    return Div(
        Skeleton(cls="h-12 w-12 rounded-full"),
        Div(
            Skeleton(cls="h-4 w-[250px]"),
            Skeleton(cls="h-4 w-[200px]"),
            cls="space-y-2"
        ),
        cls="flex items-center gap-4"
    )


@with_code
def card_example():
    return Card(
        CardHeader(
            Div(
                Skeleton(cls="h-12 w-12 rounded-full"),
                Div(
                    Skeleton(cls="h-4 w-24 mb-2"),
                    Skeleton(cls="h-3 w-16"),
                    cls="ml-4"
                ),
                cls="flex items-center"
            )
        ),
        CardContent(
            Div(
                Skeleton(cls="h-4 w-full"),
                Skeleton(cls="h-4 w-4/5"),
                Skeleton(cls="h-4 w-3/4"),
                cls="space-y-3"
            ),
            Skeleton(cls="h-8 w-24 mt-4")
        ),
        cls="max-w-80 w-full"
    )


@with_code
def loading_example():
    loading = Signal("skeleton_loading", True)

    return Div(
        loading,
        Button(
            data_text=loading.if_("Stop Loading", "Start Loading"),
            data_on_click=loading.toggle(),
            variant="outline",
            size="sm",
            cls="mb-4 w-28"
        ),
        Div(
            Div(
                Skeleton(cls="h-7 w-48 mb-3"),
                Skeleton(cls="h-5 w-full mb-2"),
                Skeleton(cls="h-5 w-3/5"),
                cls="col-start-1 row-start-1",
                data_attr_cls=loading.if_("", "invisible")
            ),
            Div(
                Div("Dashboard Overview", cls="text-lg font-semibold mb-3"),
                Div("Your weekly activity is up 12% compared to last period.", cls="text-sm text-muted-foreground mb-2"),
                Div("Keep it up — you're on track to hit your monthly goal.", cls="text-sm text-muted-foreground"),
                cls="col-start-1 row-start-1",
                data_attr_cls=loading.if_("invisible", "")
            ),
            cls="grid"
        ),
    )


API_REFERENCE = build_api_reference(
    main_props=[
        Prop("cls", "str", "CSS classes for sizing, spacing, and shape", "''"),
    ]
)

EXAMPLES_DATA = [
    {"fn": default_example, "title": "Default", "description": "Avatar circle with text lines"},
    {"fn": card_example, "title": "Card", "description": "Skeleton composed inside a Card with avatar and text block"},
    {"fn": loading_example, "title": "Loading States", "description": "Toggle between skeleton placeholders and loaded content"},
]


def create_skeleton_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)
