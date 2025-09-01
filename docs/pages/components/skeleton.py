"""
Skeleton component documentation - Loading placeholders and states.
"""

# Component metadata for auto-discovery
TITLE = "Skeleton"
DESCRIPTION = "Display a placeholder preview of your content before the data gets loaded to reduce load-time frustration."
CATEGORY = "ui"
ORDER = 25
STATUS = "stable"

from starhtml import Div, P, H3, H4, Span
from starhtml.datastar import ds_signals, ds_show, ds_on_click, value
from starui.registry.components.skeleton import Skeleton
from starui.registry.components.button import Button
from starui.registry.components.card import Card, CardContent, CardHeader, CardTitle
from utils import auto_generate_page
from widgets.component_preview import ComponentPreview


def examples():
    """Generate skeleton examples using ComponentPreview with tabs."""
    
    # Basic skeleton shapes
    yield ComponentPreview(
        Div(
            Div(
                H4("Text Lines", cls="mb-3 text-sm font-medium"),
                Skeleton(cls="h-4 w-3/4 mb-2"),
                Skeleton(cls="h-4 w-full mb-2"),
                Skeleton(cls="h-4 w-5/6"),
                cls="mb-6"
            ),
            Div(
                H4("Various Shapes", cls="mb-3 text-sm font-medium"),
                Div(
                    Skeleton(cls="h-12 w-12 rounded-full"),
                    Div(
                        Skeleton(cls="h-4 w-32 mb-2"),
                        Skeleton(cls="h-3 w-24"),
                        cls="ml-4"
                    ),
                    cls="flex items-center space-x-4"
                )
            ),
            cls="space-y-6"
        ),
        '''# Text line skeletons
Skeleton(cls="h-4 w-3/4")
Skeleton(cls="h-4 w-full") 
Skeleton(cls="h-4 w-5/6")

# Avatar and content skeleton
Div(
    Skeleton(cls="h-12 w-12 rounded-full"),
    Div(
        Skeleton(cls="h-4 w-32"),
        Skeleton(cls="h-3 w-24"),
        cls="ml-4"
    ),
    cls="flex items-center space-x-4"
)''',
        title="Basic Shapes",
        description="Common skeleton patterns for text, avatars, and content"
    )
    
    # Card skeleton layout
    yield ComponentPreview(
        Card(
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
        ),
        '''Card(
    CardHeader(
        Div(
            Skeleton(cls="h-12 w-12 rounded-full"),
            Div(
                Skeleton(cls="h-4 w-24"),
                Skeleton(cls="h-3 w-16"),
                cls="ml-4"
            ),
            cls="flex items-center"
        )
    ),
    CardContent(
        Skeleton(cls="h-4 w-full"),
        Skeleton(cls="h-4 w-4/5"),
        Skeleton(cls="h-4 w-3/4"),
        Skeleton(cls="h-8 w-24 rounded")
    )
)''',
        title="Card Layout",
        description="Skeleton for a typical user card with avatar, content, and action"
    )
    
    # Table skeleton
    yield ComponentPreview(
        Div(
            Div(
                Skeleton(cls="h-6 w-32 mb-4"),
                cls="mb-4"
            ),
            Div(
                *[
                    Div(
                        Skeleton(cls="h-10 w-20"),
                        Skeleton(cls="h-10 w-32"),
                        Skeleton(cls="h-10 w-24"),
                        Skeleton(cls="h-10 w-16"),
                        cls="grid grid-cols-4 gap-4 mb-2"
                    )
                    for _ in range(5)
                ],
                cls="space-y-2"
            ),
            cls="w-full max-w-2xl"
        ),
        '''# Table header
Skeleton(cls="h-6 w-32 mb-4")

# Table rows
Div(
    *[
        Div(
            Skeleton(cls="h-10 w-20"),
            Skeleton(cls="h-10 w-32"),
            Skeleton(cls="h-10 w-24"),
            Skeleton(cls="h-10 w-16"),
            cls="grid grid-cols-4 gap-4"
        )
        for _ in range(5)
    ],
    cls="space-y-2"
)''',
        title="Table Layout",
        description="Skeleton pattern for loading data tables"
    )
    
    # Interactive loading demo
    yield ComponentPreview(
        Div(
            Button(
                "Load Content",
                ds_on_click="$loading = true; setTimeout(() => $loading = false, 3000)"
            ),
            Div(
                # Loading state
                Div(
                    Card(
                        CardHeader(
                            Skeleton(cls="h-6 w-48 mb-2"),
                            Skeleton(cls="h-4 w-32")
                        ),
                        CardContent(
                            Skeleton(cls="h-4 w-full mb-3"),
                            Skeleton(cls="h-4 w-5/6 mb-3"),
                            Skeleton(cls="h-4 w-4/5 mb-4"),
                            Div(
                                Skeleton(cls="h-8 w-20 mr-2"),
                                Skeleton(cls="h-8 w-16"),
                                cls="flex"
                            )
                        )
                    ),
                    ds_show("$loading"),
                    cls="w-80"
                ),
                # Loaded state
                Div(
                    Card(
                        CardHeader(
                            CardTitle("Article Published Successfully"),
                            P("Your article is now live and visible to readers.", cls="text-sm text-muted-foreground")
                        ),
                        CardContent(
                            P("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation.", cls="mb-4"),
                            Div(
                                Button("View Article", variant="default", cls="mr-2"),
                                Button("Share", variant="outline"),
                                cls="flex"
                            )
                        )
                    ),
                    ds_show("!$loading"),
                    cls="w-80"
                )
            ),
            ds_signals(loading=False),
            cls="space-y-4"
        ),
        '''Button(
    "Load Content",
    ds_on_click="$loading = true; setTimeout(() => $loading = false, 3000)"
)

# Loading state with skeletons
Div(
    Card(
        CardHeader(
            Skeleton(cls="h-6 w-48"),
            Skeleton(cls="h-4 w-32")
        ),
        CardContent(
            Skeleton(cls="h-4 w-full"),
            Skeleton(cls="h-4 w-5/6"),
            Skeleton(cls="h-4 w-4/5"),
            Div(
                Skeleton(cls="h-8 w-20"),
                Skeleton(cls="h-8 w-16"),
                cls="flex gap-2"
            )
        )
    ),
    ds_show("$loading")
)

# Actual content when loaded
Div(
    Card(
        CardHeader(
            CardTitle("Article Published Successfully"),
            P("Your article is now live...", cls="text-sm text-muted-foreground")
        ),
        CardContent(
            P("Lorem ipsum dolor sit amet..."),
            Div(
                Button("View Article"),
                Button("Share", variant="outline"),
                cls="flex gap-2"
            )
        )
    ),
    ds_show("!$loading")
)''',
        title="Loading States",
        description="Interactive demo showing skeleton to content transition"
    )
    
    # List skeleton with varying sizes
    yield ComponentPreview(
        Div(
            H4("Contact List", cls="mb-4"),
            Div(
                *[
                    Div(
                        Skeleton(cls="h-10 w-10 rounded-full"),
                        Div(
                            Skeleton(cls=f"h-4 w-{width} mb-1"),
                            Skeleton(cls=f"h-3 w-{sub_width}"),
                            cls="flex-1 ml-3"
                        ),
                        Skeleton(cls="h-6 w-6 rounded"),
                        cls="flex items-center space-x-3 p-3"
                    )
                    for width, sub_width in [("32", "20"), ("28", "24"), ("36", "16"), ("24", "28")]
                ],
                cls="space-y-1 border rounded-lg"
            ),
            cls="w-full max-w-sm"
        ),
        '''Div(
    H4("Contact List"),
    Div(
        *[
            Div(
                Skeleton(cls="h-10 w-10 rounded-full"),
                Div(
                    Skeleton(cls="h-4 w-32"),
                    Skeleton(cls="h-3 w-20"),
                    cls="flex-1 ml-3"
                ),
                Skeleton(cls="h-6 w-6 rounded"),
                cls="flex items-center space-x-3 p-3"
            )
            for _ in range(4)
        ],
        cls="space-y-1 border rounded-lg"
    )
)''',
        title="List Items",
        description="Skeleton pattern for contact or user lists with varying content lengths"
    )
    
    # Dashboard skeleton layout
    yield ComponentPreview(
        Div(
            Div(
                Skeleton(cls="h-8 w-48 mb-6"),
                cls="mb-6"
            ),
            Div(
                *[
                    Card(
                        CardContent(
                            Skeleton(cls="h-4 w-24 mb-2"),
                            Skeleton(cls="h-8 w-16 mb-3"),
                            Skeleton(cls="h-3 w-20"),
                            cls="p-6"
                        )
                    )
                    for _ in range(4)
                ],
                cls="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6"
            ),
            Card(
                CardHeader(
                    Skeleton(cls="h-6 w-40 mb-2"),
                    Skeleton(cls="h-4 w-64")
                ),
                CardContent(
                    Skeleton(cls="h-48 w-full rounded")
                )
            ),
            cls="w-full max-w-4xl"
        ),
        '''# Dashboard title
Skeleton(cls="h-8 w-48")

# Stats cards
Div(
    *[
        Card(
            CardContent(
                Skeleton(cls="h-4 w-24"),  # Label
                Skeleton(cls="h-8 w-16"),  # Value
                Skeleton(cls="h-3 w-20"), # Subtitle
                cls="p-6"
            )
        )
        for _ in range(4)
    ],
    cls="grid grid-cols-4 gap-4"
)

# Main chart area
Card(
    CardHeader(
        Skeleton(cls="h-6 w-40"),
        Skeleton(cls="h-4 w-64")
    ),
    CardContent(
        Skeleton(cls="h-48 w-full rounded")
    )
)''',
        title="Dashboard Layout",
        description="Complete dashboard skeleton with stats cards and chart area"
    )


