"""
Switch component documentation - Toggle controls for live streaming and broadcast.
"""

TITLE = "Switch"
DESCRIPTION = "A toggle control for binary on/off states, commonly used for settings that take immediate effect."
CATEGORY = "form"
ORDER = 35
STATUS = "stable"

from starhtml import Div, P, Label, Span, Form, Signal, all_, collect, evt
from starui.registry.components.switch import Switch, SwitchWithLabel
from starui.registry.components.button import Button
from starui.registry.components.card import Card, CardHeader, CardContent, CardTitle, CardDescription
from starui.registry.components.badge import Badge
from starui.registry.components.progress import Progress
from utils import auto_generate_page, with_code, Prop, Component, build_api_reference


@with_code
def hero_switch_example():
    return Div(
        Div(
            Label("Live", fr="sw_live", cls="text-sm font-medium leading-none cursor-pointer"),
            Switch(signal="sw_hero_live", id="sw_live", checked=True),
            cls="flex items-center gap-3",
        ),
        SwitchWithLabel(
            label="Record to disk",
            helper_text="Capture stream locally while broadcasting",
            signal="sw_hero_record",
        ),
        SwitchWithLabel(
            label="Mute mic",
            signal="sw_hero_mute",
        ),
        cls="space-y-4 max-w-sm",
    )


@with_code
def states_example():
    return Div(
        SwitchWithLabel(label="Unchecked", signal="sw_st_off"),
        SwitchWithLabel(label="Checked", signal="sw_st_on", checked=True),
        SwitchWithLabel(label="Disabled off", signal="sw_st_dis_off", disabled=True),
        SwitchWithLabel(label="Disabled on", signal="sw_st_dis_on", disabled=True, checked=True),
        SwitchWithLabel(
            label="With error",
            signal="sw_st_err",
            error_text="Stream key is invalid",
        ),
        SwitchWithLabel(
            label="Required field",
            signal="sw_st_req",
            required=True,
            helper_text="Required before going live",
        ),
        SwitchWithLabel(
            label="Small size",
            signal="sw_st_sm",
            size="sm",
        ),
        SwitchWithLabel(
            label="Custom styling",
            signal="sw_st_custom",
            label_cls="text-green-600 dark:text-green-400",
            switch_cls="border-2 border-green-500",
            helper_text="Green tint on label and track border",
        ),
        cls="space-y-4 max-w-sm",
    )


@with_code
def stream_output_example():
    live = Signal("sw_out_live", _ref_only=True)
    transcode = Signal("sw_out_transcode", _ref_only=True)
    overlay = Signal("sw_out_overlay", _ref_only=True)
    lowlat = Signal("sw_out_lowlat", _ref_only=True)
    layer_count = Signal("sw_out_count", transcode + overlay + lowlat)

    return Card(
        CardHeader(
            CardTitle("Stream Output"),
            CardDescription("Layers applied to the broadcast encoder"),
        ),
        CardContent(
            Div(
                layer_count,
                SwitchWithLabel(
                    label="Stream live",
                    helper_text="Push to ingest server",
                    signal=live,
                    checked=True,
                ),
                Div(
                    SwitchWithLabel(label="Multi-quality transcode", signal=transcode),
                    SwitchWithLabel(label="Chat overlay", signal=overlay),
                    SwitchWithLabel(label="Low-latency mode", signal=lowlat, size="sm"),
                    cls="space-y-3 pl-4 border-l-2 border-muted",
                    data_show=live,
                    data_effect=[
                        (~live).then(transcode.set(False)),
                        (~live).then(overlay.set(False)),
                        (~live).then(lowlat.set(False)),
                    ],
                ),
                P(
                    data_text=live.if_(
                        layer_count.if_(layer_count + " layers active", "No layers enabled"),
                        "Stream offline",
                    ),
                    cls="text-sm text-muted-foreground mt-3",
                ),
                cls="space-y-4",
            )
        ),
        cls="max-w-md",
    )


