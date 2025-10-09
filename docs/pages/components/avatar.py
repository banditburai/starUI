"""
Avatar component documentation - User profile images with fallback.
Clean, minimal, and reactive.
"""

TITLE = "Avatar"
DESCRIPTION = "An image element with a fallback for representing the user."
CATEGORY = "ui"
ORDER = 15
STATUS = "stable"

from starhtml import Div, P, Span
from starui.registry.components.avatar import (
    Avatar,
    AvatarFallback,
    AvatarImage,
    AvatarWithFallback,
)
from utils import auto_generate_page, with_code, Component, build_api_reference
from widgets.component_preview import ComponentPreview


# ============================================================================
# EXAMPLE FUNCTIONS (decorated with @with_code for markdown generation)
# ============================================================================

@with_code
def basic_avatar_example():
    return Div(
        Avatar(
            AvatarImage(
                src="https://github.com/shadcn.png",
                alt="@shadcn",
            )
        ),
        Avatar(
            AvatarFallback("CN")
        ),
        Avatar(
            AvatarImage(
                src="https://avatars.githubusercontent.com/u/1?v=4",
                alt="User",
            )
        ),
        cls="flex items-center gap-4"
    )


@with_code
def avatar_sizes_example():
    sizes = [
        ("XS", "size-6"),
        ("SM", "size-8"),
        ("MD", ""),  # default size-10
        ("LG", "size-12"),
        ("XL", "size-16"),
        ("2X", "size-20")
    ]

    size_avatars = [
        Avatar(AvatarFallback(label), cls=size_cls)
        for label, size_cls in sizes
    ]

    return Div(*size_avatars, cls="flex items-center gap-4")


@with_code
def avatar_fallback_example():
    return Div(
        Avatar(AvatarFallback("CN")),
        Avatar(AvatarFallback("JD")),
        Avatar(AvatarFallback("AB")),
        cls="flex items-center gap-4"
    )


@with_code
def automatic_fallback_avatar_example():
    examples = [
        ("https://github.com/shadcn.png", "@shadcn", "CN", "Valid URL"),
        ("https://invalid-url.com/image.jpg", "Invalid", "IN", "Invalid URL"),
        (None, None, "NI", "No URL")
    ]

    def create_avatar_demo(src, alt, fallback, description):
        avatar = AvatarWithFallback(src=src, alt=alt, fallback=fallback) if src else AvatarWithFallback(fallback=fallback)
        label = P(description, cls="text-xs text-muted-foreground text-center mt-1")
        return Div(avatar, label, cls="flex flex-col items-center")

    avatar_demos = [create_avatar_demo(*example) for example in examples]

    return Div(*avatar_demos, cls="flex items-start gap-4")


@with_code
def avatar_group_example():
    return Div(
        # Basic group
        Div(
            Avatar(AvatarFallback("JD")),
            Avatar(AvatarFallback("AS")),
            Avatar(AvatarFallback("PQ")),
            Avatar(AvatarFallback("+2", cls="text-xs font-medium")),
            cls="flex -space-x-2 [&>*[data-slot=avatar]]:ring-2 [&>*[data-slot=avatar]]:ring-background"
        ),
        cls="mb-4"
    )


@with_code
def avatar_with_badge_example():
    def create_status_avatar(initials, badge_color):
        avatar = Avatar(AvatarFallback(initials))
        badge = Span(cls=f"absolute bottom-0 right-0 size-3 {badge_color} rounded-full ring-2 ring-background")
        return Div(avatar, badge, cls="relative inline-block")

    def create_count_avatar(initials, count):
        avatar = Avatar(AvatarFallback(initials))
        badge = Span(count, cls="absolute bottom-0 right-0 size-4 bg-red-500 rounded-full ring-2 ring-background flex items-center justify-center text-[8px] font-bold text-white")
        return Div(avatar, badge, cls="relative inline-block")

    return Div(
        create_status_avatar("JD", "bg-green-500"),
        create_status_avatar("AS", "bg-red-500"),
        create_status_avatar("PQ", "bg-yellow-500"),
        create_count_avatar("MN", "5"),
        cls="flex items-center gap-4"
    )


@with_code
def colored_initials_avatar_example():
    avatars = [
        ("JD", "red"),
        ("AS", "blue"),
        ("PQ", "green"),
        ("MN", "purple"),
        ("XY", "orange")
    ]

    colored_avatars = [
        Avatar(AvatarFallback(initials, cls=f"bg-{color}-600 dark:bg-{color}-500 text-white font-semibold"))
        for initials, color in avatars
    ]

    return Div(*colored_avatars, cls="flex items-center gap-4")


