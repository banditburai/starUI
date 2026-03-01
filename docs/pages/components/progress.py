"""
Progress component documentation - Task completion indicator.
"""

# Component metadata for auto-discovery
TITLE = "Progress"
DESCRIPTION = "Displays an indicator showing the completion progress of a task, typically displayed as a progress bar."
CATEGORY = "ui"
ORDER = 65
STATUS = "stable"

from starhtml import Div, P, Span, Signal, Icon, seq, set_timeout, switch, clear_timeout
from starui.registry.components.progress import Progress
from starui.registry.components.button import Button
from utils import auto_generate_page, with_code, Prop, build_api_reference


@with_code
def default_example():
    return Div(
        Progress(value=33, aria_label="Progress"),
        cls="w-full max-w-md"
    )


@with_code
def with_label_example():
    return Div(
        (pct := Signal("prog_label", 66)),
        Div(
            Span("Upload progress", cls="text-sm font-medium"),
            Span(data_text=pct.round() + "%", cls="text-sm text-muted-foreground font-mono"),
            cls="flex justify-between"
        ),
        Progress(signal=pct, aria_label="Upload progress"),
        cls="grid gap-2 w-full max-w-sm"
    )


@with_code
def sizes_example():
    sizes = [("h-1", 15), ("h-2", 40), ("h-3", 70), ("h-4", 90)]
    return Div(
        *[
            Div(
                Span(h, cls="text-xs text-muted-foreground font-mono w-8 shrink-0"),
                Progress(value=v, cls=f"{h} flex-1" if h != "h-2" else "flex-1", aria_label=f"{h} size"),
                cls="flex items-center gap-3"
            )
            for h, v in sizes
        ],
        cls="grid gap-4 w-full max-w-sm"
    )


@with_code
def reactive_example():
    return Div(
        (volume := Signal("prog_vol", 50)),
        Progress(signal=volume, aria_label="Volume"),
        Div(
            Button(
                Icon("lucide:minus", cls="size-4"),
                data_on_click=volume.set((volume - 10).max(0)),
                variant="outline",
                size="icon",
                aria_label="Decrease",
            ),
            Span(
                data_text=volume.round() + "%",
                cls="text-sm font-mono w-10 text-center",
            ),
            Button(
                Icon("lucide:plus", cls="size-4"),
                data_on_click=volume.set((volume + 10).min(100)),
                variant="outline",
                size="icon",
                aria_label="Increase",
            ),
            cls="flex items-center justify-center gap-3"
        ),
        cls="grid gap-3 w-full max-w-sm"
    )


@with_code
def multi_step_example():
    step = Signal("prog_step", 0)
    pct = Signal("prog_pct", 0)
    t1 = Signal("prog_t1", 0)
    t2 = Signal("prog_t2", 0)
    t3 = Signal("prog_t3", 0)

    label = switch([
        (step.eq(1), "Connecting..."),
        (step.eq(2), "Authenticating..."),
        (step.eq(3), "Loading data..."),
        (step.eq(4), "Complete"),
    ], default="Ready")

    start = seq(
        step.set(1), pct.set(15),
        set_timeout([step.set(2), pct.set(45)], 800, store=t1),
        set_timeout([step.set(3), pct.set(75)], 1600, store=t2),
        set_timeout([step.set(4), pct.set(100)], 2400, store=t3),
    )

    reset = seq(
        clear_timeout(t1), clear_timeout(t2), clear_timeout(t3),
        step.set(0), pct.set(0),
    )

    return Div(
        step, pct, t1, t2, t3,
        P(data_text=label, cls="text-sm font-medium"),
        Progress(signal=pct, aria_label="Deployment progress"),
        Div(
            Button("Deploy", data_on_click=start, data_attr_disabled=(step > 0) & (step < 4)),
            Button("Reset", variant="outline", data_on_click=reset, data_attr_disabled=step.eq(0)),
            cls="flex gap-2",
        ),
        cls="grid gap-3 w-full max-w-sm",
    )


EXAMPLES_DATA = [
    {"title": "Default", "description": "A simple progress bar with a static value", "fn": default_example},
    {"title": "With Label", "description": "Progress bar with a label and reactive percentage readout", "fn": with_label_example},
    {"title": "Sizes", "description": "Height variants using Tailwind classes via cls", "fn": sizes_example},
    {"title": "Reactive", "description": "Signal-driven progress bar with controls to update the value", "fn": reactive_example},
    {"title": "Multi-Step Loading", "description": "Sequenced deployment pipeline with step labels [seq(), set_timeout, switch()]", "fn": multi_step_example},
]

API_REFERENCE = build_api_reference(
    main_props=[
        Prop("value", "float | None", "Initial value in the range [0, max_value]. When omitted with Signal object, uses Signal's initial value.", "None"),
        Prop("max_value", "float", "Maximum value that represents 100%", "100"),
        Prop("signal", "str | Signal", "Signal name or Signal object for reactive updates", "auto-generated"),
        Prop("cls", "str", "Additional CSS classes (e.g., 'h-1', 'h-3', 'h-4')", "''"),
    ]
)


def create_progress_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)
