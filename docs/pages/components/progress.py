"""
Progress component documentation - Convention-based functional approach.
Clean, minimal, and easy to extend.
"""

# Component metadata for auto-discovery
TITLE = "Progress"
DESCRIPTION = "Displays an indicator showing the completion progress of a task, typically displayed as a progress bar."
CATEGORY = "ui"
ORDER = 65
STATUS = "stable"

from starhtml import Div, P, Icon, Span, H3, Button as HTMLButton, Signal, js
from starui.registry.components.progress import Progress
from starui.registry.components.button import Button
from starui.registry.components.badge import Badge
from starui.registry.components.card import Card, CardHeader, CardContent, CardTitle, CardDescription
from starui.registry.components.separator import Separator
from utils import auto_generate_page, with_code, Prop, build_api_reference
from widgets.component_preview import ComponentPreview


# ============================================================================
# EXAMPLE FUNCTIONS (decorated with @with_code for markdown generation)
# ============================================================================

# Interactive progress control
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
                    Progress(signal="volume", cls="flex-1 h-2"),
                    Span(data_text=js("$volume + '%'"), cls="text-sm font-mono ml-3 w-10 text-right"),
                    cls="flex items-center"
                ),
                Div(
                    Button(
                        Icon("lucide:minus", cls="h-4 w-4"),
                        data_on_click=js("$volume = Math.max(0, $volume - 10)"),
                        variant="outline",
                        size="sm"
                    ),
                    Button(
                        "Mute",
                        data_on_click=js("$volume = 0"),
                        variant="outline",
                        size="sm"
                    ),
                    Button(
                        Icon("lucide:plus", cls="h-4 w-4"),
                        data_on_click=js("$volume = Math.min(100, $volume + 10)"),
                        variant="outline",
                        size="sm"
                    ),
                    cls="flex gap-2 mt-4"
                )
            )
        ),
        cls="w-full max-w-xl"
    )


# File upload progress
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
                    Progress(progress_value=100, signal="file1"),
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
                    Progress(progress_value=65, signal="file2"),
                    P(
                        Span(data_text=js("$file2"), cls="font-mono"),
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
                    Progress(progress_value=28, signal="file3"),
                    P(
                        Span(data_text=js("$file3"), cls="font-mono"),
                        "% • 12.6 MB of 45.2 MB • ",
                        Span("~2 min remaining", cls="text-blue-500"),
                        cls="text-sm text-muted-foreground mt-1"
                    ),
                    cls="pb-3"
                ),
                Div(
                    P("Total: 49.4 MB", cls="text-sm font-medium mb-2"),
                    Progress(progress_value=54, signal="total", cls="h-3"),
                    cls="pt-3 border-t"
                )
            )
        ),
        cls="max-w-lg"
    )


# Animated loading progress
@with_code
def animated_loading_example():
    loading_step = Signal("loading_step", 1)
    loading_progress = Signal("loading_progress", 20)

    return Card(
        CardHeader(
            CardTitle("System Initialization"),
            CardDescription("Starting up services")
        ),
        CardContent(
            Div(
                loading_step, loading_progress,
                Div(
                    P(
                        data_text=js("""
                            $loading_step === 1 ? 'Initializing database...' :
                            $loading_step === 2 ? 'Loading configuration...' :
                            $loading_step === 3 ? 'Connecting to services...' :
                            $loading_step === 4 ? 'Verifying credentials...' :
                            'System ready!'
                        """),
                        cls="text-sm font-medium mb-2"
                    ),
                    Progress(signal="loading_progress", cls="h-2"),
                    P(
                        "Step ",
                        Span(data_text=js("$loading_step"), cls="font-mono"),
                        " of 5",
                        cls="text-sm text-muted-foreground mt-2"
                    )
                ),
                Button(
                    "Simulate Loading",
                    data_on_click=js("$loading_step = 1; $loading_progress = 20; setTimeout(() => { $loading_step = 2; $loading_progress = 40; setTimeout(() => { $loading_step = 3; $loading_progress = 60; setTimeout(() => { $loading_step = 4; $loading_progress = 80; setTimeout(() => { $loading_step = 5; $loading_progress = 100; }, 1000); }, 1000); }, 1000); }, 1000);"),
                    variant="outline",
                    size="sm",
                    cls="mt-4"
                )
            )
        ),
        cls="w-full max-w-xl"
    )


