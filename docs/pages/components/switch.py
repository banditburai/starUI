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

from starhtml import Div, P, Label, Icon, Form, Signal
from starui.registry.components.switch import Switch, SwitchWithLabel
from starui.registry.components.button import Button
from starui.registry.components.card import Card, CardHeader, CardContent, CardTitle, CardDescription
from starui.registry.components.badge import Badge
from utils import auto_generate_page, with_code, Prop, build_api_reference


@with_code
def basic_switch_example():
    return Div(
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
    )


@with_code
def switch_with_label_example():
    return Div(
        (notifications := Signal("notifications", True)),
        SwitchWithLabel(
            label="Enable notifications",
            helper_text="Receive email and push notifications",
            signal=notifications,
            checked=True
        ),
        P(
            data_text=notifications.if_("Notifications are enabled", "Notifications are disabled"),
            cls="text-sm text-muted-foreground mt-3"
        ),
        cls="max-w-sm"
    )


@with_code
def autosave_feature_example():
    return Card(
        CardHeader(
            CardTitle("Document Settings"),
            CardDescription("Configure how your document is saved")
        ),
        CardContent(
            Div(
                (auto_save := Signal("auto_save", True)),
                SwitchWithLabel(
                    label="Auto-save",
                    helper_text="Automatically save changes as you type",
                    signal=auto_save,
                    checked=True
                ),
                Div(
                    Badge(
                        Icon("lucide:check-circle", cls="h-3 w-3 mr-1"),
                        data_text=auto_save.if_("Changes saved automatically", "Remember to save manually"),
                        data_attr_variant=auto_save.if_("default", "secondary"),
                        cls="w-full justify-center"
                    ),
                    cls="mt-4"
                )
            )
        ),
        cls="max-w-md"
    )


@with_code
def email_subscriptions_example():
    return Card(
        CardHeader(
            CardTitle("Email Preferences"),
            CardDescription("Manage your email subscriptions")
        ),
        CardContent(
            Form(
                (marketing_emails := Signal("marketing_emails", False)),
                (newsletter := Signal("newsletter", False)),
                SwitchWithLabel(
                    label="Marketing emails",
                    helper_text="Product updates, feature announcements, and tips",
                    signal=marketing_emails,
                    checked=False
                ),
                Div(
                    Div(
                        Label(
                            "Weekly newsletter",
                            fr="newsletter_switch",
                            cls="text-sm font-medium cursor-pointer"
                        ),
                        Switch(
                            data_attr_disabled=~marketing_emails,
                            signal=newsletter,
                            checked=False,
                            id="newsletter_switch"
                        ),
                        cls="flex items-center gap-3"
                    ),
                    P("Our weekly roundup of news and insights", cls="text-sm text-muted-foreground mt-1.5"),
                    cls="space-y-1.5"
                ),
                Div(
                    Div(
                        Icon("lucide:info", cls="h-4 w-4 text-muted-foreground flex-shrink-0 mt-0.5"),
                        P(
                            "Newsletter requires marketing emails to be enabled",
                            cls="text-sm text-muted-foreground break-words"
                        ),
                        cls="flex items-start gap-2"
                    ),
                    data_show=~marketing_emails,
                    cls="mt-3"
                ),
                Button(
                    "Update Preferences",
                    type="submit",
                    cls="w-full mt-4"
                ),
                data_effect=(~marketing_emails).then(newsletter.set(False)),
                cls="space-y-4"
            )
        ),
        cls="w-full max-w-md"
    )


EXAMPLES_DATA = [
    {"title": "Basic Switch", "description": "Different switch states", "fn": basic_switch_example},
    {"title": "Switch with Label", "description": "Switch with label, helper text, and reactive feedback", "fn": switch_with_label_example},
    {"title": "Auto-save Feature", "description": "Document setting with status feedback", "fn": autosave_feature_example},
    {"title": "Email Subscriptions", "description": "Dependent switches for email preferences", "fn": email_subscriptions_example},
]

API_REFERENCE = build_api_reference(
    main_props=[
        Prop("checked", "bool | None", "Initial checked state of the switch", "None"),
        Prop("signal", "str", "Datastar signal name for state management", "auto-generated"),
        Prop("disabled", "bool", "Whether the switch is disabled", "False"),
        Prop("required", "bool", "Whether the switch is required", "False"),
        Prop("cls", "str", "Additional CSS classes", "''"),
    ]
)


def create_switch_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)