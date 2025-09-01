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
    ds_bind, ds_disabled, ds_on_change, ds_effect, ds_class, toggle
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
            Switch(),
            Switch(checked=True, cls="ml-4"),
            Switch(disabled=True, cls="ml-4"),
            Switch(checked=True, disabled=True, cls="ml-4"),
            P(
                "States: default, checked, disabled, checked+disabled",
                cls="text-sm text-muted-foreground mt-4"
            ),
            cls="flex items-center"
        ),
        '''Switch()
Switch(checked=True)
Switch(disabled=True)
Switch(checked=True, disabled=True)''',
        title="Basic Switch",
        description="Different switch states"
    )
    
    # With labels
    yield ComponentPreview(
        Div(
            SwitchWithLabel(
                label="Airplane Mode",
                signal="airplane"
            ),
            SwitchWithLabel(
                label="Wi-Fi",
                checked=True,
                signal="wifi",
                helper_text="Connect to available networks"
            ),
            SwitchWithLabel(
                label="Bluetooth",
                signal="bluetooth",
                helper_text="Allow Bluetooth connections",
                disabled=True
            ),
            cls="space-y-4 max-w-sm"
        ),
        '''SwitchWithLabel(
    label="Airplane Mode",
    signal="airplane"
)
SwitchWithLabel(
    label="Wi-Fi",
    checked=True,
    signal="wifi",
    helper_text="Connect to available networks"
)
SwitchWithLabel(
    label="Bluetooth",
    signal="bluetooth",
    helper_text="Allow Bluetooth connections",
    disabled=True
)''',
        title="Switch with Labels",
        description="Switches with labels and helper text"
    )
    
    # Notification settings
    yield ComponentPreview(
        Card(
            CardHeader(
                CardTitle("Notification Preferences"),
                CardDescription("Choose how you want to be notified")
            ),
            CardContent(
                Div(
                    Div(
                        Div(
                            Icon("lucide:mail", cls="h-5 w-5 text-muted-foreground"),
                            Div(
                                P("Email Notifications", cls="font-medium"),
                                P("Receive email updates about your account", cls="text-sm text-muted-foreground"),
                                cls="flex-1"
                            ),
                            Switch(signal="email_notif", checked=True),
                            cls="flex items-center gap-3"
                        ),
                        cls="pb-4"
                    ),
                    Separator(),
                    Div(
                        Div(
                            Icon("lucide:smartphone", cls="h-5 w-5 text-muted-foreground"),
                            Div(
                                P("Push Notifications", cls="font-medium"),
                                P("Get instant updates on your mobile device", cls="text-sm text-muted-foreground"),
                                cls="flex-1"
                            ),
                            Switch(signal="push_notif", checked=True),
                            cls="flex items-center gap-3"
                        ),
                        cls="py-4"
                    ),
                    Separator(),
                    Div(
                        Div(
                            Icon("lucide:message-square", cls="h-5 w-5 text-muted-foreground"),
                            Div(
                                P("SMS Notifications", cls="font-medium"),
                                P("Receive text messages for important alerts", cls="text-sm text-muted-foreground"),
                                cls="flex-1"
                            ),
                            Switch(signal="sms_notif"),
                            cls="flex items-center gap-3"
                        ),
                        cls="py-4"
                    ),
                    Separator(),
                    Div(
                        Div(
                            Icon("lucide:bell-off", cls="h-5 w-5 text-muted-foreground"),
                            Div(
                                P("Do Not Disturb", cls="font-medium"),
                                P("Pause all notifications temporarily", cls="text-sm text-muted-foreground"),
                                cls="flex-1"
                            ),
                            Switch(signal="dnd_mode"),
                            cls="flex items-center gap-3"
                        ),
                        cls="pt-4"
                    ),
                    Div(
                        Badge(
                            ds_text("$dnd_mode ? 'All notifications paused' : ([$email_notif, $push_notif, $sms_notif].filter(Boolean).length + ' active channels')"),
                            variant="secondary",
                            cls="w-full justify-center"
                        ),
                        cls="mt-4"
                    ),
                    ds_signals(email_notif=True, push_notif=True, sms_notif=False, dnd_mode=False)
                )
            ),
            cls="max-w-lg"
        ),
        '''Card(
    CardContent(
        Div(
            Icon("lucide:mail"),
            Div(
                P("Email Notifications", cls="font-medium"),
                P("Receive email updates", cls="text-sm text-muted-foreground")
            ),
            Switch(signal="email_notif", checked=True),
            cls="flex items-center gap-3"
        ),
        Separator(),
        // More notification options...
        Badge(
            ds_text("active channels count"),
            variant="secondary"
        ),
        ds_signals(email_notif=True, push_notif=True, sms_notif=False)
    )
)''',
        title="Notification Settings",
        description="Rich notification preferences with icons and descriptions"
    )
    
    # Feature flags
    yield ComponentPreview(
        Card(
            CardHeader(
                CardTitle("Feature Flags"),
                CardDescription("Enable experimental features")
            ),
            CardContent(
                Div(
                    SwitchWithLabel(
                        label="Beta Features",
                        helper_text="Try new features before they're released",
                        signal="beta",
                        checked=False
                    ),
                    SwitchWithLabel(
                        label="Developer Mode",
                        helper_text="Show advanced debugging tools",
                        signal="dev_mode",
                        disabled=ds_show("!$beta")  # Can only enable if beta is on
                    ),
                    SwitchWithLabel(
                        label="Analytics",
                        helper_text="Help improve the app by sharing usage data",
                        signal="analytics",
                        checked=True
                    ),
                    SwitchWithLabel(
                        label="Auto-Update",
                        helper_text="Automatically install updates when available",
                        signal="auto_update",
                        checked=True
                    ),
                    Div(
                        P(
                            Icon("lucide:alert-triangle", cls="h-4 w-4 inline mr-1"),
                            "Beta features may be unstable",
                            ds_show="$beta",
                            cls="text-sm text-orange-500"
                        ),
                        P(
                            Icon("lucide:info", cls="h-4 w-4 inline mr-1"),
                            "Developer mode requires beta features",
                            ds_show="!$beta && $dev_mode === false",
                            cls="text-sm text-muted-foreground"
                        ),
                        cls="mt-4 space-y-2"
                    ),
                    ds_signals(beta=False, dev_mode=False, analytics=True, auto_update=True),
                    ds_effect("if (!$beta) $dev_mode = false"),  # Auto-disable dev mode if beta is off
                    cls="space-y-4"
                )
            ),
            cls="max-w-md"
        ),
        '''SwitchWithLabel(
    label="Beta Features",
    helper_text="Try new features before release",
    signal="beta"
)
SwitchWithLabel(
    label="Developer Mode",
    helper_text="Show debugging tools",
    signal="dev_mode",
    disabled=ds_show("!$beta")  // Only available in beta
)
ds_effect("if (!$beta) $dev_mode = false")  // Auto-disable when beta is off''',
        title="Feature Flags",
        description="Dependent switches with conditional logic"
    )
    
    # Privacy settings
    yield ComponentPreview(
        Card(
            CardHeader(
                CardTitle("Privacy Settings"),
                CardDescription("Control your data and privacy")
            ),
            CardContent(
                Form(
                    Div(
                        H3("Data Collection", cls="text-sm font-semibold mb-3"),
                        SwitchWithLabel(
                            label="Usage Analytics",
                            helper_text="Anonymous usage statistics",
                            signal="usage_analytics",
                            checked=True
                        ),
                        SwitchWithLabel(
                            label="Crash Reports",
                            helper_text="Send crash reports to help fix bugs",
                            signal="crash_reports",
                            checked=True
                        ),
                        SwitchWithLabel(
                            label="Personalization",
                            helper_text="Use your data to personalize content",
                            signal="personalization"
                        ),
                        cls="space-y-3"
                    ),
                    Separator(cls="my-4"),
                    Div(
                        H3("Visibility", cls="text-sm font-semibold mb-3"),
                        SwitchWithLabel(
                            label="Public Profile",
                            helper_text="Make your profile visible to everyone",
                            signal="public_profile"
                        ),
                        SwitchWithLabel(
                            label="Show Online Status",
                            helper_text="Let others see when you're online",
                            signal="online_status",
                            disabled=ds_show("!$public_profile")
                        ),
                        SwitchWithLabel(
                            label="Activity Feed",
                            helper_text="Share your activity with followers",
                            signal="activity_feed",
                            disabled=ds_show("!$public_profile")
                        ),
                        cls="space-y-3"
                    ),
                    Button(
                        "Save Privacy Settings",
                        type="submit",
                        cls="w-full mt-6",
                        ds_on_click="event.preventDefault(); alert('Privacy settings saved!')"
                    ),
                    ds_signals(
                        usage_analytics=True,
                        crash_reports=True,
                        personalization=False,
                        public_profile=False,
                        online_status=False,
                        activity_feed=False
                    ),
                    ds_effect("if (!$public_profile) { $online_status = false; $activity_feed = false; }")
                )
            ),
            cls="max-w-md"
        ),
        '''Form(
    Div(
        H3("Data Collection"),
        SwitchWithLabel(label="Usage Analytics", signal="usage_analytics"),
        SwitchWithLabel(label="Crash Reports", signal="crash_reports"),
        SwitchWithLabel(label="Personalization", signal="personalization")
    ),
    Separator(),
    Div(
        H3("Visibility"),
        SwitchWithLabel(label="Public Profile", signal="public_profile"),
        SwitchWithLabel(
            label="Show Online Status",
            signal="online_status",
            disabled=ds_show("!$public_profile")
        )
    ),
    ds_effect("if (!$public_profile) { $online_status = false; }")
)''',
        title="Privacy Settings",
        description="Grouped switches with dependencies"
    )
    
    # Accessibility settings
    yield ComponentPreview(
        Card(
            CardHeader(
                CardTitle("Accessibility"),
                CardDescription("Make the app easier to use")
            ),
            CardContent(
                Div(
                    Div(
                        SwitchWithLabel(
                            label="High Contrast Mode",
                            helper_text="Increase color contrast for better visibility",
                            signal="high_contrast"
                        ),
                        SwitchWithLabel(
                            label="Large Text",
                            helper_text="Increase text size throughout the app",
                            signal="large_text"
                        ),
                        SwitchWithLabel(
                            label="Reduce Motion",
                            helper_text="Minimize animations and transitions",
                            signal="reduce_motion"
                        ),
                        SwitchWithLabel(
                            label="Screen Reader Support",
                            helper_text="Optimize for screen reader usage",
                            signal="screen_reader"
                        ),
                        cls="space-y-3"
                    ),
                    Div(
                        P("Preview:", cls="text-sm font-medium mb-2"),
                        Div(
                            P(
                                "Sample text",
                                cls="transition-all duration-200",
                                ds_class={
                                    "text-lg font-bold": "$large_text",
                                    "text-black dark:text-white": "$high_contrast"
                                }
                            ),
                            cls="p-4 border rounded-md",
                            ds_class={
                                "border-4 border-black dark:border-white": "$high_contrast",
                                "animate-none": "$reduce_motion"
                            }
                        ),
                        cls="mt-4"
                    ),
                    ds_signals(
                        high_contrast=False,
                        large_text=False,
                        reduce_motion=False,
                        screen_reader=False
                    )
                )
            ),
            cls="max-w-md"
        ),
        '''Card(
    CardContent(
        SwitchWithLabel(
            label="High Contrast Mode",
            helper_text="Increase color contrast",
            signal="high_contrast"
        ),
        SwitchWithLabel(
            label="Large Text",
            helper_text="Increase text size",
            signal="large_text"
        ),
        // Live preview
        Div(
            P(
                "Sample text",
                ds_class({
                    "text-lg font-bold": "$large_text",
                    "text-black dark:text-white": "$high_contrast"
                })
            ),
            ds_class({"border-4": "$high_contrast"})
        )
    )
)''',
        title="Accessibility Settings",
        description="Accessibility options with live preview"
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
            Div(
                Switch(cls="mr-4"),
                SwitchWithLabel(
                    label="Enable notifications",
                    signal="notifications",
                    checked=True
                ),
                cls="flex items-center gap-6"
            ),
            cls="flex justify-center"
        ),
        '''Switch()
SwitchWithLabel(
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