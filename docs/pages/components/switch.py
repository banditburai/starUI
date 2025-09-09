"""
Switch component documentation - Convention-based functional approach.
Clean, minimal, and easy to extend.
"""

# Component metadata for auto-discovery
TITLE = "Switch"
DESCRIPTION = "A control that allows the user to toggle between checked and not checked."
CATEGORY = "form"
ORDER = 35
STATUS = "stable"

from starhtml import Div, P, Input, Label, Icon, Span, H2, H3, Form, Code
from starhtml.datastar import (
    ds_on_click, ds_show, ds_text, ds_signals, value,
    ds_bind, ds_disabled, ds_on_change, ds_effect, ds_class
)
from starui.registry.components.switch import Switch, SwitchWithLabel
from starui.registry.components.button import Button
from starui.registry.components.card import Card, CardHeader, CardContent, CardTitle, CardDescription
from starui.registry.components.badge import Badge
from starui.registry.components.separator import Separator
from utils import auto_generate_page
from widgets.component_preview import ComponentPreview


def examples():
    """Generate switch examples using ComponentPreview with tabs."""
    
    # Basic usage
    yield ComponentPreview(
        Div(
            Div(
                Switch(),
                P("Default", cls="text-xs text-muted-foreground mt-2 text-center"),
                cls="flex flex-col items-center"
            ),
            Div(
                Switch(checked=True),
                P("Checked", cls="text-xs text-muted-foreground mt-2 text-center"),
                cls="flex flex-col items-center"
            ),
            Div(
                Switch(disabled=True),
                P("Disabled", cls="text-xs text-muted-foreground mt-2 text-center"),
                cls="flex flex-col items-center"
            ),
            Div(
                Switch(checked=True, disabled=True),
                P("Checked + Disabled", cls="text-xs text-muted-foreground mt-2 text-center"),
                cls="flex flex-col items-center"
            ),
            cls="flex items-start gap-8 justify-center"
        ),
        '''Switch()
Switch(checked=True)
Switch(disabled=True)
Switch(checked=True, disabled=True)''',
        title="Basic Switch",
        description="Different switch states"
    )
    
    # With label
    yield ComponentPreview(
        Div(
            SwitchWithLabel(
                label="Enable notifications",
                helper_text="Receive email and push notifications",
                signal="notifications",
                checked=True
            ),
            P(
                ds_text("$notifications ? 'Notifications are enabled' : 'Notifications are disabled'"),
                cls="text-sm text-muted-foreground mt-3"
            ),
            ds_signals(notifications=True),
            cls="max-w-sm"
        ),
        '''SwitchWithLabel(
    label="Enable notifications",
    helper_text="Receive email and push notifications",
    signal="notifications",
    checked=True
)
P(
    ds_text("$notifications ? 'Notifications enabled' : 'Notifications disabled'"),
    cls="text-sm text-muted-foreground"
)
ds_signals(notifications=True)''',
        title="Switch with Label",
        description="Switch with label, helper text, and reactive feedback"
    )
    
    # Dark mode toggle
    yield ComponentPreview(
        Card(
            CardHeader(
                CardTitle("Appearance"),
                CardDescription("Customize how the interface looks")
            ),
            CardContent(
                Div(
                    Div(
                        Icon("lucide:moon", cls="h-5 w-5 text-muted-foreground"),
                        Div(
                            P("Dark Mode", cls="font-medium"),
                            P("Switch to dark theme", cls="text-sm text-muted-foreground"),
                            cls="flex-1"
                        ),
                        Switch(signal="dark_mode", checked=False),
                        cls="flex items-center gap-3"
                    ),
                    ds_signals(dark_mode=False)
                )
            ),
            cls="max-w-md"
        ),
        '''Card(
    CardContent(
        Div(
            Icon("lucide:moon"),
            Div(
                P("Dark Mode", cls="font-medium"),
                P("Switch to dark theme", cls="text-sm text-muted-foreground")
            ),
            Switch(signal="dark_mode", checked=False),
            cls="flex items-center gap-3"
        ),
        ds_signals(dark_mode=False)
    )
)''',
        title="Dark Mode Toggle",
        description="Theme switcher with icon and description"
    )
    
    # Auto-save feature
    yield ComponentPreview(
        Card(
            CardHeader(
                CardTitle("Document Settings"),
                CardDescription("Configure how your document is saved")
            ),
            CardContent(
                Div(
                    SwitchWithLabel(
                        label="Auto-save",
                        helper_text="Automatically save changes as you type",
                        signal="auto_save",
                        checked=True
                    ),
                    Div(
                        Badge(
                            Icon("lucide:check-circle", cls="h-3 w-3 mr-1"),
                            ds_text("$auto_save ? 'Changes saved automatically' : 'Remember to save manually'"),
                            variant=ds_text("$auto_save ? 'default' : 'secondary'"),
                            cls="w-full justify-center"
                        ),
                        cls="mt-4"
                    ),
                    ds_signals(auto_save=True)
                )
            ),
            cls="max-w-md"
        ),
        '''SwitchWithLabel(
    label="Auto-save",
    helper_text="Automatically save changes as you type",
    signal="auto_save",
    checked=True
)
Badge(
    Icon("lucide:check-circle"),
    ds_text("$auto_save ? 'Changes saved automatically' : 'Remember to save manually'"),
    variant=ds_text("$auto_save ? 'default' : 'secondary'")
)
ds_signals(auto_save=True)''',
        title="Auto-save Feature",
        description="Document setting with status feedback"
    )
    
    # Marketing emails
    yield ComponentPreview(
        Card(
            CardHeader(
                CardTitle("Email Preferences"),
                CardDescription("Manage your email subscriptions")
            ),
            CardContent(
                Form(
                    SwitchWithLabel(
                        label="Marketing emails",
                        helper_text="Product updates, feature announcements, and tips",
                        signal="marketing_emails",
                        checked=False
                    ),
                    Div(
                        Div(
                            Label(
                                "Weekly newsletter",
                                for_="newsletter_switch",
                                cls="text-sm font-medium cursor-pointer"
                            ),
                            Switch(
                                ds_disabled("!$marketing_emails"),
                                signal="newsletter",                                                                
                                checked=False, 
                                id="newsletter_switch",
                                
                            ),
                            cls="flex items-center gap-3"
                        ),
                        P("Our weekly roundup of news and insights", cls="text-sm text-muted-foreground mt-1.5"),
                        cls="space-y-1.5"
                    ),
                    Div(
                        Div(
                            Icon("lucide:info", cls="h-4 w-4 text-muted-foreground flex-shrink-0"),
                            P(
                                "Newsletter requires marketing emails to be enabled",
                                cls="text-sm text-muted-foreground"
                            ),
                            cls="flex items-start gap-2"
                        ),
                        ds_show="!$marketing_emails",  # Show message when marketing emails is off
                        cls="mt-3"
                    ),
                    Button(
                        "Update Preferences",
                        type="submit",
                        cls="w-full mt-4",
                        ds_on_click="event.preventDefault(); alert('Email preferences updated!')"
                    ),
                    ds_signals(marketing_emails=False, newsletter=False),  # Both start as false
                    ds_effect("if (!$marketing_emails) $newsletter = false"),
                    cls="space-y-4"
                )
            ),
            cls="max-w-md"
        ),
        '''SwitchWithLabel(
    label="Marketing emails",
    helper_text="Product updates and announcements",
    signal="marketing_emails"
)
// Newsletter switch with reactive disabled state
Div(
    Label("Weekly newsletter"),
    Switch(
        signal="newsletter",
        **{"data-attr-disabled": "!$marketing_emails"}
    ),
    P("Our weekly roundup of news and insights")
)
ds_effect("if (!$marketing_emails) $newsletter = false")  // Auto-disable newsletter''',
        title="Email Subscriptions",
        description="Dependent switches for email preferences"
    )


