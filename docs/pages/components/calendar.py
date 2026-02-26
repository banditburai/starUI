TITLE = "Calendar"
DESCRIPTION = "A date picker component with range and multiple selection support."
CATEGORY = "ui"
ORDER = 25
STATUS = "stable"

from starhtml import Div, P, Span
from starui.registry.components.calendar import Calendar
from utils import auto_generate_page, Prop, build_api_reference, with_code
from widgets.component_preview import ComponentPreview



@with_code
def hero_calendar_example():
    cal_single = Calendar(mode="single")
    cal_range = Calendar(
        mode="range",
        selected=["2025-09-10", "2025-09-20"],
        month=9,
        year=2025
    )
    cal_multiple = Calendar(
        mode="multiple",
        selected=["2025-09-05", "2025-09-15", "2025-09-25"],
        month=9,
        year=2025
    )
    return Div(
        Div(
            Div(
                P("Single", cls="text-sm font-medium mb-2"),
                cal_single,
                cls="flex flex-col items-center"
            ),
            Div(
                P("Range", cls="text-sm font-medium mb-2"),
                cal_range,
                cls="flex flex-col items-center"
            ),
            Div(
                P("Multiple", cls="text-sm font-medium mb-2"),
                cal_multiple,
                cls="flex flex-col items-center"
            ),
            cls="grid grid-cols-1 lg:grid-cols-2 gap-8 max-w-4xl mx-auto"
        ),
        cls="w-full"
    )


@with_code
def date_range_selection_example():
    cal_range = Calendar(
        mode="range",
        selected=["2025-09-15", "2025-09-25"],
        month=9,
        year=2025
    )
    return Div(
        cal_range,
        Div(
            P(
                "Range: ",                
                Span(data_text=cal_range.selected.join(' to ').or_("None"), cls="font-mono text-xs")
            ),
            cls="mt-4 text-sm"
        ),
        cls="flex flex-col items-center"
    )


@with_code
def multiple_date_selection_example():
    cal_multiple = Calendar(
        mode="multiple",
        selected=["2025-09-10", "2025-09-15", "2025-09-20"],
        month=9,
        year=2025
    )
    return Div(
        cal_multiple,
        Div(
            P(
                "Selected: ",
                Span(data_text=cal_multiple.selected.join(" | ").or_("None"), cls="font-mono text-sm")
            ),
            cls="mt-4 text-sm"
        ),
        cls="flex flex-col items-center"
    )



API_REFERENCE = build_api_reference(
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
)



EXAMPLES_DATA = [
    {"title": "Calendar", "description": "Single, range, and multiple date selection modes", "fn": hero_calendar_example},
    {"title": "Date Range Selection", "description": "Select a start and end date for booking or filtering", "fn": date_range_selection_example},
    {"title": "Multiple Date Selection", "description": "Select multiple individual dates for scheduling or events", "fn": multiple_date_selection_example},
]



def create_calendar_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)
