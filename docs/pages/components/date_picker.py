"""
Date Picker component documentation — Calendar-based date selection with popover.
"""

from starhtml import Div, P, Span, Label, Signal, js
from starui.registry.components.date_picker import DatePicker, DateTimePicker, DatePickerWithInput
from starui.registry.components.card import Card, CardHeader, CardContent, CardTitle, CardDescription
from starui.registry.components.input import Input
from utils import auto_generate_page, with_code, Prop, Component, build_api_reference

# Component metadata for auto-discovery
TITLE = "Date Picker"
DESCRIPTION = "A date picker component with popover calendar for selecting dates."
CATEGORY = "ui"
ORDER = 26
STATUS = "stable"


@with_code
def hero_date_picker_example():
    return Div(
        Div(
            Div(
                P("Date", cls="text-sm font-medium mb-2"),
                DatePicker(signal="hero_dp", placeholder="Pick a date"),
                cls="flex flex-col items-center",
            ),
            Div(
                P("Date & Time", cls="text-sm font-medium mb-2"),
                DateTimePicker(signal="hero_dtp", placeholder="Pick date & time"),
                cls="flex flex-col items-center",
            ),
            Div(
                P("With Input", cls="text-sm font-medium mb-2"),
                DatePickerWithInput(signal="hero_dpi"),
                cls="flex flex-col items-center",
            ),
            cls="grid grid-cols-1 md:grid-cols-3 gap-8",
        ),
        cls="w-full max-w-4xl mx-auto",
    )


@with_code
def trip_planner_example():
    range_picker = DatePicker(
        mode="range",
        signal="trip_dates",
        placeholder="Check-in — Check-out",
    )
    departure = DatePicker(
        with_presets=True,
        signal="departure",
        placeholder="Departure date",
    )

    nights_text = js(
        f"(()=>{{const a={range_picker.selected}||[];"
        f"if(a.length!==2)return'';"
        f"const[y1,m1,d1]=a[0].split('-').map(Number);"
        f"const[y2,m2,d2]=a[1].split('-').map(Number);"
        f"const n=Math.round((new Date(y2,m2-1,d2)-new Date(y1,m1-1,d1))/864e5);"
        f"return n+' night'+(n!==1?'s':'')}})()"
    )

    return Card(
        CardHeader(
            CardTitle("Plan Your Trip"),
            CardDescription("Select your travel dates and departure"),
        ),
        CardContent(
            Div(
                Div(
                    Label("Check-in / Check-out", cls="text-sm font-medium"),
                    range_picker,
                    P(
                        Span(data_text=nights_text, cls="font-medium"),
                        cls="text-sm text-muted-foreground mt-1",
                        data_show=range_picker.selected.or_([]).length == 2,
                    ),
                    cls="space-y-1.5",
                ),
                Div(
                    Label("Departure date", cls="text-sm font-medium"),
                    departure,
                    cls="space-y-1.5",
                ),
                cls="space-y-4",
            ),
        ),
        cls="max-w-md",
    )


@with_code
def meeting_scheduler_example():
    title_sig = Signal("meeting_title", "")
    picker = DateTimePicker(signal="meeting", placeholder="Pick date and time")

    readout = js(
        f"(()=>{{const d={picker.date},t={picker.time},n={title_sig};"
        f"if(!d)return'';"
        f"const[y,m,dy]=d.split('-').map(Number);"
        f"let r=new Date(y,m-1,dy).toLocaleDateString('en-US',{{year:'numeric',month:'long',day:'numeric'}});"
        f"if(t)r+=' at '+t;"
        f"return(n?n+' on ':'')+r}})()"
    )

    return Card(
        CardHeader(
            CardTitle("Schedule a Meeting"),
            CardDescription("Pick a date, time, and add a title"),
        ),
        CardContent(
            Div(
                title_sig,
                Div(
                    Label("Meeting title", cls="text-sm font-medium"),
                    Input(placeholder="Weekly standup", signal=title_sig),
                    cls="space-y-1.5",
                ),
                Div(
                    Label("Date & time", cls="text-sm font-medium"),
                    picker,
                    cls="space-y-1.5",
                ),
                P(
                    Span(data_text=readout),
                    cls="text-sm text-muted-foreground mt-2",
                    data_show=picker.date,
                ),
                cls="space-y-4",
            ),
        ),
        cls="max-w-md",
    )


