#!/usr/bin/env python3
"""Minimal test app for migrating components one by one."""
from starhtml import *

# Use registry_loader to set up paths, but don't load all components yet
# (we'll manually import only the ones we've migrated)
import registry_loader  # This adds parent dir to sys.path

# Import components as we migrate them
from src.starui.registry.components.accordion import Accordion, AccordionItem, AccordionTrigger, AccordionContent
from src.starui.registry.components.alert import Alert, AlertTitle, AlertDescription
from src.starui.registry.components.alert_dialog import (
    AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent,
    AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle, AlertDialogTrigger
)
from src.starui.registry.components.theme_toggle import ThemeToggle

styles = Link(rel="stylesheet", href="/static/css/starui.css", type="text/css")

app, rt = star_app(
    live=True,
    hdrs=(
        fouc_script(use_data_theme=True),
        styles,
        position_handler(),
    ),
    htmlkw=dict(lang="en", dir="ltr"),
    bodykw=dict(
        cls="min-h-screen bg-background text-foreground p-8",
    ),
    iconify=True,
    clipboard=True
)


@rt("/")
def index():
    """Index page with links to each component test."""
    return Div(
        # Theme toggle in top-right
        Div(ThemeToggle(), cls="absolute top-4 right-4"),

        H1("Component Migration Test Suite", cls="text-4xl font-bold mb-8"),
        P("Click a component to test it individually:", cls="text-muted-foreground mb-4"),

        Div(
            A("Accordion", href="/accordion", cls="text-primary hover:underline block"),
            A("Alert", href="/alert", cls="text-primary hover:underline block"),
            A("Alert Dialog", href="/alert-dialog", cls="text-primary hover:underline block"),
            A("Theme Toggle", href="/theme-toggle", cls="text-primary hover:underline block"),
            cls="space-y-2"
        ),
        cls="container mx-auto"
    )


# Component test routes - add as we migrate each component

@rt("/accordion")
def test_accordion():
    return Div(
        # Theme toggle in top-right
        Div(ThemeToggle(), cls="absolute top-4 right-4"),

        H1("Accordion Component Test", cls="text-3xl font-bold mb-6"),
        A("← Back to Index", href="/", cls="text-primary hover:underline mb-4 inline-block"),

        H2("Single Mode (Collapsible)", cls="text-2xl font-semibold mb-4 mt-8"),
        Accordion(
            AccordionItem(
                AccordionTrigger("Is it accessible?"),
                AccordionContent("Yes. It adheres to the WAI-ARIA design pattern."),
                value="item-1"
            ),
            AccordionItem(
                AccordionTrigger("Is it styled?"),
                AccordionContent("Yes. It comes with default styles that match the other components."),
                value="item-2"
            ),
            AccordionItem(
                AccordionTrigger("Is it animated?"),
                AccordionContent("Yes. It's animated by default, but you can disable it if needed."),
                value="item-3"
            ),
            type="single",
            collapsible=True,
            cls="max-w-2xl"
        ),

        H2("Multiple Mode", cls="text-2xl font-semibold mb-4 mt-8"),
        Accordion(
            AccordionItem(
                AccordionTrigger("Can I open multiple items?"),
                AccordionContent("Yes! In multiple mode, you can have several items expanded at once."),
                value="multi-1"
            ),
            AccordionItem(
                AccordionTrigger("Does it remember state?"),
                AccordionContent("Yes, the state is managed via signals."),
                value="multi-2"
            ),
            AccordionItem(
                AccordionTrigger("Is it customizable?"),
                AccordionContent("Yes, you can pass custom classes and styling."),
                value="multi-3"
            ),
            type="multiple",
            default_value=["multi-1"],
            cls="max-w-2xl"
        ),

        cls="container mx-auto"
    )


