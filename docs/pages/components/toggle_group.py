"""
Toggle Group component documentation - Interactive button groups for selections.
Flexible toggle groups for single or multiple selections.
"""

# Component metadata for auto-discovery
TITLE = "Toggle Group"
DESCRIPTION = "A set of two-state buttons that can be toggled on or off. Supports single and multiple selection modes."
CATEGORY = "ui"
ORDER = 40
STATUS = "stable"

from starhtml import Div, P, H4, Icon, Label, Signal, collect
from starui.registry.components.toggle_group import ToggleGroup
from starui.registry.components.separator import Separator
from utils import auto_generate_page, with_code, Component, Prop, build_api_reference


@with_code
def editor_controls_example():
    alignment = Signal("alignment", _ref_only=True)  #: hide
    decoration = Signal("decoration", _ref_only=True)  #: hide

    return Div(
        alignment, decoration,  #: hide
        P("Text Alignment", cls="font-medium mb-4"),
        ToggleGroup(
            ("left", Icon("lucide:align-left", cls="size-4")),
            ("center", Icon("lucide:align-center", cls="size-4")),
            ("right", Icon("lucide:align-right", cls="size-4")),
            ("justify", Icon("lucide:align-justify", cls="size-4")),
            type="single",
            variant="outline",
            signal=alignment
        ),

        Separator(cls="my-6"),

        P("Text Decoration", cls="font-medium mb-4"),
        ToggleGroup(
            ("bold", Icon("lucide:bold", cls="size-4")),
            ("italic", Icon("lucide:italic", cls="size-4")),
            ("underline", Icon("lucide:underline", cls="size-4")),
            type="multiple",
            signal=decoration
        ),

        Div(
            P(
                "The quick brown fox jumps over the lazy dog.",
                cls="p-4 bg-muted rounded transition-all",
                data_class_text_left=alignment.eq("left") | ~alignment,
                data_class_text_center=alignment.eq("center"),
                data_class_text_right=alignment.eq("right"),
                data_class_text_justify=alignment.eq("justify"),
                data_class_font_bold=decoration.contains("bold"),
                data_class_italic=decoration.contains("italic"),
                data_class_underline=decoration.contains("underline")
            ),
            cls="mt-6"
        ),
        cls="w-full"
    )


@with_code
def view_mode_switcher_example():
    view_mode = Signal("view_mode", _ref_only=True)  #: hide

    return Div(
        view_mode,  #: hide
        P("View Mode", cls="font-medium mb-4"),
        ToggleGroup(
            ("grid", Div(Icon("lucide:grid-3x3", cls="size-4"), "Grid", cls="flex items-center gap-2")),
            ("list", Div(Icon("lucide:list", cls="size-4"), "List", cls="flex items-center gap-2")),
            ("card", Div(Icon("lucide:layout-grid", cls="size-4"), "Card", cls="flex items-center gap-2")),
            type="single",
            signal=view_mode,
            value="grid"
        ),
        Div(
            Div(
                Div("Inception (2010)", cls="p-4 border rounded bg-muted"),
                Div("The Matrix (1999)", cls="p-4 border rounded bg-muted"),
                Div("Interstellar (2014)", cls="p-4 border rounded bg-muted"),
                Div("Blade Runner (1982)", cls="p-4 border rounded bg-muted"),
                cls="grid grid-cols-2 gap-2",
                data_show=view_mode.eq("grid")
            ),
            Div(
                Div("Inception (2010)", cls="p-3 border rounded bg-muted mb-2"),
                Div("The Matrix (1999)", cls="p-3 border rounded bg-muted mb-2"),
                Div("Interstellar (2014)", cls="p-3 border rounded bg-muted mb-2"),
                Div("Blade Runner (1982)", cls="p-3 border rounded bg-muted"),
                data_show=view_mode.eq("list")
            ),
            Div(
                Div(
                    H4("Inception", cls="font-medium"),
                    P("2010 · Sci-Fi · 2h 28m", cls="text-sm text-muted-foreground"),
                    cls="p-4 border rounded bg-muted mb-3"
                ),
                Div(
                    H4("The Matrix", cls="font-medium"),
                    P("1999 · Sci-Fi · 2h 16m", cls="text-sm text-muted-foreground"),
                    cls="p-4 border rounded bg-muted mb-3"
                ),
                data_show=view_mode.eq("card")
            ),
            cls="mt-6 min-h-[200px]"
        ),
        cls="w-full"
    )


@with_code
def multi_select_filters_example():
    filters = Signal("filters", _ref_only=True)  #: hide

    filters_text = collect([
        (filters.contains("featured"), "Featured"),
        (filters.contains("sale"), "On Sale"),
        (filters.contains("new"), "New"),
        (filters.contains("popular"), "Popular"),
    ], join_with=", ")

    return Div(
        filters,  #: hide
        ToggleGroup(
            ("featured", Div(Icon("lucide:star", cls="size-4"), "Featured", cls="flex items-center gap-2")),
            ("sale", Div(Icon("lucide:percent", cls="size-4"), "On Sale", cls="flex items-center gap-2")),
            ("new", Div(Icon("lucide:sparkles", cls="size-4"), "New", cls="flex items-center gap-2")),
            ("popular", Div(Icon("lucide:trending-up", cls="size-4"), "Popular", cls="flex items-center gap-2")),
            type="multiple",
            variant="outline",
            signal=filters
        ),
        Div(
            P("Active:", cls="text-sm font-medium mb-2"),
            Div(
                data_text=filters_text.or_("None selected"),
                cls="text-sm bg-muted p-3 rounded font-mono"
            ),
            cls="mt-6"
        ),
    )


