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


def examples():
    """Generate alert examples using ComponentPreview with tabs."""

    @with_code
    def message_types_alert_example():
        return Div(
            Alert(
                Icon("lucide:check-circle", width="16", height="16", cls="text-green-600"),
                AlertTitle("Success"),
                AlertDescription("Your account has been created successfully!"),
                cls="mb-4"
            ),
            Alert(
                Icon("lucide:alert-triangle", width="16", height="16", cls="text-amber-600"),
                AlertTitle("Warning"),
                AlertDescription("This action cannot be undone. Please review carefully."),
                cls="mb-4"
            ),
            Alert(
                Icon("lucide:info", width="16", height="16", cls="text-blue-600"),
                AlertTitle("Information"),
                AlertDescription("New features are now available in your dashboard.")
            ),
            cls="space-y-4"
        )
    
    yield ComponentPreview(
        message_types_alert_example(),
        message_types_alert_example.code,
        title="Message Types",
        description="Success, warning, and info styled alerts"
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
        
        description = AlertDescription(
            P("There was an issue processing your payment. Please check the following:"),
            check_list
        )
        
        return Alert(
            Icon("lucide:alert-circle", width="16", height="16"),
            AlertTitle("Unable to process payment"),
            description,
            variant="destructive"
        )
    
    yield ComponentPreview(
        rich_content_alert_example(),
        rich_content_alert_example.code,
        title="Rich Content",
        description="Alerts with lists and formatted text"
    )
    
    @with_code
    def simple_alert_example():
        return Alert(
            AlertTitle("Pro tip"),
            AlertDescription("You can use Ctrl+K to quickly search and navigate through the documentation.")
        )
    
    yield ComponentPreview(
        simple_alert_example(),
        simple_alert_example.code,
        title="Without Icon",
        description="Simple alert without an icon"
    )


def create_alert_docs():
    """Create alert documentation page using convention-based approach."""    
    
    @with_code
    def hero_alert_example():
        return Div(
            Alert(
                Icon("lucide:terminal", width="16", height="16"),
                AlertTitle("Heads up!"),
                AlertDescription("You can add components and dependencies to your app using the CLI."),
                cls="mb-4"
            ),
            Alert(
                Icon("lucide:alert-circle", width="16", height="16"),
                AlertTitle("Error occurred"),
                AlertDescription("Your session has expired. Please log in again."),
                variant="destructive"
            ),
            cls="space-y-4"
        )
    
    hero_example = ComponentPreview(
        hero_alert_example(),
        hero_alert_example.code,
    )
    
    return auto_generate_page(
        TITLE,
        DESCRIPTION,
        list(examples()),
        cli_command="star add alert",
        hero_example=hero_example,
        component_slug="alert",
        api_reference=build_api_reference(
            # For Alert, users need to understand the component structure 
            # (Alert + AlertTitle + AlertDescription) more than props
            components=[
                Component("Alert", "Main container with optional variant styling"),
                Component("AlertTitle", "Bold heading text for the alert"),
                Component("AlertDescription", "Supporting description text"),
            ]
        )
    )