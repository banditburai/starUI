TITLE = "Progress"
DESCRIPTION = "Displays an indicator showing the completion progress of a task, typically displayed as a progress bar."
CATEGORY = "ui"
ORDER = 65
STATUS = "stable"

from starhtml import Div, P, Icon, Span, Signal, switch
from starhtml.datastar import set_timeout, seq
from starui.registry.components.progress import Progress
from starui.registry.components.button import Button
from starui.registry.components.card import Card, CardHeader, CardContent, CardTitle, CardDescription
from starui.registry.components.separator import Separator
from utils import auto_generate_page, with_code, Prop, build_api_reference

@with_code
def interactive_controls_example():
    volume = Signal("volume", 50)

    return Card(
        CardHeader(
            CardTitle("Volume Control"),
            CardDescription("Adjust system volume")
        ),
        CardContent(
            Div(
                volume,
                Div(
                    Icon("lucide:volume-2", cls="h-5 w-5 text-muted-foreground mr-3"),
                    Progress(signal=volume, cls="flex-1 h-2"),
                    Span(data_text=volume.round() + "%", cls="text-sm font-mono ml-3 w-10 text-right"),
                    cls="flex items-center"
                ),
                Div(
                    Button(
                        Icon("lucide:minus", cls="h-4 w-4"),
                        data_on_click=volume.set((volume - 10).max(0)),
                        variant="outline",
                        size="sm"
                    ),
                    Button(
                        "Mute",
                        data_on_click=volume.set(0),
                        variant="outline",
                        size="sm"
                    ),
                    Button(
                        Icon("lucide:plus", cls="h-4 w-4"),
                        data_on_click=volume.set((volume + 10).min(100)),
                        variant="outline",
                        size="sm"
                    ),
                    cls="flex gap-2 mt-4"
                )
            )
        ),
        cls="w-full max-w-xl"
    )


@with_code
def file_upload_progress_example():
    file1 = Signal("file1", 100)
    file2 = Signal("file2", 65)
    file3 = Signal("file3", 28)
    total = Signal("total", 54)

    return Card(
        CardHeader(
            CardTitle("Upload Progress"),
            CardDescription("Uploading 3 files")
        ),
        CardContent(
            Div(
                file1, file2, file3, total,
                Div(
                    Div(
                        Icon("lucide:file-text", cls="h-4 w-4 text-muted-foreground"),
                        P("document.pdf", cls="font-medium flex-1 ml-3"),
                        P("2.4 MB", cls="text-sm text-muted-foreground"),
                        cls="flex items-center mb-2"
                    ),
                    Progress(signal=file1),
                    Div(
                        Icon("lucide:check-circle", cls="h-4 w-4 text-green-500"),
                        P("Complete", cls="text-sm text-green-500"),
                        cls="flex items-center gap-1 mt-1"
                    ),
                    cls="pb-3"
                ),
                Separator(cls="my-3"),
                Div(
                    Div(
                        Icon("lucide:image", cls="h-4 w-4 text-muted-foreground"),
                        P("photo.jpg", cls="font-medium flex-1 ml-3"),
                        P("1.8 MB", cls="text-sm text-muted-foreground"),
                        cls="flex items-center mb-2"
                    ),
                    Progress(signal=file2),
                    P(
                        Span(data_text=file2.round(), cls="font-mono"),
                        "% • 1.2 MB of 1.8 MB",
                        cls="text-sm text-muted-foreground mt-1"
                    ),
                    cls="pb-3"
                ),
                Separator(cls="my-3"),
                Div(
                    Div(
                        Icon("lucide:video", cls="h-4 w-4 text-muted-foreground"),
                        P("video.mp4", cls="font-medium flex-1 ml-3"),
                        P("45.2 MB", cls="text-sm text-muted-foreground"),
                        cls="flex items-center mb-2"
                    ),
                    Progress(signal=file3),
                    P(
                        Span(data_text=file3.round(), cls="font-mono"),
                        "% • 12.6 MB of 45.2 MB • ",
                        Span("~2 min remaining", cls="text-blue-500"),
                        cls="text-sm text-muted-foreground mt-1"
                    ),
                    cls="pb-3"
                ),
                Div(
                    P("Total: 49.4 MB", cls="text-sm font-medium mb-2"),
                    Progress(signal=total, cls="h-3"),
                    cls="pt-3 border-t"
                )
            )
        ),
        cls="max-w-lg"
    )


