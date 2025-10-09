"""
Date Picker component documentation - Calendar date selection with popover.
"""

from starhtml import Div, P, Span, js
from starui.registry.components.date_picker import DatePicker
from utils import auto_generate_page, with_code, Prop, Component, build_api_reference
from widgets.component_preview import ComponentPreview

# Component metadata for auto-discovery
TITLE = "Date Picker"
DESCRIPTION = "A date picker component with popover calendar for selecting dates."
CATEGORY = "ui"
ORDER = 26
STATUS = "stable"


# ============================================================================
# EXAMPLE FUNCTIONS (decorated with @with_code for markdown generation)
# ============================================================================

@with_code
def date_picker_with_presets_example():
    picker = DatePicker(
        signal="demo_presets",
        placeholder="Select a date",
        with_presets=True,
    )
    return Div(
        picker.selected,
        Div(
            P(
                "Selected: ",
                Span(
                    data_text=picker.selected.or_("None"),
                    cls="font-mono text-xs",
                ),
            ),
            cls="mb-4 text-sm",
        ),
        picker,
        cls="flex flex-col items-center",
    )


@with_code
def date_range_picker_example():
    picker = DatePicker(
        signal="demo_range",
        mode="range",
        placeholder="Select date range",
    )
    return Div(
        picker.selected,
        Div(
            P(
                "Range: ",
                Span(
                    data_text=picker.selected.join(' - ').or_("None"),
                    cls="font-mono text-xs",
                ),
            ),
            cls="mb-4 text-sm",
        ),
        picker,
        cls="flex flex-col items-center",
    )


@with_code
def multiple_date_selection_example():
    picker = DatePicker(
        signal="demo_multiple",
        mode="multiple",
        placeholder="Select dates",
    )
    return Div(
        picker.selected,
        Div(
            P(
                "Selected: ",
                Span(
                    data_text=picker.selected.or_([]).length,
                    cls="font-mono",
                ),
                " dates",
            ),
            P(
                Span(
                    data_text=picker.selected.join(' | ').or_("None"),
                    cls="text-xs text-muted-foreground font-mono",
                ),
            ),
            cls="mb-4 text-sm",
        ),
        picker,
        cls="flex flex-col items-center",
    )


def examples():
    """Generate date picker examples."""
    yield ComponentPreview(
        date_picker_with_presets_example(),
        date_picker_with_presets_example.code,
        title="Date Picker with Presets",
        description="Quick date selection with predefined options",
    )

    yield ComponentPreview(
        date_range_picker_example(),
        date_range_picker_example.code,
        title="Date Range Picker",
        description="Select a start and end date for filtering or booking",
    )

    yield ComponentPreview(
        multiple_date_selection_example(),
        multiple_date_selection_example.code,
        title="Multiple Date Selection",
        description="Select multiple dates for scheduling or events",
    )


# ============================================================================
# HERO EXAMPLE (moved to module level)
# ============================================================================

@with_code
def hero_date_picker_example():
    return Div(
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
                DatePicker(
                    signal="hero_range",
                    mode="range",
                    placeholder="Pick a date range",
                ),
                cls="flex flex-col items-center",
            ),
            Div(
                P("With Presets", cls="text-sm font-medium mb-2"),
                DatePicker(
                    signal="hero_presets",
                    placeholder="Pick a date",
                    with_presets=True,
                ),
                cls="flex flex-col items-center",
            ),
            cls="grid grid-cols-1 lg:grid-cols-2 gap-8 max-w-4xl mx-auto",
        ),
        cls="w-full",
    )


# ============================================================================
# MODULE-LEVEL DATA (for markdown API)
# ============================================================================

EXAMPLES_DATA = [
    {"title": "Date Picker with Presets", "description": "Quick date selection with predefined options", "code": date_picker_with_presets_example.code},
    {"title": "Date Range Picker", "description": "Select a start and end date for filtering or booking", "code": date_range_picker_example.code},
    {"title": "Multiple Date Selection", "description": "Select multiple dates for scheduling or events", "code": multiple_date_selection_example.code},
]

API_REFERENCE = build_api_reference(
    main_props=[
        Prop("mode", "Literal['single', 'range', 'multiple']", "Selection mode for the date picker", "'single'"),
        Prop("selected", "str | list[str] | None", "Initially selected date(s)", "None"),
        Prop("placeholder", "str", "Placeholder text when no date is selected", "'Pick a date'"),
        Prop("disabled", "bool", "Whether the date picker is disabled", "False"),
        Prop("signal", "str | Signal", "Custom signal prefix for the date picker", "''"),
        Prop("with_presets", "bool", "Show preset date options (Today, Tomorrow, In a week)", "False"),
        Prop("cls", "str", "Additional CSS classes", "''"),
    ]
)


def create_date_picker_docs():
    hero_example = ComponentPreview(
        hero_date_picker_example(),
        hero_date_picker_example.code,
        copy_button=True
    )

    return auto_generate_page(
        TITLE,
        DESCRIPTION,
        list(examples()),
        cli_command="star add date-picker",
        component_slug="date-picker",
        hero_example=hero_example,
        api_reference=API_REFERENCE,
    )
