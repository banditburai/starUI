"""
Badge component documentation - Convention-based functional approach.
Clean, minimal, and easy to extend.
"""

# Component metadata for auto-discovery
TITLE = "Badge"
DESCRIPTION = "Displays a badge or a component that looks like a badge."
CATEGORY = "ui"
ORDER = 20
STATUS = "stable"

from starhtml import Div, P, Span, Icon, A, H3, H4
from starhtml.datastar import ds_on_click, ds_show, ds_signals, ds_text
from starui.registry.components.badge import Badge
from starui.registry.components.button import Button
from utils import auto_generate_page, Prop, build_api_reference, with_code
from widgets.component_preview import ComponentPreview


def examples():
    """Generate badge examples using ComponentPreview with tabs."""
    
    # Basic variants
    @with_code
    def basic_variants_example():
        return Div(
            Badge("Badge", cls="mr-2"),
            Badge("Secondary", variant="secondary", cls="mr-2"),
            Badge("Destructive", variant="destructive", cls="mr-2"),
            Badge("Outline", variant="outline"),
            cls="flex flex-wrap gap-2"
        )
    
    yield ComponentPreview(
        basic_variants_example(),
        basic_variants_example.code,
        title="Badge Variants",
        description="Different visual styles for badges"
    )
    
    # With icons
    @with_code
    def badges_with_icons_example():
        return Div(
            Badge(Icon("lucide:star", cls="w-3 h-3"), "Featured", cls="mr-2"),
            Badge(
                Div(cls="w-2 h-2 bg-green-500 rounded-full"),
                "Online",
                variant="outline"
            ),
            cls="flex gap-2"
        )
    
    yield ComponentPreview(
        badges_with_icons_example(),
        badges_with_icons_example.code,
        title="Badges with Icons",
        description="Enhance badges with icons or status indicators"
    )
    
    # Different content types
    @with_code
    def content_types_example():
        return Div(
            Badge("99+", variant="destructive", cls="mr-2"),
            Badge("v2.1.0", variant="secondary", cls="mr-2"),
            Badge("NEW", variant="default"),
            cls="flex gap-2"
        )
    
    yield ComponentPreview(
        content_types_example(),
        content_types_example.code,
        title="Content Types",
        description="Numbers, versions, and labels"
    )
    
    # As links
    @with_code
    def link_badges_example():
        return Div(
            Badge("Documentation", href="/docs", variant="outline", cls="mr-2"),
            Badge(
                Icon("lucide:external-link", cls="w-3 h-3"),
                "GitHub",
                href="https://github.com",
                variant="secondary"
            ),
            cls="flex gap-2"
        )
    
    yield ComponentPreview(
        link_badges_example(),
        link_badges_example.code,
        title="Link Badges",
        description="Badges that act as links"
    )
    
    # Status indicators
    @with_code
    def status_indicators_example():
        return Div(
            Badge("Active", variant="default", cls="mr-2"),
            Badge("Pending", variant="secondary", cls="mr-2"),
            Badge("Error", variant="destructive", cls="mr-2"),
            Badge("Draft", variant="outline"),
            cls="flex gap-2 flex-wrap"
        )
    
    yield ComponentPreview(
        status_indicators_example(),
        status_indicators_example.code,
        title="Status Indicators",
        description="Use badges to show different states"
    )
    
    # Category tags
    @with_code
    def category_tags_example():
        return Div(
            Badge("React", variant="outline", cls="mr-2"),
            Badge("TypeScript", variant="outline", cls="mr-2"),
            Badge("Next.js", variant="outline", cls="mr-2"),
            Badge("TailwindCSS", variant="outline"),
            cls="flex gap-2 flex-wrap"
        )
    
    yield ComponentPreview(
        category_tags_example(),
        category_tags_example.code,
        title="Category Tags",
        description="Use badges as category or technology tags"
    )
    
    # Notification badges - Professional implementation based on research
    @with_code
    def notification_badges_example():
        return Div(
            # Icon badges with properly proportioned icons and badges
            Div(
                Icon("lucide:bell", width="40", height="40", cls="text-muted-foreground block"),
                Span("3", 
                     cls="absolute -top-1 -right-1 z-10 min-w-[1.25rem] h-5 px-1 rounded-full bg-destructive text-destructive-foreground text-xs font-bold flex items-center justify-center ring-2 ring-background"),
                cls="relative inline-block"
            ),
            Div(
                Icon("lucide:mail", width="40", height="40", cls="text-muted-foreground block"),
                Span("12", 
                     cls="absolute -top-1 -right-1 z-10 min-w-[1.25rem] h-5 px-1 rounded-full bg-primary text-primary-foreground text-xs font-bold flex items-center justify-center ring-2 ring-background"),
                cls="relative inline-block"
            ),
            Div(
                Icon("lucide:inbox", width="40", height="40", cls="text-muted-foreground block"),
                Span("99+", 
                     cls="absolute -top-1 -right-1 z-10 min-w-[1.5rem] h-5 px-1 rounded-full bg-destructive text-destructive-foreground text-xs font-bold flex items-center justify-center ring-2 ring-background"),
                cls="relative inline-block"
            ),
            cls="flex items-center gap-8"
        )
    
    yield ComponentPreview(
        notification_badges_example(),
        notification_badges_example.code,
        title="Notification Badges on Icons",
        description="Show notification counts overlapping icons with professional positioning"
    )
    
    # Avatar badges - Professional status indicators for user interfaces
    @with_code
    def avatar_badges_example():
        return Div(
            # Avatar with unread message count
            Div(
                Div("JD", cls="size-10 rounded-full bg-blue-500 flex items-center justify-center text-white font-semibold text-sm"),
                Span("3", cls="absolute -top-1 -right-1 size-4 rounded-full bg-red-500 text-white text-xs font-bold flex items-center justify-center ring-2 ring-white"),
                cls="relative inline-block"
            ),
            # Avatar with online status - Discord-style masked ring
            Div(
                Div("AS", cls="size-10 rounded-full bg-green-500 flex items-center justify-center text-white font-semibold text-sm"),
                Span(cls="absolute bottom-0 right-0 size-3 rounded-full bg-green-400 shadow-[0_0_0_2px_theme(colors.background)]"),
                cls="relative inline-block"
            ),
            # Avatar with away status - Discord-style masked ring  
            Div(
                Div("MK", cls="size-10 rounded-full bg-orange-500 flex items-center justify-center text-white font-semibold text-sm"),
                Span(cls="absolute bottom-0 right-0 size-3 rounded-full bg-orange-400 shadow-[0_0_0_2px_theme(colors.background)]"),
                cls="relative inline-block"
            ),
            # Avatar with verified badge
            Div(
                Div("VU", cls="size-10 rounded-full bg-purple-500 flex items-center justify-center text-white font-semibold text-sm"),
                Span(
                    Icon("lucide:check", width="12", height="12", cls="text-white font-bold"),
                    cls="absolute -bottom-0.5 -right-0.5 size-4 rounded-full bg-blue-600 flex items-center justify-center shadow-[0_0_0_2px_theme(colors.background)]"
                ),
                cls="relative inline-block"
            ),
            cls="flex items-center gap-8"
        )
    
    yield ComponentPreview(
        avatar_badges_example(),
        avatar_badges_example.code,
        title="Avatar Status Indicators", 
        description="Avatar status indicators with clean background masking"
    )
    
    # Size variations (custom implementation)
    @with_code
    def size_variations_example():
        return Div(
            Badge("Small", cls="px-1.5 py-0.5 text-xs mr-2"),
            Badge("Default", cls="px-2 py-0.5 text-xs mr-2"),
            Badge("Large", cls="px-3 py-1 text-sm"),
            cls="flex gap-2 items-center"
        )
    
    yield ComponentPreview(
        size_variations_example(),
        size_variations_example.code,
        title="Size Variations",
        description="Custom size variations for different use cases"
    )