@with_code
def go_live_checklist_example():
    low_latency = Signal("sw_go_lowlat", _ref_only=True)
    vod = Signal("sw_go_vod", _ref_only=True)
    dvr = Signal("sw_go_dvr", _ref_only=True)

    return Card(
        CardHeader(
            CardTitle("Broadcast Mode"),
            CardDescription("Required features before going live"),
        ),
        CardContent(
            Form(
                SwitchWithLabel(
                    label="Low-latency ingest",
                    helper_text="Sub-second glass-to-glass delay",
                    signal=low_latency,
                    required=True,
                ),
                SwitchWithLabel(
                    label="VOD recording",
                    signal=vod,
                    required=True,
                ),
                SwitchWithLabel(
                    label="DVR rewind",
                    signal=dvr,
                    required=True,
                ),
                SwitchWithLabel(
                    label="Auto-clip highlights",
                    signal="sw_go_clip",
                ),
                Button(
                    "Go Live",
                    type="submit",
                    cls="w-full mt-4",
                    data_attr_disabled=~all_(low_latency, vod, dvr),
                    data_on_click=evt.preventDefault(),
                ),
                cls="space-y-3",
            )
        ),
        cls="max-w-md",
    )


@with_code
def encoder_settings_example():
    hd = Signal("sw_enc_hd", _ref_only=True)
    hw = Signal("sw_enc_hw", _ref_only=True)
    bframes = Signal("sw_enc_bf", _ref_only=True)
    twopass = Signal("sw_enc_2p", _ref_only=True)
    # Weighted: 1080p costs 6000, hardware saves 2000, B-frames add 500, two-pass adds 1500
    bitrate = Signal("sw_enc_kbps", hd * 6000 + hw * -2000 + bframes * 500 + twopass * 1500)
    bitrate_pct = Signal("sw_enc_pct", bitrate / 8000 * 100)

    def setting_switch(label, signal, helper_text=None, checked=False):
        return SwitchWithLabel(
            label=label,
            signal=signal,
            checked=checked,
            helper_text=helper_text,
            label_cls=signal.if_("text-green-600 dark:text-green-400"),
        )

    return Card(
        CardHeader(
            CardTitle("Encoder Settings"),
            CardDescription("Estimated bitrate from active options"),
        ),
        CardContent(
            Div(
                bitrate,
                bitrate_pct,
                setting_switch("1080p60 output", hd, helper_text="+6000 kbps", checked=True),
                setting_switch("Hardware encoding", hw, helper_text="-2000 kbps overhead"),
                setting_switch("B-frames", bframes, helper_text="+500 kbps"),
                setting_switch("Two-pass encoding", twopass, helper_text="+1500 kbps"),
                Div(
                    P(
                        "Bitrate: ",
                        Span(data_text=bitrate, cls="font-bold"),
                        " kbps",
                        cls="text-sm text-muted-foreground",
                    ),
                    Progress(signal=bitrate_pct, cls="w-full h-2 mt-2", aria_label="Estimated bitrate"),
                    cls="mt-4",
                ),
                cls="space-y-3",
            )
        ),
        cls="max-w-md",
    )


@with_code
def stream_destinations_example():
    platforms = [
        ("sw_dst_twitch", "Twitch", "Twitch"),
        ("sw_dst_yt", "YouTube", "YT"),
        ("sw_dst_fb", "Facebook Live", "FB"),
        ("sw_dst_x", "X (Twitter)", "X"),
        ("sw_dst_kick", "Kick", "Kick"),
        ("sw_dst_rumble", "Rumble", "Rumble"),
    ]

    platform_signals = {name: Signal(name, _ref_only=True) for name, _, _ in platforms}

    active_summary = collect(
        [(platform_signals[name], short) for name, _, short in platforms],
        join_with=", ",
    )

    reset_actions = [platform_signals[name].set(False) for name, _, _ in platforms]

    return Card(
        CardHeader(
            CardTitle("Stream Destinations"),
            CardDescription("Multistream to selected platforms"),
        ),
        CardContent(
            Form(
                Div(
                    *[
                        SwitchWithLabel(label=label, signal=platform_signals[name])
                        for name, label, _ in platforms
                    ],
                    cls="space-y-3",
                ),
                Div(
                    Button("Go Multistream", type="submit", cls="w-full", data_on_click=evt.preventDefault()),
                    Button("Reset All", variant="outline", cls="w-full mt-2", data_on_click=(reset_actions, dict(prevent=True))),
                    cls="mt-6",
                ),
                Div(
                    P(
                        "Active: ",
                        Span(data_text=active_summary.if_(active_summary, "None"), cls="font-medium"),
                        cls="text-sm text-muted-foreground",
                    ),
                    cls="mt-4 pt-4 border-t",
                ),
            )
        ),
        cls="max-w-sm",
    )