def create_switch_docs():
    """Create switch documentation page using convention-based approach."""
    
    api_reference = {
        "props": [
            {
                "name": "checked",
                "type": "bool | None",
                "default": "None",
                "description": "Initial checked state of the switch"
            },
            {
                "name": "signal",
                "type": "str",
                "default": "auto-generated",
                "description": "Datastar signal name for state management"
            },
            {
                "name": "disabled",
                "type": "bool",
                "default": "False",
                "description": "Whether the switch is disabled"
            },
            {
                "name": "required",
                "type": "bool",
                "default": "False",
                "description": "Whether the switch is required"
            },
            {
                "name": "cls",
                "type": "str",
                "default": "''",
                "description": "Additional CSS classes"
            }
        ],
        "helper_components": [
            {
                "name": "SwitchWithLabel",
                "description": "Switch with integrated label and helper/error text",
                "props": [
                    {
                        "name": "label",
                        "type": "str",
                        "description": "Label text for the switch"
                    },
                    {
                        "name": "helper_text",
                        "type": "str | None",
                        "description": "Helper text displayed below the switch"
                    },
                    {
                        "name": "error_text",
                        "type": "str | None",
                        "description": "Error message displayed below the switch"
                    },
                    {
                        "name": "label_cls",
                        "type": "str",
                        "description": "Additional CSS classes for the label"
                    },
                    {
                        "name": "switch_cls",
                        "type": "str",
                        "description": "Additional CSS classes for the switch itself"
                    }
                ]
            }
        ]
    }
    
    # Hero example
    hero_example = ComponentPreview(
        Div(
            SwitchWithLabel(
                label="Enable notifications",
                signal="notifications",
                checked=True
            ),
            cls="flex justify-center"
        ),
        '''SwitchWithLabel(
    label="Enable notifications", 
    signal="notifications",
    checked=True
)''',
        copy_button=True
    )
    
    return auto_generate_page(
        TITLE,
        DESCRIPTION,
        list(examples()),
        cli_command="star add switch",
        api_reference=api_reference,
        hero_example=hero_example,
        component_slug="switch"
    )