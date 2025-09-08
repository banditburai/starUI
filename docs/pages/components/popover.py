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

from starhtml import Div, P, Input, Label, Icon, Span, H2, H3, Form, Code, Ul, Li, A, Img, Strong, Hr
from starhtml.datastar import (
    ds_on_click, ds_show, ds_text, ds_signals, value,
    ds_bind, ds_disabled, ds_on_change, ds_on_input, ds_effect, ds_class, ds_style, toggle
)
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
from starui.registry.components.date_picker import DatePicker, DateTimePicker
from starui.registry.components.toggle_group import ToggleGroup
from utils import auto_generate_page
from widgets.component_preview import ComponentPreview


def examples():
    """Generate popover examples using ComponentPreview with tabs."""
    
    # Basic popover
    yield ComponentPreview(
        Popover(
            PopoverTrigger("Open Popover", variant="outline"),
            PopoverContent(
                Div(
                    H3("About This Feature", cls="font-semibold text-sm mb-2"),
                    P("Popovers are great for displaying contextual information without navigating away from the current page.", cls="text-sm text-muted-foreground mb-3"),
                    P("Click anywhere outside to close.", cls="text-xs text-muted-foreground")
                )
            )
        ),
        '''Popover(
    PopoverTrigger("Open Popover", variant="outline"),
    PopoverContent(
        Div(
            H3("About This Feature", cls="font-semibold text-sm mb-2"),
            P("Popovers are great for displaying contextual information...", 
              cls="text-sm text-muted-foreground mb-3"),
            P("Click anywhere outside to close.", cls="text-xs text-muted-foreground")
        )
    )
)''',
        title="Basic Popover",
        description="Simple popover with text content and automatic positioning"
    )
    
    # Popover with different placements
    yield ComponentPreview(
        Div(
            Popover(
                PopoverTrigger("Top", variant="outline", cls="mr-2"),
                PopoverContent(
                    P("This popover appears above the trigger", cls="text-sm"),
                    side="top"
                )
            ),
            Popover(
                PopoverTrigger("Right", variant="outline", cls="mr-2"),
                PopoverContent(
                    P("This popover appears to the right", cls="text-sm"),
                    side="right"
                )
            ),
            Popover(
                PopoverTrigger("Bottom", variant="outline", cls="mr-2"),
                PopoverContent(
                    P("This popover appears below (default)", cls="text-sm"),
                    side="bottom"
                )
            ),
            Popover(
                PopoverTrigger("Left", variant="outline"),
                PopoverContent(
                    P("This popover appears to the left", cls="text-sm"),
                    side="left"
                )
            ),
            cls="flex flex-wrap gap-2 justify-center"
        ),
        '''# Different placement options
Popover(
    PopoverTrigger("Top", variant="outline"),
    PopoverContent(P("Above the trigger"), side="top")
)

Popover(
    PopoverTrigger("Right", variant="outline"),
    PopoverContent(P("To the right"), side="right")
)

Popover(
    PopoverTrigger("Bottom", variant="outline"),
    PopoverContent(P("Below the trigger"), side="bottom")  # default
)

Popover(
    PopoverTrigger("Left", variant="outline"),
    PopoverContent(P("To the left"), side="left")
)''',
        title="Popover Placement",
        description="Control popover positioning relative to the trigger"
    )
    
    # Profile card popover
    yield ComponentPreview(
        Div(
            P("Click the profile button to see details:", cls="text-sm text-muted-foreground mb-4"),
            Popover(
                PopoverTrigger(
                    Avatar(
                        Img(src="https://github.com/shadcn.png", alt="@shadcn"),
                        size="sm"
                    ),
                    Span("@shadcn", cls="text-sm font-medium ml-2"),
                    variant="ghost",
                    cls="h-auto px-2 py-1.5"
                ),
                PopoverContent(
                    Div(
                        # Header
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
                        # Bio
                        P("Building beautiful and accessible UI components. Creator of ui/shadcn.", 
                          cls="text-sm text-muted-foreground mb-3"),
                        # Stats
                        Div(
                            Div(
                                Strong("1.2k", cls="text-sm"),
                                P("Following", cls="text-xs text-muted-foreground"),
                                cls="text-center"
                            ),
                            Div(
                                Strong("12.5k", cls="text-sm"),
                                P("Followers", cls="text-xs text-muted-foreground"),
                                cls="text-center"
                            ),
                            Div(
                                Strong("342", cls="text-sm"),
                                P("Repos", cls="text-xs text-muted-foreground"),
                                cls="text-center"
                            ),
                            cls="flex justify-around py-2 border-t border-b border-border my-3"
                        ),
                        # Actions
                        Div(
                            Button("Follow", size="sm", cls="flex-1 mr-2"),
                            Button("Message", size="sm", variant="outline", cls="flex-1"),
                            cls="flex gap-2"
                        )
                    ),
                    cls="w-96"
                )
            ),
            cls="flex flex-col items-center"
        ),
        '''Popover(
    PopoverTrigger(
        Avatar(Img(src="https://github.com/shadcn.png", alt="@shadcn"), size="sm"),
        Span("@shadcn", cls="text-sm font-medium ml-2"),
        variant="ghost",
        cls="h-auto px-2 py-1.5"
    ),
    PopoverContent(
        Div(
            # Profile header
            Div(
                Avatar(Img(src="https://github.com/shadcn.png"), size="md"),
                Div(
                    H3("shadcn", cls="font-semibold text-sm"),
                    P("@shadcn", cls="text-xs text-muted-foreground"),
                    Badge("Pro", variant="secondary")
                ),
                cls="flex items-start mb-3"
            ),
            # Bio
            P("Building beautiful and accessible UI components...", 
              cls="text-sm text-muted-foreground mb-3"),
            # Stats and actions
            Div(/* stats */),
            Div(
                Button("Follow", size="sm"),
                Button("Message", size="sm", variant="outline")
            )
        ),
        cls="w-80"
    )
)''',
        title="Profile Card Popover",
        description="Rich profile card with avatar, stats, and action buttons"
    )
    
    # Interactive form popover
    yield ComponentPreview(
        Popover(
            PopoverTrigger(
                Icon("lucide:calendar", cls="h-4 w-4 mr-2"),
                "Schedule Meeting",
                variant="outline"
            ),
            PopoverContent(
                Form(
                    Div(
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
                            placeholder="Select date and time",
                        ),
                        TextareaWithLabel(
                            label="Notes (Optional)",
                            placeholder="Add meeting agenda or notes...",
                            rows=3,
                            signal="meeting_notes"
                        ),
                        # Action buttons
                        Div(
                            Button(
                                "Cancel",
                                ds_on_click("$meeting_title = ''; $meeting_notes = ''"),
                                type="button",
                                variant="outline",
                                size="sm"
                            ),
                            Button(
                                "Schedule",
                                ds_disabled("!$meeting_title || !$meeting_datetime"),
                                ds_on_click("""
                                    if ($meeting_title && $meeting_datetime) {
                                        alert(`Meeting "${$meeting_title}" scheduled for ${new Date($meeting_datetime).toLocaleString()}`);
                                        $meeting_title = '';
                                        $meeting_notes = '';
                                    }
                                """),
                                type="button",
                                size="sm"
                            ),
                            cls="flex justify-end gap-2 pt-4"
                        ),
                        ds_signals(
                            meeting_title=value(""),
                            meeting_duration=value("30"),
                            meeting_datetime=value(""),
                            meeting_notes=value("")
                        ),
                        cls="space-y-4"
                    )
                ),
                cls="w-80"
            )
        ),
        '''Popover(
    PopoverTrigger(
        Icon("lucide:calendar"),
        "Schedule Meeting",
        variant="outline"
    ),
    PopoverContent(
        Form(
            H3("Schedule a Meeting", cls="font-semibold text-sm mb-4"),
            InputWithLabel(
                label="Meeting Title",
                placeholder="Weekly Standup",
                signal="meeting_title",
                required=True
            ),
            SelectWithLabel(
                label="Duration",
                options=[("15", "15 minutes"), ("30", "30 minutes"), ("60", "1 hour")],
                signal="meeting_duration"
            ),
            Label("Date & Time", cls="text-sm font-medium mb-1 block"),
            DateTimePicker(
                signal="meeting_datetime",
                placeholder="Select date and time",
            ),
            TextareaWithLabel(
                label="Notes (Optional)",
                placeholder="Add meeting agenda...",
                signal="meeting_notes"
            ),
            Div(
                Button("Cancel", variant="outline", size="sm"),
                Button(
                    "Schedule",
                    ds_disabled("!$meeting_title || !$meeting_datetime"),
                    ds_on_click("scheduleMeeting()"),
                    size="sm"
                ),
                cls="flex justify-end gap-2 pt-4"
            ),
            ds_signals(meeting_title="", meeting_duration="30", meeting_datetime="")
        ),
        cls="w-80"
    )
)''',
        title="Form Popover",
        description="Interactive form with validation inside a popover"
    )
    
    # Color picker popover
    yield ComponentPreview(
        Div(
            P("Choose a color:", cls="text-sm mb-4"),
            Popover(
                PopoverTrigger(
                    Div(
                        Div(
                            ds_style(background_color="$selected_color"),
                            cls="w-6 h-6 rounded border border-border mr-2"
                        ),
                        Span(ds_text("$selected_color || '#3b82f6'"), cls="text-sm font-mono"),
                        Icon("lucide:chevron-down", cls="h-4 w-4 ml-2"),
                        cls="flex items-center"
                    ),
                    variant="outline",
                    cls="h-auto px-3 py-2"
                ),
                PopoverContent(
                    Div(
                        H3("Choose Color", cls="font-semibold text-sm mb-3"),
                        # Preset colors
                        Div(
                            *[
                                Button(
                                    ds_on_click(f"$selected_color = '{color}'"),
                                    style=f"background-color: {color}; width: 32px; height: 32px; border-radius: 6px;",
                                    variant="ghost",
                                    cls="p-0 hover:scale-110 transition-transform"
                                )
                                for color in [
                                    "#ef4444", "#f97316", "#f59e0b", "#eab308",
                                    "#84cc16", "#22c55e", "#10b981", "#06b6d4",
                                    "#3b82f6", "#6366f1", "#8b5cf6", "#a855f7",
                                    "#d946ef", "#ec4899", "#f43f5e", "#64748b"
                                ]
                            ],
                            cls="grid grid-cols-4 gap-2 mb-4"
                        ),
                        Hr(cls="my-4"),
                        # Custom color input
                        Div(
                            Label("Custom Color:", cls="text-xs font-medium mb-2 block"),
                            UIInput(
                                ds_on_input("$selected_color = evt.target.value"),
                                type="color",
                                cls="w-full h-10 rounded border cursor-pointer",
                                signal="custom_color"
                            )
                        ),
                        ds_signals(
                            selected_color=value("#3b82f6"),
                            custom_color=value("#3b82f6")
                        )
                    ),
                    cls="w-64"
                )
            ),
            # Preview area
            Div(
                P("Preview:", cls="text-sm font-medium mb-2"),
                Div(
                    P("This text uses your selected color", 
                      ds_style(color="$selected_color"),
                      cls="font-medium"),
                    Div(
                        ds_style(background_color="$selected_color"),
                        cls="w-full h-16 rounded border mt-2"
                    )
                ),
                cls="mt-6 p-4 border rounded-lg"
            ),
            cls="max-w-sm"
        ),
        '''Popover(
    PopoverTrigger(
        Div(
            Div(
                ds_style(background_color="$selected_color"),
                cls="w-6 h-6 rounded border mr-2"
            ),
            Span(ds_text("$selected_color"), cls="text-sm font-mono"),
            Icon("lucide:chevron-down"),
            cls="flex items-center"
        ),
        variant="outline"
    ),
    PopoverContent(
        Div(
            H3("Choose Color", cls="font-semibold text-sm mb-3"),
            # Preset color grid
            Div(
                *[Button(
                    style=f"background-color: {color}; width: 32px; height: 32px;",
                    ds_on_click(f"$selected_color = '{color}'")
                ) for color in ["#ef4444", "#f97316", "#f59e0b", "#eab308", ...]],
                cls="grid grid-cols-4 gap-2 mb-4"
            ),
            # Custom color input
            Div(
                Label("Custom Color:"),
                Input(
                    ds_on_input("$selected_color = evt.target.value"),
                    type="color",
                    signal="custom_color"
                )
            ),
            ds_signals(selected_color="#3b82f6", custom_color="#3b82f6")
        ),
        cls="w-64"
    )
)''',
        title="Color Picker Popover",
        description="Interactive color picker with presets and custom color input"
    )
    
    # Settings panel popover
    yield ComponentPreview(
        Div(
            # Mock app header to provide context
            Div(
                Div(
                    H3("My Application", cls="font-semibold text-lg"),
                    P("Dashboard", cls="text-sm text-muted-foreground"),
                    cls="flex-1"
                ),
                Popover(
                    PopoverTrigger(
                        Icon("lucide:settings", cls="h-4 w-4"),
                        variant="ghost",
                        size="sm"
                    ),
                    PopoverContent(
                        Div(
                            # Header
                            H3("Settings", cls="font-semibold text-base mb-4"),
                            # Appearance
                            Div(
                                P("APPEARANCE", cls="text-xs font-medium text-muted-foreground mb-3"),
                                Label("Theme", cls="text-sm font-medium mb-2 block"),
                                ToggleGroup(
                                    ("light", Div(Icon("lucide:sun", cls="h-4 w-4 mr-2"), "Light", cls="flex items-center")),
                                    ("dark", Div(Icon("lucide:moon", cls="h-4 w-4 mr-2"), "Dark", cls="flex items-center")),
                                    ("system", Div(Icon("lucide:laptop", cls="h-4 w-4 mr-2"), "System", cls="flex items-center")),
                                    type="single",
                                    signal="theme_setting",
                                    variant="outline",
                                    cls="grid grid-cols-3 w-full"
                                )
                            ),
                            Separator(cls="my-4"),
                            # Preferences
                            Div(
                                P("PREFERENCES", cls="text-xs font-medium text-muted-foreground mb-3"),
                                # Notifications
                                Div(
                                    Label("Notifications", cls="text-sm font-medium"),
                                    Button(
                                        ds_text("$notifications_enabled ? 'On' : 'Off'"),
                                        ds_on_click(toggle("notifications_enabled")),
                                        size="sm",
                                        variant="outline"
                                    ),
                                    cls="flex items-center justify-between mb-3"
                                ),
                                # Auto-save
                                Div(
                                    Label("Auto-save", cls="text-sm font-medium"),
                                    Button(
                                        ds_text("$autosave_enabled ? 'On' : 'Off'"),
                                        ds_on_click(toggle("autosave_enabled")),
                                        size="sm",
                                        variant="outline"
                                    ),
                                    cls="flex items-center justify-between"
                                )
                            ),
                            Separator(cls="my-4"),
                            # Footer
                            Button(
                                "Manage Account",
                                variant="outline",
                                size="sm",
                                cls="w-full"
                            ),
                            ds_signals(
                                theme_setting=value("system"),
                                theme_setting_value=value("system"),
                                notifications_enabled=value(True),
                                autosave_enabled=value(True)
                            )
                        ),
                        cls="w-96",
                        side="bottom",
                        align="end"
                    )
                ),
                cls="flex items-center justify-between p-4 border rounded-lg bg-card"
            ),
            cls="w-full max-w-md mx-auto"
        ),
        '''Popover(
    PopoverTrigger(
        Icon("lucide:settings"),
        variant="ghost",
        size="icon"
    ),
    PopoverContent(
        Div(
            Div(
                Icon("lucide:settings"),
                H3("Quick Settings", cls="font-semibold text-sm"),
                cls="flex items-center mb-4"
            ),
            # Theme setting
            Div(
                Div(
                    Icon("lucide:palette"),
                    Div(
                        P("Theme", cls="text-sm font-medium"),
                        P("Choose your preferred theme", cls="text-xs text-muted-foreground")
                    ),
                    cls="flex items-center flex-1"
                ),
                SelectWithLabel(
                    label="Theme",
                    options=[("light", "Light"), ("dark", "Dark"), ("system", "System")],
                    signal="theme_setting"
                ),
                cls="flex items-center justify-between py-2"
            ),
            # Toggle settings
            Div(/* notification toggle */),
            Div(/* auto-save toggle */),
            # Action buttons
            Div(
                Button("More Settings", variant="ghost"),
                Button("Sign Out", variant="ghost", cls="text-destructive")
            ),
            ds_signals(theme_setting="system", notifications_enabled=True)
        ),
        cls="w-72",
        side="bottom",
        align="end"
    )
)''',
        title="Settings Panel",  
        description="Clean settings panel with theme selector and preference toggles"
    )
    
    # Help tooltip popover
    yield ComponentPreview(
        Div(
            P("Form fields with help information:", cls="text-sm font-medium mb-4"),
            Div(
                # Input with help popover
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
                                    P("Your API key is used to authenticate requests to our service.", 
                                      cls="text-sm mb-2"),
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
                    UIInput(
                        type="password",
                        placeholder="sk-1234567890abcdef",
                        cls="w-full mt-1",
                        signal="api_key"
                    ),
                    cls="mb-4"
                ),
                # Another field with help
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
                                    P("The webhook URL will receive POST requests when events occur.", 
                                      cls="text-sm mb-3"),
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
                                        Code("https://api.example.com/webhooks", 
                                             cls="text-xs bg-muted px-2 py-1 rounded block")
                                    )
                                ),
                                cls="w-72",
                                side="top"
                            )
                        ),
                        cls="text-sm font-medium flex items-center"
                    ),
                    UIInput(
                        type="url",
                        placeholder="https://api.example.com/webhook",
                        cls="w-full mt-1",
                        signal="webhook_url"
                    )
                )
            ),
            ds_signals(
                api_key=value(""),
                webhook_url=value("")
            ),
            cls="max-w-lg w-full"
        ),
        '''# Form fields with help popovers
Div(
    Label(
        "API Key ",
        Popover(
            PopoverTrigger(
                Icon("lucide:help-circle"),
                variant="ghost",
                size="icon",
                cls="h-4 w-4 p-0 ml-1"
            ),
            PopoverContent(
                Div(
                    H3("API Key Help", cls="font-semibold text-sm mb-2"),
                    P("Your API key is used to authenticate requests...", cls="text-sm mb-2"),
                    Ul(
                        Li("Keep it secret and secure"),
                        Li("Don't share it publicly"),
                        Li("Regenerate if compromised"),
                        cls="list-disc list-inside space-y-1"
                    ),
                    A("Learn more in docs", href="#", cls="text-xs text-blue-600")
                ),
                cls="w-64",
                side="top"
            )
        ),
        cls="text-sm font-medium flex items-center"
    ),
    Input(type="password", placeholder="sk-1234567890abcdef", cls="w-full mt-1")
)''',
        title="Help Tooltip Popovers",
        description="Contextual help information for form fields and UI elements"
    )
    
    # Popover with close button
    yield ComponentPreview(
        Popover(
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
        ),
        '''Popover(
    PopoverTrigger(
        Icon("lucide:info"),
        "Important Notice",
        variant="outline"
    ),
    PopoverContent(
        Div(
            # Close button in top-right corner
            PopoverClose(Icon("lucide:x"), size="sm", variant="ghost"),
            # Content
            Div(
                Icon("lucide:alert-triangle", cls="h-5 w-5 text-amber-500"),
                Div(
                    H3("System Maintenance", cls="font-semibold text-sm mb-1"),
                    P("Scheduled maintenance will occur tonight...", 
                      cls="text-sm text-muted-foreground mb-3")
                ),
                cls="flex items-start"
            ),
            # Action buttons
            Div(
                Button("Got it", size="sm", variant="outline"),
                Button("Learn more", size="sm"),
                cls="flex justify-end"
            )
        )
    )
)''',
        title="Popover with Close Button",
        description="Popover with explicit close button and action buttons"
    )


