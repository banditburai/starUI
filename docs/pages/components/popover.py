"""
Popover component documentation - Convention-based functional approach.
Clean, minimal, and easy to extend.
"""

# Component metadata for auto-discovery
TITLE = "Popover"
DESCRIPTION = "Displays rich content in a portal, triggered by a button. Uses native HTML popover API for accessibility and performance."
CATEGORY = "overlay"
ORDER = 60
STATUS = "stable"

from starhtml import Div, P, Input, Label, Icon, Span, H2, H3, Form, Code, Ul, Li, A, Img, Strong, Hr, Signal, js
from starui.registry.components.popover import (
    Popover, PopoverTrigger, PopoverContent, PopoverClose
)
from starui.registry.components.button import Button
from starui.registry.components.input import Input as UIInput, InputWithLabel
from starui.registry.components.textarea import TextareaWithLabel
from starui.registry.components.card import Card, CardHeader, CardContent, CardTitle, CardDescription
from starui.registry.components.badge import Badge
from starui.registry.components.separator import Separator
from starui.registry.components.select import SelectWithLabel
from starui.registry.components.avatar import Avatar
from starui.registry.components.switch import Switch
from starui.registry.components.date_picker import DateTimePicker
from starui.registry.components.toggle_group import ToggleGroup
from utils import auto_generate_page, with_code, Component, build_api_reference
from widgets.component_preview import ComponentPreview


# ============================================================================
# EXAMPLE FUNCTIONS (decorated with @with_code for markdown generation)
# ============================================================================

# Basic popover
@with_code
def basic_popover_example():
    return Popover(
        PopoverTrigger("Open Popover", variant="outline"),
        PopoverContent(
            Div(
                H3("About This Feature", cls="font-semibold text-sm mb-2"),
                P("Popovers are great for displaying contextual information without navigating away from the current page.", cls="text-sm text-muted-foreground mb-3"),
                P("Click anywhere outside to close.", cls="text-xs text-muted-foreground")
            )
        )
    )


@with_code
def popover_placement_examples():
    placements = [
        ("Top", "top", "This popover appears above the trigger"),
        ("Right", "right", "This popover appears to the right"),
        ("Bottom", "bottom", "This popover appears below (default)"),
        ("Left", "left", "This popover appears to the left")
    ]

    def create_placement_popover(label, side, description):
        return Popover(
            PopoverTrigger(label, variant="outline", cls="mr-2" if label != "Left" else ""),
            PopoverContent(
                P(description, cls="text-sm"),
                side=side
            )
        )

    return Div(
        *[create_placement_popover(label, side, description)
          for label, side, description in placements],
        cls="flex flex-wrap gap-2 justify-center"
    )


# Profile card popover
@with_code
def profile_card_popover_example():
    return Div(
        P("Click on the avatar to see profile details:", cls="text-sm text-muted-foreground mb-4"),
        Popover(
            PopoverTrigger(
                Avatar(
                    Img(src="https://github.com/shadcn.png", alt="@shadcn"),
                    size="sm",
                    cls="mr-2"
                ),
                Span("@shadcn", cls="text-sm font-medium"),
                variant="ghost",
                cls="flex items-center h-auto p-0 hover:bg-transparent"
            ),
            PopoverContent(
                Div(
                    Div(
                        Avatar(
                            Img(src="https://github.com/shadcn.png", alt="@shadcn"),
                            size="md",
                            cls="mr-3"
                        ),
                        Div(
                            H3("shadcn", cls="font-semibold text-sm"),
                            P("@shadcn", cls="text-xs text-muted-foreground"),
                            Badge("Pro", variant="secondary", cls="mt-1")
                        ),
                        cls="flex items-start mb-3"
                    ),
                    P("Building beautiful and accessible UI components. Creator of ui/shadcn.", cls="text-sm text-muted-foreground mb-3"),
                    Div(
                        *[Div(
                            Strong(value, cls="text-sm"),
                            P(label, cls="text-xs text-muted-foreground"),
                            cls="text-center"
                        ) for value, label in [("1.2k", "Following"), ("12.5k", "Followers"), ("342", "Repos")]],
                        cls="flex justify-around py-2 border-t border-b border-border my-3"
                    ),
                    Div(
                        Button("Follow", size="sm", cls="flex-1 mr-2"),
                        Button("Message", size="sm", variant="outline", cls="flex-1"),
                        cls="flex gap-2"
                    )
                ),
                cls="w-80"
            )
        ),
        cls="flex flex-col items-center"
    )


