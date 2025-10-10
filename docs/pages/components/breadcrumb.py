"""
Breadcrumb component documentation - Navigation hierarchy paths.
"""

TITLE = "Breadcrumb"
DESCRIPTION = "Displays the path to the current resource using a hierarchy of links."
CATEGORY = "navigation"
ORDER = 160
STATUS = "stable"

from starhtml import Div, P, Span, Icon
from starui.registry.components.breadcrumb import (
    Breadcrumb, BreadcrumbList, BreadcrumbItem,
    BreadcrumbLink, BreadcrumbPage, BreadcrumbSeparator, BreadcrumbEllipsis
)
from starui.registry.components.button import Button
from utils import auto_generate_page, Component, build_api_reference, with_code
from widgets.component_preview import ComponentPreview


# ============================================================================
# EXAMPLE FUNCTIONS (decorated with @with_code for markdown generation)
# ============================================================================

@with_code
def custom_separator_example():
    return Breadcrumb(
        BreadcrumbList(
            BreadcrumbItem(
                BreadcrumbLink("Home", href="/")
            ),
            BreadcrumbSeparator(
                Icon("lucide:slash", width="16", height="16", cls="align-middle")
            ),
            BreadcrumbItem(
                BreadcrumbLink("Library", href="/library")
            ),
            BreadcrumbSeparator(
                Icon("lucide:slash", width="16", height="16", cls="align-middle")
            ),
            BreadcrumbItem(
                BreadcrumbPage("Data")
            )
        )
    )


@with_code
def collapsed_breadcrumb_example():
    return Breadcrumb(
        BreadcrumbList(
            BreadcrumbItem(
                BreadcrumbLink("Home", href="/")
            ),
            BreadcrumbSeparator(),
            BreadcrumbItem(
                BreadcrumbEllipsis()
            ),
            BreadcrumbSeparator(),
            BreadcrumbItem(
                BreadcrumbLink("Components", href="/docs/components")
            ),
            BreadcrumbSeparator(),
            BreadcrumbItem(
                BreadcrumbPage("Breadcrumb")
            )
        )
    )


@with_code
def long_path_example():
    return Breadcrumb(
        BreadcrumbList(
            BreadcrumbItem(
                BreadcrumbLink("Home", href="/")
            ),
            BreadcrumbSeparator(),
            BreadcrumbItem(
                BreadcrumbLink("Documentation", href="/docs")
            ),
            BreadcrumbSeparator(),
            BreadcrumbItem(
                BreadcrumbLink("Components", href="/docs/components")
            ),
            BreadcrumbSeparator(),
            BreadcrumbItem(
                BreadcrumbLink("Navigation", href="/docs/components/navigation")
            ),
            BreadcrumbSeparator(),
            BreadcrumbItem(
                BreadcrumbPage("Breadcrumb")
            )
        )
    )


@with_code
def breadcrumb_with_icons_example():
    return Breadcrumb(
        BreadcrumbList(
            BreadcrumbItem(
                BreadcrumbLink(
                    Icon("lucide:home", width="16", height="16", cls="mr-1 inline-block align-text-bottom"),
                    "Home",
                    href="/"
                )
            ),
            BreadcrumbSeparator(),
            BreadcrumbItem(
                BreadcrumbLink(
                    Icon("lucide:folder", width="16", height="16", cls="mr-1 inline-block align-text-bottom"),
                    "Documents",
                    href="/documents"
                )
            ),
            BreadcrumbSeparator(),
            BreadcrumbItem(
                BreadcrumbLink(
                    Icon("lucide:folder", width="16", height="16", cls="mr-1 inline-block align-text-bottom"),
                    "Projects",
                    href="/documents/projects"
                )
            ),
            BreadcrumbSeparator(),
            BreadcrumbItem(
                BreadcrumbPage(
                    Icon("lucide:file-text", width="16", height="16", cls="mr-1 inline-block align-text-bottom"),
                    "README.md"
                )
            )
        )
    )


@with_code
def ecommerce_breadcrumb_example():
    path_items = [
        ("Shop", "/shop"),
        ("Electronics", "/shop/electronics"),
        ("Smartphones", "/shop/electronics/smartphones"),
        ("Apple", "/shop/electronics/smartphones/apple"),
        ("iPhone 15 Pro", None)  # None for current page
    ]

    def create_chevron_separator():
        return BreadcrumbSeparator(Icon("lucide:chevron-right", width="16", height="16"))

    breadcrumb_items = []
    for i, (label, href) in enumerate(path_items):
        if href:  # Link item
            breadcrumb_items.append(BreadcrumbItem(BreadcrumbLink(label, href=href)))
        else:  # Current page
            breadcrumb_items.append(BreadcrumbItem(BreadcrumbPage(label)))

        # Add separator except after last item
        if i < len(path_items) - 1:
            breadcrumb_items.append(create_chevron_separator())

    return Breadcrumb(BreadcrumbList(*breadcrumb_items))


