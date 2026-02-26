TITLE = "Tooltip"
DESCRIPTION = "A popup that displays information related to an element when the element receives keyboard focus or the mouse hovers over it."
CATEGORY = "ui"
ORDER = 65
STATUS = "stable"

from starhtml import Div, P, Span, Icon, Label, Code, Strong, H3, Signal, set_timeout
from starui.registry.components.tooltip import Tooltip, TooltipTrigger, TooltipContent, TooltipProvider
from starui.registry.components.button import Button
from starui.registry.components.badge import Badge
from starui.registry.components.input import Input as StarInput
from starui.registry.components.avatar import Avatar, AvatarFallback, AvatarImage
from utils import auto_generate_page, with_code, build_api_reference, Component



@with_code
def basic_tooltip_example():
    return Tooltip(
        TooltipTrigger(
            Button("Hover me", variant="outline")
        ),
        TooltipContent(
            "Add to library"
        )
    )


@with_code
def tooltip_positions_example():
    return Div(
        Tooltip(
            TooltipTrigger(
                Button("Top", variant="outline", cls="w-20"),
                delay_duration=200
            ),
            TooltipContent(
                "Tooltip on top",
                side="top"
            )
        ),
        Tooltip(
            TooltipTrigger(
                Button("Right", variant="outline", cls="w-20"),
                delay_duration=200
            ),
            TooltipContent(
                "Tooltip on right",
                side="right"
            )
        ),
        Tooltip(
            TooltipTrigger(
                Button("Bottom", variant="outline", cls="w-20"),
                delay_duration=200
            ),
            TooltipContent(
                "Tooltip on bottom",
                side="bottom"
            )
        ),
        Tooltip(
            TooltipTrigger(
                Button("Left", variant="outline", cls="w-20"),
                delay_duration=200
            ),
            TooltipContent(
                "Tooltip on left",
                side="left"
            )
        ),
        cls="flex gap-2 flex-wrap justify-center"
    )


@with_code
def tooltip_alignment_example():
    return Div(
        Tooltip(
            TooltipTrigger(
                Button("Top Start", variant="outline", cls="w-48"),
                delay_duration=200
            ),
            TooltipContent(
                Div(
                    Icon("lucide:arrow-left", cls="h-4 w-4 inline mr-1"),
                    "Start"
                ),
                side="top",
                align="start",
                cls="w-28"
            )
        ),
        Tooltip(
            TooltipTrigger(
                Button("Top Center", variant="outline", cls="w-48"),
                delay_duration=200
            ),
            TooltipContent(
                Div(
                    Icon("lucide:arrow-up", cls="h-4 w-4 inline mr-1"),
                    "Center"
                ),
                side="top",
                align="center",
                cls="w-28"
            )
        ),
        Tooltip(
            TooltipTrigger(
                Button("Top End", variant="outline", cls="w-48"),
                delay_duration=200
            ),
            TooltipContent(
                Div(
                    "End ",
                    Icon("lucide:arrow-right", cls="h-4 w-4 inline ml-1")
                ),
                side="top",
                align="end",
                cls="w-28"
            )
        ),
        cls="flex gap-4 justify-center flex-wrap"
    )


@with_code
def custom_delays_example():
    return Div(
        Tooltip(
            TooltipTrigger(
                Button("Instant", variant="secondary", size="sm"),
                delay_duration=0
            ),
            TooltipContent("Shows immediately")
        ),
        Tooltip(
            TooltipTrigger(
                Button("Default", variant="secondary", size="sm"),
                delay_duration=700
            ),
            TooltipContent("700ms delay")
        ),
        Tooltip(
            TooltipTrigger(
                Button("Slow", variant="secondary", size="sm"),
                delay_duration=1500
            ),
            TooltipContent("1.5 second delay")
        ),
        Tooltip(
            TooltipTrigger(
                Button("With hide delay", variant="secondary", size="sm"),
                delay_duration=200,
                hide_delay=600
            ),
            TooltipContent("Stays visible briefly")
        ),
        cls="flex gap-2 flex-wrap justify-center"
    )


@with_code
def icon_buttons_example():
    return Div(
        Tooltip(
            TooltipTrigger(
                Button(
                    Icon("lucide:settings", cls="h-4 w-4"),
                    variant="ghost",
                    size="icon"
                ),
                delay_duration=500
            ),
            TooltipContent("Settings")
        ),
        Tooltip(
            TooltipTrigger(
                Button(
                    Icon("lucide:user", cls="h-4 w-4"),
                    variant="ghost",
                    size="icon"
                ),
                delay_duration=500
            ),
            TooltipContent("Profile")
        ),
        Tooltip(
            TooltipTrigger(
                Button(
                    Icon("lucide:bell", cls="h-4 w-4"),
                    variant="ghost",
                    size="icon"
                ),
                delay_duration=500
            ),
            TooltipContent("Notifications")
        ),
        cls="flex gap-1 justify-center"
    )


