"""
Checkbox component documentation - Toggle controls for forms and settings.
"""

TITLE = "Checkbox"
DESCRIPTION = "A control that allows the user to toggle between checked and not checked."
CATEGORY = "form"
ORDER = 15
STATUS = "stable"

from starhtml import Div, P, Label, Icon, Span, H3, Form, Signal, all_, collect, evt
from starui.registry.components.checkbox import Checkbox, CheckboxWithLabel
from starui.registry.components.button import Button
from starui.registry.components.card import Card, CardHeader, CardContent, CardTitle, CardDescription
from starui.registry.components.badge import Badge
from starui.registry.components.progress import Progress
from utils import auto_generate_page, with_code, Prop, Component, build_api_reference


@with_code
def hero_checkbox_example():
    return Div(
        Div(
            Checkbox(signal="cb_hero_monitor", id="cb_monitor", checked=True),
            Div(
                Label("Monitor input", fr="cb_monitor", cls="text-sm font-medium leading-none"),
                cls="grid gap-1.5",
            ),
            cls="flex items-start gap-3",
        ),
        CheckboxWithLabel(
            label="48V phantom power",
            helper_text="Required for condenser microphones",
            signal="cb_hero_phantom",
        ),
        CheckboxWithLabel(
            label="-20dB pad",
            signal="cb_hero_pad",
        ),
        cls="space-y-4 max-w-sm",
    )


@with_code
def states_example():
    return Div(
        CheckboxWithLabel(label="Unchecked", signal="cb_st_off"),
        CheckboxWithLabel(label="Checked", signal="cb_st_on", checked=True),
        CheckboxWithLabel(
            label="Indeterminate",
            helper_text="Compile-time only — icon and data-state are fixed at render",
            signal="cb_st_ind",
            indeterminate=True,
        ),
        CheckboxWithLabel(
            label="With error",
            signal="cb_st_err",
            error_text="Input level exceeds safe range",
        ),
        CheckboxWithLabel(
            label="Custom indicator",
            helper_text="Uses indicator_cls to tint the check icon",
            signal="cb_st_custom",
            checked=True,
            indicator_cls="text-green-600 dark:text-green-400",
        ),
        cls="space-y-4 max-w-sm",
    )


@with_code
def session_prep_example():
    levels = Signal("cb_prep_levels", _ref_only=True)
    backup = Signal("cb_prep_backup", _ref_only=True)
    silence = Signal("cb_prep_silence", _ref_only=True)

    return Card(
        CardHeader(
            CardTitle("Session Prep"),
            CardDescription("Complete required checks before recording"),
        ),
        CardContent(
            Form(
                Div(
                    CheckboxWithLabel(
                        label="Input levels verified",
                        helper_text="All channels reading between -18 and -12 dBFS",
                        signal=levels,
                        required=True,
                    ),
                    CheckboxWithLabel(
                        label="Backup drive connected",
                        signal=backup,
                        required=True,
                    ),
                    CheckboxWithLabel(
                        label="Studio silence confirmed",
                        helper_text="No HVAC, phones, or foot traffic",
                        signal=silence,
                        required=True,
                    ),
                    CheckboxWithLabel(
                        label="Count in before recording",
                        signal="cb_prep_countin",
                    ),
                    cls="space-y-3",
                ),
                Button(
                    "Begin Session",
                    type="submit",
                    cls="w-full mt-4",
                    data_attr_disabled=~all_(levels, backup, silence),
                    data_on_click=evt.preventDefault(),
                ),
            )
        ),
        cls="max-w-md",
    )


@with_code
def bus_routing_example():
    drums = Signal("cb_bus_drums", _ref_only=True)
    keys = Signal("cb_bus_keys", _ref_only=True)
    brass = Signal("cb_bus_brass", _ref_only=True)
    strings = Signal("cb_bus_strings", _ref_only=True)
    optional_count = Signal("cb_bus_count", drums + keys + brass + strings)

    return Card(
        CardHeader(
            CardTitle("Bus Routing"),
            CardDescription("Configure audio bus assignments"),
        ),
        CardContent(
            Div(
                optional_count,
                Div(
                    H3("Required", cls="text-sm font-semibold mb-2 text-muted-foreground"),
                    CheckboxWithLabel(
                        label="Master",
                        helper_text="Main stereo output",
                        checked=True,
                        disabled=True,
                    ),
                    CheckboxWithLabel(
                        label="Talkback",
                        helper_text="Engineer-to-talent communication",
                        checked=True,
                        disabled=True,
                    ),
                    cls="space-y-2 mb-4",
                ),
                Div(
                    H3("Optional", cls="text-sm font-semibold mb-2 text-muted-foreground"),
                    CheckboxWithLabel(
                        label="Drums sub",
                        signal=drums,
                        checked=True,
                    ),
                    CheckboxWithLabel(
                        label="Keys sub",
                        signal=keys,
                    ),
                    CheckboxWithLabel(
                        label="Brass sub",
                        signal=brass,
                    ),
                    CheckboxWithLabel(
                        label="Strings sub",
                        signal=strings,
                    ),
                    cls="space-y-2",
                ),
                Div(
                    Badge(
                        data_text=optional_count + " optional active",
                        variant="secondary",
                    ),
                    cls="mt-4 flex justify-center",
                ),
            )
        ),
        cls="max-w-md",
    )


