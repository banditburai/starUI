TITLE = "Tooltip"
DESCRIPTION = "A popup that displays information related to an element when the element receives keyboard focus or the mouse hovers over it."
CATEGORY = "ui"
ORDER = 65
STATUS = "stable"

from starhtml import Div, P, Span, Icon, Label, Code
from starui.registry.components.tooltip import Tooltip, TooltipTrigger, TooltipContent
from starui.registry.components.button import Button
from starui.registry.components.input import Input as StarInput
from utils import auto_generate_page, with_code, build_api_reference, Component


@with_code
def basic_tooltip_example():
    return Tooltip(
        TooltipTrigger(
            Button(
                Icon("lucide:plus", cls="h-4 w-4"),
                variant="outline",
                size="icon",
            ),
        ),
        TooltipContent("Add to library"),
    )


@with_code
def toolbar_shortcuts_example():
    return Div(
        Tooltip(
            TooltipTrigger(
                Button(
                    Icon("lucide:bold", cls="h-4 w-4"),
                    variant="ghost",
                    size="icon",
                ),
                delay_duration=200,
            ),
            TooltipContent(
                Span("Bold ", Code("⌘B", cls="ml-1.5 text-muted-foreground")),
            ),
        ),
        Tooltip(
            TooltipTrigger(
                Button(
                    Icon("lucide:italic", cls="h-4 w-4"),
                    variant="ghost",
                    size="icon",
                ),
                delay_duration=200,
            ),
            TooltipContent(
                Span("Italic ", Code("⌘I", cls="ml-1.5 text-muted-foreground")),
            ),
        ),
        Tooltip(
            TooltipTrigger(
                Button(
                    Icon("lucide:underline", cls="h-4 w-4"),
                    variant="ghost",
                    size="icon",
                ),
                delay_duration=200,
            ),
            TooltipContent(
                Span("Underline ", Code("⌘U", cls="ml-1.5 text-muted-foreground")),
            ),
        ),
        Tooltip(
            TooltipTrigger(
                Button(
                    Icon("lucide:link", cls="h-4 w-4"),
                    variant="ghost",
                    size="icon",
                ),
                delay_duration=200,
            ),
            TooltipContent(
                Span("Insert link ", Code("⌘K", cls="ml-1.5 text-muted-foreground")),
            ),
        ),
        cls="flex gap-1 justify-center",
    )


@with_code
def tooltip_positions_example():
    return Div(
        Tooltip(
            TooltipTrigger(
                Button(
                    Icon("lucide:align-left", cls="h-4 w-4"),
                    variant="outline",
                    size="icon",
                ),
                delay_duration=200,
            ),
            TooltipContent("Align left", side="top"),
        ),
        Tooltip(
            TooltipTrigger(
                Button(
                    Icon("lucide:align-center", cls="h-4 w-4"),
                    variant="outline",
                    size="icon",
                ),
                delay_duration=200,
            ),
            TooltipContent("Align center", side="right"),
        ),
        Tooltip(
            TooltipTrigger(
                Button(
                    Icon("lucide:align-right", cls="h-4 w-4"),
                    variant="outline",
                    size="icon",
                ),
                delay_duration=200,
            ),
            TooltipContent("Align right", side="bottom"),
        ),
        Tooltip(
            TooltipTrigger(
                Button(
                    Icon("lucide:align-justify", cls="h-4 w-4"),
                    variant="outline",
                    size="icon",
                ),
                delay_duration=200,
            ),
            TooltipContent("Justify", side="left"),
        ),
        cls="flex gap-2 justify-center",
    )


@with_code
def disabled_button_example():
    return Div(
        Tooltip(
            TooltipTrigger(
                Button("Deploy", disabled=True),
                delay_duration=300,
            ),
            TooltipContent("Connect a Git repository first"),
        ),
        Tooltip(
            TooltipTrigger(
                Button("Merge", disabled=True, variant="outline"),
                delay_duration=300,
            ),
            TooltipContent("Resolve 2 conflicts before merging"),
        ),
        cls="flex gap-4 justify-center",
    )


@with_code
def form_field_tooltip_example():
    return Div(
        Div(
            Label("API Key", cls="text-sm font-medium"),
            Div(
                StarInput(
                    type="text",
                    placeholder="sk_live_...",
                    cls="pr-10 font-mono text-sm",
                ),
                Div(
                    Tooltip(
                        TooltipTrigger(
                            Icon(
                                "lucide:info",
                                cls="h-4 w-4 text-muted-foreground",
                            ),
                            delay_duration=300,
                        ),
                        TooltipContent(
                            "Starts with sk_live_ followed by 32 characters",
                        ),
                    ),
                    cls="absolute right-3 inset-y-0 flex items-center pointer-events-auto",
                ),
                cls="relative",
            ),
            cls="space-y-2",
        ),
        cls="max-w-md mx-auto",
    )


@with_code
def truncated_text_example():
    commit_msg = "fix: resolve race condition in WebSocket reconnection handler when multiple tabs are open simultaneously"
    return Tooltip(
        TooltipTrigger(
            P(
                commit_msg,
                cls="max-w-xs truncate cursor-help text-sm font-mono",
            ),
            delay_duration=300,
        ),
        TooltipContent(commit_msg),
    )


@with_code
def status_indicators_example():
    def status_dot(color, label, detail):
        return Tooltip(
            TooltipTrigger(
                Div(
                    Div(cls=f"h-2.5 w-2.5 rounded-full {color}"),
                    Span(label, cls="text-sm"),
                    cls="flex items-center gap-2",
                ),
                delay_duration=200,
            ),
            TooltipContent(detail),
        )

    return Div(
        status_dot("bg-green-500", "Production", "Deployed 4m ago by Sarah Chen"),
        status_dot("bg-yellow-500", "Staging", "Building from commit a3f2c91"),
        status_dot("bg-red-500", "Preview", "Build failed at 2:15 PM"),
        cls="flex flex-col gap-3 items-start mx-auto w-fit",
    )


EXAMPLES_DATA = [
    {
        "fn": basic_tooltip_example,
        "title": "Basic Tooltip",
        "description": "Label an icon button with a tooltip on hover",
    },
    {
        "fn": toolbar_shortcuts_example,
        "title": "Toolbar with Shortcuts",
        "description": "Icon buttons with keyboard shortcut hints",
    },
    {
        "fn": tooltip_positions_example,
        "title": "Tooltip Positions",
        "description": "Control which side the tooltip appears on with the side prop",
    },
    {
        "fn": disabled_button_example,
        "title": "Disabled Button",
        "description": "Explain why a button is disabled",
    },
    {
        "fn": form_field_tooltip_example,
        "title": "Form Field Helper",
        "description": "Add format hints to form inputs",
    },
    {
        "fn": truncated_text_example,
        "title": "Truncated Text",
        "description": "Reveal the full content of truncated text on hover",
    },
    {
        "fn": status_indicators_example,
        "title": "Status Indicators",
        "description": "Add context to status dots and deployment states",
    },
]

API_REFERENCE = build_api_reference(
    components=[
        Component(
            "Tooltip", "Main container component that manages tooltip state"
        ),
        Component(
            "TooltipTrigger",
            "Element that triggers tooltip display on hover/focus",
        ),
        Component(
            "TooltipContent",
            "The actual tooltip content with positioning and styling",
        ),
        Component(
            "TooltipProvider",
            "Optional provider for tooltip configuration (currently unused)",
        ),
    ]
)


def create_tooltip_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)