@with_code
def animated_loading_example():
    loading_step = Signal("loading_step", 0)
    loading_progress = Signal("loading_progress", 0)
    is_loading = Signal("is_loading", False)

    def simulate_loading():
        steps = [(1, 20), (2, 40), (3, 60), (4, 80), (5, 100)]
        return [
            is_loading.set(True),
            *[set_timeout(seq(loading_step.set(step), loading_progress.set(progress)), i * 1000)
              for i, (step, progress) in enumerate(steps)],
            set_timeout(seq(loading_step.set(0), loading_progress.set(0), is_loading.set(False)), 5000)
        ]

    return Card(
        CardHeader(
            CardTitle("System Initialization"),
            CardDescription("Starting up services")
        ),
        CardContent(
            Div(
                loading_step, loading_progress, is_loading,
                Div(
                    P(
                        data_text=switch([
                            (loading_step == 0, "Ready to start"),
                            (loading_step == 1, "Initializing database..."),
                            (loading_step == 2, "Loading configuration..."),
                            (loading_step == 3, "Connecting to services..."),
                            (loading_step == 4, "Verifying credentials..."),
                            (loading_step == 5, "System ready!")
                        ]),
                        cls="text-sm font-medium mb-2"
                    ),
                    Progress(signal=loading_progress, cls="h-2"),
                    P(
                        data_text=is_loading.if_(
                            "Step " + loading_step + " of 5",
                            "Click 'Start' to begin"
                        ),
                        cls="text-sm text-muted-foreground mt-2"
                    )
                ),
                Button(
                    data_text=is_loading.if_("Loading...", "Start Loading"),
                    data_on_click=simulate_loading(),
                    data_attr_disabled=is_loading,
                    variant="outline",
                    size="sm",
                    cls="mt-4"
                )
            )
        ),
        cls="w-full max-w-xl"
    )


@with_code
def download_manager_example():
    download1 = Signal("download1", 42)
    download1_paused = Signal("download1_paused", False)
    download2 = Signal("download2", 78)

    return Card(
        CardHeader(
            CardTitle("Download Manager"),
            CardDescription("Active downloads")
        ),
        CardContent(
            Div(
                download1, download1_paused, download2,
                Div(
                    Div(
                        Icon("lucide:download", cls="h-5 w-5 text-blue-500"),
                        Div(
                            P("StarUI-v2.0.zip", cls="font-medium"),
                            P("125 MB", cls="text-xs text-muted-foreground"),
                            cls="flex-1 ml-3"
                        ),
                        Button(
                            Span(Icon("lucide:play", cls="h-4 w-4"), data_show=download1_paused),
                            Span(Icon("lucide:pause", cls="h-4 w-4"), data_show=~download1_paused),
                            data_on_click=download1_paused.toggle(),
                            variant="ghost",
                            size="sm",
                            aria_label=download1_paused.if_("Resume", "Pause")
                        ),
                        cls="flex items-center mb-2"
                    ),
                    Progress(signal=download1, cls="h-3"),
                    Div(
                        Div(
                            Span(data_text=download1.round(), cls="font-semibold"),
                            "%",
                            cls="flex items-center gap-1"
                        ),
                        P(
                            data_text=download1_paused.if_("Paused", "~30s remaining"),
                            cls="text-sm text-muted-foreground"
                        ),
                        cls="flex justify-between items-center mt-2"
                    ),
                    cls="p-4 border rounded-lg"
                ),
                Div(
                    Div(
                        Icon("lucide:download", cls="h-5 w-5 text-blue-500"),
                        Div(
                            P("node_modules.tar.gz", cls="font-medium"),
                            P("892 MB", cls="text-xs text-muted-foreground"),
                            cls="flex-1 ml-3"
                        ),
                        Button(
                            Icon("lucide:x", cls="h-4 w-4"),
                            data_on_click=download2.set(0),
                            variant="ghost",
                            size="sm",
                            aria_label="Cancel download"
                        ),
                        cls="flex items-center mb-2"
                    ),
                    Progress(signal=download2, cls="h-3"),
                    Div(
                        Div(
                            Span(data_text=download2.round(), cls="font-semibold"),
                            "%",
                            cls="flex items-center gap-1"
                        ),
                        P(
                            data_text=(download2 > 0).if_("~38s remaining", "Cancelled"),
                            cls="text-sm text-muted-foreground"
                        ),
                        cls="flex justify-between items-center mt-2"
                    ),
                    data_show=download2 > 0,
                    cls="p-4 border rounded-lg"
                ),
                Div(
                    P(
                        data_text=(download2 > 0).if_("Queue: 2 files waiting", "Queue: 3 files waiting"),
                        cls="text-sm text-muted-foreground"
                    ),
                    cls="mt-3"
                ),
                cls="space-y-3"
            )
        ),
        cls="max-w-2xl"
    )