@with_code
def take_tracker_example():
    mic = Signal("cb_take_mic", _ref_only=True)
    hp = Signal("cb_take_hp", _ref_only=True)
    gain = Signal("cb_take_gain", _ref_only=True)
    ref = Signal("cb_take_ref", _ref_only=True)
    completed_count = Signal("cb_take_done", mic + hp + gain + ref)
    take_progress = Signal("cb_take_pct", completed_count / 4 * 100)

    def task_item(label, signal, checked=False):
        return CheckboxWithLabel(
            label=label,
            signal=signal,
            checked=checked,
            label_cls=signal.if_("line-through text-muted-foreground"),
        )

    return Card(
        CardHeader(
            CardTitle("Take Tracker"),
            CardDescription("Pre-session setup tasks"),
        ),
        CardContent(
            Div(
                completed_count,
                take_progress,
                Div(
                    task_item("Mic placement check", mic, checked=True),
                    task_item("Headphone mix approved", hp, checked=True),
                    task_item("Gain staging complete", gain),
                    task_item("Reference track loaded", ref),
                    cls="space-y-3",
                ),
                Div(
                    P(
                        "Completed: ",
                        Span(data_text=completed_count, cls="font-bold"),
                        " of 4",
                        cls="text-sm text-muted-foreground",
                    ),
                    Progress(signal=take_progress, cls="w-full h-2 mt-2", aria_label="Task completion"),
                    cls="mt-4",
                ),
            )
        ),
        cls="max-w-md",
    )


@with_code
def session_takes_example():
    takes = [
        {"id": "cb_take1", "name": "Take 1 — Intro.wav", "dur": "3:42"},
        {"id": "cb_take2", "name": "Take 2 — Verse.wav", "dur": "4:18"},
        {"id": "cb_take3", "name": "Take 3 — Chorus.wav", "dur": "2:55"},
        {"id": "cb_take4", "name": "Take 4 — Bridge.wav", "dur": "1:36"},
    ]

    take_signals = {t["id"]: Signal(t["id"], _ref_only=True) for t in takes}
    discarded_signals = {t["id"]: Signal(t["id"] + "_dis", False) for t in takes}
    select_all = Signal("cb_takes_all", False)

    selected_count = Signal(
        "cb_takes_sel",
        sum([take_signals[t["id"]] & ~discarded_signals[t["id"]] for t in takes]),
    )

    discard_actions = [
        take_signals[t["id"]].then(discarded_signals[t["id"]].set(True)) for t in takes
    ] + [select_all.set(False)]

    select_actions = [
        (~discarded_signals[t["id"]]).then(take_signals[t["id"]].set(select_all))
        for t in takes
    ]

    return Card(
        CardHeader(
            CardTitle("Session Takes"),
            CardDescription("Review and discard recordings"),
        ),
        CardContent(
            Div(
                select_all,
                *discarded_signals.values(),
                selected_count,
                Div(
                    CheckboxWithLabel(
                        label="Select All",
                        signal=select_all,
                        checkbox_cls="border-2",
                        data_on_change=select_actions,
                    ),
                    cls="border-b pb-2 mb-3",
                ),
                Div(
                    *[
                        Div(
                            CheckboxWithLabel(
                                label=t["name"],
                                signal=take_signals[t["id"]],
                                helper_text=t["dur"],
                            ),
                            data_show=~discarded_signals[t["id"]],
                        )
                        for t in takes
                    ],
                    cls="space-y-2 pl-6",
                ),
                Div(
                    Button(
                        Icon("lucide:trash-2", cls="h-4 w-4"),
                        "Discard selected",
                        data_on_click=discard_actions,
                        variant="destructive",
                        size="sm",
                        data_attr_disabled=selected_count == 0,
                    ),
                    cls="mt-4 pt-4 border-t",
                ),
            )
        ),
        cls="max-w-md",
    )


