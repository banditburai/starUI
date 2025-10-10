"""
Skeleton component documentation - Loading placeholders and states.
"""

# Component metadata for auto-discovery
TITLE = "Skeleton"
DESCRIPTION = "Display a placeholder preview of your content before the data gets loaded to reduce load-time frustration."
CATEGORY = "ui"
ORDER = 25
STATUS = "stable"

from starhtml import Div, P, H3, H4, Span, Signal, js
from starui.registry.components.skeleton import Skeleton
from starui.registry.components.button import Button
from starui.registry.components.card import Card, CardContent, CardHeader, CardTitle
from utils import auto_generate_page, with_code, Prop, build_api_reference
from widgets.component_preview import ComponentPreview


# ============================================================================
# EXAMPLE FUNCTIONS (decorated with @with_code for markdown generation)
# ============================================================================

# Basic skeleton shapes with proper circles
@with_code
def basic_shapes_skeleton_example():
    return Div(
        Div(
            H4("Text Lines", cls="mb-3 text-sm font-medium"),
            Skeleton(cls="h-4 w-3/4 mb-2"),
            Skeleton(cls="h-4 w-full mb-2"),
            Skeleton(cls="h-4 w-5/6"),
            cls="mb-6"
        ),
        Div(
            H4("Shapes", cls="mb-3 text-sm font-medium"),
            Div(
                Skeleton(cls="h-8 w-8 rounded-full mr-4"),
                Skeleton(cls="h-10 w-10 rounded-full mr-4"),
                Skeleton(cls="h-12 w-12 rounded-full mr-4"),
                Skeleton(cls="h-16 w-16 rounded-full mr-4"),
                Skeleton(cls="h-10 w-24"),
                cls="flex items-center"
            ),
            cls="mb-4"
        ),
        Div(
            H4("User Profile", cls="mb-3 text-sm font-medium"),
            Div(
                Skeleton(cls="h-14 w-14 rounded-full"),
                Div(
                    Skeleton(cls="h-4 w-32 mb-2"),
                    Skeleton(cls="h-3 w-24"),
                    cls="ml-4"
                ),
                cls="flex items-center"
            )
        ),
        cls="space-y-6"
    )


# Card skeleton layout
@with_code
def card_layout_skeleton_example():
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
            Skeleton(cls="h-4 w-full mb-3"),
            Skeleton(cls="h-4 w-4/5 mb-3"),
            Skeleton(cls="h-4 w-3/4 mb-4"),
            Skeleton(cls="h-8 w-24 rounded")
        ),
        cls="w-80"
    )


# Data table skeleton
@with_code
def data_table_skeleton_example():
    return Div(
        Div(
            Div(
                Skeleton(cls="h-4 w-16"),
                Skeleton(cls="h-4 w-20"),
                Skeleton(cls="h-4 w-12"),
                Skeleton(cls="h-4 w-14"),
                cls="grid grid-cols-4 gap-4 py-3 px-4 border-b"
            ),
            cls="bg-muted/50"
        ),
        Div(
            *[
                Div(
                    Div(
                        Skeleton(cls="h-8 w-8 rounded-full"),
                        Skeleton(cls="h-4 w-24 ml-2"),
                        cls="flex items-center"
                    ),
                    Skeleton(cls="h-4 w-32"),
                    Skeleton(cls="h-5 w-16 rounded-full"),
                    Skeleton(cls="h-6 w-6 rounded-full"),
                    cls="grid grid-cols-4 gap-4 py-4 px-4 border-b border-border/50"
                )
                for _ in range(4)
            ],
        ),
        cls="w-full max-w-3xl border rounded-lg overflow-hidden"
    )


# Interactive loading demo
@with_code
def loading_states_skeleton_example():
    loading = Signal("loading", True)

    return Div(
        H4("Loading State Toggle", cls="text-lg font-medium mb-2"),
        Div(
            loading,
            Button(
                data_text=js("$loading ? 'Stop Loading' : 'Start Loading'"),
                data_on_click=js("$loading = !$loading"),
                variant="outline",
                cls="mb-4",
            ),
            Div(
                Skeleton(cls="h-6 w-40 mb-2"),
                Skeleton(cls="h-4 w-80 mb-4"),
                Skeleton(cls="h-20 w-full rounded-lg"),
                data_show=js("$loading"),
            ),
            Div(
                H4("Content Loaded!", cls="text-lg font-semibold mb-2"),
                P("This content appears when loading is complete.", cls="mb-4"),
                Div(
                    "This is the actual content that would load.",
                    cls="p-4 bg-muted rounded-lg",
                ),
                data_show=js("!$loading"),
            ),
            cls="p-4 border rounded-lg",
        ),
        cls="mb-6",
    )


# ============================================================================
# MODULE-LEVEL DATA (for markdown API)
# ============================================================================

EXAMPLES_DATA = [
    {"title": "Basic Shapes", "description": "Text lines, perfect circles, and common patterns", "fn": basic_shapes_skeleton_example},
    {"title": "Card Layout", "description": "Skeleton for a typical user card with avatar, content, and action", "fn": card_layout_skeleton_example},
    {"title": "Data Table", "description": "Skeleton for user data table with avatars and status indicators", "fn": data_table_skeleton_example},
    {"title": "Loading States", "description": "Interactive demo showing skeleton to content transition", "fn": loading_states_skeleton_example},
]

API_REFERENCE = build_api_reference(
    main_props=[
        Prop("cls", "str", "Additional CSS classes for custom sizing and spacing", "''"),
        Prop("class_name", "str", "Alternative CSS classes prop (merged with cls)", "''"),
    ]
)


def examples():
    """Generate all skeleton examples."""
    yield ComponentPreview(
        basic_shapes_skeleton_example(),
        basic_shapes_skeleton_example.code,
        title="Basic Shapes",
        description="Text lines, perfect circles, and common patterns"
    )

    yield ComponentPreview(
        card_layout_skeleton_example(),
        card_layout_skeleton_example.code,
        title="Card Layout",
        description="Skeleton for a typical user card with avatar, content, and action"
    )

    yield ComponentPreview(
        data_table_skeleton_example(),
        data_table_skeleton_example.code,
        title="Data Table",
        description="Skeleton for user data table with avatars and status indicators"
    )

    yield ComponentPreview(
        loading_states_skeleton_example(),
        loading_states_skeleton_example.code,
        title="Loading States",
        description="Interactive demo showing skeleton to content transition"
    )



def create_skeleton_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)