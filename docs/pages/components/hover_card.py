"""
Hover Card component documentation.
"""

# Component metadata for auto-discovery
TITLE = "Hover Card"
DESCRIPTION = "For sighted users to preview content available behind a link or element on hover. Unlike popovers, hover cards are triggered by mouse hover and are ideal for supplemental information."
CATEGORY = "overlay"
ORDER = 120
STATUS = "stable"

from starhtml import Div, P, Icon, Span, H4, A, Img
from starui.registry.components.hover_card import (
    HoverCard, HoverCardTrigger, HoverCardContent,
)
from starui.registry.components.button import Button
from starui.registry.components.badge import Badge
from starui.registry.components.avatar import Avatar
from utils import auto_generate_page, with_code, Component, build_api_reference


@with_code
def user_profile_hover_card_example():
    return Div(
        HoverCard(
            HoverCardTrigger(
                Div(
                    Avatar(
                        Img(src="https://github.com/shadcn.png", alt="@shadcn"),
                        size="sm",
                    ),
                    Span("@shadcn", cls="text-sm font-medium"),
                    cls="inline-flex items-center gap-2 p-2 rounded-md hover:bg-muted/50 transition-colors",
                )
            ),
            HoverCardContent(
                Div(
                    Div(
                        Avatar(
                            Img(src="https://github.com/shadcn.png", alt="@shadcn"),
                            size="md",
                        ),
                        Div(
                            H4("shadcn", cls="text-sm font-semibold"),
                            P("@shadcn", cls="text-xs text-muted-foreground"),
                        ),
                        cls="flex items-center gap-3",
                    ),
                    P(
                        "Building beautiful and accessible UI components. Creator of ui.shadcn.com.",
                        cls="text-sm text-muted-foreground",
                    ),
                    Div(
                        Icon("lucide:calendar-days", cls="size-3.5 text-muted-foreground"),
                        Span("Joined December 2021", cls="text-xs text-muted-foreground"),
                        cls="flex items-center gap-1.5",
                    ),
                    cls="grid gap-3",
                ),
            ),
        ),
        cls="flex justify-center",
    )


@with_code
def repository_hover_card_example():
    return Div(
        HoverCard(
            HoverCardTrigger(
                A("starui/components", href="#", cls="text-primary hover:underline font-medium text-sm"),
            ),
            HoverCardContent(
                Div(
                    Div(
                        Icon("lucide:folder-git-2", cls="size-4 text-muted-foreground"),
                        H4("starui/components", cls="text-sm font-semibold text-primary"),
                        Badge("Public", variant="secondary", cls="ml-auto text-xs"),
                        cls="flex items-center gap-2",
                    ),
                    P(
                        "Beautifully designed components for building interfaces with StarHTML.",
                        cls="text-sm text-muted-foreground",
                    ),
                    Div(
                        Div(
                            Icon("lucide:star", cls="size-3.5 text-yellow-500"),
                            Span("2.1k", cls="text-sm font-medium"),
                            cls="flex items-center gap-1",
                        ),
                        Div(
                            Icon("lucide:git-fork", cls="size-3.5 text-muted-foreground"),
                            Span("184", cls="text-sm text-muted-foreground"),
                            cls="flex items-center gap-1",
                        ),
                        Div(
                            Div(cls="size-2.5 bg-blue-500 rounded-full"),
                            Span("Python", cls="text-xs text-muted-foreground"),
                            cls="flex items-center gap-1",
                        ),
                        cls="flex items-center gap-4",
                    ),
                    cls="grid gap-3",
                ),
                side="top",
            ),
        ),
        cls="text-center",
    )


@with_code
def inline_link_hover_card_example():
    return Div(
        P(
            "The component system is built on top of ",
            HoverCard(
                HoverCardTrigger(
                    A("StarHTML", href="#", cls="text-primary hover:underline font-semibold"),
                ),
                HoverCardContent(
                    Div(
                        Div(
                            Icon("lucide:book-open", cls="size-4 text-muted-foreground"),
                            H4("StarHTML Framework", cls="font-semibold text-sm"),
                            cls="flex items-center gap-2",
                        ),
                        P(
                            "A Python framework for building modern web applications with server-side rendering and reactive components.",
                            cls="text-sm text-muted-foreground",
                        ),
                        A(
                            "View Documentation",
                            Icon("lucide:arrow-right", cls="size-3"),
                            href="#",
                            cls="inline-flex items-center gap-1 text-sm text-primary hover:underline",
                        ),
                        cls="grid gap-2",
                    ),
                    side="top",
                ),
            ),
            ", a modern Python web framework with reactive components and server-side rendering.",
            cls="text-sm leading-relaxed max-w-lg",
        ),
    )


@with_code
def positioning_hover_card_examples():
    positions = [
        ("Top", "top", {}),
        ("Bottom", "bottom", {}),
        ("Left", "left", {}),
        ("Right", "right", {"align": "start"}),
    ]

    def create_positioned_hover_card(label, side, extra_props):
        return HoverCard(
            HoverCardTrigger(Button(label, variant="outline", size="sm")),
            HoverCardContent(
                Div(
                    H4(f"{label} placement", cls="font-semibold text-sm"),
                    P(f"Content positioned to the {side} of the trigger.", cls="text-sm text-muted-foreground"),
                    cls="grid gap-1",
                ),
                side=side,
                **extra_props,
            ),
        )

    return Div(
        Div(
            *[create_positioned_hover_card(label, side, extra_props)
              for label, side, extra_props in positions],
            cls="flex gap-4 items-center justify-center flex-wrap",
        ),
        cls="py-8",
    )


EXAMPLES_DATA = [
    {"title": "User Profile", "description": "Profile preview on hover — the canonical hover card use case", "fn": user_profile_hover_card_example},
    {"title": "Repository Preview", "description": "Repository metadata card triggered from a link", "fn": repository_hover_card_example},
    {"title": "Inline Link", "description": "Hover card on a link within flowing paragraph text", "fn": inline_link_hover_card_example},
    {"title": "Positioning", "description": "Control placement with the side and align props", "fn": positioning_hover_card_examples},
]

API_REFERENCE = build_api_reference(
    components=[
        Component("HoverCard", "Container that manages open state for trigger and content on hover"),
        Component("HoverCardTrigger", "Element that opens/closes the hover card based on mouse enter/leave, with delays"),
        Component("HoverCardContent", "The floating content positioned relative to its trigger with side and alignment controls"),
    ]
)


def create_hover_card_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)
