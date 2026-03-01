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

from starhtml import Div, P, Span, Icon
from starui.registry.components.tabs import Tabs, TabsList, TabsTrigger, TabsContent
from starui.registry.components.card import (
    Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter,
)
from starui.registry.components.input import Input
from starui.registry.components.label import Label
from starui.registry.components.button import Button
from starui.registry.components.separator import Separator
from starui.registry.components.switch import SwitchWithLabel
from starui.registry.components.badge import Badge
from utils import auto_generate_page, with_code, Component, build_api_reference


@with_code
def account_form_example():
    return Tabs(
        TabsList(
            TabsTrigger("Account", id="account"),
            TabsTrigger("Password", id="password"),
        ),
        TabsContent(
            Card(
                CardHeader(
                    CardTitle("Account"),
                    CardDescription("Update your account details."),
                ),
                CardContent(
                    Div(
                        Div(
                            Label("Name", fr="tab_name"),
                            Input(id="tab_name", value="Ada Lovelace"),
                            cls="grid gap-1.5",
                        ),
                        Div(
                            Label("Username", fr="tab_username"),
                            Input(id="tab_username", value="@ada"),
                            cls="grid gap-1.5",
                        ),
                        cls="space-y-4",
                    )
                ),
                CardFooter(Button("Save")),
            ),
            id="account",
        ),
        TabsContent(
            Card(
                CardHeader(
                    CardTitle("Password"),
                    CardDescription("Change your password here."),
                ),
                CardContent(
                    Div(
                        Div(
                            Label("Current password", fr="tab_curpw"),
                            Input(type="password", id="tab_curpw"),
                            cls="grid gap-1.5",
                        ),
                        Div(
                            Label("New password", fr="tab_newpw"),
                            Input(type="password", id="tab_newpw"),
                            cls="grid gap-1.5",
                        ),
                        cls="space-y-4",
                    )
                ),
                CardFooter(Button("Update password")),
            ),
            id="password",
        ),
        value="account",
        cls="w-full max-w-md",
    )


@with_code
def line_variant_example():
    return Tabs(
        TabsList(
            TabsTrigger("Overview", id="overview"),
            TabsTrigger("Specs", id="specs"),
        ),
        TabsContent(
            Div(
                Div(
                    Badge("In Stock"),
                    Badge("v4.2", variant="outline"),
                    cls="flex gap-2",
                ),
                P(
                    "Studio-grade condenser microphone with a wide frequency response "
                    "and low self-noise floor, designed for vocal recording and live streaming.",
                    cls="text-sm text-muted-foreground mt-3",
                ),
            ),
            id="overview",
            cls="min-h-[120px]",
        ),
        TabsContent(
            Div(
                Div(
                    Span("Type", cls="text-sm text-muted-foreground"),
                    Span("Condenser", cls="text-sm font-medium"),
                    cls="flex justify-between py-2",
                ),
                Separator(),
                Div(
                    Span("Pattern", cls="text-sm text-muted-foreground"),
                    Span("Cardioid", cls="text-sm font-medium"),
                    cls="flex justify-between py-2",
                ),
                Separator(),
                Div(
                    Span("Impedance", cls="text-sm text-muted-foreground"),
                    Span("200\u2126", cls="text-sm font-medium"),
                    cls="flex justify-between py-2",
                ),
            ),
            id="specs",
            cls="min-h-[120px]",
        ),
        value="overview",
        variant="line",
        cls="w-full max-w-sm",
    )


@with_code
def disabled_tab_example():
    return Tabs(
        TabsList(
            TabsTrigger("Draft", id="draft"),
            TabsTrigger("Preview", id="preview"),
            TabsTrigger("Publish", id="publish", disabled=True),
        ),
        TabsContent(
            Div(
                Div(
                    Label("Title", fr="tab_post_title"),
                    Input(id="tab_post_title", placeholder="Post title"),
                    cls="grid gap-1.5",
                ),
                Div(
                    Label("Slug", fr="tab_post_slug"),
                    Input(id="tab_post_slug", placeholder="/blog/my-post"),
                    cls="grid gap-1.5",
                ),
                cls="space-y-4",
            ),
            id="draft",
            cls="min-h-[150px]",
        ),
        TabsContent(
            Div(
                "Post preview will render here once the draft is saved.",
                cls="p-6 border border-dashed rounded-lg text-sm text-muted-foreground text-center",
            ),
            id="preview",
            cls="min-h-[150px]",
        ),
        TabsContent(
            P(
                "Save a draft first to unlock publishing.",
                cls="text-sm text-muted-foreground",
            ),
            id="publish",
            cls="min-h-[150px]",
        ),
        value="draft",
        cls="w-full max-w-sm",
    )


