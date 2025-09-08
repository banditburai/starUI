"""
Date Picker component documentation - Calendar date selection with popover.
"""

from starhtml import Div, P, Span
from starhtml.datastar import ds_signals, ds_text, value
from starui.registry.components.date_picker import (
    DatePicker,
    DatePickerWithPresets,
    DateRangePicker,
)
from utils import auto_generate_page
from widgets.component_preview import ComponentPreview

# Component metadata for auto-discovery
TITLE = "Date Picker"
DESCRIPTION = "A date picker component with popover calendar for selecting dates."
CATEGORY = "ui"
ORDER = 26
STATUS = "stable"


def examples():
    """Generate date picker examples using ComponentPreview with tabs."""

    # Date picker with presets
    yield ComponentPreview(
        Div(
            Div(
                P(
                    "Selected: ",
                    Span(
                        ds_text("$demo_presets_selected || 'None'"),
                        cls="font-mono text-xs",
                    ),
                ),
                cls="mb-4 text-sm",
            ),
            DatePickerWithPresets(
                signal="demo_presets",
                placeholder="Select a date",
            ),
            ds_signals(demo_presets_selected=value("")),
            cls="flex flex-col items-center",
        ),
        """from starui.registry.components.date_picker import DatePickerWithPresets

DatePickerWithPresets(
    signal="demo_presets",
    placeholder="Select a date"
)""",
        title="Date Picker with Presets",
        description="Quick date selection with predefined options",
    )

    # Date range picker
    yield ComponentPreview(
        Div(
            Div(
                P(
                    "Range: ",
                    Span(
                        ds_text(
                            "!$demo_range_selected || $demo_range_selected === '[]' ? 'None' : $demo_range_selected"
                        ),
                        cls="font-mono text-xs",
                    ),
                ),
                cls="mb-4 text-sm",
            ),
            DateRangePicker(
                signal="demo_range",
                placeholder="Select date range",
            ),
            ds_signals(demo_range_selected=value("[]")),
            cls="flex flex-col items-center",
        ),
        """from starui.registry.components.date_picker import DateRangePicker

DateRangePicker(
    signal="demo_range",
    placeholder="Select date range"
)""",
        title="Date Range Picker",
        description="Select a start and end date for filtering or booking",
    )

    # Multiple date selection
    yield ComponentPreview(
        Div(
            Div(
                P(
                    "Selected: ",
                    Span(
                        ds_text("(JSON.parse($demo_multiple_selected || '[]')).length"),
                        cls="font-mono",
                    ),
                    " dates",
                ),
                P(
                    Span(
                        ds_text(
                            "!$demo_multiple_selected || $demo_multiple_selected === '[]' ? '' : $demo_multiple_selected"
                        ),
                        cls="text-xs text-muted-foreground font-mono",
                    ),
                ),
                cls="mb-4 text-sm",
            ),
            DatePicker(
                signal="demo_multiple",
                mode="multiple",
                placeholder="Select dates",
            ),
            ds_signals(demo_multiple_selected=value("[]")),
            cls="flex flex-col items-center",
        ),
        """from starui.registry.components.date_picker import DatePicker

DatePicker(
    signal="demo_multiple",
    mode="multiple",
    placeholder="Select dates"
)""",
        title="Multiple Date Selection",
        description="Select multiple dates for scheduling or events",
    )


def create_date_picker_docs():
    """Create date picker documentation page using convention-based approach."""

    # Hero example - single date picker
    hero_example = ComponentPreview(
        Div(
            # All three main variations
            Div(
                Div(
                    P("Single Date", cls="text-sm font-medium mb-2"),
                    DatePicker(
                        signal="hero_single",
                        mode="single",
                        placeholder="Pick a date",
                    ),
                    cls="flex flex-col items-center",
                ),
                Div(
                    P("Date Range", cls="text-sm font-medium mb-2"),
                    DateRangePicker(
                        signal="hero_range",
                        placeholder="Pick a date range",
                    ),
                    cls="flex flex-col items-center",
                ),
                Div(
                    P("With Presets", cls="text-sm font-medium mb-2"),
                    DatePickerWithPresets(
                        signal="hero_presets",
                        placeholder="Pick a date",
                    ),
                    cls="flex flex-col items-center",
                ),
                cls="grid grid-cols-1 lg:grid-cols-2 gap-8 max-w-4xl mx-auto",
            ),
            cls="w-full",
        ),
        """from starui.registry.components.date_picker import (
    DatePicker,
    DatePickerWithPresets,
    DateRangePicker
)

# Single date selection
DatePicker(
    signal="date_picker",
    mode="single",
    placeholder="Pick a date"
)

# Date range selection  
DateRangePicker(
    signal="date_range",
    placeholder="Pick a date range"
)

# With preset options
DatePickerWithPresets(
    signal="date_presets",
    placeholder="Pick a date"
)""",
        title="",
        description="",
    )

    return auto_generate_page(
        TITLE,
        DESCRIPTION,
        list(examples()),
        cli_command="star add date_picker",
        component_slug="date_picker",
        hero_example=hero_example,
        api_reference={
            "props": [
                {
                    "name": "mode",
                    "type": "Literal['single', 'range', 'multiple']",
                    "default": "'single'",
                    "description": "Selection mode for the date picker",
                },
                {
                    "name": "selected",
                    "type": "str | list[str] | None",
                    "default": "None",
                    "description": "Initially selected date(s)",
                },
                {
                    "name": "placeholder",
                    "type": "str",
                    "default": "'Pick a date'",
                    "description": "Placeholder text when no date is selected",
                },
                {
                    "name": "disabled",
                    "type": "bool",
                    "default": "False",
                    "description": "Whether the date picker is disabled",
                },
                {
                    "name": "signal",
                    "type": "str | None",
                    "default": "None",
                    "description": "Custom signal prefix for the date picker",
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