def create_popover_docs():
    """Create popover documentation page using convention-based approach."""
    
    api_reference = {
        "props": [
            {
                "name": "children",
                "type": "tuple[FT, ...]",
                "description": "PopoverTrigger and PopoverContent components"
            },
            {
                "name": "cls",
                "type": "str",
                "default": "'relative inline-block'",
                "description": "Additional CSS classes for the container"
            }
        ],
        "sub_components": [
            {
                "name": "PopoverTrigger",
                "description": "Button that opens the popover",
                "props": [
                    {
                        "name": "variant",
                        "type": "Literal['default', 'secondary', 'destructive', 'outline', 'ghost', 'link']",
                        "default": "'default'",
                        "description": "Button variant style"
                    },
                    {
                        "name": "cls",
                        "type": "str",
                        "default": "''",
                        "description": "Additional CSS classes"
                    }
                ]
            },
            {
                "name": "PopoverContent",
                "description": "Container for popover content",
                "props": [
                    {
                        "name": "side",
                        "type": "Literal['top', 'right', 'bottom', 'left']",
                        "default": "'bottom'",
                        "description": "Preferred side for popover placement"
                    },
                    {
                        "name": "align",
                        "type": "Literal['start', 'center', 'end']",
                        "default": "'center'",
                        "description": "Alignment relative to the trigger"
                    },
                    {
                        "name": "cls",
                        "type": "str",
                        "default": "''",
                        "description": "Additional CSS classes for content styling"
                    }
                ]
            },
            {
                "name": "PopoverClose",
                "description": "Button that closes the popover",
                "props": [
                    {
                        "name": "variant",
                        "type": "Literal['default', 'secondary', 'destructive', 'outline', 'ghost', 'link']",
                        "default": "'ghost'",
                        "description": "Button variant style"
                    },
                    {
                        "name": "size",
                        "type": "Literal['default', 'sm', 'lg', 'icon']",
                        "default": "'sm'",
                        "description": "Button size"
                    },
                    {
                        "name": "cls",
                        "type": "str",
                        "default": "'absolute right-2 top-2'",
                        "description": "CSS classes for positioning"
                    }
                ]
            }
        ]
    }
    
    # Hero example
    hero_example = ComponentPreview(
        Div(
            Popover(
                PopoverTrigger("Open Popover"),
                PopoverContent(
                    Div(
                        H3("Getting Started", cls="font-semibold text-sm mb-2"),
                        P("Popovers are perfect for displaying rich content without navigating away from the current context.", 
                          cls="text-sm text-muted-foreground mb-3"),
                        Div(
                            Button("Learn More", size="sm", cls="mr-2"),
                            Button("Got it", size="sm", variant="outline")
                        )
                    )
                )
            ),
            cls="flex justify-center py-8"
        ),
        '''Popover(
    PopoverTrigger("Open Popover"),
    PopoverContent(
        Div(
            H3("Getting Started", cls="font-semibold text-sm mb-2"),
            P("Popovers are perfect for displaying rich content...", 
              cls="text-sm text-muted-foreground mb-3"),
            Div(
                Button("Learn More", size="sm"),
                Button("Got it", size="sm", variant="outline")
            )
        )
    )
)''',
        copy_button=True
    )
    
    return auto_generate_page(
        TITLE,
        DESCRIPTION,
        list(examples()),
        cli_command="star add popover",
        api_reference=api_reference,
        hero_example=hero_example,
        component_slug="popover"
    )