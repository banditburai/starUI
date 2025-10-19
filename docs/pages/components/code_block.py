TITLE = "Code Block"
DESCRIPTION = "Display code with syntax highlighting, copy functionality, and various styling options."
CATEGORY = "ui"
ORDER = 50
STATUS = "stable"

from starhtml import Div, P, H3, Pre, Code, Span, Icon, Signal
from starhtml.datastar import clipboard, set_timeout
from starui.registry.components.button import Button
from starui.registry.components.code_block import CodeBlock, CodeBlockStyles, InlineCode
from starui.registry.components.badge import Badge
from starui.registry.components.separator import Separator
from widgets.component_preview import ComponentPreview
from utils import auto_generate_page, with_code, Prop, Component, build_api_reference



def copy_button_pair(signal, content, size="sm", button_cls=""):
    """Reusable copy/check button pair with visual feedback."""
    base_button_props = {"variant": "ghost", "size": size}
    if button_cls:
        base_button_props["cls"] = button_cls

    return Div(
        Button(
            Icon("lucide:copy", cls="w-4 h-4"),
            data_on_click=[clipboard(text=content), signal.set(True), set_timeout([signal.set(False)], 2000)],
            data_show=~signal,
            **base_button_props
        ),
        Button(
            Icon("lucide:check", cls="w-4 h-4"),
            data_show=signal,
            **{**base_button_props, "cls": f"{button_cls} text-green-600".strip()}
        ),
        cls="flex"
    )



@with_code
def python_syntax_highlighting_example():
    return Div(
        P("Python Code", cls="font-medium mb-3"),
        CodeBlock('''def fibonacci(n):
    """Generate Fibonacci sequence up to n."""
    a, b = 0, 1
    sequence = []
    while a <= n:
        sequence.append(a)
        a, b = b, a + b
    return sequence

# Usage example
numbers = fibonacci(100)
print(f"Fibonacci numbers up to 100: {numbers}")''', language="python"),
        cls="w-full overflow-x-auto",
        style="scrollbar-width: thin; scrollbar-color: transparent transparent;"
    )


@with_code
def interactive_copy_feature_example():
    code = '''import asyncio
from datetime import datetime

async def process_data(data):
    """Process data asynchronously with timestamp."""
    timestamp = datetime.now().isoformat()
    print(f"[{timestamp}] Processing: {data}")

    # Simulate async work
    await asyncio.sleep(1)

    result = {
        'processed_data': data.upper(),
        'timestamp': timestamp,
        'status': 'completed'
    }

    return result

# Example usage
async def main():
    tasks = [
        process_data("hello"),
        process_data("world"),
        process_data("async")
    ]

    results = await asyncio.gather(*tasks)
    for result in results:
        print(f"Result: {result}")

if __name__ == "__main__":
    asyncio.run(main())'''

    code_content = Signal("code_content", code)
    copied = Signal("copied", False)

    return Div(
        P("Interactive Code Block", cls="font-medium mb-3"),
        Div(
            code_content, copied,
            Div(
                Span("example.py", cls="text-sm font-mono text-muted-foreground"),
                copy_button_pair(copied, code_content),
                cls="absolute top-0 left-0 right-0 z-10 flex items-center justify-between px-4 py-3 bg-muted/95 backdrop-blur-sm border-b border-border rounded-t-lg"
            ),
            # Blank lines at top provide space for overlay header
            CodeBlock(f'\n\n{code}', language="python"),
            cls="relative rounded-lg overflow-hidden"
        ),
        cls="w-full overflow-x-auto",
        style="scrollbar-width: thin; scrollbar-color: transparent transparent;"
    )


@with_code
def inline_code_snippets_example():
    return Div(
        P(
            "Use the ",
            InlineCode("useState"),
            " hook to manage component state in React. You can import it like this: ",
            InlineCode("import { useState } from 'react'"),
            ". Then call it in your component: ",
            InlineCode("const [count, setCount] = useState(0)"),
            " to create a state variable.",
            cls="text-sm leading-7 mb-4"
        ),

        P(
            "For styling, you can use CSS classes like ",
            InlineCode("bg-blue-500"),
            " for background color, ",
            InlineCode("text-white"),
            " for text color, and ",
            InlineCode("p-4"),
            " for padding.",
            cls="text-sm leading-7 mb-4"
        ),

        P(
            "Configuration files often use formats like ",
            InlineCode("config.json"),
            " or ",
            InlineCode("settings.yaml"),
            ". Environment variables are accessed via ",
            InlineCode("process.env.NODE_ENV"),
            " in Node.js.",
            cls="text-sm leading-7"
        ),

        cls="prose prose-sm w-full max-w-none px-3 sm:px-4 py-4 sm:py-6 border rounded-lg overflow-x-auto",
        style="scrollbar-width: thin; scrollbar-color: transparent transparent;"
    )