@with_code
def separator_styles_example():
    return Div(
        Breadcrumb(
            BreadcrumbList(
                BreadcrumbItem(BreadcrumbLink("Blog", href="/blog")),
                BreadcrumbSeparator(Span("•", cls="px-2 text-muted-foreground")),
                BreadcrumbItem(BreadcrumbLink("Technology", href="/blog/tech")),
                BreadcrumbSeparator(Span("•", cls="px-2 text-muted-foreground")),
                BreadcrumbItem(BreadcrumbPage("AI Trends 2024"))
            ),
            cls="mb-4"
        ),
        Breadcrumb(
            BreadcrumbList(
                BreadcrumbItem(BreadcrumbLink("Settings", href="/settings")),
                BreadcrumbSeparator(Span("→", cls="px-2 text-muted-foreground")),
                BreadcrumbItem(BreadcrumbLink("Security", href="/settings/security")),
                BreadcrumbSeparator(Span("→", cls="px-2 text-muted-foreground")),
                BreadcrumbItem(BreadcrumbPage("Two-Factor Auth"))
            ),
            cls="mb-4"
        ),
        Breadcrumb(
            BreadcrumbList(
                BreadcrumbItem(BreadcrumbLink("Docs", href="/docs")),
                BreadcrumbSeparator(Span("|", cls="px-2 text-muted-foreground")),
                BreadcrumbItem(BreadcrumbLink("API", href="/docs/api")),
                BreadcrumbSeparator(Span("|", cls="px-2 text-muted-foreground")),
                BreadcrumbItem(BreadcrumbPage("Authentication"))
            )
        )
    )


@with_code
def responsive_breadcrumb_example():
    return Breadcrumb(
        BreadcrumbList(
            BreadcrumbItem(
                BreadcrumbLink("Home", href="/")
            ),
            BreadcrumbSeparator(),
            # Show ellipsis on mobile, hide intermediate items
            BreadcrumbItem(
                BreadcrumbEllipsis(),
                cls="md:hidden"
            ),
            BreadcrumbSeparator(cls="md:hidden"),
            # Show full path on desktop
            BreadcrumbItem(
                BreadcrumbLink("Documentation", href="/docs"),
                cls="hidden md:inline-flex"
            ),
            BreadcrumbSeparator(cls="hidden md:inline-flex"),
            BreadcrumbItem(
                BreadcrumbLink("Components", href="/docs/components"),
                cls="hidden md:inline-flex"
            ),
            BreadcrumbSeparator(cls="hidden md:inline-flex"),
            BreadcrumbItem(
                BreadcrumbPage("Breadcrumb")
            )
        )
    )


@with_code
def hero_breadcrumb_example():
    return Breadcrumb(
        BreadcrumbList(
            BreadcrumbItem(
                BreadcrumbLink("Home", href="/")
            ),
            BreadcrumbSeparator(),
            BreadcrumbItem(
                BreadcrumbLink("Components", href="/components")
            ),
            BreadcrumbSeparator(),
            BreadcrumbItem(
                BreadcrumbPage("Breadcrumb")
            )
        )
    )


# ============================================================================
# MODULE-LEVEL DATA
# ============================================================================

EXAMPLES_DATA = [
    {"fn": hero_breadcrumb_example, "title": "Breadcrumb", "description": "Navigation breadcrumb trail"},
    {"fn": custom_separator_example, "title": "Custom Separator", "description": "Use custom separator between items"},
    {"fn": collapsed_breadcrumb_example, "title": "Collapsed", "description": "Collapse middle items for long paths"},
    {"fn": long_path_example, "title": "Long Path", "description": "Handle deeply nested navigation paths"},
    {"fn": breadcrumb_with_icons_example, "title": "With Icons", "description": "Add icons to breadcrumb items"},
    {"fn": ecommerce_breadcrumb_example, "title": "E-commerce", "description": "Product category navigation"},
    {"fn": separator_styles_example, "title": "Separator Styles", "description": "Different separator styles"},
    {"fn": responsive_breadcrumb_example, "title": "Responsive", "description": "Breadcrumb that adapts to screen size"},
]

API_REFERENCE = build_api_reference(
    components=[
        Component("Breadcrumb", "Main breadcrumb container"),
        Component("BreadcrumbList", "List wrapper for breadcrumb items"),
        Component("BreadcrumbItem", "Individual breadcrumb item"),
        Component("BreadcrumbLink", "Clickable link in breadcrumb"),
        Component("BreadcrumbPage", "Current page indicator (non-clickable)"),
        Component("BreadcrumbSeparator", "Separator between items"),
        Component("BreadcrumbEllipsis", "Collapsed items indicator"),
    ]
)


# ============================================================================
# DOCS PAGE
# ============================================================================

def create_breadcrumb_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)
