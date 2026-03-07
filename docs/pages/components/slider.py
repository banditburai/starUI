TITLE = "Slider"
DESCRIPTION = (
    "A range input component for selecting a single value or a range of values."
)
CATEGORY = "form"
ORDER = 30
STATUS = "stable"

from starhtml import Div, P, Span, Signal, Icon, Form
from components.slider import Slider, SliderWithLabel
from components.button import Button
from components.card import Card, CardHeader, CardContent, CardTitle, CardDescription
from components.badge import Badge
from utils import auto_generate_page, with_code, Prop, Component, build_api_reference


@with_code
def hero_slider_example():
    return Div(
        SliderWithLabel(
            label="Font size",
            default_value=24,
            min=8,
            max=72,
            step=1,
            value_text="px",
        ),
        cls="w-full max-w-sm",
    )


@with_code
def states_example():
    return Div(
        SliderWithLabel(
            label="Opacity",
            default_value=100,
            min=0,
            max=100,
            value_text="%",
        ),
        SliderWithLabel(
            label="Master Scale",
            default_value=100,
            min=25,
            max=400,
            value_text="%",
            disabled=True,
        ),
        SliderWithLabel(
            label="Blur Radius",
            default_value=48,
            min=0,
            max=100,
            value_text="px",
            error_text="Blur above 40px degrades export quality",
        ),
        SliderWithLabel(
            label="Feather",
            default_value=4,
            min=0,
            max=20,
            value_text="px",
            helper_text="Soft edge width for selection masks",
        ),
        cls="grid gap-6 w-full max-w-sm",
    )


@with_code
def typography_preview_example():
    font_size = Signal("sl_font_size", 18)  #: hide
    return Card(
        CardHeader(
            CardTitle("Type Settings"),
            CardDescription("Adjust font size and preview live"),
        ),
        CardContent(
            Div(
                font_size,  #: hide
                Div(
                    Span("Font size", cls="text-sm font-medium"),
                    Span(
                        data_text=font_size,
                        cls="text-sm text-muted-foreground font-mono",
                    ),
                    cls="flex justify-between mb-2",
                ),
                Slider(
                    signal=font_size,
                    default_value=18,
                    min=12,
                    max=48,
                    aria_label="Font size",
                ),
                P(
                    "The quick brown fox jumps over the lazy dog",
                    data_style_font_size=font_size + "px",
                    cls="mt-6 text-foreground transition-none leading-snug",
                    style="font-size: 18px",
                ),
                cls="space-y-1",
            ),
        ),
        cls="w-full max-w-md",
    )


@with_code
def image_adjustments_example():
    brightness = Signal("sl_bright", 100)  #: hide
    contrast = Signal("sl_contrast", 100)  #: hide
    saturation = Signal("sl_sat", 100)  #: hide
    all_default = brightness.eq(100) & contrast.eq(100) & saturation.eq(100)  #: hide
    return Card(
        CardHeader(
            CardTitle("Image Adjustments"),
            CardDescription(
                Span("Filter preview", cls="mr-2"),
                Badge(
                    data_text=all_default.if_("Default", "Modified"),
                    variant="secondary",
                ),
            ),
        ),
        CardContent(
            Div(
                brightness, contrast, saturation,  #: hide
                Div(
                    cls="h-24 rounded-lg bg-gradient-to-br from-blue-400 via-purple-500 to-pink-500",
                    data_style_filter="brightness("
                    + brightness / 100
                    + ") contrast("
                    + contrast / 100
                    + ") saturate("
                    + saturation / 100
                    + ")",
                    style="filter: brightness(1) contrast(1) saturate(1)",
                ),
                SliderWithLabel(
                    label="Brightness",
                    signal=brightness,
                    default_value=100,
                    min=0,
                    max=200,
                    value_text="%",
                    cls="mt-4",
                ),
                SliderWithLabel(
                    label="Contrast",
                    signal=contrast,
                    default_value=100,
                    min=0,
                    max=200,
                    value_text="%",
                ),
                SliderWithLabel(
                    label="Saturation",
                    signal=saturation,
                    default_value=100,
                    min=0,
                    max=200,
                    value_text="%",
                ),
                Button(
                    "Reset",
                    variant="outline",
                    size="sm",
                    cls="mt-2",
                    data_on_click=[
                        brightness.set(100),
                        contrast.set(100),
                        saturation.set(100),
                    ],
                    data_attr_disabled=all_default,
                ),
                cls="space-y-3",
            ),
        ),
        cls="w-full max-w-md",
    )