# Interactive form popover
@with_code
def form_popover_example():
    meeting_title = Signal("meeting_title", "")
    meeting_duration = Signal("meeting_duration", "30")
    meeting_datetime = Signal("meeting_datetime", "")
    meeting_notes = Signal("meeting_notes", "")

    return Popover(
        PopoverTrigger(
            Icon("lucide:calendar", cls="h-4 w-4 mr-2"),
            "Schedule Meeting",
            variant="outline"
        ),
        PopoverContent(
            Form(
                Div(
                    meeting_title,
                    meeting_duration,
                    meeting_datetime,
                    meeting_notes,
                    H3("Schedule a Meeting", cls="font-semibold text-sm mb-4"),
                    InputWithLabel(
                        label="Meeting Title",
                        placeholder="Weekly Standup",
                        signal="meeting_title",
                        required=True
                    ),
                    SelectWithLabel(
                        label="Duration",
                        options=[
                            ("15", "15 minutes"),
                            ("30", "30 minutes"),
                            ("60", "1 hour"),
                            ("120", "2 hours")
                        ],
                        value="30",
                        signal="meeting_duration"
                    ),
                    Label("Date & Time", cls="text-sm font-medium mb-1 block"),
                    DateTimePicker(
                        signal="meeting_datetime",
                        placeholder="Select date and time"
                    ),
                    TextareaWithLabel(
                        label="Notes (Optional)",
                        placeholder="Add meeting agenda or notes...",
                        rows=3,
                        signal="meeting_notes"
                    ),
                    Div(
                        Button(
                            "Cancel",
                            type="button",
                            variant="outline",
                            size="sm",
                            data_on_click=js("$meeting_title = ''; $meeting_notes = ''")
                        ),
                        Button(
                            "Schedule",
                            type="button",
                            size="sm",
                            data_attr_disabled=js("!$meeting_title || !$meeting_datetime"),
                            data_on_click=js("""
                                if ($meeting_title && $meeting_datetime) {
                                    alert(`Meeting \"${$meeting_title}\" scheduled for ${new Date($meeting_datetime).toLocaleString()}`);
                                    $meeting_title = '';
                                    $meeting_notes = '';
                                }
                            """)
                        ),
                        cls="flex justify-end gap-2 pt-4"
                    ),
                    cls="space-y-4"
                )
            ),
            cls="w-80"
        )
    )


# Color picker popover
@with_code
def color_picker_popover_example():
    selected_color = Signal("selected_color", "#3b82f6")
    custom_color = Signal("custom_color", "#3b82f6")

    return Div(
        selected_color,
        custom_color,
        P("Choose a color:", cls="text-sm mb-4"),
        Popover(
            PopoverTrigger(
                Div(
                    Div(
                        data_style_background_color=js("$selected_color"),
                        cls="w-6 h-6 rounded border border-border mr-2"
                    ),
                    Span(data_text=js("$selected_color || '#3b82f6'"), cls="text-sm font-mono"),
                    Icon("lucide:chevron-down", cls="h-4 w-4 ml-2"),
                    cls="flex items-center"
                ),
                variant="outline",
                cls="h-auto px-3 py-2"
            ),
            PopoverContent(
                Div(
                    H3("Choose Color", cls="font-semibold text-sm mb-3"),
                    Div(
                        *[
                            Button(
                                data_on_click=js(f"$selected_color = '{color}'"),
                                style=f"background-color: {color}; width: 32px; height: 32px; border-radius: 6px;",
                                variant="ghost",
                                cls="p-0 hover:scale-110 transition-transform"
                            )
                            for color in [
                                "#0d2b45", "#203c56", "#544e68", "#8d697a",
                                "#d08159", "#ffaa5e", "#ffd4a3", "#ffecd6"
                            ]
                        ],
                        cls="grid grid-cols-4 gap-2 mb-4"
                    ),
                    Hr(cls="my-4"),
                    Div(
                        Label("Custom Color:", cls="text-xs font-medium mb-2 block"),
                        Input(
                            data_on_input=js("$custom_color = evt.target.value; $selected_color = evt.target.value"),
                            type="color",
                            cls="w-full h-10 rounded border cursor-pointer",
                            value="#3b82f6",
                        ),
                        data_effect=js("if ($selected_color !== $custom_color) { $custom_color = $selected_color }")
                    )
                ),
                cls="w-64"
            )
        ),
        Div(
            P("Preview:", cls="text-sm font-medium mb-2"),
            Div(
                P("This text uses your selected color", data_style_color=js("$selected_color"), cls="font-medium"),
                Div(data_style_background_color=js("$selected_color"), cls="w-full h-16 rounded border mt-2")
            ),
            cls="mt-6 p-4 border rounded-lg"
        ),
        cls="max-w-sm"
    )


