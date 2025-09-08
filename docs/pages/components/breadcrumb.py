"""
Breadcrumb component documentation - Navigation hierarchy paths.
"""

# Component metadata for auto-discovery
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
from widgets.component_preview import ComponentPreview


def examples():
    """Generate Breadcrumb examples using ComponentPreview with tabs."""
    
    # Note: Basic breadcrumb moved to hero example
    # This will be the first example after the hero
    
    # Custom separator
    yield ComponentPreview(
        Breadcrumb(
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
        ),
        '''Breadcrumb(
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
)''',
        title="Custom Separator",
        description="Use custom icons as separators between items"
    )
    
    # Long breadcrumb with ellipsis
    yield ComponentPreview(
        Breadcrumb(
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
        ),
        '''Breadcrumb(
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
)''',
        title="Collapsed",
        description="Use ellipsis to indicate hidden intermediate steps"
    )
    
    # Long path without ellipsis
    yield ComponentPreview(
        Breadcrumb(
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
        ),
        '''Breadcrumb(
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
)''',
        title="Long Path",
        description="Full breadcrumb trail with multiple levels"
    )
    
    # Breadcrumb with icons
    yield ComponentPreview(
        Breadcrumb(
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
        ),
        '''Breadcrumb(
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
)''',
        title="With Icons",
        description="Breadcrumb items with icons for better visual context"
    )
    
    # E-commerce product breadcrumb
    yield ComponentPreview(
        Breadcrumb(
            BreadcrumbList(
                BreadcrumbItem(
                    BreadcrumbLink("Shop", href="/shop")
                ),
                BreadcrumbSeparator(
                    Icon("lucide:chevron-right", width="16", height="16")
                ),
                BreadcrumbItem(
                    BreadcrumbLink("Electronics", href="/shop/electronics")
                ),
                BreadcrumbSeparator(
                    Icon("lucide:chevron-right", width="16", height="16")
                ),
                BreadcrumbItem(
                    BreadcrumbLink("Smartphones", href="/shop/electronics/smartphones")
                ),
                BreadcrumbSeparator(
                    Icon("lucide:chevron-right", width="16", height="16")
                ),
                BreadcrumbItem(
                    BreadcrumbLink("Apple", href="/shop/electronics/smartphones/apple")
                ),
                BreadcrumbSeparator(
                    Icon("lucide:chevron-right", width="16", height="16")
                ),
                BreadcrumbItem(
                    BreadcrumbPage("iPhone 15 Pro")
                )
            )
        ),
        '''Breadcrumb(
    BreadcrumbList(
        BreadcrumbItem(
            BreadcrumbLink("Shop", href="/shop")
        ),
        BreadcrumbSeparator(
            Icon("lucide:chevron-right", width="16", height="16")
        ),
        BreadcrumbItem(
            BreadcrumbLink("Electronics", href="/shop/electronics")
        ),
        BreadcrumbSeparator(
            Icon("lucide:chevron-right", width="16", height="16")
        ),
        BreadcrumbItem(
            BreadcrumbLink("Smartphones", href="/shop/electronics/smartphones")
        ),
        BreadcrumbSeparator(
            Icon("lucide:chevron-right", width="16", height="16")
        ),
        BreadcrumbItem(
            BreadcrumbLink("Apple", href="/shop/electronics/smartphones/apple")
        ),
        BreadcrumbSeparator(
            Icon("lucide:chevron-right", width="16", height="16")
        ),
        BreadcrumbItem(
            BreadcrumbPage("iPhone 15 Pro")
        )
    )
)''',
        title="E-commerce Product Path",
        description="Product category hierarchy with chevron separators"
    )
    
    # Different separator styles
    yield ComponentPreview(
        Div(
            # Dot separator
            Breadcrumb(
                BreadcrumbList(
                    BreadcrumbItem(
                        BreadcrumbLink("Blog", href="/blog")
                    ),
                    BreadcrumbSeparator(
                        Span("•", cls="px-2 text-muted-foreground")
                    ),
                    BreadcrumbItem(
                        BreadcrumbLink("Technology", href="/blog/tech")
                    ),
                    BreadcrumbSeparator(
                        Span("•", cls="px-2 text-muted-foreground")
                    ),
                    BreadcrumbItem(
                        BreadcrumbPage("AI Trends 2024")
                    )
                ),
                cls="mb-4"
            ),
            # Arrow separator
            Breadcrumb(
                BreadcrumbList(
                    BreadcrumbItem(
                        BreadcrumbLink("Settings", href="/settings")
                    ),
                    BreadcrumbSeparator(
                        Span("→", cls="px-2 text-muted-foreground")
                    ),
                    BreadcrumbItem(
                        BreadcrumbLink("Security", href="/settings/security")
                    ),
                    BreadcrumbSeparator(
                        Span("→", cls="px-2 text-muted-foreground")
                    ),
                    BreadcrumbItem(
                        BreadcrumbPage("Two-Factor Auth")
                    )
                ),
                cls="mb-4"
            ),
            # Pipe separator
            Breadcrumb(
                BreadcrumbList(
                    BreadcrumbItem(
                        BreadcrumbLink("Docs", href="/docs")
                    ),
                    BreadcrumbSeparator(
                        Span("|", cls="px-2 text-muted-foreground")
                    ),
                    BreadcrumbItem(
                        BreadcrumbLink("API", href="/docs/api")
                    ),
                    BreadcrumbSeparator(
                        Span("|", cls="px-2 text-muted-foreground")
                    ),
                    BreadcrumbItem(
                        BreadcrumbPage("Authentication")
                    )
                )
            )
        ),
        '''# Dot separator
Breadcrumb(
    BreadcrumbList(
        BreadcrumbItem(BreadcrumbLink("Blog", href="/blog")),
        BreadcrumbSeparator(Span("•", cls="px-2 text-muted-foreground")),
        BreadcrumbItem(BreadcrumbLink("Technology", href="/blog/tech")),
        BreadcrumbSeparator(Span("•", cls="px-2 text-muted-foreground")),
        BreadcrumbItem(BreadcrumbPage("AI Trends 2024"))
    )
)

# Arrow separator
Breadcrumb(
    BreadcrumbList(
        BreadcrumbItem(BreadcrumbLink("Settings", href="/settings")),
        BreadcrumbSeparator(Span("→", cls="px-2 text-muted-foreground")),
        BreadcrumbItem(BreadcrumbLink("Security", href="/settings/security")),
        BreadcrumbSeparator(Span("→", cls="px-2 text-muted-foreground")),
        BreadcrumbItem(BreadcrumbPage("Two-Factor Auth"))
    )
)

# Pipe separator
Breadcrumb(
    BreadcrumbList(
        BreadcrumbItem(BreadcrumbLink("Docs", href="/docs")),
        BreadcrumbSeparator(Span("|", cls="px-2 text-muted-foreground")),
        BreadcrumbItem(BreadcrumbLink("API", href="/docs/api")),
        BreadcrumbSeparator(Span("|", cls="px-2 text-muted-foreground")),
        BreadcrumbItem(BreadcrumbPage("Authentication"))
    )
)''',
        title="Separator Styles",
        description="Different separator styles: dots, arrows, and pipes"
    )
    
    # Responsive breadcrumb
    yield ComponentPreview(
        Breadcrumb(
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
        ),
        '''Breadcrumb(
    BreadcrumbList(
        BreadcrumbItem(
            BreadcrumbLink("Home", href="/")
        ),
        BreadcrumbSeparator(),
        # Ellipsis shown on mobile
        BreadcrumbItem(
            BreadcrumbEllipsis(),
            cls="md:hidden"
        ),
        BreadcrumbSeparator(cls="md:hidden"),
        # Full path shown on desktop
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
)''',
        title="Responsive",
        description="Shows ellipsis on mobile, full path on desktop"
    )