# Battery status indicator
@with_code
def system_monitoring_example():
    def create_metric(icon, color, label, value_text, progress_val, note=None, with_separator=False):
        items = [
            Div(
                Div(
                    Icon(icon, cls=f"h-5 w-5 text-{color}-500 mr-3"),
                    P(label, cls="font-medium"),
                    Span(value_text, cls="text-sm font-mono ml-auto"),
                    cls="flex items-center"
                ),
                Progress(progress_value=progress_val, cls="h-2"),
                P(note, cls="text-xs text-muted-foreground mt-1") if note else None,
                cls="space-y-2"
            )
        ]
        if with_separator:
            items.insert(0, Separator(cls="my-3"))
        return items

    return Card(
        CardHeader(
            CardTitle("Device Status"),
            CardDescription("System resource monitoring")
        ),
        CardContent(
            Div(
                *create_metric("lucide:battery-charging", "green", "Battery", "87%", 87,
                              "Charging • 23 min to full"),
                *create_metric("lucide:cpu", "blue", "CPU Usage", "42%", 42,
                              with_separator=True),
                *create_metric("lucide:hard-drive", "purple", "Memory", "6.8/16 GB", 42.5),
                *create_metric("lucide:thermometer", "orange", "Temperature", "65°C", 65,
                              "Normal operating range"),
                cls="space-y-3"
            )
        ),
        cls="w-full max-w-2xl"
    )


# Download progress with speed
@with_code
def download_manager_example():
    download1 = Signal("download1", 42)
    download2 = Signal("download2", 78)

    return Card(
        CardHeader(
            CardTitle("Download Manager"),
            CardDescription("Active downloads")
        ),
        CardContent(
            Div(
                download1, download2,
                Div(
                    Div(
                        Icon("lucide:download", cls="h-5 w-5 text-blue-500"),
                        Div(
                            P("StarUI-v2.0.zip", cls="font-medium"),
                            P("125 MB", cls="text-xs text-muted-foreground"),
                            cls="flex-1 ml-3"
                        ),
                        Button(
                            Icon("lucide:pause", cls="h-4 w-4"),
                            variant="ghost",
                            size="sm"
                        ),
                        cls="flex items-center mb-2"
                    ),
                    Progress(progress_value=42, signal="download1", cls="h-3"),
                    Div(
                        Div(
                            Span(data_text=js("$download1"), cls="font-semibold"),
                            "%",
                            cls="flex items-center gap-1"
                        ),
                        P("~30s remaining", cls="text-sm text-muted-foreground"),
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
                            variant="ghost",
                            size="sm"
                        ),
                        cls="flex items-center mb-2"
                    ),
                    Progress(progress_value=78, signal="download2", cls="h-3"),
                    Div(
                        Div(
                            Span(data_text=js("$download2"), cls="font-semibold"),
                            "%",
                            cls="flex items-center gap-1"
                        ),
                        P("~38s remaining", cls="text-sm text-muted-foreground"),
                        cls="flex justify-between items-center mt-2"
                    ),
                    cls="p-4 border rounded-lg"
                ),
                Div(
                    P("Queue: 2 files waiting", cls="text-sm text-muted-foreground"),
                    cls="mt-3"
                ),
                cls="space-y-3"
            )
        ),
        cls="max-w-2xl"
    )


@with_code
def storage_usage_example():
    storage_categories = [
        ("blue-500", "Documents", "24.2 GB", 24.2),
        ("green-500", "Photos", "18.6 GB", 18.6),
        ("purple-500", "Videos", "15.8 GB", 15.8),
        ("orange-500", "Other", "9.8 GB", 9.8)
    ]

    def create_storage_item(color, category, size, value):
        return Div(
            Div(
                Div(
                    Div(cls=f"w-3 h-3 bg-{color} rounded-full"),
                    P(category, cls="text-sm"),
                    cls="flex items-center gap-2"
                ),
                P(size, cls="text-sm text-muted-foreground"),
                cls="flex items-center justify-between"
            ),
            Progress(progress_value=value, max_value=100, cls="h-1"),
            cls="space-y-2"
        )

    return Card(
        CardHeader(
            CardTitle("Storage Usage"),
            CardDescription("Cloud storage breakdown")
        ),
        CardContent(
            Div(
                Div(
                    Div(
                        Icon("lucide:cloud", cls="h-5 w-5 text-blue-500 mr-3"),
                        P("Total Usage", cls="text-sm text-muted-foreground"),
                        cls="flex items-center mb-2"
                    ),
                    P("68.4 GB of 100 GB", cls="font-semibold text-lg"),
                    Progress(progress_value=68.4, cls="h-4"),
                    P(
                        Badge("31.6 GB", variant="outline"),
                        " available",
                        cls="text-sm mt-2"
                    ),
                    cls="space-y-2"
                ),
                Separator(cls="my-4"),
                *[create_storage_item(color, category, size, value)
                  for color, category, size, value in storage_categories],
                Button(
                    Icon("lucide:hard-drive", cls="h-4 w-4 mr-2"),
                    "Manage Storage",
                    variant="outline",
                    cls="w-full mt-4"
                ),
                cls="space-y-3"
            )
        ),
        cls="w-full max-w-2xl"
    )