@with_code
def dob_example():
    picker = DatePicker(
        signal="dob",
        caption_layout="dropdown",
        placeholder="Date of birth",
    )
    return Div(
        Label("Date of birth", cls="text-sm font-medium"),
        picker,
        P(
            Span(data_text=picker.selected.or_("Not set"), cls="font-mono text-xs"),
            cls="text-sm text-muted-foreground mt-1",
        ),
        cls="grid w-full max-w-sm gap-1.5",
    )


@with_code
def states_example():
    return Div(
        Div(
            P("Disabled", cls="text-sm font-medium mb-2"),
            DatePicker(signal="disabled_dp", disabled=True, placeholder="Not available"),
            cls="flex flex-col",
        ),
        Div(
            P("Custom width", cls="text-sm font-medium mb-2"),
            DatePicker(signal="wide_dp", width="w-[360px]", placeholder="Full-width picker"),
            cls="flex flex-col",
        ),
        cls="grid grid-cols-1 sm:grid-cols-2 gap-6 max-w-3xl",
    )


EXAMPLES_DATA = [
    {
        "title": "Three Picker Variants",
        "description": "The full surface area: DatePicker for calendar selection, DateTimePicker for date + time, and DatePickerWithInput for typed entry with a calendar fallback.",
        "fn": hero_date_picker_example,
    },
    {
        "title": "Trip Planner",
        "description": "A booking scenario with a range picker for check-in/check-out dates and a presets picker for quick departure selection. The computed nights readout updates reactively.",
        "fn": trip_planner_example,
    },
    {
        "title": "Schedule a Meeting",
        "description": "DateTimePicker composed with an Input for meeting title. The readout combines both signals into a formatted summary.",
        "fn": meeting_scheduler_example,
    },
    {
        "title": "Date of Birth",
        "description": "A profile form pattern using caption_layout='dropdown' for quick month/year navigation — ideal for dates far from today.",
        "fn": dob_example,
    },
    {
        "title": "States",
        "description": "Disabled and custom-width variants.",
        "fn": states_example,
    },
]

API_REFERENCE = build_api_reference(
    main_props=[
        Prop("mode", "Literal['single', 'range', 'multiple']", "Selection mode for the date picker", "'single'"),
        Prop("caption_layout", "Literal['label', 'dropdown']", "Calendar header style — 'label' shows text, 'dropdown' shows month/year selects", "'label'"),
        Prop("selected", "str | list[str] | None", "Initially selected date(s)", "None"),
        Prop("placeholder", "str", "Placeholder text when no date is selected", "'Pick a date'"),
        Prop("disabled", "bool", "Whether the date picker is disabled", "False"),
        Prop("signal", "str | Signal", "Custom signal prefix for the date picker", "''"),
        Prop("width", "str", "Tailwind width class for the trigger button", "'w-[280px]'"),
        Prop("with_presets", "bool", "Show preset date options (Today, Tomorrow, In a week) — single mode only", "False"),
        Prop("cls", "str", "Additional CSS classes", "''"),
    ],
    components=[
        Component("DateTimePicker", "Date + time picker with hour/minute dropdowns and AM/PM toggle. Exposes .datetime, .date, and .time signals."),
        Component("DatePickerWithInput", "Text input with calendar popover fallback. Accepts typed dates in YYYY-MM-DD format. Exposes .selected signal."),
    ],
)


def create_date_picker_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)
