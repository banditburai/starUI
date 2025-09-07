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
from starhtml.datastar import ds_signals, ds_show, ds_on_click, ds_text, value
from starui.registry.components.skeleton import Skeleton
from starui.registry.components.button import Button
from starui.registry.components.card import Card, CardContent, CardHeader, CardTitle
from utils import auto_generate_page
from widgets.component_preview import ComponentPreview


def examples():
    """Generate skeleton examples using ComponentPreview with tabs."""
    
    # Basic skeleton shapes with proper circles
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
                H4("Shapes", cls="mb-3 text-sm font-medium"),
                Div(
                    # Perfect circles - Skeleton component now handles rounded-full properly
                    Skeleton(cls="h-8 w-8 rounded-full mr-4"),
                    Skeleton(cls="h-10 w-10 rounded-full mr-4"),  
                    Skeleton(cls="h-12 w-12 rounded-full mr-4"),
                    Skeleton(cls="h-16 w-16 rounded-full mr-4"),
                    # Rectangle with default rounded-md
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
        ),
        '''# Text lines
Skeleton(cls="h-4 w-3/4")
Skeleton(cls="h-4 w-full") 
Skeleton(cls="h-4 w-5/6")

# Perfect circles - Skeleton detects rounded-full and skips default rounded-md
Skeleton(cls="h-8 w-8 rounded-full")
Skeleton(cls="h-10 w-10 rounded-full")  
Skeleton(cls="h-12 w-12 rounded-full")
Skeleton(cls="h-16 w-16 rounded-full")

# User profile with circular avatar
Div(
    Skeleton(cls="h-14 w-14 rounded-full"),
    Div(
        Skeleton(cls="h-4 w-32"),
        Skeleton(cls="h-3 w-24"),
        cls="ml-4"
    ),
    cls="flex items-center"
)''',
        title="Basic Shapes",
        description="Text lines, perfect circles, and common patterns"
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
    
    # Data table skeleton
    yield ComponentPreview(
        Div(
            # Table header
            Div(
                Div(
                    Skeleton(cls="h-4 w-16"),  # Name
                    Skeleton(cls="h-4 w-20"),  # Email
                    Skeleton(cls="h-4 w-12"),  # Role
                    Skeleton(cls="h-4 w-14"),  # Status
                    cls="grid grid-cols-4 gap-4 py-3 px-4 border-b"
                ),
                cls="bg-muted/50"
            ),
            # Table rows
            Div(
                *[
                    Div(
                        Div(
                            Skeleton(cls="h-8 w-8 rounded-full"),  # Avatar
                            Skeleton(cls="h-4 w-24 ml-2"),         # Name
                            cls="flex items-center"
                        ),
                        Skeleton(cls="h-4 w-32"),                  # Email
                        Skeleton(cls="h-5 w-16 rounded-full"),     # Role badge
                        Skeleton(cls="h-6 w-6 rounded-full"),      # Status dot
                        cls="grid grid-cols-4 gap-4 py-4 px-4 border-b border-border/50"
                    )
                    for _ in range(4)
                ],
            ),
            cls="w-full max-w-3xl border rounded-lg overflow-hidden"
        ),
        '''# Table with header and data rows
Div(
    # Header
    Div(
        Div(
            Skeleton(cls="h-4 w-16"),  # Column headers
            Skeleton(cls="h-4 w-20"),
            Skeleton(cls="h-4 w-12"), 
            Skeleton(cls="h-4 w-14"),
            cls="grid grid-cols-4 gap-4 py-3 px-4"
        ),
        cls="bg-muted/50 border-b"
    ),
    # Data rows
    Div(
        *[
            Div(
                Div(
                    Skeleton(cls="h-8 w-8 rounded-full"),
                    Skeleton(cls="h-4 w-24"),
                    cls="flex items-center gap-2"
                ),
                Skeleton(cls="h-4 w-32"),
                Skeleton(cls="h-5 w-16 rounded-full"),
                Skeleton(cls="h-6 w-6 rounded-full"),
                cls="grid grid-cols-4 gap-4 py-4 px-4 border-b"
            )
            for _ in range(4)
        ]
    ),
    cls="border rounded-lg overflow-hidden"
)''',
        title="Data Table",
        description="Skeleton for user data table with avatars and status indicators"
    )
    
    # Interactive loading demo - exact copy from test sandbox
    yield ComponentPreview(
        Div(
            H4("Loading State Toggle", cls="text-lg font-medium mb-2"),
            Div(
                Button(
                    ds_text("$loading ? 'Stop Loading' : 'Start Loading'"),
                    ds_on_click("$loading = !$loading"),
                    variant="outline",
                    cls="mb-4",
                ),
                Div(
                    Skeleton(cls="h-6 w-40 mb-2"),  # "Content Loaded!" title width
                    Skeleton(cls="h-4 w-80 mb-4"),  # Paragraph text width  
                    Skeleton(cls="h-20 w-full rounded-lg"),  # Content box with rounded corners
                    ds_show("$loading"),
                ),
                Div(
                    H4("Content Loaded!", cls="text-lg font-semibold mb-2"),
                    P("This content appears when loading is complete.", cls="mb-4"),
                    Div(
                        "This is the actual content that would load.",
                        cls="p-4 bg-muted rounded-lg",
                    ),
                    ds_show("!$loading"),
                ),
                ds_signals(loading=True),
                cls="p-4 border rounded-lg",
            ),
            cls="mb-6",
        ),
        '''Button(
    ds_text("$loading ? 'Stop Loading' : 'Start Loading'"),
    ds_on_click="$loading = !$loading",
    variant="outline"
)

# Loading skeletons that match actual content
Div(
    Skeleton(cls="h-6 w-40"),    # Title width
    Skeleton(cls="h-4 w-80"),    # Paragraph width
    Skeleton(cls="h-20 w-full rounded-lg"),  # Content box
    ds_show("$loading")
)

# Loaded content
Div(
    H4("Content Loaded!"),
    P("This content appears when loading is complete."),
    Div(
        "This is the actual content that would load.",
        cls="p-4 bg-muted rounded-lg"
    ),
    ds_show("!$loading")
)

ds_signals(loading=True)''',
        title="Loading States",
        description="Interactive demo showing skeleton to content transition"
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