def create_badge_docs():
    """Create badge documentation page using convention-based approach."""
    from utils import auto_generate_page
    
    # Hero example - comprehensive showcase matching ShadCN
    @with_code
    def hero_badge_example():
        return Div(
            # First row - all variants
            Div(
                Badge("Badge"),
                Badge("Secondary", variant="secondary"),
                Badge("Destructive", variant="destructive"),
                Badge("Outline", variant="outline"),
                cls="flex w-full flex-wrap gap-2"
            ),
            # Second row - practical examples
            Div(
                Badge(
                    Icon("lucide:badge-check", cls="w-3 h-3 mr-1"),
                    "Verified",
                    variant="secondary",
                    cls="bg-blue-500 text-white dark:bg-blue-600"
                ),
                Badge(
                    "8",
                    cls="h-5 min-w-[1.25rem] rounded-full px-1 font-mono tabular-nums"
                ),
                Badge(
                    "99",
                    variant="destructive",
                    cls="h-5 min-w-[1.25rem] rounded-full px-1 font-mono tabular-nums"
                ),
                Badge(
                    "20+",
                    variant="outline",
                    cls="h-5 min-w-[1.25rem] rounded-full px-1 font-mono tabular-nums"
                ),
                cls="flex w-full flex-wrap gap-2"
            ),
            cls="flex flex-col items-center gap-2"
        )
    
    hero_example = ComponentPreview(
        hero_badge_example(),
        hero_badge_example.code,
        copy_button=True
    )
    
    return auto_generate_page(
        TITLE,
        DESCRIPTION,
        list(examples()),
        cli_command="star add badge",
        hero_example=hero_example,
        component_slug="badge",
        api_reference=build_api_reference(
            main_props=[
                Prop("variant", "Literal['default', 'secondary', 'destructive', 'outline']", 
                     "Badge visual variant", "'default'"),
                Prop("href", "str | None", 
                     "Optional URL to make badge a link", "None"),
                Prop("cls", "str", 
                     "Additional CSS classes", "''"),
            ]
        )
    )