# Settings panel popover
@with_code
def settings_panel_popover_example():
    return Div(
            Div(
                Div(
                    Span("Dashboard", cls="text-lg font-semibold"),
                    Div(
                        Span("Projects", cls="text-sm text-muted-foreground"),
                        Span("Team", cls="text-sm text-muted-foreground"),
                        Span("Analytics", cls="text-sm text-muted-foreground"),
                        cls="flex gap-6"
                    ),
                    cls="flex items-center gap-8"
                ),
                Popover(
                    PopoverTrigger(
                        Icon("lucide:settings", cls="h-4 w-4"),
                        variant="ghost",
                        size="icon"
                    ),
                    PopoverContent(
                        Div(
                            Div(
                                Icon("lucide:settings", cls="h-4 w-4 mr-2"),
                                H3("Settings", cls="font-semibold text-base"),
                                cls="flex items-center mb-4"
                            ),
                            Div(
                                P("APPEARANCE", cls="text-xs font-medium text-muted-foreground mb-3"),
                                Div(
                                    Label("Theme", cls="text-sm font-medium mb-2 block"),
                                    ToggleGroup(
                                        ("light", Div(Icon("lucide:sun", cls="h-4 w-4"), Span("Light", cls="ml-2 text-sm"), cls="flex items-center")),
                                        ("dark", Div(Icon("lucide:moon", cls="h-4 w-4"), Span("Dark", cls="ml-2 text-sm"), cls="flex items-center")),
                                        ("system", Div(Icon("lucide:laptop", cls="h-4 w-4"), Span("System", cls="ml-2 text-sm"), cls="flex items-center")),
                                        signal="theme_setting",
                                        variant="outline",
                                        cls="grid grid-cols-3 w-full"
                                    ),
                                    data_effect=js("$theme_setting_value = 'system'")
                                )
                            ),
                            Separator(cls="my-4"),
                            Div(
                                P("PREFERENCES", cls="text-xs font-medium text-muted-foreground mb-3"),
                                Div(
                                    Label("Notifications", cls="text-sm font-medium"),
                                    Switch(signal="notifications_enabled", checked=True),
                                    cls="flex items-center justify-between mb-3"
                                ),
                                Div(
                                    Label("Auto-save", cls="text-sm font-medium"),
                                    Switch(signal="autosave_enabled", checked=True),
                                    cls="flex items-center justify-between"
                                )
                            ),
                            Separator(cls="my-4"),
                            Button("Manage Account", variant="outline", size="sm", cls="w-full")
                        ),
                        cls="w-96",
                        side="bottom",
                        align="end"
                    )
                ),
                cls="flex items-center justify-between p-4 border rounded-lg bg-card"
            ),
            cls="w-full max-w-md mx-auto"
        )


