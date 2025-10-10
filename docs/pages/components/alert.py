"""
Alert component documentation - Important messages and notifications.
"""

# Component metadata for auto-discovery
TITLE = "Alert"
DESCRIPTION = "Displays a callout for user attention."
CATEGORY = "ui"
ORDER = 2
STATUS = "stable"

from starhtml import Div, P, Strong, Code, Ul, Li, Icon
from starui.registry.components.alert import Alert, AlertTitle, AlertDescription
from starui.registry.components.button import Button
from utils import auto_generate_page, with_code, Component, build_api_reference
from widgets.component_preview import ComponentPreview


# ============================================================================
# EXAMPLE FUNCTIONS (decorated with @with_code for markdown generation)
# ============================================================================

@with_code
def basic_alert_example():
    return Alert(
        Icon("lucide:terminal", width="16", height="16"),
        AlertTitle("Heads up!"),
        AlertDescription("You can add components and dependencies to your app using the CLI.")
    )


@with_code
def destructive_alert_example():
    return Alert(
        Icon("lucide:alert-circle", width="16", height="16"),
        AlertTitle("Error occurred"),
        AlertDescription("Your session has expired. Please log in again."),
        variant="destructive"
    )


@with_code
def message_types_alert_example():
    return Div(
        Alert(
            Icon("lucide:check-circle", width="16", height="16", cls="text-green-600"),
            AlertTitle("Success"),
            AlertDescription("Your account has been created successfully!")
        ),
        Alert(
            Icon("lucide:alert-triangle", width="16", height="16", cls="text-amber-600"),
            AlertTitle("Warning"),
            AlertDescription("This action cannot be undone. Please review carefully.")
        ),
        Alert(
            Icon("lucide:info", width="16", height="16", cls="text-blue-600"),
            AlertTitle("Information"),
            AlertDescription("New features are now available in your dashboard.")
        ),
        cls="space-y-4"
    )


@with_code
def rich_content_alert_example():
    payment_checks = [
        "Verify your card details are correct",
        "Ensure you have sufficient funds",
        "Check that your billing address matches"
    ]

    check_list = Ul(
        *[Li(check) for check in payment_checks],
        cls="mt-2 ml-6 list-disc space-y-1 text-sm"
    )

    return Alert(
        Icon("lucide:alert-circle", width="16", height="16"),
        AlertTitle("Unable to process payment"),
        AlertDescription(
            P("There was an issue processing your payment. Please check the following:"),
            check_list
        ),
        variant="destructive"
    )


@with_code
def simple_alert_example():
    return Alert(
        AlertTitle("Pro tip"),
        AlertDescription("You can use Ctrl+K to quickly search and navigate through the documentation.")
    )


# ============================================================================
# HERO EXAMPLE
# ============================================================================

@with_code
def hero_alert_example():
    return Div(
        Alert(
            Icon("lucide:terminal", width="16", height="16"),
            AlertTitle("Heads up!"),
            AlertDescription("You can add components and dependencies to your app using the CLI.")
        ),
        Alert(
            Icon("lucide:alert-circle", width="16", height="16"),
            AlertTitle("Error occurred"),
            AlertDescription("Your session has expired. Please log in again."),
            variant="destructive"
        ),
        cls="space-y-4"
    )


# ============================================================================
# MODULE EXPORTS (for markdown generation)
# ============================================================================

EXAMPLES_DATA = [
    {"fn": hero_alert_example, "title": "Hero Alert", "description": "Default alert with icon and message"},
    {"fn": basic_alert_example, "title": "Basic Alert", "description": "Default alert with icon and message"},
    {"fn": destructive_alert_example, "title": "Destructive", "description": "Error or destructive action alert"},
    {"fn": message_types_alert_example, "title": "Message Types", "description": "Success, warning, and info styled alerts"},
    {"fn": rich_content_alert_example, "title": "Rich Content", "description": "Alerts with lists and formatted text"},
    {"fn": simple_alert_example, "title": "Without Icon", "description": "Simple alert without an icon"},
]

API_REFERENCE = build_api_reference(
    components=[
        Component("Alert", "Main container with optional variant styling"),
        Component("AlertTitle", "Bold heading text for the alert"),
        Component("AlertDescription", "Supporting description text"),
    ]
)


# ============================================================================
# PAGE GENERATION
# ============================================================================

def create_alert_docs():
    """Create alert documentation page using convention-based approach."""
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)
