"""
Tooltip component documentation - Popup text that appears on hover.
Clean, accessible, and highly customizable.
"""

# Component metadata for auto-discovery
TITLE = "Tooltip"
DESCRIPTION = "A popup that displays information related to an element when the element receives keyboard focus or the mouse hovers over it."
CATEGORY = "ui"
ORDER = 65
STATUS = "stable"

from starhtml import Div, P, Span, Icon, Label, Code, Strong, H3, Signal, js
from starui.registry.components.tooltip import Tooltip, TooltipTrigger, TooltipContent, TooltipProvider
from starui.registry.components.button import Button
from starui.registry.components.badge import Badge
from starui.registry.components.input import Input as StarInput
from starui.registry.components.avatar import Avatar, AvatarFallback, AvatarImage
from utils import auto_generate_page, with_code, build_api_reference, Component
from widgets.component_preview import ComponentPreview


# ============================================================================
# EXAMPLE FUNCTIONS (decorated with @with_code for markdown generation)
# ============================================================================

# Basic tooltip
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


# Tooltip positions
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


# Tooltip alignment
@with_code
def tooltip_alignment_example():
    return Div(
        Tooltip(
            TooltipTrigger(
                Button("Start", variant="outline", cls="w-24"),
                delay_duration=200
            ),
            TooltipContent(
                "Aligned to start",
                side="top",
                align="start"
            )
        ),
        Tooltip(
            TooltipTrigger(
                Button("Center", variant="outline", cls="w-24"),
                delay_duration=200
            ),
            TooltipContent(
                "Aligned to center",
                side="top",
                align="center"
            )
        ),
        Tooltip(
            TooltipTrigger(
                Button("End", variant="outline", cls="w-24"),
                delay_duration=200
            ),
            TooltipContent(
                "Aligned to end",
                side="top",
                align="end"
            )
        ),
        cls="flex gap-4 justify-center"
    )


# Custom delays
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


# Icon buttons with tooltips
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


# Form field with tooltip
@with_code
def form_field_tooltip_example():
    return Div(
        Label("Email", cls="text-sm font-medium"),
        Div(
            StarInput(
                type="email",
                placeholder="Enter your email",
                cls="pr-8"
            ),
            Tooltip(
                TooltipTrigger(
                    Icon("lucide:info", cls="h-4 w-4 text-muted-foreground"),
                    cls="absolute right-2 top-1/2 -translate-y-1/2",
                    delay_duration=300
                ),
                TooltipContent(
                    "We'll never share your email with anyone else"
                )
            ),
            cls="relative"
        ),
        cls="space-y-1 max-w-xs"
    )


# Rich content tooltips
@with_code
def rich_content_tooltips_example():
    return Div(
        # Multi-line tooltip
        Tooltip(
            TooltipTrigger(
                Badge("Pro", variant="default"),
                delay_duration=300
            ),
            TooltipContent(
                Div(
                    Strong("Pro Features"),
                    P("• Unlimited projects", cls="text-xs mt-1"),
                    P("• Priority support", cls="text-xs"),
                    P("• Advanced analytics", cls="text-xs"),
                    cls="space-y-0"
                ),
                cls="max-w-xs"
            )
        ),
        # Tooltip with keyboard shortcut
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
        # Warning tooltip
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
                cls="bg-destructive text-destructive-foreground"
            )
        ),
        cls="flex gap-4 items-center justify-center flex-wrap"
    )


# Keyboard accessible tooltips
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


# Dynamic tooltip content
@with_code
def dynamic_content_example():
    copied = Signal("copied", False)
    clicks = Signal("clicks", 0)

    return Div(
        copied,
        clicks,
        # Copy button with feedback
        Tooltip(
            TooltipTrigger(
                Button(
                    Icon("lucide:copy", cls="h-4 w-4"),
                    variant="outline",
                    size="icon",
                    data_on_click=js("$copied = true; setTimeout(() => $copied = false, 2000)")
                ),
                delay_duration=300
            ),
            TooltipContent(
                Span(data_text=js("$copied ? 'Copied!' : 'Click to copy'"))
            ),
            signal="tooltip_copy"
        ),
        # Click counter
        Tooltip(
            TooltipTrigger(
                Button(
                    "Click Counter",
                    variant="secondary",
                    data_on_click=js("$clicks++")
                ),
                delay_duration=300
            ),
            TooltipContent(
                Span("Clicked ", Span(data_text=js("$clicks"), cls="font-bold"), " times")
            ),
            signal="tooltip_counter"
        ),
        cls="flex gap-4 justify-center"
    )


# Custom styled tooltips
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
                cls="bg-slate-900 text-white border border-slate-700"
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
                cls="bg-green-500 text-white"
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
                cls="bg-yellow-500 text-white"
            )
        ),
        Tooltip(
            TooltipTrigger(
                Button("Glass", variant="outline"),
                delay_duration=200
            ),
            TooltipContent(
                "Glassmorphism effect",
                cls="bg-white/10 backdrop-blur-md border border-white/20 text-white"
            )
        ),
        cls="flex gap-2 justify-center flex-wrap"
    )


