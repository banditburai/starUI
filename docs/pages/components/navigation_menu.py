"""
Navigation Menu component documentation - Horizontal nav with hover-activated content panels.
"""

# Component metadata for auto-discovery
TITLE = "Navigation Menu"
DESCRIPTION = "A collection of links for navigating websites, with hover-activated content panels."
CATEGORY = "ui"
ORDER = 60
STATUS = "stable"

from starhtml import Div, P
from components.navigation_menu import (
    NavigationMenu,
    NavigationMenuContent,
    NavigationMenuItem,
    NavigationMenuLink,
    NavigationMenuList,
    NavigationMenuListContent,
    NavigationMenuListItem,
    NavigationMenuTrigger,
)
from utils import auto_generate_page, with_code, Component, build_api_reference


@with_code
def hero_example():
    return Div(
        NavigationMenu(
            NavigationMenuList(
                NavigationMenuItem(
                    NavigationMenuTrigger("Getting Started"),
                    NavigationMenuContent(
                        NavigationMenuListContent(
                            Div(
                                NavigationMenuLink(
                                    Div(
                                        "StarUI",
                                        cls="mb-2 text-lg font-medium",
                                    ),
                                    P(
                                        "Components you copy-paste. No npm install. No node_modules.",
                                        cls="text-sm leading-tight text-muted-foreground",
                                    ),
                                    href="#",
                                    cls="flex h-full w-full select-none flex-col justify-end rounded-md bg-gradient-to-b from-muted/50 to-muted p-6 no-underline outline-none focus:shadow-md",
                                ),
                                cls="row-span-3",
                            ),
                            NavigationMenuListItem(
                                P(
                                    "How to install dependencies and structure your app.",
                                    cls="line-clamp-2 text-sm leading-snug text-muted-foreground",
                                ),
                                title="Installation",
                                href="#",
                            ),
                            NavigationMenuListItem(
                                P(
                                    "Styles for headings, paragraphs, lists, and inline code.",
                                    cls="line-clamp-2 text-sm leading-snug text-muted-foreground",
                                ),
                                title="Typography",
                                href="#",
                            ),
                            NavigationMenuListItem(
                                P(
                                    "Colors, spacing, and dark mode configuration.",
                                    cls="line-clamp-2 text-sm leading-snug text-muted-foreground",
                                ),
                                title="Theming",
                                href="#",
                            ),
                        ),
                    ),
                ),
                NavigationMenuItem(
                    NavigationMenuTrigger("Components"),
                    NavigationMenuContent(
                        NavigationMenuListContent(
                            NavigationMenuListItem(
                                P(
                                    "A callout for drawing attention to important information.",
                                    cls="line-clamp-2 text-sm leading-snug text-muted-foreground",
                                ),
                                title="Alert",
                                href="#",
                            ),
                            NavigationMenuListItem(
                                P(
                                    "Trigger actions and events with multiple style variants.",
                                    cls="line-clamp-2 text-sm leading-snug text-muted-foreground",
                                ),
                                title="Button",
                                href="#",
                            ),
                            NavigationMenuListItem(
                                P(
                                    "Group related content with header, body, and footer sections.",
                                    cls="line-clamp-2 text-sm leading-snug text-muted-foreground",
                                ),
                                title="Card",
                                href="#",
                            ),
                            NavigationMenuListItem(
                                P(
                                    "A modal overlay for confirmations, forms, and focused tasks.",
                                    cls="line-clamp-2 text-sm leading-snug text-muted-foreground",
                                ),
                                title="Dialog",
                                href="#",
                            ),
                            NavigationMenuListItem(
                                P(
                                    "Toggle sections of content open and closed.",
                                    cls="line-clamp-2 text-sm leading-snug text-muted-foreground",
                                ),
                                title="Accordion",
                                href="#",
                            ),
                            NavigationMenuListItem(
                                P(
                                    "Switch between different views with tabbed navigation.",
                                    cls="line-clamp-2 text-sm leading-snug text-muted-foreground",
                                ),
                                title="Tabs",
                                href="#",
                            ),
                            cls="lg:grid-cols-2",
                        ),
                    ),
                ),
                NavigationMenuItem(
                    NavigationMenuLink("Documentation", href="#"),
                ),
            ),
        ),
        cls="flex items-center justify-center min-h-[300px]",
    )


