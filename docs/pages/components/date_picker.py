"""
Date Picker component documentation - Calendar date selection with popover.
"""

from starhtml import Div, P, Span
from starui.registry.components.date_picker import DatePicker
from utils import auto_generate_page, with_code, Prop, Component, build_api_reference
from widgets.component_preview import ComponentPreview

# Component metadata for auto-discovery
TITLE = "Date Picker"
DESCRIPTION = "A date picker component with popover calendar for selecting dates."
CATEGORY = "ui"
ORDER = 26
STATUS = "stable"



@with_code
def hero_date_picker_example():
    pickers = [
        ("Single Date", {"signal": "hero_single", "mode": "single", "placeholder": "Pick a date"}),
        ("Date Range", {"signal": "hero_range", "mode": "range", "placeholder": "Pick a date range"}),
        ("With Presets", {"signal": "hero_presets", "placeholder": "Pick a date", "with_presets": True}),
    ]

    return Div(
        Div(
            *[
                Div(
                    P(label, cls="text-sm font-medium mb-2"),
                    DatePicker(**props),
                    cls="flex flex-col items-center",
                )
                for label, props in pickers
            ],
            cls="grid grid-cols-1 lg:grid-cols-2 gap-8 max-w-4xl mx-auto",
        ),
        cls="w-full",
    )


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



EXAMPLES_DATA = [
    {"title": "Date Picker", "description": "Single, range, and preset date selection modes", "fn": hero_date_picker_example},
    {"title": "Date Picker with Presets", "description": "Quick date selection with predefined options", "fn": date_picker_with_presets_example},
    {"title": "Date Range Picker", "description": "Select a start and end date for filtering or booking", "fn": date_range_picker_example},
    {"title": "Multiple Date Selection", "description": "Select multiple dates for scheduling or events", "fn": multiple_date_selection_example},
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
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)