@with_code
def color_mixer_example():
    red = Signal("sl_red", 99)  #: hide
    green = Signal("sl_green", 102)  #: hide
    blue = Signal("sl_blue", 204)  #: hide

    def channel_row(label, sig, aria):
        return Div(
            Span(label, cls="text-sm font-medium w-8"),
            Button(
                Icon("lucide:minus", cls="size-3"),
                data_on_click=sig.set((sig - 1).max(0)),
                variant="outline",
                size="icon",
                cls="size-7",
                aria_label=f"Decrease {aria}",
            ),
            Slider(
                signal=sig,
                min=0,
                max=255,
                aria_label=aria,
                cls="flex-1",
            ),
            Button(
                Icon("lucide:plus", cls="size-3"),
                data_on_click=sig.set((sig + 1).min(255)),
                variant="outline",
                size="icon",
                cls="size-7",
                aria_label=f"Increase {aria}",
            ),
            cls="flex items-center gap-2",
        )

    return Card(
        CardHeader(
            CardTitle("Color Mixer"),
            CardDescription("Blend RGB channels to pick a color"),
        ),
        CardContent(
            Div(
                red, green, blue,  #: hide
                Div(
                    cls="h-20 rounded-lg border",
                    data_style_background_color="rgb("
                    + red
                    + ","
                    + green
                    + ","
                    + blue
                    + ")",
                    style="background-color: rgb(99, 102, 204)",
                ),
                channel_row("R", red, "Red channel"),
                channel_row("G", green, "Green channel"),
                channel_row("B", blue, "Blue channel"),
                Span(
                    data_text="rgb(" + red + ", " + green + ", " + blue + ")",
                    cls="block text-center text-xs font-mono text-muted-foreground mt-1",
                ),
                cls="space-y-3",
            ),
        ),
        cls="w-full max-w-md",
    )


@with_code
def layer_opacity_example():
    bg_opacity = Signal("sl_bg_op", 100)  #: hide
    art_opacity = Signal("sl_art_op", 75)  #: hide
    text_opacity = Signal("sl_txt_op", 90)  #: hide

    layers = [
        ("Background", bg_opacity, "bg-blue-500/80", 100),
        ("Artwork", art_opacity, "bg-purple-500/80", 75),
        ("Text", text_opacity, "bg-amber-500/80", 90),
    ]

    return Card(
        CardHeader(
            CardTitle("Layer Opacity"),
            CardDescription("Control transparency per layer"),
        ),
        CardContent(
            Div(
                bg_opacity, art_opacity, text_opacity,  #: hide
                *[
                    Div(
                        Span(label, cls="text-xs font-medium text-muted-foreground"),
                        Div(
                            cls=f"h-12 w-full rounded {color}",
                            data_style_opacity=sig / 100,
                            style=f"opacity: {default / 100}",
                        ),
                        Slider(
                            signal=sig,
                            default_value=default,
                            min=0,
                            max=100,
                            orientation="vertical",
                            aria_label=f"{label} opacity",
                        ),
                        Span(
                            data_text=sig + "%",
                            cls="text-xs font-mono text-muted-foreground",
                        ),
                        cls="flex flex-col items-center gap-2",
                    )
                    for label, sig, color, default in layers
                ],
                cls="grid grid-cols-3 gap-4",
            ),
        ),
        cls="w-full max-w-md",
    )


