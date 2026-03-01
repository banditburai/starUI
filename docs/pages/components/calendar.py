TITLE = "Calendar"
DESCRIPTION = "A calendar component with single, range, and multiple selection modes."
CATEGORY = "ui"
ORDER = 25
STATUS = "stable"

from starhtml import Div, P, Signal, Span, js
from starui.registry.components.calendar import Calendar
from utils import auto_generate_page, Prop, build_api_reference, with_code


@with_code
def hero_calendar_example():
    cal_single = Calendar(mode="single")
    cal_range = Calendar(mode="range")
    cal_multiple = Calendar(mode="multiple")
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
            cls="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl mx-auto"
        ),
        cls="w-full"
    )


@with_code
def date_range_readout_example():
    cal = Calendar(mode="range")
    return Div(
        cal,
        Div(
            P(
                "Range: ",
                Span(data_text=cal.selected.join(' to ').or_("Select a range"), cls="font-mono text-xs"),
            ),
            cls="mt-4 text-sm"
        ),
        cls="flex flex-col items-center"
    )


@with_code
def on_select_callback_example():
    last_picked = Signal("cal_last_picked", "")
    cal = Calendar(
        mode="single",
        on_select=last_picked.set(js("d")),
    )
    return Div(
        cal,
        Div(
            P(
                "Last picked: ",
                Span(data_text=last_picked.or_("nothing yet"), cls="font-mono text-xs"),
            ),
            cls="mt-4 text-sm"
        ),
        cls="flex flex-col items-center"
    )


@with_code
def calendar_signals_example():
    cal = Calendar(signal="demo", mode="single")
    return Div(
        cal,
        Div(
            P("Month display: ", Span(data_text=cal.month_display, cls="font-mono text-xs")),
            P("Month: ", Span(data_text=cal.month, cls="font-mono text-xs")),
            P("Year: ", Span(data_text=cal.year, cls="font-mono text-xs")),
            P("Selected: ", Span(data_text=cal.selected.or_("none"), cls="font-mono text-xs")),
            cls="mt-4 text-sm space-y-1"
        ),
        cls="flex flex-col items-center"
    )


@with_code
def disabled_calendar_example():
    return Div(
        Calendar(disabled=True, month=3, year=2025),
        cls="flex flex-col items-center"
    )


API_REFERENCE = build_api_reference(
    main_props=[
        Prop("mode", "Literal['single', 'range', 'multiple']",
             "Selection mode for the calendar", "'single'"),
        Prop("caption_layout", "Literal['label', 'dropdown']",
             "Navigation caption style — simple label or month/year dropdowns", "'label'"),
        Prop("selected", "str | list[str] | None",
             "Initially selected date(s)", "None"),
        Prop("month", "int | None",
             "Starting month (1-12)", "None (current month)"),
        Prop("year", "int | None",
             "Starting year", "None (current year)"),
        Prop("disabled", "bool",
             "Whether the calendar is disabled", "False"),
        Prop("on_select", "str | list | None",
             "JavaScript expression(s) executed after a date is selected. In the handler, `d` is the selected date string.", "None"),
        Prop("signal", "str | Signal",
             "Custom signal prefix for the calendar", "''"),
        Prop("cls", "str",
             "Additional CSS classes", "''"),
    ]
)


EXAMPLES_DATA = [
    {"title": "Selection Modes", "description": "Single, range, and multiple date selection modes side by side", "fn": hero_calendar_example},
    {"title": "Date Range with Readout", "description": "Range mode with a reactive display of the selected dates", "fn": date_range_readout_example},
    {"title": "on_select Callback", "description": "Sync a separate signal when a date is picked using on_select", "fn": on_select_callback_example},
    {"title": "CalendarElement Signals", "description": "Access .month_display, .month, .year, and .selected from the returned CalendarElement", "fn": calendar_signals_example},
    {"title": "Disabled", "description": "A fully disabled calendar with no interaction", "fn": disabled_calendar_example},
]


def create_calendar_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)