# Truncated text with tooltip
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


# Avatar tooltips
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


# ============================================================================
# MODULE-LEVEL DATA (for markdown API)
# ============================================================================

EXAMPLES_DATA = [
    {"title": "Basic Tooltip", "description": "Simple tooltip on hover", "code": basic_tooltip_example.code},
    {"title": "Tooltip Positions", "description": "Tooltips can be positioned on any side of the trigger element", "code": tooltip_positions_example.code},
    {"title": "Tooltip Alignment", "description": "Control tooltip alignment relative to the trigger", "code": tooltip_alignment_example.code},
    {"title": "Custom Delays", "description": "Configure show and hide delays for different UX patterns", "code": custom_delays_example.code},
    {"title": "Icon Buttons", "description": "Tooltips provide context for icon-only buttons", "code": icon_buttons_example.code},
    {"title": "Form Field Helper", "description": "Add helpful information to form inputs", "code": form_field_tooltip_example.code},
    {"title": "Rich Content", "description": "Tooltips with formatted text, icons, and custom styling", "code": rich_content_tooltips_example.code},
    {"title": "Keyboard Navigation", "description": "Tooltips are fully accessible via keyboard with focus triggers and Escape to close", "code": keyboard_navigation_example.code},
    {"title": "Dynamic Content", "description": "Tooltip content that updates based on application state", "code": dynamic_content_example.code},
    {"title": "Custom Styling", "description": "Apply custom themes and styles to tooltips", "code": custom_styling_example.code},
    {"title": "Truncated Text", "description": "Show full content when text is truncated", "code": truncated_text_example.code},
    {"title": "Avatar Group", "description": "Add member names to avatar groups", "code": avatar_tooltips_example.code},
]

API_REFERENCE = build_api_reference(
    components=[
        Component("Tooltip", "Main container component that manages tooltip state"),
        Component("TooltipTrigger", "Element that triggers tooltip display on hover/focus"),
        Component("TooltipContent", "The actual tooltip content with positioning and styling"),
        Component("TooltipProvider", "Optional provider for tooltip configuration (currently unused)"),
    ]
)


def examples():
    """Generate all tooltip examples."""
    yield ComponentPreview(
        basic_tooltip_example(),
        basic_tooltip_example.code,
        title="Basic Tooltip",
        description="Simple tooltip on hover"
    )

    yield ComponentPreview(
        tooltip_positions_example(),
        tooltip_positions_example.code,
        title="Tooltip Positions",
        description="Tooltips can be positioned on any side of the trigger element"
    )

    yield ComponentPreview(
        tooltip_alignment_example(),
        tooltip_alignment_example.code,
        title="Tooltip Alignment",
        description="Control tooltip alignment relative to the trigger"
    )

    yield ComponentPreview(
        custom_delays_example(),
        custom_delays_example.code,
        title="Custom Delays",
        description="Configure show and hide delays for different UX patterns"
    )

    yield ComponentPreview(
        icon_buttons_example(),
        icon_buttons_example.code,
        title="Icon Buttons",
        description="Tooltips provide context for icon-only buttons"
    )

    yield ComponentPreview(
        form_field_tooltip_example(),
        form_field_tooltip_example.code,
        title="Form Field Helper",
        description="Add helpful information to form inputs"
    )

    yield ComponentPreview(
        rich_content_tooltips_example(),
        rich_content_tooltips_example.code,
        title="Rich Content",
        description="Tooltips with formatted text, icons, and custom styling"
    )

    yield ComponentPreview(
        keyboard_navigation_example(),
        keyboard_navigation_example.code,
        title="Keyboard Navigation",
        description="Tooltips are fully accessible via keyboard with focus triggers and Escape to close"
    )

    yield ComponentPreview(
        dynamic_content_example(),
        dynamic_content_example.code,
        title="Dynamic Content",
        description="Tooltip content that updates based on application state"
    )

    yield ComponentPreview(
        custom_styling_example(),
        custom_styling_example.code,
        title="Custom Styling",
        description="Apply custom themes and styles to tooltips"
    )

    yield ComponentPreview(
        truncated_text_example(),
        truncated_text_example.code,
        title="Truncated Text",
        description="Show full content when text is truncated"
    )

    yield ComponentPreview(
        avatar_tooltips_example(),
        avatar_tooltips_example.code,
        title="Avatar Group",
        description="Add member names to avatar groups"
    )


def create_tooltip_docs():
    """Create tooltip documentation page using convention-based approach."""
    from utils import auto_generate_page

    return auto_generate_page(
        TITLE,
        DESCRIPTION,
        list(examples()),
        cli_command="star add tooltip",
        api_reference=API_REFERENCE,
        component_slug="tooltip"
    )