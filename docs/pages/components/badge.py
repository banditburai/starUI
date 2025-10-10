"""
Badge component documentation - Convention-based functional approach.
Clean, minimal, and easy to extend.
"""

TITLE = "Badge"
DESCRIPTION = "Displays a badge or a component that looks like a badge."
CATEGORY = "ui"
ORDER = 20
STATUS = "stable"

from starhtml import Div, P, Span, Icon, A, H3, H4
from starui.registry.components.badge import Badge
from starui.registry.components.button import Button
from utils import auto_generate_page, Prop, build_api_reference, with_code
from widgets.component_preview import ComponentPreview


# ============================================================================
# EXAMPLE FUNCTIONS (decorated with @with_code for markdown generation)
# ============================================================================

@with_code
def basic_variants_example():
    badges = [
        ("Badge", "default"),
        ("Secondary", "secondary"),
        ("Destructive", "destructive"),
        ("Outline", "outline")
    ]

    badge_components = [
        Badge(text, variant=variant if variant != "default" else None, cls="mr-2" if i < len(badges) - 1 else "")
        for i, (text, variant) in enumerate(badges)
    ]

    return Div(*badge_components, cls="flex flex-wrap gap-2")


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


@with_code
def content_types_example():
    badges = [
        ("99+", "destructive"),
        ("v2.1.0", "secondary"),
        ("NEW", "default")
    ]

    badge_components = [
        Badge(text, variant=variant if variant != "default" else None, cls="mr-2" if i < len(badges) - 1 else "")
        for i, (text, variant) in enumerate(badges)
    ]

    return Div(*badge_components, cls="flex gap-2")


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


@with_code
def status_indicators_example():
    statuses = [
        ("Active", "default"),
        ("Pending", "secondary"),
        ("Error", "destructive"),
        ("Draft", "outline")
    ]

    status_badges = [
        Badge(status, variant=variant if variant != "default" else None, cls="mr-2" if i < len(statuses) - 1 else "")
        for i, (status, variant) in enumerate(statuses)
    ]

    return Div(*status_badges, cls="flex gap-2 flex-wrap")


@with_code
def category_tags_example():
    technologies = ["React", "TypeScript", "Next.js", "TailwindCSS"]

    tech_badges = [
        Badge(tech, variant="outline", cls="mr-2" if i < len(technologies) - 1 else "")
        for i, tech in enumerate(technologies)
    ]

    return Div(*tech_badges, cls="flex gap-2 flex-wrap")


@with_code
def notification_badges_example():
    notifications = [
        ("lucide:bell", "3", "bg-destructive text-destructive-foreground", "min-w-[1.25rem]"),
        ("lucide:mail", "12", "bg-primary text-primary-foreground", "min-w-[1.25rem]"),
        ("lucide:inbox", "99+", "bg-destructive text-destructive-foreground", "min-w-[1.5rem]")
    ]

    def create_notification_icon(icon_name, count, badge_color, badge_width):
        icon = Icon(icon_name, width="40", height="40", cls="text-muted-foreground block")
        badge = Span(count, cls=f"absolute -top-1 -right-1 z-10 {badge_width} h-5 px-1 rounded-full {badge_color} text-xs font-bold flex items-center justify-center ring-2 ring-background")
        return Div(icon, badge, cls="relative inline-block")

    notification_icons = [create_notification_icon(*notification) for notification in notifications]

    return Div(*notification_icons, cls="flex items-center gap-8")