@rt("/alert")
def test_alert():
    return Div(
        # Theme toggle in top-right
        Div(ThemeToggle(), cls="absolute top-4 right-4"),

        H1("Alert Component Test", cls="text-3xl font-bold mb-6"),
        A("← Back to Index", href="/", cls="text-primary hover:underline mb-4 inline-block"),

        H2("Alert Variants", cls="text-2xl font-semibold mb-4 mt-8"),
        Div(
            Alert(
                AlertTitle("Default Alert"),
                AlertDescription("This is a default alert message."),
            ),
            Alert(
                AlertTitle("Destructive Alert"),
                AlertDescription("This is a destructive alert message."),
                variant="destructive",
            ),
            cls="space-y-4 max-w-2xl"
        ),

        H2("Alert with Icon", cls="text-2xl font-semibold mb-4 mt-8"),
        Div(
            Alert(
                Icon("lucide:info"),
                AlertTitle("Heads up!"),
                AlertDescription("You can add icons to alerts for better visual communication."),
            ),
            Alert(
                Icon("lucide:alert-triangle"),
                AlertTitle("Warning"),
                AlertDescription("This alert includes an icon to draw attention to important information."),
                variant="destructive",
            ),
            cls="space-y-4 max-w-2xl"
        ),

        cls="container mx-auto"
    )


@rt("/alert-dialog")
def test_alert_dialog():
    return Div(
        # Theme toggle in top-right
        Div(ThemeToggle(), cls="absolute top-4 right-4"),

        H1("Alert Dialog Component Test", cls="text-3xl font-bold mb-6"),
        A("← Back to Index", href="/", cls="text-primary hover:underline mb-4 inline-block"),

        H2("Alert Dialog Variants", cls="text-2xl font-semibold mb-4 mt-8"),
        Div(
            # Basic alert dialog
            AlertDialog(
                trigger=AlertDialogTrigger("Show Alert"),
                content=AlertDialogContent(
                    AlertDialogHeader(
                        AlertDialogTitle("Are you absolutely sure?"),
                        AlertDialogDescription(
                            "This action cannot be undone. This will permanently delete your "
                            "account and remove your data from our servers."
                        ),
                    ),
                    AlertDialogFooter(
                        AlertDialogCancel("Cancel"),
                        AlertDialogAction(
                            "Continue",
                            action="console.log('Action confirmed!')",
                        ),
                    ),
                ),
            ),
            # Destructive alert dialog
            AlertDialog(
                trigger=AlertDialogTrigger("Delete Item", variant="destructive"),
                content=AlertDialogContent(
                    AlertDialogHeader(
                        AlertDialogTitle("Delete Item"),
                        AlertDialogDescription(
                            "Are you sure you want to delete this item? This action is irreversible."
                        ),
                    ),
                    AlertDialogFooter(
                        AlertDialogCancel("Cancel"),
                        AlertDialogAction(
                            "Delete",
                            variant="destructive",
                            action="console.log('Item deleted!')",
                        ),
                    ),
                ),
            ),
            # Alert dialog with custom action
            AlertDialog(
                trigger=AlertDialogTrigger("Confirm Action", variant="outline"),
                content=AlertDialogContent(
                    AlertDialogHeader(
                        AlertDialogTitle("Confirm Action"),
                        AlertDialogDescription(
                            "This will apply the changes you've made. Do you want to proceed?"
                        ),
                    ),
                    AlertDialogFooter(
                        AlertDialogCancel("Not now"),
                        AlertDialogAction(
                            "Yes, apply changes",
                            action="alert('Changes applied successfully!')",
                        ),
                    ),
                ),
            ),
            cls="flex flex-wrap gap-4",
        ),

        cls="container mx-auto"
    )


@rt("/theme-toggle")
def test_theme_toggle():
    return Div(
        # Theme toggle in top-right
        Div(ThemeToggle(), cls="absolute top-4 right-4"),

        H1("Theme Toggle Component Test", cls="text-3xl font-bold mb-6"),
        A("← Back to Index", href="/", cls="text-primary hover:underline mb-4 inline-block"),

        H2("Instructions", cls="text-2xl font-semibold mb-4 mt-8"),
        P("Click the theme toggle button in the top-right corner to switch between light and dark themes.", cls="text-muted-foreground mb-4"),
        P("The theme preference is saved to localStorage and will persist across page reloads.", cls="text-muted-foreground mb-4"),

        H2("Theme-aware Content", cls="text-2xl font-semibold mb-4 mt-8"),
        Div(
            P("This text should adapt to the current theme.", cls="mb-2"),
            P("Background and foreground colors are theme-aware.", cls="mb-2"),
            Div("Bordered box", cls="border border-border p-4 rounded-md bg-card text-card-foreground"),
            cls="space-y-4 max-w-2xl"
        ),

        cls="container mx-auto"
    )


serve()