@with_code
def form_field_tooltip_example():
    return Div(
        Div(
            Label("Email", cls="text-sm font-medium"),
            Div(
                StarInput(
                    type="email",
                    placeholder="Enter your email",
                    cls="pr-10"
                ),
                Div(
                    Tooltip(
                        TooltipTrigger(
                            Icon("lucide:info", cls="h-4 w-4 text-muted-foreground"),
                            delay_duration=300
                        ),
                        TooltipContent(
                            "We'll never share your email with anyone else",
                            cls="max-w-xs"
                        )
                    ),
                    cls="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-auto"
                ),
                cls="relative"
            ),
            cls="space-y-2"
        ),
        cls="max-w-md mx-auto"
    )


@with_code
def rich_content_tooltips_example():
    return Div(
        Tooltip(
            TooltipTrigger(
                Badge("Pro", variant="default"),
                delay_duration=300
            ),
            TooltipContent(
                Div(
                    P(Strong("Pro Features"), cls="font-semibold mb-1"),
                    P("• Unlimited projects", cls="text-xs whitespace-nowrap"),
                    P("• Priority support", cls="text-xs whitespace-nowrap"),
                    P("• Advanced analytics", cls="text-xs whitespace-nowrap")
                )
            )
        ),
        Tooltip(
            TooltipTrigger(
                Button(
                    Icon("lucide:download", cls="mr-2 h-4 w-4"),
                    "Download",
                    variant="outline",
                    size="sm"
                ),
                delay_duration=300
            ),
            TooltipContent(
                Div(
                    Icon("lucide:file-text", cls="h-4 w-4 inline mr-1"),
                    "Download as PDF (",
                    Code("⌘D", cls="text-xs"),
                    ")"
                )
            )
        ),
        Tooltip(
            TooltipTrigger(
                Button(
                    Icon("lucide:trash-2", cls="h-4 w-4"),
                    variant="destructive",
                    size="icon"
                ),
                delay_duration=300
            ),
            TooltipContent(
                Div(
                    Icon("lucide:alert-triangle", cls="h-4 w-4 inline mr-1"),
                    "This action cannot be undone!"
                ),
                cls="bg-destructive text-destructive-foreground [&>div:last-child]:bg-destructive"
            )
        ),
        cls="flex gap-4 items-center justify-center flex-wrap"
    )


@with_code
def keyboard_navigation_example():
    return Div(
        P("Tab through these elements and press Escape to close tooltips:",
          cls="text-sm text-muted-foreground mb-4"),
        Div(
            Tooltip(
                TooltipTrigger(
                    Button("First", variant="outline"),
                    delay_duration=500
                ),
                TooltipContent("Press Tab to navigate")
            ),
            Tooltip(
                TooltipTrigger(
                    Button("Second", variant="outline"),
                    delay_duration=500
                ),
                TooltipContent("Press Escape to close")
            ),
            Tooltip(
                TooltipTrigger(
                    Button("Third", variant="outline"),
                    delay_duration=500
                ),
                TooltipContent("Fully keyboard accessible")
            ),
            cls="flex gap-2 justify-center"
        ),
        cls="text-center"
    )


@with_code
def dynamic_content_example():
    copied = Signal("copied", False)
    clicks = Signal("clicks", 0)

    return Div(
        copied,
        clicks,
        Tooltip(
            TooltipTrigger(
                Button(
                    Icon("lucide:copy", cls="h-4 w-4"),
                    variant="outline",
                    size="icon",
                    data_on_click=[copied.set(True), set_timeout(copied.set(False), 2000)]
                ),
                delay_duration=300
            ),
            TooltipContent(
                Span(data_text=copied.if_('Copied!', 'Click to copy'))
            )
        ),
        Tooltip(
            TooltipTrigger(
                Button(
                    "Click Counter",
                    variant="secondary",
                    data_on_click=clicks.add(1)
                ),
                delay_duration=300
            ),
            TooltipContent(
                Span("Clicked ", Span(data_text=clicks, cls="font-bold"), " times")
            )
        ),
        cls="flex gap-4 justify-center"
    )


