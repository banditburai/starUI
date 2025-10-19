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
from starui.registry.components.avatar import Avatar, AvatarFallback, AvatarImage
from utils import auto_generate_page, with_code, Component, build_api_reference
from widgets.component_preview import ComponentPreview



@with_code
def hero_avatar_example():
    return Div(
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
        Avatar(AvatarFallback("CN")),
        Avatar(AvatarFallback("JD", cls="bg-red-600 dark:bg-red-500 text-white font-semibold")),
        Avatar(AvatarFallback("AS", cls="bg-blue-600 dark:bg-blue-500 text-white font-semibold")),
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
        Div(
            Avatar(AvatarFallback("A", cls="text-xs")),
            Avatar(AvatarFallback("B", cls="text-xs")),
            Avatar(AvatarFallback("+2", cls="text-xs font-medium")),
            cls="flex -space-x-3 [&>*[data-slot=avatar]]:ring-2 [&>*[data-slot=avatar]]:ring-background [&>*[data-slot=avatar]]:size-8"
        ),
        cls="flex items-center gap-3 flex-wrap justify-center"
    )


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

    avatar_demos = [
        Div(
            Avatar(
                AvatarImage(src=src, alt=alt) if src else None,
                AvatarFallback(fallback)
            ),
            P(description, cls="text-xs text-muted-foreground text-center mt-1"),
            cls="flex flex-col items-center"
        )
        for src, alt, fallback, description in examples
    ]

    return Div(*avatar_demos, cls="flex items-start gap-4")


@with_code
def avatar_group_example():
    return Div(
        Avatar(AvatarFallback("JD")),
        Avatar(AvatarFallback("AS")),
        Avatar(AvatarFallback("PQ")),
        Avatar(AvatarFallback("+2", cls="text-xs font-medium")),
        cls="flex -space-x-2 [&>*[data-slot=avatar]]:ring-2 [&>*[data-slot=avatar]]:ring-background"
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


EXAMPLES_DATA = [
    {"fn": hero_avatar_example, "title": "Avatar", "description": "Display user avatar with image and fallback"},
    {"fn": basic_avatar_example, "title": "Basic Avatar", "description": "Simple avatar with image"},
    {"fn": avatar_sizes_example, "title": "Sizes", "description": "Avatars in different sizes"},
    {"fn": avatar_fallback_example, "title": "Fallback", "description": "Avatar with initials fallback"},
    {"fn": automatic_fallback_avatar_example, "title": "Automatic Fallback", "description": "Automatically extract initials from name"},
    {"fn": avatar_group_example, "title": "Avatar Group", "description": "Display multiple avatars together"},
    {"fn": avatar_with_badge_example, "title": "With Badge", "description": "Avatar with status badge"},
    {"fn": colored_initials_avatar_example, "title": "Colored Initials", "description": "Avatars with colored backgrounds"},
]

API_REFERENCE = build_api_reference(
    components=[
        Component("Avatar", "Main avatar container"),
        Component("AvatarImage", "Image displayed in avatar"),
        Component("AvatarFallback", "Fallback content when image fails or loads"),
    ]
)



def create_avatar_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)
