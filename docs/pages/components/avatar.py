"""
Avatar component documentation - User profile images with fallback.
"""

TITLE = "Avatar"
DESCRIPTION = "An image element with a fallback for representing the user."
CATEGORY = "ui"
ORDER = 15
STATUS = "stable"

from starhtml import Div, P, Span
from starui.registry.components.avatar import Avatar, AvatarFallback, AvatarImage
from utils import auto_generate_page, with_code, Prop, Component, build_api_reference


@with_code
def hero_avatar_example():
    return Div(
        Avatar(
            AvatarImage(
                src="https://avatars.githubusercontent.com/u/1024025?v=4",
                alt="Sarah Miller"
            )
        ),
        Avatar(
            AvatarImage(
                src="https://avatars.githubusercontent.com/u/25?v=4",
                alt="James Chen"
            )
        ),
        Avatar(AvatarFallback("AR")),
        Avatar(AvatarFallback("TK", cls="bg-red-600 dark:bg-red-500 text-white font-semibold")),
        Avatar(AvatarFallback("LW", cls="bg-blue-600 dark:bg-blue-500 text-white font-semibold")),
        Avatar(
            AvatarImage(
                src="https://invalid-url.example.com/missing.jpg",
                alt="Dev Patel"
            ),
            AvatarFallback("DP")
        ),
        cls="flex items-center gap-3 flex-wrap justify-center"
    )


@with_code
def avatar_sizes_example():
    sizes = [
        ("XS", "size-6"),
        ("SM", "size-8"),
        ("MD", ""),
        ("LG", "size-12"),
        ("XL", "size-16"),
        ("2X", "size-20")
    ]

    return Div(
        *[Avatar(AvatarFallback(label), cls=size_cls) for label, size_cls in sizes],
        cls="flex items-center gap-4"
    )


@with_code
def image_error_fallback_avatar_example():
    examples = [
        ("https://avatars.githubusercontent.com/u/25?v=4", "James Chen", "JC", "Valid URL"),
        ("https://invalid-url.example.com/missing.jpg", "Dev Patel", "DP", "Broken URL"),
        (None, None, "AR", "No image"),
    ]

    return Div(
        *[Div(
            Avatar(
                AvatarImage(src=src, alt=alt) if src else None,
                AvatarFallback(initials)
            ),
            P(label, cls="text-xs text-muted-foreground text-center mt-1"),
            cls="flex flex-col items-center"
        ) for src, alt, initials, label in examples],
        cls="flex items-start gap-6"
    )


@with_code
def status_badge_avatar_example():
    def with_status(initials, color, label):
        return Div(
            Avatar(AvatarFallback(initials)),
            Span(
                cls=f"absolute bottom-0 right-0 size-3 {color} rounded-full ring-2 ring-background",
                role="status",
                aria_label=label,
            ),
            cls="relative inline-block"
        )

    def with_count(src, alt, initials, count):
        return Div(
            Avatar(
                AvatarImage(src=src, alt=alt),
                AvatarFallback(initials)
            ),
            Span(
                str(count),
                cls="absolute -top-1 -right-1 size-5 bg-red-500 rounded-full ring-2 ring-background flex items-center justify-center text-[10px] font-bold text-white",
                role="status",
                aria_label=f"{count} notifications",
            ),
            cls="relative inline-block"
        )

    return Div(
        with_status("SM", "bg-green-500", "Online"),
        with_status("JC", "bg-red-500", "Busy"),
        with_status("AR", "bg-yellow-500", "Away"),
        with_count(
            "https://avatars.githubusercontent.com/u/1024025?v=4",
            "Sarah Miller", "SM", 3
        ),
        cls="flex items-center gap-5"
    )


@with_code
def avatar_group_example():
    members = [
        ("https://avatars.githubusercontent.com/u/25?v=4", "James Chen", "JC"),
        ("https://avatars.githubusercontent.com/u/1024025?v=4", "Sarah Miller", "SM"),
        (None, "Ava Rodriguez", "AR"),
        (None, "Tom Kim", "TK"),
    ]

    return Div(
        *[Avatar(
            AvatarImage(src=src, alt=name) if src else None,
            AvatarFallback(initials, cls="text-xs")
        ) for src, name, initials in members],
        Avatar(AvatarFallback("+3", cls="text-xs font-medium")),
        cls="flex -space-x-3 [&>*[data-slot=avatar]]:ring-2 [&>*[data-slot=avatar]]:ring-background [&>*[data-slot=avatar]]:size-9"
    )


@with_code
def user_profile_avatar_example():
    def profile_row(src, alt, initials, name, detail, color=""):
        return Div(
            Avatar(
                AvatarImage(src=src, alt=alt) if src else None,
                AvatarFallback(initials, cls=f"{color} text-white font-semibold" if color else "")
            ),
            Div(
                P(name, cls="text-sm font-medium leading-none"),
                P(detail, cls="text-sm text-muted-foreground"),
                cls="space-y-1"
            ),
            cls="flex items-center gap-3"
        )

    return Div(
        profile_row(
            "https://avatars.githubusercontent.com/u/25?v=4",
            "James Chen", "JC",
            "James Chen", "james@example.com"
        ),
        profile_row(
            None, None, "AR",
            "Ava Rodriguez", "Engineering Lead",
            color="bg-red-600 dark:bg-red-500"
        ),
        profile_row(
            None, None, "TK",
            "Tom Kim", "Last active 2 hours ago",
            color="bg-blue-600 dark:bg-blue-500"
        ),
        cls="space-y-4"
    )


EXAMPLES_DATA = [
    {"fn": hero_avatar_example, "title": "Image & Fallback", "description": "Image avatars, initials fallback, colored backgrounds, and automatic error recovery"},
    {"fn": avatar_sizes_example, "title": "Sizes", "description": "Override the default size-10 using Tailwind size utilities on the Avatar container"},
    {"fn": image_error_fallback_avatar_example, "title": "Image Error Fallback", "description": "AvatarFallback content appears when the image URL is broken or omitted"},
    {"fn": status_badge_avatar_example, "title": "Status & Badges", "description": "Overlay status dots and notification counts using absolute positioning with accessible labels"},
    {"fn": avatar_group_example, "title": "Avatar Group", "description": "Stack avatars with negative spacing and ring borders via the data-slot selector"},
    {"fn": user_profile_avatar_example, "title": "User Profiles", "description": "Avatar paired with name and metadata in common layout patterns"},
]

API_REFERENCE = build_api_reference(
    main_props=[
        Prop("cls", "str", "Additional CSS classes. Use Tailwind size utilities (size-6 through size-20) to override the default size-10", "''"),
    ],
    components=[
        Component("Avatar", "Root container. Renders as a rounded-full overflow-hidden flex container with data-slot='avatar' for parent-context selectors"),
        Component("AvatarImage", "Image element with built-in error detection via Datastar signals. Props: src (str, required), alt (str), loading (str, default 'lazy'), signal (str | Signal) for external error state control"),
        Component("AvatarFallback", "Displayed when no AvatarImage is provided or the image fails to load. Accepts any children — typically 1-2 character initials"),
    ]
)


def create_avatar_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)
