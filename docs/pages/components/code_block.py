TITLE = "Code Block"
DESCRIPTION = "Display code with syntax highlighting, copy functionality, and theme-aware styling."
CATEGORY = "ui"
ORDER = 50
STATUS = "stable"

from starhtml import Div, P, H3, Span, Icon, Signal, clipboard
from starhtml.datastar import set_timeout
from starui.registry.components.button import Button
from starui.registry.components.code_block import CodeBlock, InlineCode
from starui.registry.components.separator import Separator
from utils import auto_generate_page, with_code, Component, build_api_reference


def copy_button(signal, content, size="sm", button_cls=""):
    """Copy/check button pair with visual feedback."""
    return Div(
        Button(
            Icon("lucide:copy", cls="w-4 h-4"),
            aria_label="Copy code",
            data_on_click=[clipboard(text=content), signal.set(True), set_timeout([signal.set(False)], 2000)],
            data_show=~signal,
            variant="ghost", size=size, cls=button_cls,
        ),
        Button(
            Icon("lucide:check", cls="w-4 h-4"),
            aria_label="Copied",
            data_show=signal,
            variant="ghost", size=size, cls=f"{button_cls} text-green-600".strip(),
        ),
        cls="flex"
    )


@with_code
def python_syntax_highlighting_example():
    return Div(
        CodeBlock('''from starhtml import Div, H1, P, Form, Input
from starui.registry.components.button import Button
from starui.registry.components.card import Card, CardContent, CardHeader, CardTitle


def contact_form():
    return Card(
        CardHeader(CardTitle("Get in touch")),
        CardContent(
            Form(
                Div(
                    Input(type="text", name="name", placeholder="Name"),
                    Input(type="email", name="email", placeholder="Email"),
                    cls="grid gap-3",
                ),
                Input(type="text", name="subject", placeholder="Subject", cls="mt-3"),
                Button("Send message", type="submit", cls="mt-4 w-full"),
                method="post", action="/contact",
            ),
        ),
    )''', language="python"),
        cls="w-full",
    )


@with_code
def interactive_copy_feature_example():
    code = '''from dataclasses import dataclass, field


@dataclass
class AppConfig:
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    db_url: str = "sqlite:///app.db"
    allowed_origins: list[str] = field(
        default_factory=lambda: ["http://localhost:3000"]
    )

    @property
    def is_production(self) -> bool:
        return not self.debug'''

    copied = Signal("copied", False)

    return Div(
        Div(
            copied,
            Div(
                Span("config.py", cls="text-sm font-mono text-foreground/70"),
                copy_button(copied, code),
                cls="flex items-center justify-between px-4 py-2 bg-muted/80 border-b border-border rounded-t-lg"
            ),
            CodeBlock(code, language="python", cls="!rounded-t-none !border-t-0"),
            cls="rounded-lg overflow-hidden"
        ),
        cls="w-full",
    )


@with_code
def inline_code_snippets_example():
    return Div(
        P(
            "Components are imported from the registry, e.g. ",
            InlineCode("from starui.registry.components.button import Button"),
            ". Each component accepts a ",
            InlineCode("cls"),
            " parameter for additional Tailwind classes and ",
            InlineCode("**kwargs"),
            " for HTML attributes.",
            cls="text-sm leading-7 mb-4"
        ),
        P(
            "Reactive state uses ",
            InlineCode("Signal"),
            " objects. Toggle visibility with ",
            InlineCode("data_show"),
            ", bind values with ",
            InlineCode("data_model"),
            ", and handle events with ",
            InlineCode("data_on_click"),
            ".",
            cls="text-sm leading-7 mb-4"
        ),
        P(
            "Run ",
            InlineCode("star add button card input"),
            " to scaffold components, or ",
            InlineCode("star list"),
            " to see what's available.",
            cls="text-sm leading-7"
        ),
        cls="prose prose-sm w-full max-w-none px-3 sm:px-4 py-4 sm:py-6 border rounded-lg",
    )


@with_code
def documentation_layout_example():
    install_methods = [
        ("pip", "pip install starui", "mb-4"),
        ("uv", "uv add starui", "mb-6"),
    ]

    copied_signals = {name: Signal(f"{name}_copied", False) for name, _, _ in install_methods}

    def install_block(manager, command, margin_cls):
        signal = copied_signals[manager]
        return Div(
            signal,
            P(manager, cls="text-xs text-muted-foreground mb-1"),
            Div(
                CodeBlock(command, language="bash", cls="text-sm py-3"),
                copy_button(signal, command, size="icon", button_cls="absolute top-1/2 right-2 -translate-y-1/2 h-8 w-8"),
                cls="relative"
            ),
            cls=margin_cls
        )

    return Div(
        Div(
            H3("Installation", cls="text-lg font-semibold mb-3"),
            P("Install StarUI and initialize your project:", cls="text-sm text-muted-foreground mb-3"),
            *[install_block(*m) for m in install_methods],
            cls="mb-8"
        ),

        Separator(cls="mb-8"),

        Div(
            H3("Add Components", cls="text-lg font-semibold mb-3"),
            P("Scaffold the components you need:", cls="text-sm text-muted-foreground mb-3"),
            CodeBlock('''# Initialize a new project
star init

# Add individual components
star add button
star add card input select

# See all available components
star list''', language="bash")
        ),

        cls="w-full px-3 sm:px-4 py-4 sm:py-6 border rounded-lg",
    )


@with_code
def terminal_output_example():
    return Div(
        Div(
            Div(
                Div(
                    *[Div(cls=f"w-3 h-3 rounded-full bg-{c}-500") for c in ["red", "yellow", "green"]],
                    cls="flex gap-2"
                ),
                Span("Terminal", cls="text-sm text-muted-foreground"),
                cls="flex items-center justify-between px-4 py-2 bg-muted/80 border-b border-border rounded-t-lg"
            ),
            CodeBlock('''$ star init
Initializing StarUI project...
  Writing pyproject.toml
  Writing static/css/input.css
  Writing tailwind.config.js
Done.

$ star add button card
Fetching: button, card
  src/components/button.py  written
  src/components/card.py    written
2 components added.

$ star dev
Watching for changes...
Serving on http://localhost:5001''',
                       language="bash",
                       style="border-top-left-radius: 0; border-top-right-radius: 0; border-top-width: 0;"),
            cls="rounded-lg overflow-hidden"
        ),
        cls="w-full",
    )


EXAMPLES_DATA = [
    {"title": "Syntax Highlighting", "description": "Python code with automatic token coloring via the Starlighter engine", "fn": python_syntax_highlighting_example},
    {"title": "Copy to Clipboard", "description": "File header with a copy button using Datastar signals and the clipboard action", "fn": interactive_copy_feature_example},
    {"title": "Inline Code", "description": "InlineCode for referencing symbols, commands, and parameters within prose", "fn": inline_code_snippets_example},
    {"title": "Documentation Layout", "description": "Installation instructions with per-command copy buttons and a quick-start guide", "fn": documentation_layout_example},
    {"title": "Terminal Output", "description": "Dark-themed code block styled as terminal output with real CLI commands", "fn": terminal_output_example},
]

API_REFERENCE = build_api_reference(
    components=[
        Component("CodeBlock", "Display multi-line code with syntax highlighting"),
        Component("CodeBlockStyles", "Generate theme-aware styles for code blocks (add once to app headers)"),
        Component("InlineCode", "Highlight short code snippets within text and documentation"),
    ]
)


def create_code_block_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)