@with_code
def application_metrics_example():
    metrics = [
        {"icon": "lucide:zap", "label": "API Response Time", "value": 85, "unit": "850 / 1000 ms", "color": "green", "note": "Optimal performance"},
        {"icon": "lucide:cpu", "label": "Memory Usage", "value": 92, "unit": "7.4 / 8 GB", "color": "orange", "note": "Near capacity"},
        {"icon": "lucide:hard-drive", "label": "Storage", "value": 45, "unit": "450 / 1000 GB", "color": "blue", "note": None},
        {"icon": "lucide:database", "label": "DB Connections", "value": 24, "unit": "12 / 50 active", "color": "blue", "note": None},
    ]

    def metric_item(icon, label, value, unit, color, note):
        return Div(
            Div(
                Icon(icon, cls=f"h-5 w-5 text-{color}-500"),
                Div(
                    P(label, cls="font-medium text-sm"),
                    P(unit, cls="text-xs text-muted-foreground"),
                    cls="flex-1 ml-3"
                ),
                Span(f"{value}%", cls="text-sm font-mono"),
                cls="flex items-center mb-2"
            ),
            Progress(value=value, cls="h-2"),
            P(note, cls="text-xs text-muted-foreground mt-1") if note else None,
            cls="space-y-1"
        )

    return Card(
        CardHeader(
            CardTitle("Application Metrics"),
            CardDescription("Real-time performance monitoring")
        ),
        CardContent(
            Div(
                *[metric_item(**m) for m in metrics],
                cls="grid gap-4 sm:grid-cols-2"
            )
        ),
        cls="w-full max-w-3xl"
    )


EXAMPLES_DATA = [
    {"title": "Interactive Controls", "description": "Progress bar with interactive controls for adjusting values", "fn": interactive_controls_example},
    {"title": "File Upload", "description": "Multiple file upload with individual and total progress", "fn": file_upload_progress_example},
    {"title": "Animated Loading", "description": "Multi-step loading with animated progress", "fn": animated_loading_example},
    {"title": "Download Manager", "description": "Download progress with pause/resume and cancel", "fn": download_manager_example},
    {"title": "Application Metrics", "description": "Dashboard showing multiple metrics with helper function and color coding", "fn": application_metrics_example},
]

API_REFERENCE = build_api_reference(
    main_props=[
        Prop("value", "float | None", "Initial value in the range [0, max_value]. When omitted with Signal object, uses Signal's initial value.", "None"),
        Prop("max_value", "float", "Maximum value that represents 100%", "100"),
        Prop("signal", "str | Signal", "Signal name or Signal object for reactive updates", "auto-generated"),
        Prop("cls", "str", "Additional CSS classes (e.g., 'h-2', 'h-3')", "''"),
    ]
)


def create_progress_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)