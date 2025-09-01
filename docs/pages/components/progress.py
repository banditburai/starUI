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

from starhtml import Div, P, Icon, Span, H3, Button as HTMLButton
from starhtml.datastar import (
    ds_on_click, ds_show, ds_text, ds_signals, value,
    ds_bind, ds_disabled, ds_on_change, ds_effect, ds_class, ds_style
)
from starui.registry.components.progress import Progress
from starui.registry.components.button import Button
from starui.registry.components.badge import Badge
from starui.registry.components.card import Card, CardHeader, CardContent, CardTitle, CardDescription
from starui.registry.components.separator import Separator
from utils import auto_generate_page
from widgets.component_preview import ComponentPreview


def examples():
    """Generate progress examples using ComponentPreview with tabs."""
    
    # Basic progress
    yield ComponentPreview(
        Div(
            Progress(progress_value=33),
            P("33% Complete", cls="text-sm text-muted-foreground mt-2 text-center"),
            cls="w-full max-w-md mx-auto"
        ),
        '''Progress(progress_value=33)
P("33% Complete")''',
        title="Basic Progress",
        description="Simple progress bar with percentage"
    )
    
    # File upload progress
    yield ComponentPreview(
        Card(
            CardHeader(
                CardTitle("Upload Progress"),
                CardDescription("Uploading 3 files")
            ),
            CardContent(
                Div(
                    Div(
                        Div(
                            Icon("lucide:file-text", cls="h-4 w-4 mr-2"),
                            P("document.pdf", cls="font-medium"),
                            P("2.4 MB", cls="text-sm text-muted-foreground ml-auto"),
                            cls="flex items-center"
                        ),
                        Progress(progress_value=100, signal="file1"),
                        P(
                            Icon("lucide:check-circle", cls="h-4 w-4 mr-1 text-green-500 inline"),
                            "Complete",
                            cls="text-sm text-green-500"
                        ),
                        cls="space-y-2"
                    ),
                    Separator(),
                    Div(
                        Div(
                            Icon("lucide:image", cls="h-4 w-4 mr-2"),
                            P("photo.jpg", cls="font-medium"),
                            P("1.8 MB", cls="text-sm text-muted-foreground ml-auto"),
                            cls="flex items-center"
                        ),
                        Progress(progress_value=65, signal="file2"),
                        P(
                            Span(ds_text("$file2"), cls="font-mono"),
                            "% • 1.2 MB of 1.8 MB",
                            cls="text-sm text-muted-foreground"
                        ),
                        cls="space-y-2"
                    ),
                    Separator(),
                    Div(
                        Div(
                            Icon("lucide:video", cls="h-4 w-4 mr-2"),
                            P("video.mp4", cls="font-medium"),
                            P("45.2 MB", cls="text-sm text-muted-foreground ml-auto"),
                            cls="flex items-center"
                        ),
                        Progress(progress_value=28, signal="file3"),
                        P(
                            Span(ds_text("$file3"), cls="font-mono"),
                            "% • 12.6 MB of 45.2 MB • ",
                            Span("~2 min remaining", cls="text-blue-500"),
                            cls="text-sm text-muted-foreground"
                        ),
                        cls="space-y-2"
                    ),
                    Div(
                        P("Total: 49.4 MB", cls="text-sm text-muted-foreground"),
                        Progress(progress_value=54, signal="total", cls="h-3"),
                        cls="space-y-2 pt-2"
                    ),
                    ds_signals(file1=100, file2=65, file3=28, total=54)
                )
            ),
            cls="max-w-lg"
        ),
        '''Card(
    CardContent(
        Div(
            Icon("lucide:file-text"), P("document.pdf"),
            Progress(progress_value=100),
            P(Icon("lucide:check-circle"), "Complete")
        ),
        Separator(),
        Div(
            Icon("lucide:image"), P("photo.jpg"),
            Progress(progress_value=65),
            P("65% • 1.2 MB of 1.8 MB")
        ),
        Div(
            P("Total: 49.4 MB"),
            Progress(progress_value=54, cls="h-3")
        )
    )
)''',
        title="File Upload",
        description="Multiple file upload with individual and total progress"
    )
    
    # Animated loading progress
    yield ComponentPreview(
        Card(
            CardHeader(
                CardTitle("System Initialization"),
                CardDescription("Starting up services")
            ),
            CardContent(
                Div(
                    Div(
                        P(
                            ds_text("""
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
                            Span(ds_text("$loading_step"), cls="font-mono"),
                            " of 5",
                            cls="text-sm text-muted-foreground mt-2"
                        )
                    ),
                    Button(
                        "Simulate Loading",
                        ds_on_click="""
                            $loading_step = 1; $loading_progress = 20;
                            setTimeout(() => { $loading_step = 2; $loading_progress = 40; }, 1000);
                            setTimeout(() => { $loading_step = 3; $loading_progress = 60; }, 2000);
                            setTimeout(() => { $loading_step = 4; $loading_progress = 80; }, 3000);
                            setTimeout(() => { $loading_step = 5; $loading_progress = 100; }, 4000);
                        """,
                        variant="outline",
                        size="sm",
                        cls="mt-4"
                    ),
                    ds_signals(loading_step=1, loading_progress=20)
                )
            ),
            cls="max-w-md"
        ),
        '''// Animated multi-step progress
Progress(signal="loading_progress")
P(ds_text("$loading_step === 1 ? 'Initializing...' : ..."))
Button("Start", ds_on_click="""
    $loading_step = 1; $loading_progress = 20;
    setTimeout(() => { $loading_step++; $loading_progress += 20; }, 1000);
    // ... more steps
""")''',
        title="Animated Loading",
        description="Multi-step loading with animated progress"
    )
    
    # Skills progress bars
    yield ComponentPreview(
        Card(
            CardHeader(
                CardTitle("Skills Assessment"),
                CardDescription("Technical proficiency levels")
            ),
            CardContent(
                Div(
                    Div(
                        Div(
                            P("JavaScript", cls="font-medium"),
                            Badge("Expert", variant="default", cls="ml-auto"),
                            cls="flex items-center justify-between mb-2"
                        ),
                        Progress(progress_value=90, cls="h-2"),
                        cls="space-y-2"
                    ),
                    Div(
                        Div(
                            P("Python", cls="font-medium"),
                            Badge("Advanced", variant="secondary", cls="ml-auto"),
                            cls="flex items-center justify-between mb-2"
                        ),
                        Progress(progress_value=75, cls="h-2"),
                        cls="space-y-2"
                    ),
                    Div(
                        Div(
                            P("React", cls="font-medium"),
                            Badge("Advanced", variant="secondary", cls="ml-auto"),
                            cls="flex items-center justify-between mb-2"
                        ),
                        Progress(progress_value=80, cls="h-2"),
                        cls="space-y-2"
                    ),
                    Div(
                        Div(
                            P("Docker", cls="font-medium"),
                            Badge("Intermediate", variant="outline", cls="ml-auto"),
                            cls="flex items-center justify-between mb-2"
                        ),
                        Progress(progress_value=60, cls="h-2"),
                        cls="space-y-2"
                    ),
                    Div(
                        Div(
                            P("Machine Learning", cls="font-medium"),
                            Badge("Learning", variant="outline", cls="ml-auto"),
                            cls="flex items-center justify-between mb-2"
                        ),
                        Progress(progress_value=35, cls="h-2"),
                        cls="space-y-2"
                    ),
                    cls="space-y-4"
                )
            ),
            cls="max-w-md"
        ),
        '''Card(
    CardContent(
        Div(
            Div(P("JavaScript"), Badge("Expert")),
            Progress(progress_value=90)
        ),
        Div(
            Div(P("Python"), Badge("Advanced")),
            Progress(progress_value=75)
        ),
        // More skills...
    )
)''',
        title="Skills Assessment",
        description="Multiple progress bars showing proficiency levels"
    )
    
    # Download progress with speed
    yield ComponentPreview(
        Card(
            CardHeader(
                CardTitle("Download Manager"),
                CardDescription("Active downloads")
            ),
            CardContent(
                Div(
                    Div(
                        Div(
                            Icon("lucide:download", cls="h-5 w-5 mr-2 text-blue-500"),
                            Div(
                                P("StarUI-v2.0.zip", cls="font-medium"),
                                P("125 MB", cls="text-sm text-muted-foreground"),
                                cls="flex-1"
                            ),
                            Button(
                                Icon("lucide:pause", cls="h-4 w-4"),
                                variant="ghost",
                                size="sm"
                            ),
                            cls="flex items-center"
                        ),
                        Progress(progress_value=42, signal="download1", cls="h-3"),
                        Div(
                            P(
                                Span(ds_text("$download1"), cls="font-mono"),
                                "% • 52.5 MB of 125 MB",
                                cls="text-sm"
                            ),
                            P(
                                Icon("lucide:arrow-down", cls="h-3 w-3 inline"),
                                " 2.4 MB/s • ~30s remaining",
                                cls="text-sm text-muted-foreground"
                            ),
                            cls="flex justify-between"
                        ),
                        cls="space-y-2 p-3 border rounded-md"
                    ),
                    Div(
                        Div(
                            Icon("lucide:download", cls="h-5 w-5 mr-2 text-blue-500"),
                            Div(
                                P("node_modules.tar.gz", cls="font-medium"),
                                P("892 MB", cls="text-sm text-muted-foreground"),
                                cls="flex-1"
                            ),
                            Button(
                                Icon("lucide:x", cls="h-4 w-4"),
                                variant="ghost",
                                size="sm"
                            ),
                            cls="flex items-center"
                        ),
                        Progress(progress_value=78, signal="download2", cls="h-3"),
                        Div(
                            P(
                                Span(ds_text("$download2"), cls="font-mono"),
                                "% • 696 MB of 892 MB",
                                cls="text-sm"
                            ),
                            P(
                                Icon("lucide:arrow-down", cls="h-3 w-3 inline"),
                                " 5.1 MB/s • ~38s remaining",
                                cls="text-sm text-muted-foreground"
                            ),
                            cls="flex justify-between"
                        ),
                        cls="space-y-2 p-3 border rounded-md"
                    ),
                    Div(
                        P("Queue: 2 files waiting", cls="text-sm text-muted-foreground"),
                        cls="mt-3"
                    ),
                    ds_signals(download1=42, download2=78)
                )
            ),
            cls="max-w-lg"
        ),
        '''Card(
    CardContent(
        Div(
            Icon("lucide:download"), P("StarUI-v2.0.zip"),
            Progress(progress_value=42, cls="h-3"),
            P("42% • 52.5 MB of 125 MB"),
            P(Icon("lucide:arrow-down"), "2.4 MB/s • ~30s")
        ),
        // More downloads...
    )
)''',
        title="Download Manager",
        description="Download progress with speed and time remaining"
    )
    
    # Storage usage
    yield ComponentPreview(
        Card(
            CardHeader(
                CardTitle("Storage Usage"),
                CardDescription("Cloud storage breakdown")
            ),
            CardContent(
                Div(
                    Div(
                        P("Total Usage", cls="text-sm text-muted-foreground"),
                        P("68.4 GB of 100 GB", cls="font-semibold text-lg"),
                        Progress(progress_value=68.4, cls="h-4"),
                        cls="space-y-2"
                    ),
                    Separator(cls="my-4"),
                    Div(
                        Div(
                            Div(
                                Div(cls="w-3 h-3 bg-blue-500 rounded-full"),
                                P("Documents", cls="text-sm"),
                                cls="flex items-center gap-2"
                            ),
                            P("24.2 GB", cls="text-sm text-muted-foreground"),
                            cls="flex items-center justify-between"
                        ),
                        Progress(progress_value=24.2, max_value=100, cls="h-1"),
                        cls="space-y-2"
                    ),
                    Div(
                        Div(
                            Div(
                                Div(cls="w-3 h-3 bg-green-500 rounded-full"),
                                P("Photos", cls="text-sm"),
                                cls="flex items-center gap-2"
                            ),
                            P("18.6 GB", cls="text-sm text-muted-foreground"),
                            cls="flex items-center justify-between"
                        ),
                        Progress(progress_value=18.6, max_value=100, cls="h-1"),
                        cls="space-y-2"
                    ),
                    Div(
                        Div(
                            Div(
                                Div(cls="w-3 h-3 bg-purple-500 rounded-full"),
                                P("Videos", cls="text-sm"),
                                cls="flex items-center gap-2"
                            ),
                            P("15.8 GB", cls="text-sm text-muted-foreground"),
                            cls="flex items-center justify-between"
                        ),
                        Progress(progress_value=15.8, max_value=100, cls="h-1"),
                        cls="space-y-2"
                    ),
                    Div(
                        Div(
                            Div(
                                Div(cls="w-3 h-3 bg-orange-500 rounded-full"),
                                P("Other", cls="text-sm"),
                                cls="flex items-center gap-2"
                            ),
                            P("9.8 GB", cls="text-sm text-muted-foreground"),
                            cls="flex items-center justify-between"
                        ),
                        Progress(progress_value=9.8, max_value=100, cls="h-1"),
                        cls="space-y-2"
                    ),
                    Button(
                        Icon("lucide:hard-drive", cls="h-4 w-4 mr-2"),
                        "Manage Storage",
                        variant="outline",
                        cls="w-full mt-4"
                    ),
                    cls="space-y-3"
                )
            ),
            cls="max-w-md"
        ),
        '''Card(
    CardContent(
        Div(
            P("Total Usage"),
            P("68.4 GB of 100 GB"),
            Progress(progress_value=68.4, cls="h-4")
        ),
        Separator(),
        Div(
            Div(Div(cls="w-3 h-3 bg-blue-500"), P("Documents")),
            P("24.2 GB"),
            Progress(progress_value=24.2, cls="h-1")
        ),
        // More categories...
    )
)''',
        title="Storage Usage",
        description="Storage breakdown with categorized progress bars"
    )
    
    # Course progress
    yield ComponentPreview(
        Card(
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
                            Icon("lucide:check-circle", cls="h-4 w-4 text-green-500"),
                            P("HTML & CSS", cls="text-sm font-medium"),
                            Badge("Complete", variant="secondary", cls="ml-auto"),
                            cls="flex items-center"
                        ),
                        Progress(progress_value=100, cls="h-1 mt-2"),
                        cls="space-y-1"
                    ),
                    Div(
                        Div(
                            Icon("lucide:check-circle", cls="h-4 w-4 text-green-500"),
                            P("JavaScript", cls="text-sm font-medium"),
                            Badge("Complete", variant="secondary", cls="ml-auto"),
                            cls="flex items-center"
                        ),
                        Progress(progress_value=100, cls="h-1 mt-2"),
                        cls="space-y-1"
                    ),
                    Div(
                        Div(
                            Icon("lucide:loader-2", cls="h-4 w-4 text-blue-500 animate-spin"),
                            P("React", cls="text-sm font-medium"),
                            P("3 of 8", cls="text-xs text-muted-foreground ml-auto"),
                            cls="flex items-center"
                        ),
                        Progress(progress_value=37.5, cls="h-1 mt-2"),
                        cls="space-y-1"
                    ),
                    Div(
                        Div(
                            Icon("lucide:lock", cls="h-4 w-4 text-muted-foreground"),
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
            cls="max-w-md"
        ),
        '''Card(
    CardContent(
        Div(
            P("Overall Progress"),
            Progress(progress_value=72, cls="h-3"),
            P("18 of 25 lessons completed")
        ),
        Separator(),
        Div(
            Icon("lucide:check-circle"), P("HTML & CSS"), Badge("Complete"),
            Progress(progress_value=100, cls="h-1")
        ),
        Div(
            Icon("lucide:loader-2"), P("React"), P("3 of 8"),
            Progress(progress_value=37.5, cls="h-1")
        ),
        // More modules...
    )
)''',
        title="Course Progress",
        description="Educational progress tracking with module breakdown"
    )


def create_progress_docs():
    """Create progress documentation page using convention-based approach."""
    
    api_reference = {
        "props": [
            {
                "name": "progress_value",
                "type": "float | None",
                "default": "None",
                "description": "Current progress value (0-100 or 0-max_value)"
            },
            {
                "name": "max_value",
                "type": "float",
                "default": "100",
                "description": "Maximum value for the progress bar"
            },
            {
                "name": "signal",
                "type": "str",
                "default": "auto-generated",
                "description": "Datastar signal name for dynamic updates"
            },
            {
                "name": "cls",
                "type": "str",
                "default": "''",
                "description": "Additional CSS classes (e.g., 'h-4' for height)"
            }
        ]
    }
    
    # Hero example
    hero_example = ComponentPreview(
        Div(
            Progress(progress_value=60),
            P(
                "Processing... ",
                Span("60%", cls="font-bold"),
                cls="text-sm text-muted-foreground mt-2 text-center"
            ),
            cls="w-full max-w-md mx-auto"
        ),
        '''Progress(progress_value=60)
P("Processing... ", Span("60%", cls="font-bold"))''',
        copy_button=True
    )
    
    return auto_generate_page(
        TITLE,
        DESCRIPTION,
        list(examples()),
        cli_command="star add progress",
        api_reference=api_reference,
        hero_example=hero_example,
        component_slug="progress"
    )