def create_skeleton_docs():
    """Create skeleton documentation page using convention-based approach."""
    from utils import auto_generate_page
    
    api_reference = {
        "props": [
            {
                "name": "cls",
                "type": "str",
                "default": "''",
                "description": "Additional CSS classes for custom sizing and spacing"
            },
            {
                "name": "class_name",
                "type": "str", 
                "default": "''",
                "description": "Additional CSS classes (alternative to cls)"
            }
        ]
    }
    
    # Hero example
    hero_example = ComponentPreview(
        Div(
            Div(
                Skeleton(cls="h-4 w-full mb-2"),
                Skeleton(cls="h-4 w-4/5 mb-2"),
                Skeleton(cls="h-4 w-3/4"),
                cls="mb-4"
            ),
            Div(
                Skeleton(cls="h-12 w-12 rounded-full mr-4"),
                Div(
                    Skeleton(cls="h-4 w-32 mb-2"),
                    Skeleton(cls="h-3 w-24")
                ),
                cls="flex items-center"
            ),
            cls="space-y-4 max-w-sm"
        ),
        '''# Text content skeleton
Skeleton(cls="h-4 w-full")
Skeleton(cls="h-4 w-4/5") 
Skeleton(cls="h-4 w-3/4")

# User profile skeleton
Div(
    Skeleton(cls="h-12 w-12 rounded-full"),
    Div(
        Skeleton(cls="h-4 w-32"),
        Skeleton(cls="h-3 w-24")
    ),
    cls="flex items-center space-x-4"
)''',
        copy_button=True
    )
    
    return auto_generate_page(
        TITLE,
        DESCRIPTION,
        list(examples()),
        cli_command="star add skeleton", 
        api_reference=api_reference,
        hero_example=hero_example,
        component_slug="skeleton"
    )