@with_code
def export_settings_example():
    quality = Signal("sl_exp_q", 85)  #: hide
    dpi = Signal("sl_exp_dpi", 150)  #: hide
    est_size = Signal("sl_exp_sz", quality * dpi / 100)  #: hide
    return Card(
        CardHeader(
            CardTitle("Export Settings"),
            CardDescription("Configure output quality and resolution"),
        ),
        CardContent(
            Form(
                quality, dpi, est_size,  #: hide
                SliderWithLabel(
                    label="JPEG Quality",
                    signal=quality,
                    default_value=85,
                    min=1,
                    max=100,
                    value_text="%",
                ),
                SliderWithLabel(
                    label="DPI",
                    signal=dpi,
                    default_value=150,
                    min=72,
                    max=600,
                    helper_text="72 for screen, 300+ for print",
                ),
                SliderWithLabel(
                    label="Width Range",
                    default_value=[1024, 1920],
                    min=320,
                    max=3840,
                    step=10,
                    value_text=["px", "px"],
                ),
                Div(
                    Span("Est. size: ", cls="text-sm text-muted-foreground"),
                    Span(
                        data_text=est_size,
                        cls="text-sm font-mono font-medium",
                    ),
                    Span(" KB", cls="text-sm text-muted-foreground"),
                    cls="flex items-center gap-1 mt-2",
                ),
                Button(
                    Icon("lucide:download", cls="size-4"),
                    "Export",
                    type="submit",
                    cls="w-full mt-4",
                ),
                cls="space-y-4",
            ),
        ),
        cls="w-full max-w-md",
    )


EXAMPLES_DATA = [
    {
        "fn": hero_slider_example,
        "title": "Slider",
        "description": "Labeled slider with value suffix and constrained range",
    },
    {
        "fn": states_example,
        "title": "States",
        "description": "Default, disabled, error, and helper text states",
    },
    {
        "fn": typography_preview_example,
        "title": "Live Preview",
        "description": "Slider drives font size in real time via signal binding",
    },
    {
        "fn": image_adjustments_example,
        "title": "Image Adjustments",
        "description": "Brightness, contrast, and saturation sliders with live CSS filter preview and batch reset",
    },
    {
        "fn": color_mixer_example,
        "title": "Color Mixer",
        "description": "RGB channel sliders with +/- buttons driving a live color swatch",
    },
    {
        "fn": layer_opacity_example,
        "title": "Vertical",
        "description": "Vertical sliders controlling per-layer opacity with live preview",
    },
    {
        "fn": export_settings_example,
        "title": "Form & Range Slider",
        "description": "Export form with single-value sliders, a dual-thumb range slider for resolution bounds, and a derived file-size estimate",
    },
]


API_REFERENCE = build_api_reference(
    main_props=[
        Prop(
            "value",
            "list[float] | float | None",
            "Controlled value. When provided, component is controlled",
            "None",
        ),
        Prop(
            "default_value",
            "list[float] | float | None",
            "Initial value for uncontrolled mode. Defaults to [min] if not specified",
            "None",
        ),
        Prop(
            "signal",
            "str | Signal | None",
            "Signal name or Signal object for reactive two-way binding",
            "None",
        ),
        Prop("min", "float", "Minimum value", "0"),
        Prop("max", "float", "Maximum value", "100"),
        Prop("step", "float", "Step increment", "1"),
        Prop(
            "orientation",
            '"horizontal" | "vertical"',
            "Slider orientation",
            '"horizontal"',
        ),
        Prop("disabled", "bool", "Disables the slider", "False"),
        Prop("name", "str | None", "Form input name", "None"),
        Prop("show_value", "bool", "Display current value", "False"),
        Prop(
            "value_text",
            "str | list[str] | None",
            "Custom text suffix to display after numeric value",
            "None",
        ),
        Prop(
            "aria_label",
            "str | None",
            "Accessible label for the slider input",
            "None",
        ),
        Prop("cls", "str", "Additional CSS classes", "''"),
        Prop("id", "str | None", "HTML id for the slider input", "auto-generated"),
    ],
    components=[
        Component(
            "Slider",
            "Main slider component for selecting single values using native <input type='range'>. Delegates to RangeSlider when given a list of 2+ values.",
        ),
        Component(
            "SliderWithLabel",
            "Convenience wrapper with label, helper text, and error text",
        ),
        Component("RangeSlider", "Dual-thumb slider for selecting value ranges"),
        Component("SliderTrack", "Track element (sub-component)"),
        Component("SliderRange", "Filled range element (sub-component)"),
    ],
)


def create_slider_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)