@with_code
def export_settings_example():
    formats = [
        ("cb_exp_wav", "WAV", "WAV", True),
        ("cb_exp_mp3", "MP3", "MP3", False),
        ("cb_exp_flac", "FLAC", "FLAC", False),
    ]

    rates = [
        ("cb_exp_44", "44.1 kHz", "44.1 kHz", True),
        ("cb_exp_48", "48 kHz", "48 kHz", False),
        ("cb_exp_96", "96 kHz", "96 kHz", False),
    ]

    metadata = [
        ("cb_exp_art", "Embed artwork", "Artwork", False),
        ("cb_exp_ts", "Include timestamps", "Timestamps", True),
    ]

    all_options = formats + rates + metadata
    option_signals = {name: Signal(name, _ref_only=True) for name, _, _, _ in all_options}
    reset_actions = [option_signals[name].set(False) for name, _, _, _ in all_options]

    active_summary = collect(
        [(option_signals[name], collect_label) for name, _, collect_label, _ in all_options],
        join_with=", ",
    )

    def option_group(title, options, mb_class="mb-6"):
        return Div(
            H3(title, cls="text-sm font-semibold mb-3"),
            Div(
                *[
                    CheckboxWithLabel(label=label, signal=option_signals[name], checked=checked)
                    for name, label, _, checked in options
                ],
                cls="space-y-2",
            ),
            cls=mb_class,
        )

    return Card(
        CardHeader(
            CardTitle("Export Settings"),
            CardDescription("Configure output format and options"),
        ),
        CardContent(
            Form(
                option_group("Format", formats),
                option_group("Sample Rate", rates),
                option_group("Metadata", metadata, mb_class=""),
                Div(
                    Button("Export", type="submit", cls="w-full", data_on_click=evt.preventDefault()),
                    Button("Reset", variant="outline", cls="w-full mt-2", data_on_click=(reset_actions, dict(prevent=True))),
                    cls="mt-6",
                ),
                Div(
                    P(
                        "Selected: ",
                        Span(data_text=active_summary.if_(active_summary, "None"), cls="font-medium"),
                        cls="text-sm text-muted-foreground",
                    ),
                    cls="mt-4 pt-4 border-t",
                ),
            )
        ),
        cls="max-w-sm",
    )


API_REFERENCE = build_api_reference(
    main_props=[
        Prop("checked", "bool | None", "Initial checked state", "None"),
        Prop("signal", "str | Signal", "Signal name for reactive state management", "auto-generated"),
        Prop("indeterminate", "bool", "Show indeterminate state (minus icon). Use for parent checkboxes when some children are selected", "False"),
        Prop("disabled", "bool", "Disables the checkbox and blocks pointer events", "False"),
        Prop("required", "bool", "Marks as required for form validation. CheckboxWithLabel appends a red asterisk", "False"),
        Prop("name", "str | None", "Name attribute for form submission", "None"),
        Prop("value", "str | None", "Value submitted with forms when checked", "'on'"),
        Prop("label", "str", "Label text (CheckboxWithLabel only)"),
        Prop("helper_text", "str | None", "Muted text below the label (CheckboxWithLabel only)", "None"),
        Prop("error_text", "str | None", "Destructive text below the control. Sets aria-invalid on the checkbox (CheckboxWithLabel only)", "None"),
        Prop("cls", "str", "Additional CSS classes", "''"),
        Prop("indicator_cls", "str", "Additional CSS classes for the check/minus icon overlay", "''"),
        Prop("label_cls", "str", "Additional CSS classes for the label element (CheckboxWithLabel only)", "''"),
        Prop("checkbox_cls", "str", "Additional CSS classes for the inner checkbox (CheckboxWithLabel only)", "''"),
    ],
    components=[
        Component("Checkbox", "Standalone checkbox control. Renders a native input with an icon overlay. Compose with Label for manual layout"),
        Component("CheckboxWithLabel", "Convenience wrapper that composes Checkbox + Label + helper text + error text with standard spacing"),
    ],
)


EXAMPLES_DATA = [
    {"fn": hero_checkbox_example, "title": "Checkbox", "description": "Bare Checkbox with manual label composition, and CheckboxWithLabel convenience wrapper"},
    {"fn": states_example, "title": "States", "description": "All visual states — unchecked, checked, indeterminate, error text, and custom indicator styling"},
    {"fn": session_prep_example, "title": "Form Validation", "description": "Required checkboxes that gate form submission with all_() signal logic"},
    {"fn": bus_routing_example, "title": "Disabled States", "description": "Required buses locked as disabled, optional buses interactive with active count"},
    {"fn": take_tracker_example, "title": "Progress Tracking", "description": "Reactive strikethrough styling and progress bar driven by checkbox signals"},
    {"fn": session_takes_example, "title": "Select All", "description": "Bulk selection with select-all toggle and destructive batch action"},
    {"fn": export_settings_example, "title": "Grouped Filters", "description": "Grouped checkboxes with reset and active summary via collect()"},
]


def create_checkbox_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)