@with_code
def custom_styling_example():
    return Div(
        Tooltip(
            TooltipTrigger(
                Button("Dark", variant="outline"),
                delay_duration=200
            ),
            TooltipContent(
                "Dark themed tooltip",
                cls="bg-slate-900 text-white border border-slate-700 [&>div:last-child]:bg-slate-900"
            )
        ),
        Tooltip(
            TooltipTrigger(
                Button("Success", variant="outline", cls="text-green-600 border-green-600"),
                delay_duration=200
            ),
            TooltipContent(
                Div(
                    Icon("lucide:check-circle", cls="h-4 w-4 inline mr-1"),
                    "Operation successful!"
                ),
                cls="bg-green-500 text-white [&>div:last-child]:bg-green-500"
            )
        ),
        Tooltip(
            TooltipTrigger(
                Button("Warning", variant="outline", cls="text-yellow-600 border-yellow-600"),
                delay_duration=200
            ),
            TooltipContent(
                Div(
                    Icon("lucide:alert-triangle", cls="h-4 w-4 inline mr-1"),
                    "Please review"
                ),
                cls="bg-yellow-500 text-white [&>div:last-child]:bg-yellow-500"
            )
        ),
        cls="flex gap-2 justify-center flex-wrap"
    )


@with_code
def truncated_text_example():
    return Div(
        H3("Hover over truncated text:", cls="text-sm font-medium mb-2"),
        Tooltip(
            TooltipTrigger(
                P(
                    "This is a very long text that will be truncated with an ellipsis to demonstrate the tooltip pattern for showing full content when text overflows its container",
                    cls="max-w-xs truncate cursor-help"
                ),
                delay_duration=300
            ),
            TooltipContent(
                "This is a very long text that will be truncated with an ellipsis to demonstrate the tooltip pattern for showing full content when text overflows its container",
                cls="max-w-sm"
            )
        )
    )


@with_code
def avatar_tooltips_example():
    return Div(
        H3("Team members:", cls="text-sm font-medium mb-2"),
        Div(
            Tooltip(
                TooltipTrigger(
                    Avatar(AvatarFallback("JD")),
                    delay_duration=300
                ),
                TooltipContent("John Doe")
            ),
            Tooltip(
                TooltipTrigger(
                    Avatar(AvatarFallback("AS")),
                    delay_duration=300
                ),
                TooltipContent("Alice Smith")
            ),
            Tooltip(
                TooltipTrigger(
                    Avatar(AvatarFallback("BP")),
                    delay_duration=300
                ),
                TooltipContent("Bob Peterson")
            ),
            Tooltip(
                TooltipTrigger(
                    Avatar(AvatarFallback("+3", cls="text-xs")),
                    delay_duration=300
                ),
                TooltipContent("3 more members")
            ),
            cls="flex -space-x-2"
        )
    )



EXAMPLES_DATA = [
    {"fn": basic_tooltip_example, "title": "Basic Tooltip", "description": "Simple tooltip on hover"},
    {"fn": tooltip_positions_example, "title": "Tooltip Positions", "description": "Tooltips can be positioned on any side of the trigger element"},
    {"fn": tooltip_alignment_example, "title": "Tooltip Alignment", "description": "Control tooltip alignment relative to the trigger"},
    {"fn": custom_delays_example, "title": "Custom Delays", "description": "Configure show and hide delays for different UX patterns"},
    {"fn": icon_buttons_example, "title": "Icon Buttons", "description": "Tooltips provide context for icon-only buttons"},
    {"fn": form_field_tooltip_example, "title": "Form Field Helper", "description": "Add helpful information to form inputs"},
    {"fn": rich_content_tooltips_example, "title": "Rich Content", "description": "Tooltips with formatted text, icons, and custom styling"},
    {"fn": keyboard_navigation_example, "title": "Keyboard Navigation", "description": "Tooltips are fully accessible via keyboard with focus triggers and Escape to close"},
    {"fn": dynamic_content_example, "title": "Dynamic Content", "description": "Tooltip content that updates based on application state"},
    {"fn": custom_styling_example, "title": "Custom Styling", "description": "Apply custom themes and styles to tooltips"},
    {"fn": truncated_text_example, "title": "Truncated Text", "description": "Show full content when text is truncated"},
    {"fn": avatar_tooltips_example, "title": "Avatar Group", "description": "Add member names to avatar groups"},
]

API_REFERENCE = build_api_reference(
    components=[
        Component("Tooltip", "Main container component that manages tooltip state"),
        Component("TooltipTrigger", "Element that triggers tooltip display on hover/focus"),
        Component("TooltipContent", "The actual tooltip content with positioning and styling"),
        Component("TooltipProvider", "Optional provider for tooltip configuration (currently unused)"),
    ]
)


def create_tooltip_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)