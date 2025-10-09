"""
Tabs component documentation - Layered content sections.
"""

# Component metadata for auto-discovery
TITLE = "Tabs"
DESCRIPTION = "A set of layered sections of content—known as tab panels—that are displayed one at a time."
CATEGORY = "ui"
ORDER = 30
STATUS = "stable"

from starhtml import Div, P, H2, H3, H4, Pre, Code, Button as HTMLButton
from starui.registry.components.tabs import Tabs, TabsList, TabsTrigger, TabsContent
from starui.registry.components.button import Button
from widgets.component_preview import ComponentPreview
from utils import auto_generate_page, with_code, Component, build_api_reference


# ============================================================================
# EXAMPLE FUNCTIONS (decorated with @with_code for markdown generation)
# ============================================================================

# Dashboard tabs
@with_code
def dashboard_tabs_example():
    return Tabs(
        TabsList(
            TabsTrigger("Overview", id="overview"),
            TabsTrigger("Analytics", id="analytics"),
            TabsTrigger("Reports", id="reports")
        ),
        TabsContent(
            Div(
                P("Welcome to your dashboard. Here you can see a summary of your activity.", cls="text-muted-foreground mb-4"),
                Div(
                    Div("Total Users: 1,234", cls="p-3 bg-muted rounded-lg text-sm"),
                    Div("Active Sessions: 89", cls="p-3 bg-muted rounded-lg text-sm"),
                    Div("Revenue: $12,450", cls="p-3 bg-muted rounded-lg text-sm"),
                    cls="grid grid-cols-3 gap-3"
                )
            ),
            id="overview"
        ),
        TabsContent(
            Div(
                P("View detailed analytics and metrics for your account.", cls="text-muted-foreground mb-4"),
                Div("📊 Analytics charts would go here", cls="p-8 border border-dashed rounded-lg text-center text-muted-foreground")
            ),
            id="analytics"
        ),
        TabsContent(
            Div(
                P("Generate and download comprehensive reports for your data.", cls="text-muted-foreground mb-4"),
                Button("Download Report", variant="outline", cls="mr-2"),
                Button("Generate New Report")
            ),
            id="reports"
        ),
        default_value="overview",
        cls="w-full"
    )


# Code preview tabs
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
            id="preview"
        ),
        TabsContent(
            Pre(
                Code('''Button("Click me!")
Button("Secondary", variant="secondary")
Button("Outline", variant="outline")'''),
                cls="p-4 bg-muted rounded-lg text-sm overflow-x-auto"
            ),
            id="code"
        ),
        default_value="preview",
        cls="w-full"
    )


# Settings tabs
@with_code
def settings_tabs_example():
    return Tabs(
        TabsList(
            TabsTrigger("General", id="general"),
            TabsTrigger("Security", id="security"),
            TabsTrigger("Notifications", id="notifications")
        ),
        TabsContent(
            Div(
                P("Manage your account preferences and basic information.", cls="text-muted-foreground mb-4"),
                Div(
                    "Username, language, timezone settings would go here",
                    cls="p-4 border rounded-lg text-sm text-muted-foreground"
                )
            ),
            id="general"
        ),
        TabsContent(
            Div(
                P("Configure your account security and authentication settings.", cls="text-muted-foreground mb-4"),
                Div(
                    "Password, two-factor auth settings would go here",
                    cls="p-4 border rounded-lg text-sm text-muted-foreground"
                )
            ),
            id="security"
        ),
        TabsContent(
            Div(
                P("Control how and when you receive notifications from our platform.", cls="text-muted-foreground mb-4"),
                Div(
                    "Email, push notification settings would go here",
                    cls="p-4 border rounded-lg text-sm text-muted-foreground"
                )
            ),
            id="notifications"
        ),
        default_value="general",
        cls="w-full"
    )


# Plain variant tabs
@with_code
def plain_variant_tabs_example():
    return Tabs(
        TabsList(
            TabsTrigger("Documentation", id="docs"),
            TabsTrigger("Examples", id="examples"),
            TabsTrigger("API Reference", id="api")
        ),
        TabsContent(
            Div(
                P("Read the comprehensive guides and tutorials to get started.", cls="text-muted-foreground mb-3"),
                P("Learn how to integrate components into your application with step-by-step instructions and best practices.", cls="text-sm text-muted-foreground")
            ),
            id="docs"
        ),
        TabsContent(
            Div(
                P("Explore interactive examples and code samples for all components.", cls="text-muted-foreground mb-3"),
                P("Copy and paste working examples directly into your project with full source code.", cls="text-sm text-muted-foreground")
            ),
            id="examples"
        ),
        TabsContent(
            Div(
                P("Complete API documentation for all components and their props.", cls="text-muted-foreground mb-3"),
                P("TypeScript definitions, method signatures, and usage patterns for every component.", cls="text-sm text-muted-foreground")
            ),
            id="api"
        ),
        default_value="docs",
        variant="plain",
        cls="w-full"
    )