# Course progress
@with_code
def course_progress_example():
    return Card(
        CardHeader(
            CardTitle("Course Progress"),
            CardDescription("Web Development Bootcamp")
        ),
        CardContent(
            Div(
                Div(
                    Div(
                        P("Overall Progress", cls="font-medium"),
                        Badge("In Progress", variant="secondary"),
                        cls="flex items-center justify-between mb-2"
                    ),
                    Progress(progress_value=72, cls="h-3"),
                    P("18 of 25 lessons completed", cls="text-sm text-muted-foreground mt-1"),
                    cls="space-y-2"
                ),
                Separator(cls="my-4"),
                Div(
                    Div(
                        Icon("lucide:check-circle", cls="h-4 w-4 text-green-500 mr-3"),
                        P("HTML & CSS", cls="text-sm font-medium"),
                        Badge("Complete", variant="secondary", cls="ml-auto"),
                        cls="flex items-center"
                    ),
                    Progress(progress_value=100, cls="h-1 mt-2"),
                    cls="space-y-1"
                ),
                Div(
                    Div(
                        Icon("lucide:check-circle", cls="h-4 w-4 text-green-500 mr-3"),
                        P("JavaScript", cls="text-sm font-medium"),
                        Badge("Complete", variant="secondary", cls="ml-auto"),
                        cls="flex items-center"
                    ),
                    Progress(progress_value=100, cls="h-1 mt-2"),
                    cls="space-y-1"
                ),
                Div(
                    Div(
                        Icon("lucide:loader-2", cls="h-4 w-4 text-blue-500 animate-spin mr-3"),
                        P("React", cls="text-sm font-medium"),
                        P("3 of 8", cls="text-xs text-muted-foreground ml-auto"),
                        cls="flex items-center"
                    ),
                    Progress(progress_value=37.5, cls="h-1 mt-2"),
                    cls="space-y-1"
                ),
                Div(
                    Div(
                        Icon("lucide:lock", cls="h-4 w-4 text-muted-foreground mr-3"),
                        P("Node.js", cls="text-sm font-medium text-muted-foreground"),
                        Badge("Locked", variant="outline", cls="ml-auto"),
                        cls="flex items-center"
                    ),
                    Progress(progress_value=0, cls="h-1 mt-2"),
                    cls="space-y-1"
                ),
                Button(
                    "Continue Learning",
                    cls="w-full mt-4"
                ),
                cls="space-y-3"
            )
        ),
        cls="w-full max-w-2xl"
    )


# ============================================================================
# MODULE-LEVEL DATA (for markdown API)
# ============================================================================

EXAMPLES_DATA = [
    {"title": "Interactive Controls", "description": "Progress bar with interactive controls for adjusting values", "fn": interactive_controls_example},
    {"title": "File Upload", "description": "Multiple file upload with individual and total progress", "fn": file_upload_progress_example},
    {"title": "Animated Loading", "description": "Multi-step loading with animated progress", "fn": animated_loading_example},
    {"title": "System Monitoring", "description": "Real-time system resource monitoring with progress indicators", "fn": system_monitoring_example},
    {"title": "Download Manager", "description": "Download progress with speed and time remaining", "fn": download_manager_example},
    {"title": "Storage Usage", "description": "Storage breakdown with categorized progress bars", "fn": storage_usage_example},
    {"title": "Course Progress", "description": "Educational progress tracking with module breakdown", "fn": course_progress_example},
]

API_REFERENCE = build_api_reference(
    main_props=[
        Prop("progress_value", "float | None", "Current value in the range [0, max_value]", "None"),
        Prop("max_value", "float", "Maximum value that represents 100%", "100"),
        Prop("signal", "str | None", "Datastar signal name for reactive updates", "auto-generated"),
        Prop("cls", "str", "Additional CSS classes (e.g., 'h-2', 'h-3')", "''"),
    ]
)


def examples():
    """Generate all progress examples."""
    yield ComponentPreview(
        interactive_controls_example(),
        interactive_controls_example.code,
        title="Interactive Controls",
        description="Progress bar with interactive controls for adjusting values"
    )

    yield ComponentPreview(
        file_upload_progress_example(),
        file_upload_progress_example.code,
        title="File Upload",
        description="Multiple file upload with individual and total progress"
    )

    yield ComponentPreview(
        animated_loading_example(),
        animated_loading_example.code,
        title="Animated Loading",
        description="Multi-step loading with animated progress"
    )

    yield ComponentPreview(
        system_monitoring_example(),
        system_monitoring_example.code,
        title="System Monitoring",
        description="Real-time system resource monitoring with progress indicators"
    )

    yield ComponentPreview(
        download_manager_example(),
        download_manager_example.code,
        title="Download Manager",
        description="Download progress with speed and time remaining"
    )

    yield ComponentPreview(
        storage_usage_example(),
        storage_usage_example.code,
        title="Storage Usage",
        description="Storage breakdown with categorized progress bars"
    )

    yield ComponentPreview(
        course_progress_example(),
        course_progress_example.code,
        title="Course Progress",
        description="Educational progress tracking with module breakdown"
    )


# ============================================================================
# DOCUMENTATION PAGE GENERATION
# ============================================================================


def create_progress_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)