"""
Breadcrumb component documentation - Navigation hierarchy paths.
"""

TITLE = "Breadcrumb"
DESCRIPTION = "Displays the path to the current resource using a hierarchy of links."
CATEGORY = "navigation"
ORDER = 160
STATUS = "stable"

from starhtml import Div, Span, Icon
from starui.registry.components.breadcrumb import (
    Breadcrumb, BreadcrumbList, BreadcrumbItem,
    BreadcrumbLink, BreadcrumbPage, BreadcrumbSeparator, BreadcrumbEllipsis
)
from utils import auto_generate_page, Prop, Component, build_api_reference, with_code


@with_code
def hero_breadcrumb_example():
    return Breadcrumb(
        BreadcrumbList(
            BreadcrumbItem(
                BreadcrumbLink("Projects", href="/projects")
            ),
            BreadcrumbSeparator(),
            BreadcrumbItem(
                BreadcrumbLink("Acme Redesign", href="/projects/acme-redesign")
            ),
            BreadcrumbSeparator(),
            BreadcrumbItem(
                BreadcrumbPage("Tasks")
            )
        )
    )


@with_code
def custom_separator_example():
    return Div(
        Breadcrumb(
            BreadcrumbList(
                BreadcrumbItem(BreadcrumbLink("Settings", href="/settings")),
                BreadcrumbSeparator(
                    Icon("lucide:slash", cls="h-4 w-4 align-middle")
                ),
                BreadcrumbItem(BreadcrumbLink("Security", href="/settings/security")),
                BreadcrumbSeparator(
                    Icon("lucide:slash", cls="h-4 w-4 align-middle")
                ),
                BreadcrumbItem(BreadcrumbPage("Two-Factor Auth"))
            )
        ),
        Breadcrumb(
            BreadcrumbList(
                BreadcrumbItem(BreadcrumbLink("Blog", href="/blog")),
                BreadcrumbSeparator(Span("·", cls="px-1 text-muted-foreground")),
                BreadcrumbItem(BreadcrumbLink("Engineering", href="/blog/engineering")),
                BreadcrumbSeparator(Span("·", cls="px-1 text-muted-foreground")),
                BreadcrumbItem(BreadcrumbPage("Migrating to Postgres"))
            )
        ),
        Breadcrumb(
            BreadcrumbList(
                BreadcrumbItem(BreadcrumbLink("Docs", href="/docs")),
                BreadcrumbSeparator(Span("→", cls="px-1 text-muted-foreground")),
                BreadcrumbItem(BreadcrumbLink("API", href="/docs/api")),
                BreadcrumbSeparator(Span("→", cls="px-1 text-muted-foreground")),
                BreadcrumbItem(BreadcrumbPage("Authentication"))
            )
        ),
        cls="space-y-4"
    )


@with_code
def with_icons_breadcrumb_example():
    return Breadcrumb(
        BreadcrumbList(
            BreadcrumbItem(
                BreadcrumbLink(
                    Icon("lucide:home", cls="size-4"),
                    "Home",
                    href="/",
                    cls="inline-flex items-center gap-1.5"
                )
            ),
            BreadcrumbSeparator(),
            BreadcrumbItem(
                BreadcrumbLink(
                    Icon("lucide:folder", cls="size-4"),
                    "Documents",
                    href="/documents",
                    cls="inline-flex items-center gap-1.5"
                )
            ),
            BreadcrumbSeparator(),
            BreadcrumbItem(
                BreadcrumbPage(
                    Icon("lucide:file-text", cls="size-4"),
                    "deploy.yml",
                    cls="inline-flex items-center gap-1.5"
                )
            )
        )
    )


@with_code
def programmatic_breadcrumb_example():
    segments = [
        ("Shop", "/shop"),
        ("Audio", "/shop/audio"),
        ("Headphones", "/shop/audio/headphones"),
        ("Sennheiser HD 600", None),
    ]

    items = []
    for i, (label, href) in enumerate(segments):
        if i > 0:
            items.append(BreadcrumbSeparator())
        items.append(
            BreadcrumbItem(
                BreadcrumbLink(label, href=href) if href else BreadcrumbPage(label)
            )
        )

    return Breadcrumb(BreadcrumbList(*items))


@with_code
def responsive_breadcrumb_example():
    return Breadcrumb(
        BreadcrumbList(
            BreadcrumbItem(
                BreadcrumbLink("Home", href="/")
            ),
            BreadcrumbSeparator(),
            BreadcrumbItem(
                BreadcrumbEllipsis(),
                cls="md:hidden"
            ),
            BreadcrumbSeparator(cls="md:hidden"),
            BreadcrumbItem(
                BreadcrumbLink("Team", href="/team"),
                cls="hidden md:inline-flex"
            ),
            BreadcrumbSeparator(cls="hidden md:inline-flex"),
            BreadcrumbItem(
                BreadcrumbLink("Permissions", href="/team/permissions"),
                cls="hidden md:inline-flex"
            ),
            BreadcrumbSeparator(cls="hidden md:inline-flex"),
            BreadcrumbItem(
                BreadcrumbPage("Roles")
            )
        )
    )


EXAMPLES_DATA = [
    {"fn": hero_breadcrumb_example, "title": "Default", "description": "Three-segment breadcrumb with the default chevron separator and current page marker"},
    {"fn": custom_separator_example, "title": "Custom Separators", "description": "Override the default chevron by passing any child to BreadcrumbSeparator — icons, text characters, or styled spans"},
    {"fn": with_icons_breadcrumb_example, "title": "With Icons", "description": "Pair icons with text in BreadcrumbLink and BreadcrumbPage for a file-browser style path"},
    {"fn": programmatic_breadcrumb_example, "title": "From Data", "description": "Build breadcrumbs from a list of (label, href) tuples — create a fresh BreadcrumbSeparator per iteration"},
    {"fn": responsive_breadcrumb_example, "title": "Responsive", "description": "Collapse middle segments into BreadcrumbEllipsis on mobile using Tailwind responsive utilities"},
]

API_REFERENCE = build_api_reference(
    main_props=[
        Prop("href", "str", "Link destination for BreadcrumbLink. Renders as an <a> element", "'#'"),
        Prop("cls", "str", "Additional CSS classes — accepted by all sub-components", "''"),
    ],
    components=[
        Component("Breadcrumb", "Root <nav aria-label='breadcrumb'> container"),
        Component("BreadcrumbList", "Ordered list (<ol>) wrapper. Provides flex layout with gap and text-sm styling"),
        Component("BreadcrumbItem", "List item (<li>) for a single breadcrumb segment"),
        Component("BreadcrumbLink", "Anchor (<a>) with hover color transition. Props: href (str, default '#')"),
        Component("BreadcrumbPage", "Current page indicator (<span aria-current='page'>). Non-interactive, styled in foreground color"),
        Component("BreadcrumbSeparator", "Visual separator (<li role='presentation' aria-hidden='true'>). Defaults to a chevron-right icon — pass any child to override"),
        Component("BreadcrumbEllipsis", "Collapsed-items indicator with a horizontal dots icon and sr-only 'More' text for screen readers"),
    ]
)


def create_breadcrumb_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)