@with_code
def icon_tabs_example():
    return Tabs(
        TabsList(
            TabsTrigger(Icon("lucide:user"), "Profile", id="profile"),
            TabsTrigger(Icon("lucide:settings"), "Settings", id="settings"),
            TabsTrigger(Icon("lucide:bell"), "Alerts", id="alerts"),
        ),
        TabsContent(
            Div(
                Div(
                    Label("Display name", fr="tab_display"),
                    Input(id="tab_display", value="Ada Lovelace"),
                    cls="grid gap-1.5",
                ),
                Div(
                    Label("Email", fr="tab_email"),
                    Input(type="email", id="tab_email", value="ada@example.com"),
                    cls="grid gap-1.5",
                ),
                cls="space-y-4",
            ),
            id="profile",
            cls="min-h-[140px]",
        ),
        TabsContent(
            Div(
                SwitchWithLabel(
                    label="Two-factor authentication",
                    signal="sw_tab_2fa",
                ),
                SwitchWithLabel(
                    label="Session timeout",
                    signal="sw_tab_timeout",
                    helper_text="Log out after 30 minutes of inactivity",
                ),
                cls="space-y-4",
            ),
            id="settings",
            cls="min-h-[140px]",
        ),
        TabsContent(
            Div(
                SwitchWithLabel(
                    label="Email notifications",
                    signal="sw_tab_email_notif",
                    checked=True,
                ),
                SwitchWithLabel(
                    label="Push notifications",
                    signal="sw_tab_push_notif",
                ),
                cls="space-y-4",
            ),
            id="alerts",
            cls="min-h-[140px]",
        ),
        value="profile",
        cls="w-full max-w-sm",
    )


@with_code
def auto_indexed_example():
    return Tabs(
        TabsList(
            TabsTrigger("RGB"),
            TabsTrigger("HSL"),
            TabsTrigger("HEX"),
        ),
        TabsContent(
            Div(
                Div(
                    Label("R", fr="tab_r"),
                    Input(type="number", id="tab_r", value="99", min=0, max=255),
                    cls="grid gap-1.5",
                ),
                Div(
                    Label("G", fr="tab_g"),
                    Input(type="number", id="tab_g", value="102", min=0, max=255),
                    cls="grid gap-1.5",
                ),
                Div(
                    Label("B", fr="tab_b"),
                    Input(type="number", id="tab_b", value="241", min=0, max=255),
                    cls="grid gap-1.5",
                ),
                cls="grid grid-cols-3 gap-3",
            ),
            cls="min-h-[80px]",
        ),
        TabsContent(
            Div(
                Div(
                    Label("H", fr="tab_h"),
                    Input(type="number", id="tab_h", value="239", min=0, max=360),
                    cls="grid gap-1.5",
                ),
                Div(
                    Label("S", fr="tab_s"),
                    Input(type="number", id="tab_s", value="84", min=0, max=100),
                    cls="grid gap-1.5",
                ),
                Div(
                    Label("L", fr="tab_l"),
                    Input(type="number", id="tab_l", value="67", min=0, max=100),
                    cls="grid gap-1.5",
                ),
                cls="grid grid-cols-3 gap-3",
            ),
            cls="min-h-[80px]",
        ),
        TabsContent(
            Div(
                Label("Hex", fr="tab_hex"),
                Input(id="tab_hex", value="#6366F1", cls="font-mono"),
                cls="grid gap-1.5",
            ),
            cls="min-h-[80px]",
        ),
        cls="w-full max-w-md",
    )


EXAMPLES_DATA = [
    {"title": "Account Form", "description": "Card and form composition with string id pairing", "fn": account_form_example},
    {"title": "Line Variant", "description": "Underline indicator with Badge and Separator composition", "fn": line_variant_example},
    {"title": "Disabled Tab", "description": "Blog editor workflow with a disabled Publish trigger", "fn": disabled_tab_example},
    {"title": "With Icons", "description": "Lucide icons inside triggers with auto-sizing", "fn": icon_tabs_example},
    {"title": "Auto-Indexed", "description": "Zero-config pairing — no id or value props needed", "fn": auto_indexed_example},
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
