"""
Calendar component documentation - Date picker with range and multiple selection support.
"""

from starhtml import Div, P, Span
from starhtml.datastar import ds_signals, ds_text, value
from starui.registry.components.calendar import Calendar
from utils import auto_generate_page
from widgets.component_preview import ComponentPreview

# Component metadata for auto-discovery
TITLE = "Calendar"
DESCRIPTION = "A date picker component with range and multiple selection support."
CATEGORY = "ui"
ORDER = 25
STATUS = "stable"


def examples():
    """Generate calendar examples using ComponentPreview with tabs."""

    # Date range selection
    yield ComponentPreview(
        Div(
            Calendar(
                signal="demo_range",
                mode="range",
                selected=["2025-09-15", "2025-09-25"],
                month=9,
                year=2025,
            ),
            Div(
                P(
                    "Range: ",
                    Span(
                        ds_text("JSON.stringify($demo_range_selected)"),
                        cls="font-mono text-xs",
                    ),
                ),
                cls="mt-4 text-sm",
            ),
            ds_signals(demo_range_selected=value(["2025-09-15", "2025-09-25"])),
            cls="flex flex-col items-center",
        ),
        """from starui.registry.components.calendar import Calendar

Calendar(
    signal="demo_range",
    mode="range",
    selected=["2025-09-15", "2025-09-25"],
    month=9,
    year=2025
)""",
        title="Date Range Selection",
        description="Select a start and end date for booking or filtering",
    )

    # Multiple date selection - with correct month
    yield ComponentPreview(
        Div(
            Calendar(
                signal="demo_multiple",
                mode="multiple",
                selected=["2025-09-10", "2025-09-15", "2025-09-20"],
                month=9,
                year=2025,
            ),
            Div(
                P(
                    "Selected: ",
                    Span(
                        ds_text("($demo_multiple_selected || []).length"),
                        cls="font-mono",
                    ),
                    " dates",
                ),
                cls="mt-4 text-sm",
            ),
            ds_signals(
                demo_multiple_selected=value(["2025-09-10", "2025-09-15", "2025-09-20"])
            ),
            cls="flex flex-col items-center",
        ),
        """from starui.registry.components.calendar import Calendar

Calendar(
    signal="demo_multiple",
    mode="multiple",
    selected=["2025-09-10", "2025-09-15", "2025-09-20"],
    month=9,
    year=2025
)""",
        title="Multiple Date Selection",
        description="Select multiple individual dates for scheduling or events",
    )


def create_calendar_docs():
    """Create calendar documentation page using convention-based approach."""

    # Hero example - single date picker
    hero_example = ComponentPreview(
        Div(
            # All three modes showcased
            Div(
                Div(
                    P("Single", cls="text-sm font-medium mb-2"),
                    Calendar(
                        signal="hero_single",
                        mode="single",
                    ),
                    cls="flex flex-col items-center",
                ),
                Div(
                    P("Range", cls="text-sm font-medium mb-2"),
                    Calendar(
                        signal="hero_range",
                        mode="range",
                        selected=["2025-09-10", "2025-09-20"],
                        month=9,
                        year=2025,
                    ),
                    cls="flex flex-col items-center",
                ),
                Div(
                    P("Multiple", cls="text-sm font-medium mb-2"),
                    Calendar(
                        signal="hero_multiple",
                        mode="multiple",
                        selected=["2025-09-05", "2025-09-15", "2025-09-25"],
                        month=9,
                        year=2025,
                    ),
                    cls="flex flex-col items-center",
                ),
                cls="grid grid-cols-1 md:grid-cols-3 gap-8",
            ),
            cls="w-full",
        ),
        """from starui.registry.components.calendar import Calendar

# Single date selection
Calendar(
    signal="date_picker",
    mode="single"
)

# Date range selection  
Calendar(
    signal="date_range",
    mode="range",
    selected=["2025-09-10", "2025-09-20"]
)

# Multiple dates
Calendar(
    signal="multi_dates",
    mode="multiple",
    selected=["2025-09-05", "2025-09-15", "2025-09-25"]
)""",
        title="",
        description="",
    )

    return auto_generate_page(
        TITLE,
        DESCRIPTION,
        list(examples()),
        cli_command="star add calendar",
        component_slug="calendar",
        hero_example=hero_example,
        api_reference={
            "props": [
                {
                    "name": "mode",
                    "type": "Literal['single', 'range', 'multiple']",
                    "default": "'single'",
                    "description": "Selection mode for the calendar",
                },
                {
                    "name": "selected",
                    "type": "str | list[str] | None",
                    "default": "None",
                    "description": "Initially selected date(s)",
                },
                {
                    "name": "month",
                    "type": "int | None",
                    "default": "None",
                    "description": "Starting month (1-12)",
                },
                {
                    "name": "year",
                    "type": "int | None",
                    "default": "None",
                    "description": "Starting year",
                },
                {
                    "name": "disabled",
                    "type": "bool",
                    "default": "False",
                    "description": "Whether calendar is disabled",
                },
                {
                    "name": "signal",
                    "type": "str | None",
                    "default": "None",
                    "description": "Custom signal prefix for the calendar",
                },
                {
                    "name": "cls",
                    "type": "str",
                    "default": "''",
                    "description": "Additional CSS classes",
                },
            ]
        },
    )
