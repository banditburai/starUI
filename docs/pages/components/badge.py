"""
Badge component documentation - Inline labels, counts, and status indicators.
"""

TITLE = "Badge"
DESCRIPTION = "Displays a badge or a component that looks like a badge."
CATEGORY = "ui"
ORDER = 20
STATUS = "stable"

from starhtml import Div, Icon
from starui.registry.components.badge import Badge
from utils import auto_generate_page, Prop, Component, build_api_reference, with_code


@with_code
def hero_badge_example():
    return Div(
        Div(
            Badge("Published"),
            Badge("In Review", variant="secondary"),
            Badge("Rejected", variant="destructive"),
            Badge("Draft", variant="outline"),
            cls="flex flex-wrap gap-2"
        ),
        Div(
            Badge(
                Icon("lucide:badge-check", cls="w-3 h-3"),
                "Verified",
                variant="secondary",
                cls="bg-blue-600 text-white dark:bg-blue-700"
            ),
            Badge("3", cls="h-5 min-w-5 rounded-full px-1 font-mono tabular-nums"),
            Badge("99+", variant="destructive", cls="h-5 min-w-5 rounded-full px-1 font-mono tabular-nums"),
            Badge("v0.2.0", variant="outline"),
            cls="flex flex-wrap gap-2"
        ),
        cls="flex flex-col items-center gap-3"
    )


@with_code
def with_icons_badge_example():
    return Div(
        Badge(Icon("lucide:star", cls="w-3 h-3"), "Featured"),
        Badge(
            Div(cls="w-2 h-2 bg-green-500 rounded-full"),
            "Online",
            variant="outline"
        ),
        Badge(
            "Deploying",
            Icon("lucide:loader", cls="w-3 h-3 animate-spin"),
            variant="secondary"
        ),
        Badge(
            Icon("lucide:shield-check", cls="w-3 h-3"),
            "Verified",
        ),
        cls="flex gap-2 flex-wrap"
    )


@with_code
def link_badge_example():
    return Div(
        Badge("Changelog", href="/changelog", variant="outline"),
        Badge(
            Icon("lucide:external-link", cls="w-3 h-3"),
            "Source Code",
            href="https://github.com",
            variant="secondary"
        ),
        Badge(
            "Get Started",
            href="/docs/getting-started",
        ),
        cls="flex gap-2 flex-wrap"
    )


@with_code
def clickable_badge_example():
    return Div(
        Badge("Python", clickable=True, variant="outline"),
        Badge("FastHTML", clickable=True, variant="outline"),
        Badge("Datastar", clickable=True, variant="outline"),
        Badge(
            Icon("lucide:x", cls="w-3 h-3"),
            "Remove Filter",
            clickable=True,
            variant="destructive",
        ),
        cls="flex gap-2 flex-wrap"
    )


@with_code
def custom_styling_badge_example():
    return Div(
        Div(
            Badge("SM", cls="h-5 min-w-5 rounded-full px-1 text-[10px]"),
            Badge("Default"),
            Badge("LG", cls="px-3 py-1 text-sm"),
            cls="flex gap-2 items-center"
        ),
        Div(
            Badge("Success", cls="bg-green-700 text-white border-transparent"),
            Badge("Danger", cls="bg-red-600 text-white border-transparent"),
            Badge("Info", cls="bg-blue-600 text-white border-transparent"),
            cls="flex gap-2"
        ),
        cls="flex flex-col gap-3"
    )


EXAMPLES_DATA = [
    {"fn": hero_badge_example, "title": "Variants & Shapes", "description": "The four built-in variants plus icon badges and numeric pill counters"},
    {"fn": with_icons_badge_example, "title": "With Icons", "description": "Prepend or append icons, status dots, and spinners as Badge children"},
    {"fn": link_badge_example, "title": "As Link", "description": "Pass href to render Badge as an anchor element with hover states"},
    {"fn": clickable_badge_example, "title": "Clickable", "description": "Pass clickable=True to render as a semantic button element for interactive use"},
    {"fn": custom_styling_badge_example, "title": "Custom Styling", "description": "Override size, shape, and color via cls — Badge has no built-in size props"},
]

API_REFERENCE = build_api_reference(
    main_props=[
        Prop("variant", "Literal['default', 'secondary', 'outline', 'destructive']", "Visual style variant", "'default'"),
        Prop("href", "str | None", "URL to link to. Renders Badge as an <a> element with hover states", "None"),
        Prop("clickable", "bool", "Render as a <button> element for interactive badges", "False"),
        Prop("cls", "str", "Additional CSS classes for size, shape, or color overrides", "''"),
    ],
    components=[
        Component("Badge", "Inline label. Renders as <span> by default, <a> when href is set, <button> when clickable is True. Accepts arbitrary children — text, icons, status dots"),
    ]
)


def create_badge_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)
