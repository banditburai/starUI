"""
Card component documentation - Structured content containers.
"""

TITLE = "Card"
DESCRIPTION = "Displays a card with header, content, and footer."
CATEGORY = "layout"
ORDER = 10
STATUS = "stable"

from starhtml import Div, P, Icon, Signal, Span
from starui.registry.components.card import (
    Card, CardHeader, CardTitle, CardDescription, CardAction, CardContent, CardFooter
)
from starui.registry.components.button import Button
from starui.registry.components.badge import Badge
from starui.registry.components.switch import SwitchWithLabel
from starui.registry.components.dropdown_menu import (
    DropdownMenu, DropdownMenuTrigger, DropdownMenuContent,
    DropdownMenuItem, DropdownMenuSeparator,
)
from utils import auto_generate_page, Prop, Component, build_api_reference, with_code


@with_code
def hero_card_example():
    return Card(
        CardHeader(
            CardTitle("Project Status"),
            CardDescription("Track deployment progress across environments"),
        ),
        CardContent(
            P("Production is running v2.4.1 with zero errors in the last 24 hours. Staging has v2.5.0-rc1 queued for review.")
        ),
        CardFooter(
            Button("Deploy"),
            Button("Cancel", variant="outline"),
        ),
        cls="w-full max-w-md",
    )


@with_code
def card_action_example():
    return Card(
        CardHeader(
            CardTitle("Team Members"),
            CardDescription("Manage access and permissions"),
            CardAction(
                DropdownMenu(
                    DropdownMenuTrigger(
                        Icon("lucide:ellipsis", cls="h-4 w-4"),
                        variant="ghost",
                        size="icon",
                        cls="h-7 w-7",
                        aria_label="Team options",
                    ),
                    DropdownMenuContent(
                        DropdownMenuItem(Icon("lucide:user-plus", cls="h-4 w-4"), "Invite member"),
                        DropdownMenuItem(Icon("lucide:settings", cls="h-4 w-4"), "Settings"),
                        DropdownMenuSeparator(),
                        DropdownMenuItem(Icon("lucide:archive", cls="h-4 w-4"), "Archive team"),
                    ),
                )
            ),
        ),
        CardContent(
            P("3 active members with admin, editor, and viewer roles assigned.")
        ),
        cls="w-full max-w-md",
    )


@with_code
def card_dividers_example():
    rows = [
        ("Pro Plan", "$29/mo"),
        ("API Calls", "12,847"),
        ("Storage", "4.2 GB"),
    ]
    return Card(
        CardHeader(
            CardTitle("Billing Summary"),
            CardDescription("Current period usage"),
            cls="border-b",
        ),
        CardContent(
            Div(
                *[
                    Div(
                        Span(label, cls="text-sm"),
                        Span(value, cls="text-sm font-medium"),
                        cls="flex justify-between",
                    )
                    for label, value in rows
                ],
                Div(
                    Span("Total", cls="text-sm font-medium"),
                    Span("$29/mo", cls="text-sm font-bold"),
                    cls="flex justify-between border-t pt-2 mt-2",
                ),
                cls="space-y-2",
            )
        ),
        CardFooter(
            Button("Download Invoice", variant="outline", cls="w-full"),
            cls="border-t",
        ),
        cls="w-full max-w-sm",
    )


@with_code
def card_image_example():
    return Card(
        Div(
            Icon("lucide:image", cls="h-12 w-12 text-muted-foreground/20"),
            cls="bg-muted flex items-center justify-center h-48",
        ),
        CardHeader(
            Div(
                Badge("Featured"),
                Badge("Tutorial", variant="outline"),
                cls="flex gap-2",
            ),
            CardTitle("Getting Started with StarUI"),
            CardDescription("Learn to build accessible interfaces in under 10 minutes."),
        ),
        CardFooter(
            Button(Icon("lucide:book-open", cls="h-4 w-4"), "Read More", variant="outline"),
        ),
        cls="w-full max-w-sm overflow-hidden",
    )


@with_code
def heading_levels_example():
    return Div(
        Card(
            CardHeader(
                CardTitle("Page Title", level="h1", cls="text-2xl"),
                CardDescription("level='h1' for standalone page cards"),
            ),
            CardContent(
                P("Use h1 for the primary card on a page, such as a dashboard hero or profile header.", cls="text-sm text-muted-foreground")
            ),
        ),
        Card(
            CardHeader(
                CardTitle("Section Heading", level="h2", cls="text-xl"),
                CardDescription("level='h2' for section-level cards"),
            ),
            CardContent(
                P("Defaults to h3, suitable for most card grids.", cls="text-sm text-muted-foreground")
            ),
        ),
        cls="grid grid-cols-1 md:grid-cols-2 gap-4 w-full max-w-2xl",
    )


@with_code
def settings_card_example():
    notifications = Signal("card_settings_notifications", True)
    marketing = Signal("card_settings_marketing", False)
    updates = Signal("card_settings_updates", True)

    return Card(
        notifications,
        marketing,
        updates,
        CardHeader(
            CardTitle("Notifications"),
            CardDescription("Choose which notifications you receive"),
            cls="border-b",
        ),
        CardContent(
            Div(
                SwitchWithLabel(
                    label="Push notifications",
                    signal=notifications,
                    helper_text="Receive alerts on your device",
                ),
                SwitchWithLabel(
                    label="Marketing emails",
                    signal=marketing,
                    helper_text="Product news and special offers",
                ),
                SwitchWithLabel(
                    label="Product updates",
                    signal=updates,
                    helper_text="New features and changelog",
                ),
                cls="space-y-4",
            )
        ),
        CardFooter(
            Button("Save preferences", cls="w-full"),
            cls="border-t",
        ),
        cls="w-full max-w-md",
    )


API_REFERENCE = build_api_reference(
    main_props=[
        Prop("level", "Literal['h1', 'h2', 'h3', 'h4', 'h5', 'h6']",
             "HTML heading tag for CardTitle. Choose based on document outline", "'h3'"),
        Prop("cls", "str", "Additional CSS classes (available on all subcomponents)", "''"),
    ],
    components=[
        Component("Card", "Root container with background, border, shadow, and vertical gap"),
        Component("CardHeader", "Contains title, description, and optional action. Auto-detects CardAction to enable two-column grid layout"),
        Component("CardTitle", "Semantic heading element. Use level prop (h1-h6) to set the HTML tag. Defaults to h3"),
        Component("CardDescription", "Muted supporting text below the title"),
        Component("CardAction", "Auto-positioned in the top-right of CardHeader via CSS grid. No extra configuration needed"),
        Component("CardContent", "Main content area with horizontal padding"),
        Component("CardFooter", "Flex-layout action bar. Add border-t class for an opt-in top divider"),
    ]
)


EXAMPLES_DATA = [
    {"fn": hero_card_example, "title": "Card", "description": "Basic anatomy with header, content, and footer"},
    {"fn": card_action_example, "title": "With Card Action", "description": "Dropdown menu auto-positioned in the header via CSS grid"},
    {"fn": card_dividers_example, "title": "With Dividers", "description": "Opt-in border-b and border-t classes for section dividers"},
    {"fn": card_image_example, "title": "With Image", "description": "Media card with badge metadata and icon placeholder"},
    {"fn": heading_levels_example, "title": "Heading Levels", "description": "CardTitle level prop for semantic HTML headings (h1-h6)"},
    {"fn": settings_card_example, "title": "Settings Card", "description": "Interactive card composing switches with border dividers"},
]


def create_card_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)
