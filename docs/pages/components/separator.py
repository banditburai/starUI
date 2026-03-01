TITLE = "Separator"
DESCRIPTION = "Visually or semantically separates content with horizontal or vertical dividers."
CATEGORY = "ui"
ORDER = 25
STATUS = "stable"

from starhtml import Div, P, Span, Icon, Code
from starui.registry.components.separator import Separator
from starui.registry.components.button import Button
from utils import with_code, Prop, build_api_reference, auto_generate_page


@with_code
def default_example():
    return Div(
        Div(
            P("Separator", cls="text-sm font-semibold"),
            P("A visual divider between sections.", cls="text-sm text-muted-foreground"),
        ),
        Separator(cls="my-4"),
        Div(
            Span("Docs", cls="text-sm"),
            Span("API", cls="text-sm"),
            Span("Source", cls="text-sm"),
            cls="flex gap-4"
        ),
        cls="max-w-sm"
    )


@with_code
def vertical_example():
    return Div(
        Div(
            Button(Icon("lucide:bold", cls="size-4"), variant="ghost", size="sm"),
            Button(Icon("lucide:italic", cls="size-4"), variant="ghost", size="sm"),
            Button(Icon("lucide:underline", cls="size-4"), variant="ghost", size="sm"),
            Separator(orientation="vertical", cls="mx-2 h-6"),
            Button(Icon("lucide:align-left", cls="size-4"), variant="ghost", size="sm"),
            Button(Icon("lucide:align-center", cls="size-4"), variant="ghost", size="sm"),
            Button(Icon("lucide:align-right", cls="size-4"), variant="ghost", size="sm"),
            Separator(orientation="vertical", cls="mx-2 h-6"),
            Button(Icon("lucide:list", cls="size-4"), variant="ghost", size="sm"),
            Button(Icon("lucide:list-ordered", cls="size-4"), variant="ghost", size="sm"),
            cls="flex items-center p-2 border rounded-lg"
        ),
        cls="flex justify-center"
    )


@with_code
def accessibility_example():
    return Div(
        Div(
            P("Decorative", cls="text-sm font-medium mb-2"),
            Separator(),
            P(
                "Default. Renders ",
                Code("aria-hidden=\"true\""),
                " — invisible to screen readers.",
                cls="text-sm text-muted-foreground mt-2"
            ),
        ),
        Div(
            P("Semantic", cls="text-sm font-medium mb-2"),
            Separator(decorative=False),
            P(
                "Renders ",
                Code("role=\"separator\""),
                " and ",
                Code("aria-orientation"),
                " — announced as a content boundary.",
                cls="text-sm text-muted-foreground mt-2"
            ),
        ),
        cls="max-w-sm space-y-8"
    )


@with_code
def custom_styles_example():
    styles = [
        ("Default", ""),
        ("Thick", "h-0.5"),
        ("Colored", "bg-blue-500"),
        ("Dashed", "border-t border-dashed border-muted-foreground bg-transparent h-0"),
        ("Gradient", "bg-gradient-to-r from-transparent via-muted-foreground to-transparent"),
    ]
    return Div(
        *[
            Div(
                P(label, cls="text-sm text-muted-foreground mb-2"),
                Separator(cls=cls) if cls else Separator()
            )
            for label, cls in styles
        ],
        cls="max-w-sm space-y-6"
    )


EXAMPLES_DATA = [
    {"fn": default_example, "title": "Default", "description": "Horizontal separator between content sections"},
    {"fn": vertical_example, "title": "Vertical", "description": "Vertical separators grouping related toolbar actions"},
    {"fn": accessibility_example, "title": "Accessibility", "description": "Decorative vs semantic separators for screen readers"},
    {"fn": custom_styles_example, "title": "Custom Styles", "description": "Thickness, color, dashed, and gradient variations"},
]

API_REFERENCE = build_api_reference(
    main_props=[
        Prop("orientation", "Literal['horizontal', 'vertical']", "Orientation of the separator", "'horizontal'"),
        Prop("decorative", "bool", "If True (default), adds aria-hidden. If False, adds role=\"separator\" and aria-orientation", "True"),
        Prop("cls", "str", "Additional CSS classes", "''"),
    ]
)


def create_separator_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)
