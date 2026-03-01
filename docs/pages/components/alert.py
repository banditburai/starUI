"""
Alert component documentation - Callouts and inline notifications.
"""

TITLE = "Alert"
DESCRIPTION = "Displays a callout for user attention."
CATEGORY = "ui"
ORDER = 2
STATUS = "stable"

from starhtml import Div, P, Code, Ul, Li, Icon
from starui.registry.components.alert import Alert, AlertTitle, AlertDescription
from starui.registry.components.button import Button
from utils import auto_generate_page, with_code, Prop, Component, build_api_reference


@with_code
def hero_alert_example():
    return Div(
        Alert(
            Icon("lucide:rocket", cls="h-4 w-4"),
            AlertTitle("Deployment complete"),
            AlertDescription("Your app has been deployed to production. DNS propagation may take up to 5 minutes.")
        ),
        Alert(
            Icon("lucide:alert-circle", cls="h-4 w-4"),
            AlertTitle("Build failed"),
            AlertDescription("Missing required field 'database_url' in config.toml. Check your environment variables."),
            variant="destructive"
        ),
        cls="space-y-4"
    )


@with_code
def with_action_alert_example():
    return Div(
        Alert(
            Icon("lucide:arrow-up-circle", cls="h-4 w-4"),
            AlertTitle("Update available"),
            AlertDescription(
                Div(
                    P("StarUI v0.3.0 includes 4 new components and improved accessibility."),
                    Div(
                        Button("View changelog", variant="outline", size="sm"),
                        Button("Update now", size="sm"),
                        cls="flex gap-2 mt-3"
                    )
                )
            ),
        ),
        Alert(
            Icon("lucide:hard-drive", cls="h-4 w-4"),
            AlertTitle("Storage quota at 92%"),
            AlertDescription(
                Div(
                    P("You've used 4.6 GB of 5 GB. Uploads will be blocked when you reach the limit."),
                    Button("Manage storage", variant="outline", size="sm", cls="mt-3"),
                )
            ),
            variant="destructive"
        ),
        cls="space-y-4"
    )


@with_code
def form_validation_alert_example():
    errors = [
        "Email address is required",
        "Password must be at least 8 characters",
        "You must accept the terms of service"
    ]

    return Alert(
        Icon("lucide:x-circle", cls="h-4 w-4"),
        AlertTitle(f"{len(errors)} errors in your submission"),
        AlertDescription(
            P("Please fix the following before continuing:"),
            Ul(
                *[Li(e) for e in errors],
                cls="mt-2 ml-6 list-disc space-y-1 text-sm"
            )
        ),
        variant="destructive"
    )


@with_code
def custom_icon_styling_alert_example():
    return Div(
        Alert(
            Icon("lucide:check-circle", cls="h-4 w-4 text-green-600"),
            AlertTitle("Changes saved"),
            AlertDescription("Your profile settings have been updated.")
        ),
        Alert(
            Icon("lucide:alert-triangle", cls="h-4 w-4 text-amber-600"),
            AlertTitle("API rate limit approaching"),
            AlertDescription("You've used 4,800 of 5,000 requests this hour. Throttling begins at the limit.")
        ),
        Alert(
            Icon("lucide:info", cls="h-4 w-4 text-blue-600"),
            AlertTitle("Scheduled maintenance"),
            AlertDescription("Database maintenance is planned for Saturday 2am–4am UTC. Expect brief downtime.")
        ),
        cls="space-y-4"
    )


@with_code
def without_icon_alert_example():
    return Alert(
        AlertTitle("Keyboard shortcut"),
        AlertDescription(
            P("Press ", Code("Ctrl+K", cls="text-xs bg-muted px-1 py-0.5 rounded"),
              " to open the command palette from anywhere in the app.")
        )
    )


EXAMPLES_DATA = [
    {"fn": hero_alert_example, "title": "Default & Destructive", "description": "The two built-in variants — default for informational, destructive for errors"},
    {"fn": with_action_alert_example, "title": "With Actions", "description": "Alerts with buttons for user response — upgrade prompts, storage warnings"},
    {"fn": form_validation_alert_example, "title": "Form Validation", "description": "Error summary with a structured list of field-level issues"},
    {"fn": custom_icon_styling_alert_example, "title": "Custom Icon Styling", "description": "Convey intent by pairing colored icons with the default variant — not built-in variants"},
    {"fn": without_icon_alert_example, "title": "Without Icon", "description": "Alert with just a title and description, no icon column"},
]

API_REFERENCE = build_api_reference(
    main_props=[
        Prop("variant", "Literal['default', 'destructive']", "Visual style variant", "'default'"),
        Prop("live", "bool", "When True, sets role='alert' for screen reader live region announcements. Use only for dynamically inserted alerts", "False"),
        Prop("cls", "str", "Additional CSS classes", "''"),
    ],
    components=[
        Component("Alert", "Root container. Uses CSS grid for icon + content layout"),
        Component("AlertTitle", "Bold single-line heading (clamped with line-clamp-1)"),
        Component("AlertDescription", "Supporting content — accepts text, paragraphs, lists, or any rich content"),
    ]
)


def create_alert_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)