@with_code
def active_link_example():
    return Div(
        NavigationMenu(
            NavigationMenuList(
                NavigationMenuItem(
                    NavigationMenuTrigger("Guides"),
                    NavigationMenuContent(
                        NavigationMenuListContent(
                            NavigationMenuListItem(
                                P(
                                    "Add and configure components in your project.",
                                    cls="line-clamp-2 text-sm leading-snug text-muted-foreground",
                                ),
                                title="Installation",
                                href="#",
                            ),
                            NavigationMenuListItem(
                                P(
                                    "Organize layouts with pages and partials.",
                                    cls="line-clamp-2 text-sm leading-snug text-muted-foreground",
                                ),
                                title="Project Structure",
                                href="#",
                            ),
                            NavigationMenuListItem(
                                P(
                                    "Deploy to Vercel, Railway, or any Python host.",
                                    cls="line-clamp-2 text-sm leading-snug text-muted-foreground",
                                ),
                                title="Deployment",
                                href="#",
                            ),
                            cls="md:w-[250px] lg:w-[300px] lg:grid-cols-1",
                        ),
                    ),
                ),
                NavigationMenuItem(
                    NavigationMenuTrigger("API"),
                    NavigationMenuContent(
                        NavigationMenuListContent(
                            NavigationMenuListItem(
                                P(
                                    "Define endpoints with type-safe request handling.",
                                    cls="line-clamp-2 text-sm leading-snug text-muted-foreground",
                                ),
                                title="Routes",
                                href="#",
                            ),
                            NavigationMenuListItem(
                                P(
                                    "Reactive state shared between server and client.",
                                    cls="line-clamp-2 text-sm leading-snug text-muted-foreground",
                                ),
                                title="Signals",
                                href="#",
                            ),
                            NavigationMenuListItem(
                                P(
                                    "Build UI with composable Python functions.",
                                    cls="line-clamp-2 text-sm leading-snug text-muted-foreground",
                                ),
                                title="Components",
                                href="#",
                            ),
                            NavigationMenuListItem(
                                P(
                                    "Connect to databases, queues, and external services.",
                                    cls="line-clamp-2 text-sm leading-snug text-muted-foreground",
                                ),
                                title="Integrations",
                                href="#",
                            ),
                            cls="md:w-[400px] lg:w-[450px] lg:grid-cols-2",
                        ),
                    ),
                ),
                NavigationMenuItem(
                    NavigationMenuLink("Changelog", href="#", active=True),
                ),
            ),
        ),
        cls="flex items-center justify-center min-h-[300px]",
    )


EXAMPLES_DATA = [
    {
        "title": "Navigation Menu",
        "description": "Getting Started features a gradient hero item spanning the full grid height alongside three list items. Components shows a two-column grid. The standalone Documentation link needs no dropdown.",
        "fn": hero_example,
    },
    {
        "title": "With Active Link",
        "description": "The active prop on NavigationMenuLink highlights the current page with font-medium. The two panels have different widths — Guides is a narrow single-column list, API is a wider two-column grid — so the shared viewport resizes when switching between them.",
        "fn": active_link_example,
    },
]

API_REFERENCE = build_api_reference(
    components=[
        Component(
            "NavigationMenu",
            "Root navigation container managing active item state via signal",
        ),
        Component(
            "NavigationMenuList",
            "Horizontal list container for navigation items",
        ),
        Component(
            "NavigationMenuItem",
            "Individual item wrapper (trigger + content pair or standalone link)",
        ),
        Component(
            "NavigationMenuTrigger",
            "Button that reveals content panel on hover/click with animated chevron",
        ),
        Component(
            "NavigationMenuContent",
            "Content panel that registers with the shared viewport popover; shown via data_show",
        ),
        Component(
            "NavigationMenuLink",
            "Styled anchor for standalone or in-panel links; active prop for current page",
        ),
        Component(
            "NavigationMenuListContent",
            "Grid container (ul) for organizing list items within a content panel",
        ),
        Component(
            "NavigationMenuListItem",
            "Link with a title heading and child description inside a content panel",
        ),
    ]
)


def create_navigation_menu_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)
