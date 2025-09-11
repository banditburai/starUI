"""
Avatar component documentation - User profile images with fallback.
Clean, minimal, and reactive.
"""

# Component metadata for auto-discovery
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
from utils import with_code, Component, build_api_reference
from widgets.component_preview import ComponentPreview


def examples():
    """Generate avatar examples using ComponentPreview with tabs."""
    
    # Basic composition
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
    
    yield ComponentPreview(
        basic_avatar_example(),
        basic_avatar_example.code,
        title="Basic Avatar",
        description="Compose avatars with image and fallback components"
    )
    
    # Sizes using custom classes
    @with_code
    def avatar_sizes_example():
        return Div(
            Avatar(AvatarFallback("XS"), cls="size-6"),
            Avatar(AvatarFallback("SM"), cls="size-8"),
            Avatar(AvatarFallback("MD")),  # default size-10
            Avatar(AvatarFallback("LG"), cls="size-12"),
            Avatar(AvatarFallback("XL"), cls="size-16"),
            Avatar(AvatarFallback("2X"), cls="size-20"),
            cls="flex items-center gap-4"
        )
    
    yield ComponentPreview(
        avatar_sizes_example(),
        avatar_sizes_example.code,
        title="Avatar Sizes",
        description="Use size classes to create different avatar sizes"
    )
    
    # With Fallback
    @with_code
    def avatar_fallback_example():
        return Div(
            Avatar(AvatarFallback("CN")),
            Avatar(AvatarFallback("JD")),
            Avatar(AvatarFallback("AB")),
            cls="flex items-center gap-4"
        )
    
    yield ComponentPreview(
        avatar_fallback_example(),
        avatar_fallback_example.code,
        title="Avatar Fallback",
        description="Display initials when no image is available"
    )
    
    # Automatic Fallback with Datastar
    @with_code
    def automatic_fallback_avatar_example():
        return Div(
            Div(
                AvatarWithFallback(
                    src="https://github.com/shadcn.png",
                    alt="@shadcn",
                    fallback="CN",
                ),
                P("Valid URL", cls="text-xs text-muted-foreground text-center mt-1"),
                cls="flex flex-col items-center"
            ),
            Div(
                AvatarWithFallback(
                    src="https://invalid-url.com/image.jpg",
                    alt="Invalid",
                    fallback="IN",
                ),
                P("Invalid URL", cls="text-xs text-muted-foreground text-center mt-1"),
                cls="flex flex-col items-center"
            ),
            Div(
                AvatarWithFallback(fallback="NI"),
                P("No URL", cls="text-xs text-muted-foreground text-center mt-1"),
                cls="flex flex-col items-center"
            ),
            cls="flex items-start gap-4"
        )
    
    yield ComponentPreview(
        automatic_fallback_avatar_example(),
        automatic_fallback_avatar_example.code,
        title="Automatic Fallback",
        description="Uses Datastar signals to automatically show fallback when image fails"
    )
    
    # Avatar Group Pattern
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
    
    yield ComponentPreview(
        avatar_group_example(),
        avatar_group_example.code,
        title="Avatar Group",
        description="Create overlapping avatar groups with Tailwind utilities"
    )
    
    # With Badge Pattern
    @with_code
    def avatar_with_badge_example():
        return Div(
            # Green status badge
            Div(
                Avatar(AvatarFallback("JD")),
                Span(cls="absolute bottom-0 right-0 size-3 bg-green-500 rounded-full ring-2 ring-background"),
                cls="relative inline-block"
            ),
            # Red status badge
            Div(
                Avatar(AvatarFallback("AS")),
                Span(cls="absolute bottom-0 right-0 size-3 bg-red-500 rounded-full ring-2 ring-background"),
                cls="relative inline-block"
            ),
            # Yellow status badge
            Div(
                Avatar(AvatarFallback("PQ")),
                Span(cls="absolute bottom-0 right-0 size-3 bg-yellow-500 rounded-full ring-2 ring-background"),
                cls="relative inline-block"
            ),
            # Badge with count
            Div(
                Avatar(AvatarFallback("MN")),
                Span("5", cls="absolute bottom-0 right-0 size-4 bg-red-500 rounded-full ring-2 ring-background flex items-center justify-center text-[8px] font-bold text-white"),
                cls="relative inline-block"
            ),
            cls="flex items-center gap-4"
        )
    
    yield ComponentPreview(
        avatar_with_badge_example(),
        avatar_with_badge_example.code,
        title="Avatar with Badge",
        description="Add status indicators or notification badges using absolute positioning"
    )
    
    # Colored Initials Pattern
    @with_code
    def colored_initials_avatar_example():
        return Div(
            Avatar(AvatarFallback("JD", cls="bg-red-600 dark:bg-red-500 text-white font-semibold")),
            Avatar(AvatarFallback("AS", cls="bg-blue-600 dark:bg-blue-500 text-white font-semibold")),
            Avatar(AvatarFallback("PQ", cls="bg-green-600 dark:bg-green-500 text-white font-semibold")),
            Avatar(AvatarFallback("MN", cls="bg-purple-600 dark:bg-purple-500 text-white font-semibold")),
            Avatar(AvatarFallback("XY", cls="bg-orange-600 dark:bg-orange-500 text-white font-semibold")),
            cls="flex items-center gap-4"
        )
    
    yield ComponentPreview(
        colored_initials_avatar_example(),
        colored_initials_avatar_example.code,
        title="Colored Initials",
        description="Create colorful initial avatars with theme-aware backgrounds"
    )


def create_avatar_docs():
    """Create the Avatar component documentation page."""
    
    # For Avatar, users need to understand component composition and structure
    # rather than detailed props - examples demonstrate usage patterns clearly
    api_reference = build_api_reference(
        components=[
            Component("Avatar", "Main container component for avatar content"),
            Component("AvatarImage", "Image element with automatic loading and fallback support"),
            Component("AvatarFallback", "Fallback content (usually initials) when image unavailable"),
            Component("AvatarWithFallback", "Complete avatar with automatic Datastar-powered error handling"),
        ]
    )
    
    # Hero example showing diverse avatar types
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
        api_reference=api_reference,
        hero_example=hero_example,
        component_slug="avatar"
    )