@with_code
def scene_layers_example():
    renderer = Signal("sw_scene_render", _ref_only=True)

    layers = [
        ("sw_scene_cam", "Webcam", "sw_scene_cam_p"),
        ("sw_scene_screen", "Screen capture", "sw_scene_screen_p"),
        ("sw_scene_lower", "Lower thirds", "sw_scene_lower_p"),
    ]

    layer_signals = {name: Signal(name, _ref_only=True) for name, _, _ in layers}
    preview_signals = {prev: Signal(prev, _ref_only=True) for _, _, prev in layers}
    active_count = Signal(
        "sw_scene_count",
        sum(layer_signals[name] for name, _, _ in layers),
    )

    return Card(
        CardHeader(
            CardTitle("Scene Layers"),
            CardDescription("Sources composited into the broadcast"),
        ),
        CardContent(
            Div(
                active_count,
                SwitchWithLabel(
                    label="Studio mode",
                    helper_text="Preview scene before pushing live",
                    signal=renderer,
                    checked=True,
                ),
                Div(
                    *[
                        Div(
                            SwitchWithLabel(label=label, signal=layer_signals[name]),
                            Div(
                                Span("Preview", cls="text-xs text-muted-foreground"),
                                Switch(
                                    signal=preview_signals[prev],
                                    size="sm",
                                    cls="border-2 border-amber-500",
                                    data_attr_disabled=~layer_signals[name],
                                ),
                                cls="flex items-center gap-2",
                            ),
                            cls="flex items-center justify-between",
                        )
                        for name, label, prev in layers
                    ],
                    cls="space-y-3 pl-4 border-l-2 border-muted",
                    data_show=renderer,
                    data_effect=[
                        (~renderer).then(layer_signals[name].set(False))
                        for name, _, _ in layers
                    ] + [
                        (~renderer).then(preview_signals[prev].set(False))
                        for _, _, prev in layers
                    ],
                ),
                Div(
                    Badge(
                        data_text=renderer.if_(active_count + " active", "Studio off"),
                        variant="secondary",
                    ),
                    cls="mt-4 flex justify-center",
                ),
                cls="space-y-4",
            )
        ),
        cls="max-w-md",
    )


API_REFERENCE = build_api_reference(
    main_props=[
        Prop("checked", "bool | None", "Initial checked state", "None"),
        Prop("signal", "str | Signal", "Signal name for reactive state management", "auto-generated"),
        Prop("disabled", "bool", "Disables the switch and blocks pointer events", "False"),
        Prop("required", "bool", "Marks as required. SwitchWithLabel appends a red asterisk", "False"),
        Prop("size", '"default" | "sm"', "Switch track and thumb size", '"default"'),
        Prop("label", "str", "Label text (SwitchWithLabel only)"),
        Prop("helper_text", "str | None", "Muted text below the label (SwitchWithLabel only)", "None"),
        Prop("error_text", "str | None", "Destructive text below the control. Sets aria-invalid (SwitchWithLabel only)", "None"),
        Prop("cls", "str", "Additional CSS classes", "''"),
        Prop("label_cls", "str", "Additional CSS classes for the label (SwitchWithLabel only)", "''"),
        Prop("switch_cls", "str", "Additional CSS classes for the switch track. Cannot override checked/unchecked background colors (SwitchWithLabel only)", "''"),
    ],
    components=[
        Component("Switch", "Standalone switch control. Renders a button with role=switch and reactive thumb. Compose with Label for manual layout"),
        Component("SwitchWithLabel", "Convenience wrapper composing Switch + Label + helper/error text with standard spacing"),
    ],
)


EXAMPLES_DATA = [
    {"fn": hero_switch_example, "title": "Switch", "description": "Bare Switch with manual label composition, and SwitchWithLabel convenience wrapper"},
    {"fn": states_example, "title": "States", "description": "All visual states — unchecked, checked, disabled, error text, required, small size, and custom styling"},
    {"fn": stream_output_example, "title": "Conditional Display", "description": "Master switch cascading dependent encoding layers with data_effect and data_show"},
    {"fn": go_live_checklist_example, "title": "Form Validation", "description": "Required switches that gate form submission with all_() signal logic"},
    {"fn": encoder_settings_example, "title": "Signal Arithmetic", "description": "Weighted bitrate calculation and progress bar driven by per-switch multipliers"},
    {"fn": stream_destinations_example, "title": "Collect and Reset", "description": "Active platform summary via collect() with batch reset"},
    {"fn": scene_layers_example, "title": "Dependent Switches", "description": "Multi-level dependency chain with studio mode, per-layer enable, and preview switches"},
]


def create_switch_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)