@with_code
def form_integration_example():
    methods = Signal("methods", _ref_only=True)  #: hide
    frequency = Signal("frequency", _ref_only=True)  #: hide

    methods_text = collect([
        (methods.contains("email"), "Email"),
        (methods.contains("sms"), "SMS"),
        (methods.contains("push"), "Push"),
    ], join_with=", ")

    no_methods = ~(methods.length > 0)

    return Div(
        methods, frequency,  #: hide
        P("Notification Preferences", cls="font-medium mb-4"),
        Div(
            Label("Communication Methods:", cls="text-sm font-medium mb-2 block"),
            ToggleGroup(
                ("email", Div(Icon("lucide:mail", cls="size-4"), "Email", cls="flex items-center gap-2")),
                ("sms", Div(Icon("lucide:message-square", cls="size-4"), "SMS", cls="flex items-center gap-2")),
                ("push", Div(Icon("lucide:bell", cls="size-4"), "Push", cls="flex items-center gap-2")),
                type="multiple",
                variant="outline",
                signal=methods
            ),
            cls="mb-6"
        ),
        Div(
            Label("Frequency:", cls="text-sm font-medium mb-2 block"),
            ToggleGroup(
                ("immediate", "Immediate"),
                ("daily", "Daily Digest"),
                ("weekly", "Weekly Summary"),
                ("never", "Never"),
                type="single",
                variant="outline",
                signal=frequency,
                orientation="vertical",
            ),
            cls="mb-6 transition-opacity",
            data_class_opacity_0=no_methods,
            data_class_pointer_events_none=no_methods,
        ),
        Div(
            P("Summary:", cls="text-sm font-medium mb-2"),
            Div(
                P(data_text="Methods: " + methods_text.or_("None"),
                  cls="text-sm mb-1"),
                P(data_text="Frequency: " + frequency.or_("Not set"),
                  cls="text-sm"),
                cls="bg-muted p-3 rounded text-sm"
            ),
        ),
        cls="w-full max-w-lg"
    )


@with_code
def disabled_states_example():
    return Div(
        ToggleGroup(
            ("available", "Available"),
            ("busy", "Busy"),
            ("away", "Away"),
            ("offline", "Offline"),
            type="single",
            disabled=True,
            variant="outline"
        ),
    )


EXAMPLES_DATA = [
    {
        "title": "Editor Controls",
        "description": "Single-select alignment and multi-select decoration in one editor. The preview text reacts to both groups via data_class bindings.",
        "fn": editor_controls_example,
    },
    {
        "title": "View Mode Switcher",
        "description": "Switch between grid, list, and card layouts. Each mode shows different content via data_show bound to the group signal.",
        "fn": view_mode_switcher_example,
    },
    {
        "title": "Multi-Select Filters",
        "description": "Use type='multiple' for non-exclusive selections. The collect() helper joins active filter names into a summary string.",
        "fn": multi_select_filters_example,
        "preview_class": "min-h-[150px]",
    },
    {
        "title": "Form Integration",
        "description": "Chain toggle groups with conditional visibility — the frequency selector appears only after choosing at least one communication method. Uses orientation='vertical' for the second group.",
        "fn": form_integration_example,
    },
    {
        "title": "Disabled",
        "description": "Pass disabled=True to prevent interaction on all items. Renders with reduced opacity.",
        "fn": disabled_states_example,
        "preview_class": "min-h-[100px]",
    },
]

API_REFERENCE = build_api_reference(
    components=[
        Component(
            name="ToggleGroup",
            description=(
                "A toggle group with single or multiple selection. Pass items as (value, content) tuples. "
                "Selection state is stored in the signal directly (str for single, list[str] for multiple)."
            ),
            props=[
                Prop("type", "Literal['single','multiple']", "Selection mode", "'single'"),
                Prop("signal", "str | Signal", "Datastar signal for selection state — auto-generated if omitted", "''"),
                Prop("value", "str | list[str] | None", "Initial selection value(s)", "None"),
                Prop("variant", "Literal['default','outline']", "Visual style applied to all items", "'default'"),
                Prop("size", "Literal['default','sm','lg']", "Button size applied to all items", "'default'"),
                Prop("orientation", "Literal['horizontal','vertical']", "Layout direction of the group", "'horizontal'"),
                Prop("disabled", "bool", "Disable interaction on all items", "False"),
                Prop("cls", "str", "Additional CSS classes", "''"),
            ],
        ),
    ]
)


def create_toggle_group_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)