def create_breadcrumb_docs():
    """Create breadcrumb documentation page using convention-based approach."""
    from utils import auto_generate_page
    
    # Hero example - basic breadcrumb
    hero_example = ComponentPreview(
        Breadcrumb(
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
        ),
        '''Breadcrumb(
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
)'''
    )
    
    return auto_generate_page(
        TITLE,
        DESCRIPTION,
        list(examples()),
        cli_command="star add breadcrumb",
        hero_example=hero_example,
        component_slug="breadcrumb",
        api_reference={
            "components": [
                {
                    "name": "Breadcrumb",
                    "description": "The root breadcrumb container"
                },
                {
                    "name": "BreadcrumbList",
                    "description": "Contains the ordered list of breadcrumb items"
                },
                {
                    "name": "BreadcrumbItem",
                    "description": "Individual breadcrumb item container"
                },
                {
                    "name": "BreadcrumbLink",
                    "description": "Clickable breadcrumb link"
                },
                {
                    "name": "BreadcrumbPage",
                    "description": "Current page breadcrumb item (non-clickable)"
                },
                {
                    "name": "BreadcrumbSeparator",
                    "description": "Visual separator between breadcrumb items"
                },
                {
                    "name": "BreadcrumbEllipsis",
                    "description": "Collapsed breadcrumb indicator"
                }
            ]
        }
    )