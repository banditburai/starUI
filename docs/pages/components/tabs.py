"""
Tabs component documentation - Layered content sections.
Navigate between different views with accessible tab controls.
"""

# Component metadata for auto-discovery
TITLE = "Tabs"
DESCRIPTION = "A set of layered sections of content—known as tab panels—that are displayed one at a time."
CATEGORY = "ui"
ORDER = 30
STATUS = "stable"

from starhtml import Div, P, Pre, Code
from starui.registry.components.tabs import Tabs, TabsList, TabsTrigger, TabsContent
from starui.registry.components.button import Button
from utils import auto_generate_page, with_code, Component, build_api_reference



@with_code
def dashboard_tabs_example():
    return Tabs(
        TabsList(
            TabsTrigger("Overview"),
            TabsTrigger("Analytics"),
            TabsTrigger("Reports")
        ),
        TabsContent(
            P("Welcome to your dashboard. Here you can see a summary of your activity.", cls="text-muted-foreground mb-4"),
            Div(
                Div("Total Users: 1,234", cls="p-3 bg-muted rounded-lg text-sm"),
                Div("Active Sessions: 89", cls="p-3 bg-muted rounded-lg text-sm"),
                Div("Revenue: $12,450", cls="p-3 bg-muted rounded-lg text-sm"),
                cls="grid grid-cols-3 gap-3"
            ),
            cls="min-h-[200px]"
        ),
        TabsContent(
            P("View detailed analytics and metrics for your account.", cls="text-muted-foreground mb-4"),
            Div("📊 Analytics charts would go here", cls="p-8 border border-dashed rounded-lg text-center text-muted-foreground"),
            cls="min-h-[200px]"
        ),
        TabsContent(
            P("Generate and download comprehensive reports for your data.", cls="text-muted-foreground mb-4"),
            Div(
                Button("Download Report", variant="outline", cls="mr-2"),
                Button("Generate New Report")
            ),
            cls="min-h-[200px]"
        ),
        cls="w-full"
    )


@with_code
def code_preview_tabs_example():
    return Tabs(
        TabsList(
            TabsTrigger("Preview", id="preview"),
            TabsTrigger("Code", id="code")
        ),
        TabsContent(
            Div(
                Button("Click me!", cls="mr-2"),
                Button("Secondary", variant="secondary", cls="mr-2"),
                Button("Outline", variant="outline"),
                cls="p-6 border rounded-lg"
            ),
            id="preview",
            cls="min-h-[120px]"
        ),
        TabsContent(
            Pre(
                Code('''Button("Click me!")
Button("Secondary", variant="secondary")
Button("Outline", variant="outline")'''),
                cls="p-4 bg-muted rounded-lg text-sm overflow-x-auto"
            ),
            id="code",
            cls="min-h-[120px]"
        ),
        value="preview",
        cls="w-full"
    )


@with_code
def settings_tabs_example():
    return Tabs(
        TabsList(
            TabsTrigger("General", id="general"),
            TabsTrigger("Security", id="security"),
            TabsTrigger("Notifications", id="notifications")
        ),
        TabsContent(
            P("Manage your account preferences and basic information.", cls="text-muted-foreground mb-4"),
            Div(
                "Username, language, timezone settings would go here",
                cls="p-4 border rounded-lg text-sm text-muted-foreground"
            ),
            id="general",
            cls="min-h-[150px]"
        ),
        TabsContent(
            P("Configure your account security and authentication settings.", cls="text-muted-foreground mb-4"),
            Div(
                "Password, two-factor auth settings would go here",
                cls="p-4 border rounded-lg text-sm text-muted-foreground"
            ),
            id="security",
            cls="min-h-[150px]"
        ),
        TabsContent(
            P("Control how and when you receive notifications from our platform.", cls="text-muted-foreground mb-4"),
            Div(
                "Email, push notification settings would go here",
                cls="p-4 border rounded-lg text-sm text-muted-foreground"
            ),
            id="notifications",
            cls="min-h-[150px]"
        ),
        value="general",
        cls="w-full"
    )


