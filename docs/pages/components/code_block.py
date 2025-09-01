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
from starui.registry.components.code_block import CodeBlock, InlineCode
from starui.registry.components.button import Button
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
    
    # Multiple language support
    yield ComponentPreview(
        Div(
            # JavaScript
            Div(
                Div(
                    Badge("JavaScript", variant="outline"),
                    cls="mb-3"
                ),
                CodeBlock('''// Modern JavaScript with async/await
async function fetchUserData(userId) {
    try {
        const response = await fetch(`/api/users/${userId}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const userData = await response.json();
        return userData;
    } catch (error) {
        console.error('Failed to fetch user data:', error);
        return null;
    }
}

// Usage with destructuring
const { name, email, avatar } = await fetchUserData(123) || {};''', language="javascript"),
                cls="mb-6"
            ),
            
            # CSS
            Div(
                Div(
                    Badge("CSS", variant="outline"),
                    cls="mb-3"
                ),
                CodeBlock('''/* Modern CSS with custom properties */
:root {
    --primary-color: #3b82f6;
    --secondary-color: #64748b;
    --border-radius: 0.5rem;
    --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}

.button {
    background: var(--primary-color);
    color: white;
    border-radius: var(--border-radius);
    box-shadow: var(--shadow-lg);
    transition: all 0.2s ease-in-out;
}

.button:hover {
    transform: translateY(-1px);
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
}''', language="css"),
                cls="mb-6"
            ),
            
            # HTML
            Div(
                Div(
                    Badge("HTML", variant="outline"),
                    cls="mb-3"
                ),
                CodeBlock('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Modern Web Page</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <header class="header">
        <nav class="navigation">
            <a href="#home" class="nav-link">Home</a>
            <a href="#about" class="nav-link">About</a>
            <a href="#contact" class="nav-link">Contact</a>
        </nav>
    </header>
    
    <main class="main-content">
        <section class="hero">
            <h1>Welcome to Our Site</h1>
            <p>Beautiful, modern web experiences.</p>
        </section>
    </main>
</body>
</html>''', language="html"),
                cls=""
            ),
            
            cls="max-w-3xl space-y-6"
        ),
        '''from starui.registry.components.code_block import CodeBlock

# JavaScript
CodeBlock(\'\'\'async function fetchUserData(userId) {
    const response = await fetch(`/api/users/${userId}`);
    return response.json();
}\'\'\'', language="javascript")

# CSS  
CodeBlock(\'\'\'/* Custom properties */
:root {
    --primary-color: #3b82f6;
}

.button {
    background: var(--primary-color);
}\'\'\', language="css")

# HTML
CodeBlock(\'\'\'<!DOCTYPE html>
<html lang="en">
<head>
    <title>Page Title</title>
</head>
<body>
    <h1>Hello World</h1>
</body>
</html>\'\'\', language="html")''',
        title="Multiple Languages",
        description="Syntax highlighting support for various programming languages"
    )
    
    # Code block with copy functionality (manual implementation)
    yield ComponentPreview(
        Div(
            P("Interactive Code Block", cls="font-medium mb-3"),
            
            # Code block with copy button
            Div(
                # Header with copy button
                Div(
                    Span("example.py", cls="text-sm font-mono text-muted-foreground"),
                    Button(
                        Icon("lucide:copy", cls="w-4 h-4 mr-2"),
                        "Copy",
                        ds_on_click("navigator.clipboard.writeText($code_content); $copied = true; setTimeout(() => $copied = false, 2000)"),
                        variant="ghost",
                        size="sm",
                        cls="ml-auto"
                    ),
                    Button(
                        Icon("lucide:check", cls="w-4 h-4 mr-2"),
                        "Copied!",
                        ds_show("$copied"),
                        variant="ghost", 
                        size="sm",
                        cls="ml-auto text-green-600"
                    ),
                    cls="flex items-center justify-between px-4 py-2 bg-muted border-b"
                ),
                
                # Code content
                Div(
                    CodeBlock('''import asyncio
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
                    cls="overflow-x-auto"
                ),
                
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
                cls="border rounded-lg overflow-hidden"
            ),
            
            cls="max-w-3xl"
        ),
        '''from starui.registry.components.code_block import CodeBlock
from starui.registry.components.button import Button
from starhtml import Div, Span, Icon
from starhtml.datastar import ds_on_click, ds_show, ds_signals, value

# Code block with copy functionality
Div(
    # Header
    Div(
        Span("example.py", cls="text-sm font-mono text-muted-foreground"),
        Button(
            Icon("lucide:copy", cls="w-4 h-4 mr-2"),
            "Copy",
            ds_on_click("navigator.clipboard.writeText($code_content); $copied = true; setTimeout(() => $copied = false, 2000)"),
            variant="ghost",
            size="sm"
        ),
        Button(
            Icon("lucide:check", cls="w-4 h-4 mr-2"),
            "Copied!",
            ds_show("$copied"),
            variant="ghost",
            size="sm",
            cls="text-green-600"
        ),
        cls="flex items-center justify-between px-4 py-2 bg-muted border-b"
    ),
    
    # Code content
    CodeBlock(code_content, language="python"),
    
    ds_signals(code_content=value("..."), copied=False),
    cls="border rounded-lg overflow-hidden"
)''',
        title="Interactive Copy Feature",
        description="Add copy functionality to code blocks with visual feedback"
    )
    
    # Inline code usage
    yield ComponentPreview(
        Div(
            P([
                "Use the ",
                InlineCode("useState"),
                " hook to manage component state in React. You can import it like this: ",
                InlineCode("import { useState } from 'react'"),
                ". Then call it in your component: ",
                InlineCode("const [count, setCount] = useState(0)"),
                " to create a state variable."
            ], cls="text-sm leading-relaxed mb-4"),
            
            P([
                "For styling, you can use CSS classes like ",
                InlineCode("bg-blue-500"),
                " for background color, ",
                InlineCode("text-white"),
                " for text color, and ",
                InlineCode("p-4"),
                " for padding."
            ], cls="text-sm leading-relaxed mb-4"),
            
            P([
                "Configuration files often use formats like ",
                InlineCode("config.json"),
                " or ",
                InlineCode("settings.yaml"),
                ". Environment variables are accessed via ",
                InlineCode("process.env.NODE_ENV"),
                " in Node.js."
            ], cls="text-sm leading-relaxed"),
            
            cls="max-w-2xl p-4 border rounded-lg"
        ),
        '''from starui.registry.components.code_block import InlineCode
from starhtml import P

P([
    "Use the ",
    InlineCode("useState"),
    " hook to manage component state in React. Import it like: ",
    InlineCode("import { useState } from 'react'"),
    "."
])

P([
    "For styling, use CSS classes like ",
    InlineCode("bg-blue-500"),
    " for background and ",
    InlineCode("text-white"),
    " for text color."
])''',
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
                
                # npm
                Div(
                    Div(
                        Badge("npm", variant="secondary"),
                        cls="mb-2"
                    ),
                    CodeBlock("npm install starui", language="bash"),
                    cls="mb-4"
                ),
                
                # pnpm
                Div(
                    Div(
                        Badge("pnpm", variant="secondary"),
                        cls="mb-2"
                    ),
                    CodeBlock("pnpm add starui", language="bash"),
                    cls="mb-4"
                ),
                
                # yarn
                Div(
                    Div(
                        Badge("yarn", variant="secondary"),
                        cls="mb-2"
                    ),
                    CodeBlock("yarn add starui", language="bash"),
                    cls="mb-6"
                ),
                
                cls="mb-8"
            ),
            
            Separator(cls="mb-8"),
            
            # Usage section
            Div(
                H3("Quick Start", cls="text-lg font-semibold mb-3"),
                P("Import and use components in your project:", cls="text-sm text-muted-foreground mb-3"),
                
                CodeBlock('''from starui.registry.components.button import Button
from starui.registry.components.card import Card, CardHeader, CardTitle, CardContent
from starhtml import Div, H1, P

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
from starhtml import H3, P, Div

# Documentation with multiple code blocks
H3("Installation")
P("Install using your preferred package manager:")

# npm
Badge("npm", variant="secondary")
CodeBlock("npm install starui", language="bash")

# Usage example
H3("Quick Start")
CodeBlock(\'\'\'from starui.registry.components.button import Button

def my_app():
    return Button("Click me!")\'\'\'', language="python")''',
        title="Documentation Layout",
        description="Structure documentation with code blocks for installation and usage examples"
    )
    
    # Code comparison
    yield ComponentPreview(
        Div(
            H4("Before vs After", cls="text-lg font-semibold mb-6 text-center"),
            
            Div(
                # Before
                Div(
                    Div(
                        Badge("Before", variant="destructive"),
                        cls="mb-3"
                    ),
                    CodeBlock('''# Old way - verbose and repetitive
def create_user_card(name, email, avatar):
    html = f"""
    <div class="user-card">
        <div class="user-avatar">
            <img src="{avatar}" alt="{name}">
        </div>
        <div class="user-info">
            <h3 class="user-name">{name}</h3>
            <p class="user-email">{email}</p>
        </div>
        <div class="user-actions">
            <button class="btn btn-primary">View Profile</button>
            <button class="btn btn-secondary">Send Message</button>
        </div>
    </div>
    """
    return html''', language="python"),
                    cls="flex-1"
                ),
                
                # After  
                Div(
                    Div(
                        Badge("After", variant="default", cls="bg-green-600 text-white"),
                        cls="mb-3"
                    ),
                    CodeBlock('''# New way - clean and component-based
from starui.registry.components import Card, CardContent, Avatar, Button
from starhtml import Div, H3, P

def create_user_card(name, email, avatar):
    return Card(
        CardContent(
            Div(
                Avatar(src=avatar, alt=name),
                Div(
                    H3(name, cls="font-semibold"),
                    P(email, cls="text-muted-foreground"),
                    cls="ml-4"
                ),
                cls="flex items-center mb-4"
            ),
            Div(
                Button("View Profile", variant="primary", cls="mr-2"),
                Button("Send Message", variant="outline"),
                cls="flex gap-2"
            )
        )
    )''', language="python"),
                    cls="flex-1"
                ),
                
                cls="grid grid-cols-1 lg:grid-cols-2 gap-6"
            ),
            
            cls="max-w-6xl"
        ),
        '''from starui.registry.components.code_block import CodeBlock
from starui.registry.components.badge import Badge

# Before/After comparison
Div(
    # Before
    Div(
        Badge("Before", variant="destructive"),
        CodeBlock(\'\'\'# Old verbose approach
def old_way():
    return f"""<div>{content}</div>\"\"\"\'\'\', language="python")
    ),
    
    # After
    Div(
        Badge("After", variant="default", cls="bg-green-600 text-white"),
        CodeBlock(\'\'\'# Clean component approach
from starui import Component

def new_way():
    return Component(content)\'\'\', language="python")
    ),
    
    cls="grid grid-cols-1 lg:grid-cols-2 gap-6"
)''',
        title="Code Comparison",
        description="Show before/after code examples with clear visual distinction"
    )
    
    # Terminal/command output
    yield ComponentPreview(
        Div(
            P("Terminal Output", cls="font-medium mb-3"),
            
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
                    Span("Terminal", cls="text-sm text-muted-foreground"),
                    cls="flex items-center justify-between px-4 py-2 bg-gray-800 border-b border-gray-700"
                ),
                
                # Terminal content
                CodeBlock('''$ star create my-project
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
                
                cls="border rounded-lg overflow-hidden bg-gray-900"
            ),
            
            cls="max-w-2xl"
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
        cls="flex items-center justify-between px-4 py-2 bg-gray-800"
    ),
    
    # Terminal content
    CodeBlock(\'\'\'$ star create my-project
Creating new StarUI project...
✓ Project directory created
✓ Dependencies installed

Success! Your project is ready.\'\'\', 
              language="bash",
              cls="bg-gray-900 text-green-400 font-mono"),
    
    cls="border rounded-lg overflow-hidden bg-gray-900"
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
                CodeBlock('''from starui.registry.components.button import Button
from starhtml import Div, H1, P

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
            P([
                "Import the component with ",
                InlineCode("from starui import CodeBlock"),
                " and use it to display syntax-highlighted code blocks."
            ], cls="text-sm text-muted-foreground text-center"),
            
            cls="max-w-2xl mx-auto"
        ),
        '''from starui.registry.components.code_block import CodeBlock, InlineCode

# Syntax-highlighted code block
CodeBlock(\'\'\'def hello_world():
    print("Hello, World!")
    
hello_world()\'\'\'', language="python")

# Inline code within text
P([
    "Use ",
    InlineCode("CodeBlock"),
    " for multi-line code and ",
    InlineCode("InlineCode"),
    " for inline snippets."
])''',
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
        component_slug="code-block"
    )