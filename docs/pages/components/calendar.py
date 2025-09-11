"""
Calendar component documentation - Date picker with range and multiple selection support.
"""

from starhtml import Div, P, Span
from starhtml.datastar import ds_signals, ds_text, value
from starui.registry.components.calendar import Calendar
from utils import auto_generate_page, Prop, build_api_reference, with_code
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
    @with_code
    def date_range_selection_example():
        return Div(
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
            ds_signals(demo_range_selected=value('["2025-09-15", "2025-09-25"]')),
            cls="flex flex-col items-center",
        )
    
    yield ComponentPreview(
        date_range_selection_example(),
        date_range_selection_example.code,
        title="Date Range Selection",
        description="Select a start and end date for booking or filtering",
    )

    # Multiple date selection - with correct month
    @with_code
    def multiple_date_selection_example():
        return Div(
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
                        ds_text("(JSON.parse($demo_multiple_selected || '[]')).length"),
                        cls="font-mono",
                    ),
                    " dates",
                ),
                cls="mt-4 text-sm",
            ),
            ds_signals(
                demo_multiple_selected=value('["2025-09-10", "2025-09-15", "2025-09-20"]')
            ),
            cls="flex flex-col items-center",
        )
    
    yield ComponentPreview(
        multiple_date_selection_example(),
        multiple_date_selection_example.code,
        title="Multiple Date Selection",
        description="Select multiple individual dates for scheduling or events",
    )


def create_calendar_docs():
    """Create calendar documentation page using convention-based approach."""

    # Hero example - single date picker
    @with_code
    def hero_calendar_example():
        return Div(
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
                cls="grid grid-cols-1 lg:grid-cols-2 gap-8 max-w-4xl mx-auto",
            ),
            ds_signals(
                hero_single_selected=value(""),
                hero_range_selected=value('["2025-09-10", "2025-09-20"]'),
                hero_multiple_selected=value('["2025-09-05", "2025-09-15", "2025-09-25"]')
            ),
            cls="w-full",
        )
    
    hero_example = ComponentPreview(
        hero_calendar_example(),
        hero_calendar_example.code,
        copy_button=True
    )

    return auto_generate_page(
        TITLE,
        DESCRIPTION,
        list(examples()),
        cli_command="star add calendar",
        component_slug="calendar",
        hero_example=hero_example,
        api_reference=build_api_reference(
            main_props=[
                Prop("mode", "Literal['single', 'range', 'multiple']", 
                     "Selection mode for the calendar", "'single'"),
                Prop("selected", "str | list[str] | None", 
                     "Initially selected date(s)", "None"),
                Prop("month", "int | None", 
                     "Starting month (1-12)", "None"),
                Prop("year", "int | None", 
                     "Starting year", "None"),
                Prop("disabled", "bool", 
                     "Whether calendar is disabled", "False"),
                Prop("signal", "str | None", 
                     "Custom signal prefix for the calendar", "None"),
                Prop("cls", "str", 
                     "Additional CSS classes", "''"),
            ]
        ),
    )