# Navigation-style tabs
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
            Div(
                P("Welcome to our platform! Discover amazing tools and services designed for developers.", cls="text-lg text-muted-foreground mb-4"),
                Button("Get Started", cls="mr-2"),
                Button("Learn More", variant="outline")
            ),
            id="home"
        ),
        TabsContent(
            Div(
                P("We're passionate about building tools that make developers more productive.", cls="text-muted-foreground mb-4"),
                P("Founded in 2020, we've been creating amazing products for developers worldwide, focusing on simplicity and performance.", cls="text-sm text-muted-foreground")
            ),
            id="about"
        ),
        TabsContent(
            Div(
                P("We offer comprehensive solutions to help your business grow.", cls="text-muted-foreground mb-4"),
                Div(
                    "🚀 Web Development - Full-stack applications",
                    "📱 Mobile Apps - iOS and Android development",
                    "☁️ Cloud Solutions - Scalable infrastructure",
                    cls="grid grid-cols-1 gap-3 text-sm"
                )
            ),
            id="services"
        ),
        TabsContent(
            Div(
                P("Ready to work with us? We'd love to hear about your project!", cls="text-muted-foreground mb-4"),
                Div(
                    P("📧 hello@example.com", cls="text-sm text-muted-foreground"),
                    P("📞 (555) 123-4567", cls="text-sm text-muted-foreground"),
                    cls="space-y-2"
                )
            ),
            id="contact"
        ),
        default_value="home",
        variant="plain",
        cls="w-full"
    )


# ============================================================================
# MODULE-LEVEL DATA (for markdown API)
# ============================================================================

EXAMPLES_DATA = [
    {"title": "Dashboard Tabs", "description": "Multiple tabs for different content sections", "code": dashboard_tabs_example.code},
    {"title": "Code Preview", "description": "Tabs for showing preview and code", "code": code_preview_tabs_example.code},
    {"title": "Settings Tabs", "description": "Multi-section settings interface", "code": settings_tabs_example.code},
    {"title": "Plain Variant", "description": "Clean minimal tabs without background styling", "code": plain_variant_tabs_example.code},
    {"title": "Navigation Tabs", "description": "Website navigation-style tabs using plain variant", "code": navigation_tabs_example.code},
]

API_REFERENCE = build_api_reference(
    components=[
        Component("Tabs", "Main container managing active tab state"),
        Component("TabsList", "Container for a set of tab triggers"),
        Component("TabsTrigger", "Clickable tab; use matching id to pair with content"),
        Component("TabsContent", "Panel content associated with a trigger id"),
    ]
)


def examples():
    """Generate all tabs examples."""
    yield ComponentPreview(
        dashboard_tabs_example(),
        dashboard_tabs_example.code,
        title="Dashboard Tabs",
        description="Multiple tabs for different content sections"
    )

    yield ComponentPreview(
        code_preview_tabs_example(),
        code_preview_tabs_example.code,
        title="Code Preview",
        description="Tabs for showing preview and code"
    )

    yield ComponentPreview(
        settings_tabs_example(),
        settings_tabs_example.code,
        title="Settings Tabs",
        description="Multi-section settings interface"
    )

    yield ComponentPreview(
        plain_variant_tabs_example(),
        plain_variant_tabs_example.code,
        title="Plain Variant",
        description="Clean minimal tabs without background styling"
    )

    yield ComponentPreview(
        navigation_tabs_example(),
        navigation_tabs_example.code,
        title="Navigation Tabs",
        description="Website navigation-style tabs using plain variant"
    )


def create_tabs_docs():

    # Hero example - simple account/password tabs
    @with_code
    def hero_tabs_example():
        return Tabs(
            TabsList(
                TabsTrigger("Account", id="account"),
                TabsTrigger("Password", id="password")
            ),
            TabsContent(
                Div(
                    H4("Account", cls="text-lg font-medium mb-2"),
                    P("Make changes to your account here. Click save when you're done.", cls="text-muted-foreground")
                ),
                id="account"
            ),
            TabsContent(
                Div(
                    H4("Password", cls="text-lg font-medium mb-2"),
                    P("Change your password here. After saving, you'll be logged out.", cls="text-muted-foreground")
                ),
                id="password"
            ),
            default_value="account",
            cls="w-full max-w-md"
        )

    hero_example = ComponentPreview(
        hero_tabs_example(),
        hero_tabs_example.code,
        copy_button=True
    )

    return auto_generate_page(
        TITLE,
        DESCRIPTION,
        list(examples()),
        cli_command="star add tabs",
        hero_example=hero_example,
        component_slug="tabs",
        api_reference=API_REFERENCE
    )