@with_code
def documentation_layout_example():
    package_managers = [
        ("npm", "npm install starui", "mb-4"),
        ("pnpm", "pnpm add starui", "mb-4"),
        ("yarn", "yarn add starui", "mb-6")
    ]

    copied_signals = {name: Signal(f"{name}_copied", False) for name, _, _ in package_managers}

    def create_package_manager_block(manager, command, margin_cls):
        signal = copied_signals[manager]
        button_position_cls = "absolute top-1/2 right-2 -translate-y-1/2 h-8 w-8"
        return Div(
            signal,
            P(manager, cls="text-xs text-muted-foreground mb-1"),
            Div(
                CodeBlock(command, language="bash", cls="text-sm py-3"),
                copy_button_pair(signal, command, size="icon", button_cls=button_position_cls),
                cls="relative"
            ),
            cls=margin_cls
        )

    return Div(
        Div(
            H3("Installation", cls="text-lg font-semibold mb-3"),
            P("Install StarUI using your preferred package manager:", cls="text-sm text-muted-foreground mb-3"),
            *[create_package_manager_block(*pm) for pm in package_managers],
            cls="mb-8"
        ),

        Separator(cls="mb-8"),

        Div(
            H3("Quick Start", cls="text-lg font-semibold mb-3"),
            P("Import and use components in your project:", cls="text-sm text-muted-foreground mb-3"),
            CodeBlock('''from starhtml import Div, H1, P
from starui import Button, Card, CardHeader, CardTitle, CardContent

def my_app():
    return Div(
        Card(
            CardHeader(
                CardTitle("Welcome to StarUI")
            ),
            CardContent(
                P("Build beautiful interfaces with ease."),
                Button("Get Started", variant="primary", cls="mt-4")
            )
        ),
        cls="max-w-md mx-auto mt-8"
    )''', language="python")
        ),

        cls="w-full px-3 sm:px-4 py-4 sm:py-6 border rounded-lg overflow-x-auto",
        style="scrollbar-width: thin; scrollbar-color: transparent transparent;"
    )


@with_code
def terminal_output_example():
    return Div(
        P("Terminal Output", cls="font-medium mb-3"),

        Div(
            Div(
                Div(
                    *[Div(cls=f"w-3 h-3 rounded-full bg-{color}-500") for color in ["red", "yellow", "green"]],
                    cls="flex gap-2"
                ),
                Span("Terminal", cls="text-sm text-muted-foreground"),
                cls="absolute top-0 left-0 right-0 z-10 flex items-center justify-between px-4 py-3 bg-gray-800 border-b border-gray-700 rounded-t-lg"
            ),
            
            CodeBlock('''

$ star create my-project
Creating new StarUI project...
✓ Project directory created
✓ Dependencies installed  
✓ Configuration files generated
✓ Example components added

Success! Your project is ready.

$ cd my-project
$ star dev
Starting development server...
Server running at http://localhost:3000

$ star add button
Adding Button component...
✓ Component files created
✓ Styles updated
✓ Documentation generated

Component 'Button' added successfully!
Run 'star dev' to see your changes.''',
                       language="bash",
                       cls="bg-gray-900 text-green-400 font-mono"),

            cls="relative rounded-lg overflow-hidden"
        ),

        cls="w-full overflow-x-auto",
        style="scrollbar-width: thin; scrollbar-color: transparent transparent;"
    )



EXAMPLES_DATA = [
    {"title": "Python Syntax Highlighting", "description": "Display Python code with automatic syntax highlighting", "fn": python_syntax_highlighting_example},
    {"title": "Interactive Copy Feature", "description": "Add copy-to-clipboard functionality with visual feedback", "fn": interactive_copy_feature_example},
    {"title": "Inline Code Snippets", "description": "Highlight short code snippets within text and documentation", "fn": inline_code_snippets_example},
    {"title": "Documentation Layout", "description": "Structure documentation with code blocks for installation and usage examples", "fn": documentation_layout_example},
    {"title": "Terminal Output", "description": "Style code blocks to look like terminal output with custom colors", "fn": terminal_output_example},
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