@with_code
def avatar_badges_example():
    def create_avatar(initials, bg_color):
        return Div(initials, cls=f"size-10 rounded-full {bg_color} flex items-center justify-center text-white font-semibold text-sm")

    def create_count_badge(count):
        return Span(count, cls="absolute -top-1 -right-1 size-4 rounded-full bg-red-500 text-white text-xs font-bold flex items-center justify-center ring-2 ring-white")

    def create_status_indicator(color):
        return Span(cls=f"absolute bottom-0 right-0 size-3 rounded-full {color} shadow-[0_0_0_2px_theme(colors.background)]")

    def create_verified_badge():
        check_icon = Icon("lucide:check", width="12", height="12", cls="text-white font-bold")
        return Span(check_icon, cls="absolute -bottom-0.5 -right-0.5 size-4 rounded-full bg-blue-600 flex items-center justify-center shadow-[0_0_0_2px_theme(colors.background)]")

    avatars = [
        Div(create_avatar("JD", "bg-blue-500"), create_count_badge("3"), cls="relative inline-block"),
        Div(create_avatar("AS", "bg-green-500"), create_status_indicator("bg-green-400"), cls="relative inline-block"),
        Div(create_avatar("MK", "bg-orange-500"), create_status_indicator("bg-orange-400"), cls="relative inline-block"),
        Div(create_avatar("VU", "bg-purple-500"), create_verified_badge(), cls="relative inline-block")
    ]

    return Div(*avatars, cls="flex items-center gap-8")


@with_code
def size_variations_example():
    sizes = [
        ("Small", "px-1.5 py-0.5 text-xs"),
        ("Default", "px-2 py-0.5 text-xs"),
        ("Large", "px-3 py-1 text-sm")
    ]

    size_badges = [
        Badge(label, cls=f"{size_cls} {'mr-2' if i < len(sizes) - 1 else ''}")
        for i, (label, size_cls) in enumerate(sizes)
    ]

    return Div(*size_badges, cls="flex gap-2 items-center")


@with_code
def hero_badge_example():
    return Div(
        Div(
            Badge("Badge"),
            Badge("Secondary", variant="secondary"),
            Badge("Destructive", variant="destructive"),
            Badge("Outline", variant="outline"),
            cls="flex w-full flex-wrap gap-2"
        ),
        Div(
            Badge(
                Icon("lucide:badge-check", cls="w-3 h-3 mr-1"),
                "Verified",
                variant="secondary",
                cls="bg-blue-500 text-white dark:bg-blue-600"
            ),
            Badge("8", cls="h-5 min-w-[1.25rem] rounded-full px-1 font-mono tabular-nums"),
            Badge("99", variant="destructive", cls="h-5 min-w-[1.25rem] rounded-full px-1 font-mono tabular-nums"),
            Badge("20+", variant="outline", cls="h-5 min-w-[1.25rem] rounded-full px-1 font-mono tabular-nums"),
            cls="flex w-full flex-wrap gap-2"
        ),
        cls="flex flex-col items-center gap-2"
    )


# ============================================================================
# EXAMPLES GENERATOR (for rendering on the page)
# ============================================================================

# ============================================================================
# MODULE-LEVEL DATA
# ============================================================================

EXAMPLES_DATA = [
    {"fn": hero_badge_example, "title": "Badge", "description": "Display small count and labeling"},
    {"fn": basic_variants_example, "title": "Basic Variants", "description": "Default, secondary, outline, and destructive variants"},
    {"fn": badges_with_icons_example, "title": "With Icons", "description": "Badges enhanced with icons"},
    {"fn": content_types_example, "title": "Content Types", "description": "Numbers, text, and combined content"},
    {"fn": link_badges_example, "title": "Link Badges", "description": "Interactive badges as links"},
    {"fn": status_indicators_example, "title": "Status Indicators", "description": "Online, offline, and busy status"},
    {"fn": category_tags_example, "title": "Category Tags", "description": "Tag items with categories"},
    {"fn": notification_badges_example, "title": "Notification Badges", "description": "Alert counts on buttons and icons"},
    {"fn": avatar_badges_example, "title": "Avatar Badges", "description": "Status badges on avatars"},
    {"fn": size_variations_example, "title": "Size Variations", "description": "Small and large badge sizes"},
]

API_REFERENCE = build_api_reference(
    main_props=[
        Prop("variant", "Literal['default','secondary','outline','destructive']", "Visual style variant", "'default'"),
        Prop("cls", "str", "Additional CSS classes", "''"),
    ]
)


# ============================================================================
# DOCS PAGE
# ============================================================================

def create_badge_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)