# Help tooltip popover
@with_code
def help_tooltip_popovers_example():
    return Div(
        P("Form fields with help information:", cls="text-sm font-medium mb-4"),
        Div(
                Div(
                    Label(
                        "API Key ",
                        Popover(
                            PopoverTrigger(
                                Icon("lucide:help-circle", cls="h-3 w-3 text-muted-foreground"),
                                variant="ghost",
                                size="icon",
                                cls="h-4 w-4 p-0 ml-1"
                            ),
                            PopoverContent(
                                Div(
                                    H3("API Key Help", cls="font-semibold text-sm mb-2"),
                                    P("Your API key is used to authenticate requests to our service.", cls="text-sm mb-2"),
                                    Ul(
                                        Li("Keep it secret and secure", cls="text-sm"),
                                        Li("Don't share it publicly", cls="text-sm"),
                                        Li("Regenerate if compromised", cls="text-sm"),
                                        cls="list-disc list-inside space-y-1 text-muted-foreground"
                                    ),
                                    Hr(cls="my-3"),
                                    A(
                                        Icon("lucide:external-link", cls="h-3 w-3 mr-2"),
                                        "Learn more in docs",
                                        href="#",
                                        cls="text-xs text-blue-600 hover:text-blue-800 flex items-center"
                                    )
                                ),
                                cls="w-64",
                                side="top"
                            )
                        ),
                        cls="text-sm font-medium flex items-center"
                    ),
                    Input(type="password", placeholder="sk-1234567890abcdef", cls="w-full mt-1"),
                    cls="mb-4"
                ),
                Div(
                    Label(
                        "Webhook URL ",
                        Popover(
                            PopoverTrigger(
                                Icon("lucide:help-circle", cls="h-3 w-3 text-muted-foreground"),
                                variant="ghost",
                                size="icon",
                                cls="h-4 w-4 p-0 ml-1"
                            ),
                            PopoverContent(
                                Div(
                                    H3("Webhook Configuration", cls="font-semibold text-sm mb-2"),
                                    P("The webhook URL will receive POST requests when events occur.", cls="text-sm mb-3"),
                                    Div(
                                        H3("Requirements:", cls="text-xs font-semibold mb-1"),
                                        Ul(
                                            Li("Must be HTTPS", cls="text-xs"),
                                            Li("Must respond with 200 OK", cls="text-xs"),
                                            Li("Should handle JSON payload", cls="text-xs"),
                                            cls="list-disc list-inside space-y-1 text-muted-foreground mb-3"
                                        )
                                    ),
                                    Div(
                                        H3("Example:", cls="text-xs font-semibold mb-1"),
                                        Code("https://api.example.com/webhooks", cls="text-xs bg-muted px-2 py-1 rounded block")
                                    )
                                ),
                                cls="w-72",
                                side="top"
                            )
                        ),
                        cls="text-sm font-medium flex items-center"
                    ),
                    Input(type="url", placeholder="https://api.example.com/webhook", cls="w-full mt-1")
                )
            ),
            cls="max-w-md"
        )


# Popover with close button
@with_code
def popover_with_close_button_example():
    return Popover(
        PopoverTrigger(
            Icon("lucide:info", cls="h-4 w-4 mr-2"),
            "Important Notice",
            variant="outline"
        ),
        PopoverContent(
            Div(
                PopoverClose(
                    Icon("lucide:x", cls="h-3 w-3"),
                    size="sm",
                    variant="ghost"
                ),
                Div(
                    Icon("lucide:alert-triangle", cls="h-5 w-5 text-amber-500 mr-3"),
                    Div(
                        H3("System Maintenance", cls="font-semibold text-sm mb-1"),
                        P("Scheduled maintenance will occur tonight from 2:00 AM to 4:00 AM EST.",
                          cls="text-sm text-muted-foreground mb-3"),
                        P("During this time, some features may be unavailable.",
                          cls="text-sm text-muted-foreground mb-3")
                    ),
                    cls="flex items-start"
                ),
                Div(
                    Button("Got it", size="sm", variant="outline"),
                    Button("Learn more", size="sm", cls="ml-2"),
                    cls="flex justify-end"
                ),
                cls="space-y-3"
            )
        )
    )


