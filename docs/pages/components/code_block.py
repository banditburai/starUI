"""
Code Block component documentation - Syntax-highlighted code display.
Beautiful code blocks with syntax highlighting and copy functionality.
"""

# Component metadata for auto-discovery
TITLE = "Code Block" 
DESCRIPTION = "Display code with syntax highlighting, copy functionality, and various styling options."
CATEGORY = "ui"
ORDER = 50
STATUS = "stable"

from starhtml import Div, P, H3, H4, Pre, Code, Button as HTMLButton, Span, Icon
from starhtml.datastar import ds_signals, ds_on_click, ds_text, ds_show, value, ds_bind
from starui.registry.components.button import Button
from starui.registry.components.code_block import CodeBlock, InlineCode
from starui.registry.components.badge import Badge
from starui.registry.components.separator import Separator
from widgets.component_preview import ComponentPreview


def examples():
    """Generate code block examples using ComponentPreview with tabs."""
    
    # Basic syntax highlighting
    yield ComponentPreview(
        Div(
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
            cls="max-w-2xl"
        ),
        '''from starui.registry.components.code_block import CodeBlock

CodeBlock(\'\'\'def fibonacci(n):
    """Generate Fibonacci sequence up to n."""
    a, b = 0, 1
    sequence = []
    while a <= n:
        sequence.append(a)
        a, b = b, a + b
    return sequence

# Usage example
numbers = fibonacci(100)
print(f"Fibonacci numbers up to 100: {numbers}")\'\'\'', language="python")''',
        title="Python Syntax Highlighting",
        description="Beautiful syntax highlighting for Python code with proper indentation and colors"
    )
    
    # Code block with copy functionality (manual implementation)
    yield ComponentPreview(
        Div(
            P("Interactive Code Block", cls="font-medium mb-3"),
            
            # Code block with copy button - using relative positioning
            Div(
                # Header that overlaps the CodeBlock
                Div(
                    Span("example.py", cls="text-sm font-mono text-muted-foreground"),
                    Div(
                        Button(
                            Icon("lucide:copy", cls="w-4 h-4"),
                            ds_on_click("navigator.clipboard.writeText($code_content); $copied = true; setTimeout(() => $copied = false, 2000)"),
                            ds_show("!$copied"),
                            variant="ghost",
                            size="sm"
                        ),
                        Button(
                            Icon("lucide:check", cls="w-4 h-4"),
                            ds_show("$copied"),
                            variant="ghost", 
                            size="sm",
                            cls="text-green-600"
                        ),
                        cls="flex"
                    ),
                    cls="absolute top-0 left-0 right-0 z-10 flex items-center justify-between px-4 py-3 bg-muted/95 backdrop-blur-sm border-b border-border rounded-t-lg"
                ),
                
                # Code content with blank lines to account for header overlay
                CodeBlock('''

import asyncio
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
    asyncio.run(main())''', language="python"),
                
                ds_signals(
                    code_content=value('''import asyncio
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
    asyncio.run(main())'''),
                    copied=False
                ),
                cls="relative rounded-lg overflow-hidden"
            ),
            
            cls="max-w-3xl"
        ),
        '''from starhtml import Div, Span, Icon
from starhtml.datastar import ds_on_click, ds_show, ds_signals, value
from starui.registry.components.code_block import CodeBlock
from starui.registry.components.button import Button

# Code block with copy functionality
Div(
    # Header
    Div(
        Span("example.py", cls="text-sm font-mono text-muted-foreground"),
        Div(
            Button(
                Icon("lucide:copy", cls="w-4 h-4"),
                ds_on_click("navigator.clipboard.writeText($code_content); $copied = true; setTimeout(() => $copied = false, 2000)"),
                ds_show("!$copied"),
                variant="ghost",
                size="sm"
            ),
            Button(
                Icon("lucide:check", cls="w-4 h-4"),
                ds_show("$copied"),
                variant="ghost",
                size="sm",
                cls="text-green-600"
            ),
            cls="flex"
        ),
        cls="flex items-center justify-between px-4 py-2 bg-muted rounded-t-lg"
    ),
    
    # Code content
    CodeBlock(code_content, language="python", cls="rounded-t-none"),
    
    ds_signals(code_content=value("..."), copied=False)
)''',
        title="Interactive Copy Feature",
        description="Add copy functionality to code blocks with visual feedback"
    )
    
    # Inline code usage
    yield ComponentPreview(
        Div(
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
            
            cls="prose prose-sm max-w-2xl p-6 border rounded-lg"
        ),
        '''from starui.registry.components.code_block import InlineCode
from starhtml import P

P(
    "Use the ",
    InlineCode("useState"),
    " hook to manage component state in React. Import it like: ",
    InlineCode("import { useState } from 'react'"),
    "."
)

P(
    "For styling, use CSS classes like ",
    InlineCode("bg-blue-500"),
    " for background and ",
    InlineCode("text-white"),
    " for text color."
)''',
        title="Inline Code Snippets",
        description="Highlight code snippets within paragraphs and documentation"
    )
    
    # Documentation examples
    yield ComponentPreview(
        Div(
            # Installation section
            Div(
                H3("Installation", cls="text-lg font-semibold mb-3"),
                P("Install StarUI using your preferred package manager:", cls="text-sm text-muted-foreground mb-3"),
                
                # npm with proper CodeBlock
                Div(
                    P("npm", cls="text-xs text-muted-foreground mb-1"),
                    Div(
                        CodeBlock("npm install starui", language="bash", cls="text-sm py-3"),
                        Button(
                            Icon("lucide:copy", cls="w-4 h-4"),
                            ds_on_click("navigator.clipboard.writeText('npm install starui'); $npm_copied = true; setTimeout(() => $npm_copied = false, 2000)"),
                            ds_show("!$npm_copied"),
                            variant="ghost",
                            size="icon",
                            cls="absolute top-1/2 right-2 -translate-y-1/2 h-8 w-8"
                        ),
                        Button(
                            Icon("lucide:check", cls="w-4 h-4"),
                            ds_show("$npm_copied"),
                            variant="ghost",
                            size="icon",
                            cls="absolute top-1/2 right-2 -translate-y-1/2 h-8 w-8 text-green-600"
                        ),
                        ds_signals(npm_copied=False),
                        cls="relative"
                    ),
                    cls="mb-4"
                ),
                
                # pnpm with proper CodeBlock
                Div(
                    P("pnpm", cls="text-xs text-muted-foreground mb-1"),
                    Div(
                        CodeBlock("pnpm add starui", language="bash", cls="text-sm py-3"),
                        Button(
                            Icon("lucide:copy", cls="w-4 h-4"),
                            ds_on_click("navigator.clipboard.writeText('pnpm add starui'); $pnpm_copied = true; setTimeout(() => $pnpm_copied = false, 2000)"),
                            ds_show("!$pnpm_copied"),
                            variant="ghost",
                            size="icon",
                            cls="absolute top-1/2 right-2 -translate-y-1/2 h-8 w-8"
                        ),
                        Button(
                            Icon("lucide:check", cls="w-4 h-4"),
                            ds_show("$pnpm_copied"),
                            variant="ghost",
                            size="icon",
                            cls="absolute top-1/2 right-2 -translate-y-1/2 h-8 w-8 text-green-600"
                        ),
                        ds_signals(pnpm_copied=False),
                        cls="relative"
                    ),
                    cls="mb-4"
                ),
                
                # yarn with proper CodeBlock
                Div(
                    P("yarn", cls="text-xs text-muted-foreground mb-1"),
                    Div(
                        CodeBlock("yarn add starui", language="bash", cls="text-sm py-3"),
                        Button(
                            Icon("lucide:copy", cls="w-4 h-4"),
                            ds_on_click("navigator.clipboard.writeText('yarn add starui'); $yarn_copied = true; setTimeout(() => $yarn_copied = false, 2000)"),
                            ds_show("!$yarn_copied"),
                            variant="ghost",
                            size="icon",
                            cls="absolute top-1/2 right-2 -translate-y-1/2 h-8 w-8"
                        ),
                        Button(
                            Icon("lucide:check", cls="w-4 h-4"),
                            ds_show("$yarn_copied"),
                            variant="ghost",
                            size="icon",
                            cls="absolute top-1/2 right-2 -translate-y-1/2 h-8 w-8 text-green-600"
                        ),
                        ds_signals(yarn_copied=False),
                        cls="relative"
                    ),
                    cls="mb-6"
                ),
                
                cls="mb-8"
            ),
            
            Separator(cls="mb-8"),
            
            # Usage section
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
    )''', language="python"),
                
                cls=""
            ),
            
            cls="max-w-3xl p-6 border rounded-lg"
        ),
        '''from starui.registry.components.code_block import CodeBlock
from starui.registry.components.badge import Badge
from starhtml import H3, P, Div, Span
from starui.registry.components.button import Button

# Documentation with multiple code blocks
H3("Installation")
P("Install using your preferred package manager:")

# Inline command with copy button
Div(
    Span("npm install starui", cls="font-mono text-sm"),
    Button(
        Icon("lucide:copy", cls="w-4 h-4"),
        ds_on_click("navigator.clipboard.writeText('npm install starui')"),
        variant="ghost",
        size="sm"
    ),
    cls="flex items-center justify-between px-3 py-2 bg-muted rounded-md"
)

# Usage example
H3("Quick Start")
CodeBlock(\'\'\'from starhtml import Div, H1, P
from starui.registry.components.button import Button

def my_app():
    return Button("Click me!")\'\'\'', language="python")''',
        title="Documentation Layout",
        description="Structure documentation with code blocks for installation and usage examples"
    )
    
    # Terminal/command output
    yield ComponentPreview(
        Div(
            P("Terminal Output", cls="font-medium mb-3"),
            
            # Terminal-style code block with overlay header
            Div(
                # Terminal header overlay
                Div(
                    Div(
                        Div(cls="w-3 h-3 rounded-full bg-red-500"),
                        Div(cls="w-3 h-3 rounded-full bg-yellow-500"),
                        Div(cls="w-3 h-3 rounded-full bg-green-500"),
                        cls="flex gap-2"
                    ),
                    Span("Terminal", cls="text-sm text-muted-foreground"),
                    cls="absolute top-0 left-0 right-0 z-10 flex items-center justify-between px-4 py-3 bg-gray-800 border-b border-gray-700 rounded-t-lg"
                ),
                
                # Terminal content with blank lines for header space
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
            
            cls="w-full max-w-4xl"
        ),
        '''from starui.registry.components.code_block import CodeBlock
from starhtml import Div, Span

# Terminal-style code block
Div(
    # Terminal header
    Div(
        Div(
            Div(cls="w-3 h-3 rounded-full bg-red-500"),
            Div(cls="w-3 h-3 rounded-full bg-yellow-500"),
            Div(cls="w-3 h-3 rounded-full bg-green-500"),
            cls="flex gap-2"
        ),
        Span("Terminal"),
        cls="flex items-center justify-between px-4 py-2 bg-gray-800 rounded-t-lg"
    ),
    
    # Terminal content
    CodeBlock(\'\'\'$ star create my-project
Creating new StarUI project...
✓ Project directory created
✓ Dependencies installed

Success! Your project is ready.\'\'\', 
              language="bash",
              cls="bg-gray-900 text-green-400 font-mono rounded-t-none"),
    
    cls="bg-gray-900"
)''',
        title="Terminal Output",
        description="Style code blocks to look like terminal output with custom colors"
    )


def create_code_block_docs():
    """Create code block documentation page using convention-based approach."""
    from utils import auto_generate_page
    
    # Hero example showcasing basic functionality
    hero_example = ComponentPreview(
        Div(
            # Main code block
            Div(
                CodeBlock('''from starhtml import Div, H1, P
from starui import Button

def welcome_component():
    """A simple welcome component with a button."""
    return Div(
        H1("Welcome to StarUI", cls="text-2xl font-bold mb-4"),
        P("Build beautiful interfaces with Python components.", 
          cls="text-muted-foreground mb-6"),
        Button("Get Started", variant="primary")
    )''', language="python"),
                cls="mb-4"
            ),
            
            # Inline code example
            P(
                "Import the component with ",
                InlineCode("from starui import Button"),
                " and use it to display syntax-highlighted code blocks.",
                cls="text-sm text-muted-foreground max-w-2xl"
            ),
            
            cls="max-w-2xl"
        ),
        '''from starui.registry.components.code_block import CodeBlock, InlineCode

# Syntax-highlighted code block
CodeBlock(\'\'\'def hello_world():
    print("Hello, World!")
    
hello_world()\'\'\'', language="python")

# Inline code within text
P(
    "Use ",
    InlineCode("CodeBlock"),
    " for multi-line code and ",
    InlineCode("InlineCode"),
    " for inline snippets."
)''',
        copy_button=True
    )
    
    api_reference = {
        "components": [
            {
                "name": "CodeBlock",
                "description": "Display multi-line code with syntax highlighting",
                "props": [
                    {
                        "name": "code",
                        "type": "str",
                        "default": "Required",
                        "description": "The code content to display"
                    },
                    {
                        "name": "language",
                        "type": "str",
                        "default": "'python'",
                        "description": "Programming language for syntax highlighting"
                    },
                    {
                        "name": "class_name",
                        "type": "str",
                        "default": "''",
                        "description": "Additional CSS classes"
                    },
                    {
                        "name": "cls",
                        "type": "str",
                        "default": "''",
                        "description": "CSS classes (alternative to class_name)"
                    }
                ]
            },
            {
                "name": "InlineCode",
                "description": "Display inline code snippets without syntax highlighting",
                "props": [
                    {
                        "name": "text",
                        "type": "str",
                        "default": "Required",
                        "description": "The code text to display inline"
                    },
                    {
                        "name": "class_name",
                        "type": "str",
                        "default": "''",
                        "description": "Additional CSS classes"
                    },
                    {
                        "name": "cls",
                        "type": "str",
                        "default": "''",
                        "description": "CSS classes (alternative to class_name)"
                    }
                ]
            }
        ]
    }
    
    return auto_generate_page(
        TITLE,
        DESCRIPTION,
        list(examples()),
        cli_command="star add code-block",
        api_reference=api_reference,
        hero_example=hero_example,
        component_slug="code_block"
    )