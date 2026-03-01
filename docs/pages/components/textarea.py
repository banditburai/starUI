TITLE = "Textarea"
DESCRIPTION = "A multi-line text input field for longer content like comments, messages, and descriptions."
CATEGORY = "form"
ORDER = 25
STATUS = "stable"

from starhtml import Div, P, Span, Icon, Signal, switch, clipboard
from starui.registry.components.textarea import Textarea, TextareaWithLabel
from starui.registry.components.button import Button
from starui.registry.components.card import Card, CardHeader, CardContent, CardTitle, CardDescription
from starui.registry.components.badge import Badge
from starui.registry.components.label import Label
from utils import auto_generate_page, with_code, Prop, build_api_reference


@with_code
def default_example():
    return Div(
        Textarea(placeholder="Add a comment..."),
        TextareaWithLabel(
            label="Commit message",
            placeholder="fix: resolve null pointer in auth middleware",
            helper_text="Describe what changed and why",
        ),
        cls="space-y-6 w-full max-w-sm",
    )


@with_code
def states_example():
    return Div(
        TextareaWithLabel(
            label="System log",
            value="Build completed at 14:32 UTC. 0 errors, 0 warnings.",
            disabled=True,
        ),
        TextareaWithLabel(
            label="License",
            value="MIT License\n\nCopyright (c) 2026 Acme Corp.\nPermission is hereby granted...",
            readonly=True,
        ),
        TextareaWithLabel(
            label="Description",
            required=True,
            placeholder="Required field",
            helper_text="Minimum 10 characters",
        ),
        TextareaWithLabel(
            label="Bio",
            value="Software engineer who loves building tools.",
            error_text="Must be under 20 characters",
        ),
        cls="grid w-full max-w-lg gap-6",
    )


@with_code
def rows_and_resize_example():
    return Div(
        Div(
            Label("Compact (rows=2)"),
            Textarea(rows=2, placeholder="Short input..."),
            cls="grid gap-1.5",
        ),
        Div(
            Label("Standard (rows=5)"),
            Textarea(rows=5, placeholder="Multi-line input..."),
            cls="grid gap-1.5",
        ),
        Div(
            Label("Auto-grow"),
            Textarea(placeholder="Grows with content — no rows prop set"),
            cls="grid gap-1.5",
        ),
        Div(
            Label("Vertical resize"),
            Textarea(rows=4, resize="vertical", placeholder="Drag the bottom edge..."),
            cls="grid gap-1.5",
        ),
        cls="grid w-full max-w-lg gap-6",
    )


@with_code
def character_limit_example():
    bio = Signal("ta_bio", "")

    return Card(
        bio,
        CardHeader(
            CardTitle("Bio"),
            CardDescription("A few words about yourself"),
        ),
        CardContent(
            TextareaWithLabel(
                label="Bio",
                placeholder="A few words about yourself...",
                maxlength=280,
                signal=bio,
                rows=3,
            ),
            Div(
                Div(
                    Div(
                        cls="h-1 bg-primary rounded-full transition-all duration-300",
                        data_style_width=(bio.length >= 280).if_("100%", (bio.length / 280 * 100) + "%"),
                    ),
                    cls="w-full bg-secondary rounded-full h-1",
                ),
                P(
                    Span(cls="font-mono font-medium", data_text=bio.length),
                    " / 280",
                    cls="text-sm text-right",
                    data_attr_cls=switch([
                        (bio.length >= 280, "text-destructive"),
                        (bio.length >= 250, "text-orange-500"),
                    ], default="text-muted-foreground"),
                ),
                cls="space-y-2 mt-3",
            ),
            Button(
                "Save",
                cls="w-full mt-4",
                data_attr_disabled=bio.length.eq(0),
            ),
        ),
        cls="w-full max-w-sm",
    )


@with_code
def code_input_example():
    code = Signal("ta_code", "def fibonacci(n):\n    a, b = 0, 1\n    for _ in range(n):\n        a, b = b, a + b\n    return a")
    copied = Signal("ta_copied", False)

    return Div(
        code,
        copied,
        Div(
            Badge("Python", variant="outline"),
            cls="flex items-center justify-between mb-2",
        ),
        Textarea(
            signal=code,
            rows=8,
            resize="vertical",
            cls="font-mono text-sm",
            placeholder="# Enter code here...",
        ),
        Div(
            P(
                "Lines: ",
                Span(cls="font-mono", data_text=code.split('\n').length),
                " | Chars: ",
                Span(cls="font-mono", data_text=code.length),
                cls="text-xs text-muted-foreground",
            ),
            Button(
                Icon("lucide:check", cls="h-4 w-4 mr-2", data_show=copied),
                Icon("lucide:copy", cls="h-4 w-4 mr-2", data_show=copied.eq(False)),
                Span("Copied!", data_show=copied),
                Span("Copy", data_show=copied.eq(False)),
                size="sm",
                variant="outline",
                data_on_click=clipboard(code, signal=copied),
            ),
            cls="flex items-center justify-between mt-2",
        ),
        cls="w-full max-w-md",
    )


EXAMPLES_DATA = [
    {"title": "Default", "description": "Bare Textarea and TextareaWithLabel", "fn": default_example},
    {"title": "States", "description": "Disabled, readonly, required, and error states", "fn": states_example},
    {"title": "Rows and Resize", "description": "Fixed height, auto-grow, and resize control", "fn": rows_and_resize_example},
    {"title": "Character Limit", "description": "Reactive counter with color-coded feedback", "fn": character_limit_example},
    {"title": "Code Input", "description": "Monospace textarea with clipboard and line count", "fn": code_input_example},
]

API_REFERENCE = build_api_reference(
    main_props=[
        Prop("placeholder", "str | None", "Placeholder text shown when empty", "None"),
        Prop("value", "str | None", "Initial text value", "None"),
        Prop("signal", "str | None", "Datastar signal for two-way binding", "None"),
        Prop("rows", "int | None", "Number of visible text rows (auto-grows when omitted)", "None"),
        Prop("maxlength", "int | None", "Maximum number of characters", "None"),
        Prop("resize", "Literal['none','both','horizontal','vertical'] | None", "Controls textarea resizing behavior", "None"),
        Prop("disabled", "bool", "Whether the textarea is disabled", "False"),
        Prop("readonly", "bool", "Whether the textarea is read-only", "False"),
        Prop("required", "bool", "Whether the textarea is required", "False"),
        Prop("autofocus", "bool", "Auto-focus on page load", "False"),
        Prop("cls", "str", "Additional CSS classes", "''"),
    ]
)


def create_textarea_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)