@with_code
def hero_avatar_example():
    return Div(
        # Regular avatars with images
        Avatar(
            AvatarImage(
                src="https://github.com/shadcn.png",
                alt="@shadcn"
            )
        ),
        Avatar(
            AvatarImage(
                src="https://avatars.githubusercontent.com/u/2?v=4",
                alt="User 2"
            )
        ),
        # Fallback avatars
        Avatar(AvatarFallback("CN")),
        # Colored initials
        Avatar(AvatarFallback("JD", cls="bg-red-600 dark:bg-red-500 text-white font-semibold")),
        Avatar(AvatarFallback("AS", cls="bg-blue-600 dark:bg-blue-500 text-white font-semibold")),
        # With badge
        Div(
            Avatar(
                AvatarImage(
                    src="https://avatars.githubusercontent.com/u/3?v=4",
                    alt="User 3"
                )
            ),
            Span(cls="absolute bottom-0 right-0 size-3 bg-green-500 rounded-full ring-2 ring-background"),
            cls="relative inline-block"
        ),
        Div(
            Avatar(AvatarFallback("MN")),
            Span("3", cls="absolute bottom-0 right-0 size-4 bg-red-500 rounded-full ring-2 ring-background flex items-center justify-center text-[8px] font-bold text-white"),
            cls="relative inline-block"
        ),
        # Group
        Div(
            Avatar(AvatarFallback("A", cls="text-xs")),
            Avatar(AvatarFallback("B", cls="text-xs")),
            Avatar(AvatarFallback("+2", cls="text-xs font-medium")),
            cls="flex -space-x-3 [&>*[data-slot=avatar]]:ring-2 [&>*[data-slot=avatar]]:ring-background [&>*[data-slot=avatar]]:size-8"
        ),
        cls="flex items-center gap-3 flex-wrap justify-center"
    )


# ============================================================================
# EXAMPLES GENERATOR (for rendering on the page)
# ============================================================================

def examples():
    yield ComponentPreview(
        basic_avatar_example(),
        basic_avatar_example.code,
        title="Basic Avatar",
        description="Compose avatars with image and fallback components"
    )

    yield ComponentPreview(
        avatar_sizes_example(),
        avatar_sizes_example.code,
        title="Avatar Sizes",
        description="Use size classes to create different avatar sizes"
    )

    yield ComponentPreview(
        avatar_fallback_example(),
        avatar_fallback_example.code,
        title="Avatar Fallback",
        description="Display initials when no image is available"
    )

    yield ComponentPreview(
        automatic_fallback_avatar_example(),
        automatic_fallback_avatar_example.code,
        title="Automatic Fallback",
        description="Uses Datastar signals to automatically show fallback when image fails"
    )

    yield ComponentPreview(
        avatar_group_example(),
        avatar_group_example.code,
        title="Avatar Group",
        description="Create overlapping avatar groups with Tailwind utilities"
    )

    yield ComponentPreview(
        avatar_with_badge_example(),
        avatar_with_badge_example.code,
        title="Avatar with Badge",
        description="Add status indicators or notification badges using absolute positioning"
    )

    yield ComponentPreview(
        colored_initials_avatar_example(),
        colored_initials_avatar_example.code,
        title="Colored Initials",
        description="Create colorful initial avatars with theme-aware backgrounds"
    )


# ============================================================================
# MODULE EXPORTS (for markdown generation)
# ============================================================================

EXAMPLES_DATA = [
    {"title": "Basic Avatar", "description": "Compose avatars with image and fallback components", "code": basic_avatar_example.code},
    {"title": "Avatar Sizes", "description": "Use size classes to create different avatar sizes", "code": avatar_sizes_example.code},
    {"title": "Avatar Fallback", "description": "Display initials when no image is available", "code": avatar_fallback_example.code},
    {"title": "Automatic Fallback", "description": "Uses Datastar signals to automatically show fallback when image fails", "code": automatic_fallback_avatar_example.code},
    {"title": "Avatar Group", "description": "Create overlapping avatar groups with Tailwind utilities", "code": avatar_group_example.code},
    {"title": "Avatar with Badge", "description": "Add status indicators or notification badges using absolute positioning", "code": avatar_with_badge_example.code},
    {"title": "Colored Initials", "description": "Create colorful initial avatars with theme-aware backgrounds", "code": colored_initials_avatar_example.code},
]

API_REFERENCE = build_api_reference(
    components=[
        Component("Avatar", "Main container component for avatar content"),
        Component("AvatarImage", "Image element with automatic loading and fallback support"),
        Component("AvatarFallback", "Fallback content (usually initials) when image unavailable"),
        Component("AvatarWithFallback", "Complete avatar with automatic Datastar-powered error handling"),
    ]
)


# ============================================================================
# DOCS PAGE
# ============================================================================

def create_avatar_docs():
    """Create the Avatar component documentation page."""
    hero_example = ComponentPreview(
        hero_avatar_example(),
        hero_avatar_example.code,
        copy_button=True
    )

    return auto_generate_page(
        TITLE,
        DESCRIPTION,
        list(examples()),
        cli_command="star add avatar",
        api_reference=API_REFERENCE,
        hero_example=hero_example,
        component_slug="avatar"
    )
