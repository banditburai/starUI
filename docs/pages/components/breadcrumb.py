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
# EXAMPLES GENERATOR (for rendering on the page)
# ============================================================================

def examples():
    yield ComponentPreview(
        custom_separator_example(),
        custom_separator_example.code,
        title="Custom Separator",
        description="Use custom icons as separators between items"
    )

    yield ComponentPreview(
        collapsed_breadcrumb_example(),
        collapsed_breadcrumb_example.code,
        title="Collapsed",
        description="Use ellipsis to indicate hidden intermediate steps"
    )

    yield ComponentPreview(
        long_path_example(),
        long_path_example.code,
        title="Long Path",
        description="Full breadcrumb trail with multiple levels"
    )

    yield ComponentPreview(
        breadcrumb_with_icons_example(),
        breadcrumb_with_icons_example.code,
        title="With Icons",
        description="Breadcrumb items with icons for better visual context"
    )

    yield ComponentPreview(
        ecommerce_breadcrumb_example(),
        ecommerce_breadcrumb_example.code,
        title="E-commerce Product Path",
        description="Product category hierarchy with chevron separators"
    )

    yield ComponentPreview(
        separator_styles_example(),
        separator_styles_example.code,
        title="Separator Styles",
        description="Different separator styles: dots, arrows, and pipes"
    )

    yield ComponentPreview(
        responsive_breadcrumb_example(),
        responsive_breadcrumb_example.code,
        title="Responsive",
        description="Shows ellipsis on mobile, full path on desktop"
    )


# ============================================================================
# MODULE EXPORTS (for markdown generation)
# ============================================================================

EXAMPLES_DATA = [
    {"title": "Custom Separator", "description": "Use custom icons as separators between items", "code": custom_separator_example.code},
    {"title": "Collapsed", "description": "Use ellipsis to indicate hidden intermediate steps", "code": collapsed_breadcrumb_example.code},
    {"title": "Long Path", "description": "Full breadcrumb trail with multiple levels", "code": long_path_example.code},
    {"title": "With Icons", "description": "Breadcrumb items with icons for better visual context", "code": breadcrumb_with_icons_example.code},
    {"title": "E-commerce Product Path", "description": "Product category hierarchy with chevron separators", "code": ecommerce_breadcrumb_example.code},
    {"title": "Separator Styles", "description": "Different separator styles: dots, arrows, and pipes", "code": separator_styles_example.code},
    {"title": "Responsive", "description": "Shows ellipsis on mobile, full path on desktop", "code": responsive_breadcrumb_example.code},
]

API_REFERENCE = build_api_reference(
    components=[
        Component("Breadcrumb", "The root breadcrumb container"),
        Component("BreadcrumbList", "Contains the ordered list of breadcrumb items"),
        Component("BreadcrumbItem", "Individual breadcrumb item container"),
        Component("BreadcrumbLink", "Clickable breadcrumb link"),
        Component("BreadcrumbPage", "Current page breadcrumb item (non-clickable)"),
        Component("BreadcrumbSeparator", "Visual separator between breadcrumb items"),
        Component("BreadcrumbEllipsis", "Collapsed breadcrumb indicator"),
    ]
)


# ============================================================================
# DOCS PAGE
# ============================================================================

def create_breadcrumb_docs():
    """Create breadcrumb documentation page using convention-based approach."""
    hero_example = ComponentPreview(
        hero_breadcrumb_example(),
        hero_breadcrumb_example.code,
        copy_button=True
    )

    return auto_generate_page(
        TITLE,
        DESCRIPTION,
        list(examples()),
        cli_command="star add breadcrumb",
        api_reference=API_REFERENCE,
        hero_example=hero_example,
        component_slug="breadcrumb"
    )