# ============================================================================
# MODULE-LEVEL DATA (for markdown API)
# ============================================================================

EXAMPLES_DATA = [
    {"title": "Basic Popover", "description": "Simple popover with text content and automatic positioning", "code": basic_popover_example.code},
    {"title": "Popover Placement", "description": "Control popover positioning relative to the trigger", "code": popover_placement_examples.code},
    {"title": "Profile Card Popover", "description": "Rich profile card with avatar, stats, and action buttons", "code": profile_card_popover_example.code},
    {"title": "Form Popover", "description": "Interactive form with validation inside a popover", "code": form_popover_example.code},
    {"title": "Color Picker Popover", "description": "Interactive color picker with presets and custom color input", "code": color_picker_popover_example.code},
    {"title": "Settings Panel", "description": "Clean settings panel with theme selector and preference toggles", "code": settings_panel_popover_example.code},
    {"title": "Help Tooltip Popovers", "description": "Contextual help information for form fields and UI elements", "code": help_tooltip_popovers_example.code},
    {"title": "Popover with Close Button", "description": "Popover with explicit close button and action buttons", "code": popover_with_close_button_example.code},
]

API_REFERENCE = build_api_reference(
    components=[
        Component("Popover", "Container that wires a unique signal to trigger and content using the native popover API"),
        Component("PopoverTrigger", "Button that toggles the popover open/closed"),
        Component("PopoverContent", "Floating content positioned via ds_position with side and align controls"),
        Component("PopoverClose", "Helper button that hides the popover; can be placed inside content"),
    ]
)


def examples():
    """Generate all popover examples."""
    yield ComponentPreview(
        basic_popover_example(),
        basic_popover_example.code,
        title="Basic Popover",
        description="Simple popover with text content and automatic positioning"
    )

    yield ComponentPreview(
        popover_placement_examples(),
        popover_placement_examples.code,
        title="Popover Placement",
        description="Control popover positioning relative to the trigger"
    )

    yield ComponentPreview(
        profile_card_popover_example(),
        profile_card_popover_example.code,
        title="Profile Card Popover",
        description="Rich profile card with avatar, stats, and action buttons"
    )

    yield ComponentPreview(
        form_popover_example(),
        form_popover_example.code,
        title="Form Popover",
        description="Interactive form with validation inside a popover"
    )

    yield ComponentPreview(
        color_picker_popover_example(),
        color_picker_popover_example.code,
        title="Color Picker Popover",
        description="Interactive color picker with presets and custom color input"
    )

    yield ComponentPreview(
        settings_panel_popover_example(),
        settings_panel_popover_example.code,
        title="Settings Panel",
        description="Clean settings panel with theme selector and preference toggles"
    )

    yield ComponentPreview(
        help_tooltip_popovers_example(),
        help_tooltip_popovers_example.code,
        title="Help Tooltip Popovers",
        description="Contextual help information for form fields and UI elements"
    )

    yield ComponentPreview(
        popover_with_close_button_example(),
        popover_with_close_button_example.code,
        title="Popover with Close Button",
        description="Popover with explicit close button and action buttons"
    )


# ============================================================================
# DOCUMENTATION PAGE GENERATION
# ============================================================================


def create_popover_docs():
    @with_code
    def hero_popover_example():
        return Div(
            Popover(
                PopoverTrigger("Open Popover"),
                PopoverContent(
                    Div(
                        H3("Getting Started", cls="font-semibold text-sm mb-2"),
                        P("Popovers are perfect for displaying rich content without navigating away from the current context.", cls="text-sm text-muted-foreground mb-3"),
                        Div(Button("Learn More", size="sm", cls="mr-2"), Button("Got it", size="sm", variant="outline"))
                    )
                )
            ),
            cls="flex justify-center py-8"
        )

    hero_example = ComponentPreview(
        hero_popover_example(),
        hero_popover_example.code,
        copy_button=True
    )

    return auto_generate_page(
        TITLE,
        DESCRIPTION,
        list(examples()),
        cli_command="star add popover",
        api_reference=API_REFERENCE,
        hero_example=hero_example,
        component_slug="popover"
    )