@with_code
def plain_variant_tabs_example():
    return Tabs(
        TabsList(
            TabsTrigger("Documentation", id="docs"),
            TabsTrigger("Examples", id="examples"),
            TabsTrigger("API Reference", id="api")
        ),
        TabsContent(
            P("Read the comprehensive guides and tutorials to get started.", cls="text-muted-foreground mb-3"),
            P("Learn how to integrate components into your application with step-by-step instructions and best practices.", cls="text-sm text-muted-foreground"),
            id="docs",
            cls="min-h-[100px]"
        ),
        TabsContent(
            P("Explore interactive examples and code samples for all components.", cls="text-muted-foreground mb-3"),
            P("Copy and paste working examples directly into your project with full source code.", cls="text-sm text-muted-foreground"),
            id="examples",
            cls="min-h-[100px]"
        ),
        TabsContent(
            P("Complete API documentation for all components and their props.", cls="text-muted-foreground mb-3"),
            P("TypeScript definitions, method signatures, and usage patterns for every component.", cls="text-sm text-muted-foreground"),
            id="api",
            cls="min-h-[100px]"
        ),
        value="docs",
        variant="plain",
        cls="w-full"
    )


@with_code
def navigation_tabs_example():
    return Tabs(
        TabsList(
            TabsTrigger("Home", id="home"),
            TabsTrigger("About", id="about"),
            TabsTrigger("Services", id="services"),
            TabsTrigger("Contact", id="contact")
        ),
        TabsContent(
            P("Welcome to our platform! Discover amazing tools and services designed for developers.", cls="text-lg text-muted-foreground mb-4"),
            Div(
                Button("Get Started", cls="mr-2"),
                Button("Learn More", variant="outline")
            ),
            id="home",
            cls="min-h-[150px]"
        ),
        TabsContent(
            P("We're passionate about building tools that make developers more productive.", cls="text-muted-foreground mb-4"),
            P("Founded in 2020, we've been creating amazing products for developers worldwide, focusing on simplicity and performance.", cls="text-sm text-muted-foreground"),
            id="about",
            cls="min-h-[150px]"
        ),
        TabsContent(
            P("We offer comprehensive solutions to help your business grow.", cls="text-muted-foreground mb-4"),
            Div(
                "🚀 Web Development - Full-stack applications",
                "📱 Mobile Apps - iOS and Android development",
                "☁️ Cloud Solutions - Scalable infrastructure",
                cls="grid grid-cols-1 gap-3 text-sm"
            ),
            id="services",
            cls="min-h-[150px]"
        ),
        TabsContent(
            P("Ready to work with us? We'd love to hear about your project!", cls="text-muted-foreground mb-4"),
            Div(
                P("📧 hello@example.com", cls="text-sm text-muted-foreground"),
                P("📞 (555) 123-4567", cls="text-sm text-muted-foreground"),
                cls="space-y-2"
            ),
            id="contact",
            cls="min-h-[150px]"
        ),
        value="home",
        variant="plain",
        cls="w-full"
    )


EXAMPLES_DATA = [
    {"title": "Dashboard Tabs", "description": "Multiple tabs for different content sections", "fn": dashboard_tabs_example},
    {"title": "Code Preview", "description": "Tabs for showing preview and code", "fn": code_preview_tabs_example},
    {"title": "Settings Tabs", "description": "Multi-section settings interface", "fn": settings_tabs_example},
    {"title": "Plain Variant", "description": "Clean minimal tabs without background styling", "fn": plain_variant_tabs_example},
    {"title": "Navigation Tabs", "description": "Website navigation-style tabs using plain variant", "fn": navigation_tabs_example},
]

API_REFERENCE = build_api_reference(
    components=[
        Component("Tabs", "Main container managing active tab state"),
        Component("TabsList", "Container for a set of tab triggers"),
        Component("TabsTrigger", "Clickable tab; use matching id to pair with content"),
        Component("TabsContent", "Panel content associated with a trigger id"),
    ]
)


def create_tabs_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)
