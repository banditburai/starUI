#!/usr/bin/env python3
"""StarUI Documentation Server."""

import sys
from pathlib import Path
from contextlib import asynccontextmanager

# Add docs directory to path so component modules can import utils
sys.path.insert(0, str(Path(__file__).parent))

from starhtml import *
from starhtml.datastar import get_starhtml_action_plugins, ds_on_click, ds_text, ds_signals, ds_show
from starhtml import position_handler

from component_registry import get_registry
from layouts.base import DocsLayout, LayoutConfig, FooterConfig, SidebarConfig
from pages.components_index import create_components_index

# Global sidebar sections - initialized once at startup
DOCS_SIDEBAR_SECTIONS = []


@asynccontextmanager
async def lifespan(app):
    """Lifespan context manager for proper startup/shutdown."""
    print("[STARTUP] Initializing StarUI Documentation Server...")
    
    # Initialize components and sidebar on startup
    await initialize_docs_sidebar()
    print(f"[STARTUP] Sidebar initialized with {len(DOCS_SIDEBAR_SECTIONS)} sections")
    
    # Pre-build and cache the sidebar navigation
    from layouts.sidebar import build_sidebar_nav
    nav = build_sidebar_nav(DOCS_SIDEBAR_SECTIONS)
    print("[STARTUP] Sidebar navigation pre-built and cached")
    
    yield
    
    print("[SHUTDOWN] StarUI Documentation Server shutting down...")


async def initialize_docs_sidebar():
    """Initialize sidebar sections once at startup."""
    global DOCS_SIDEBAR_SECTIONS
    
    print("[STARTUP] Discovering components...")
    components_dir = Path(__file__).parent / "pages" / "components"
    if not components_dir.exists():
        print("[STARTUP] No components directory found")
        return
    
    registry = get_registry()
    component_count = 0
    
    for component_file in sorted(components_dir.glob("*.py")):
        if component_file.stem in ["__init__", "__pycache__"]:
            continue
        
        try:
            module_name = f"pages.components.{component_file.stem}"
            module = __import__(module_name, fromlist=["*"])
            
            if hasattr(module, "TITLE"):
                registry.register(
                    name=component_file.stem,
                    title=getattr(module, "TITLE", component_file.stem.title()),
                    description=getattr(module, "DESCRIPTION", ""),
                    category=getattr(module, "CATEGORY", "ui"),
                    order=getattr(module, "ORDER", 100),
                    status=getattr(module, "STATUS", "stable"),
                    examples=getattr(module, "examples", lambda: [])(),
                    create_docs=getattr(module, f"create_{component_file.stem}_docs", lambda: None),
                )
                component_count += 1
        except Exception as e:
            print(f"[STARTUP] Failed to load component {component_file.stem}: {e}")
    
    print(f"[STARTUP] Loaded {component_count} components")
    
    # Build sidebar sections
    all_components = []
    for name, component in registry.components.items():
        all_components.append({
            "href": f"/components/{name}",
            "label": component["title"],
        })
    
    all_components.sort(key=lambda x: x["label"])
    
    DOCS_SIDEBAR_SECTIONS = [
        {
            "title": "Getting Started",
            "items": [
                {"href": "/docs", "label": "Introduction"},
                {"href": "/installation", "label": "Installation"},
            ]
        },
        {
            "title": "Components",
            "items": all_components
        }
    ]


app, rt = star_app(
    title="StarUI Documentation",
    live=True,
    hdrs=(
        fouc_script(use_data_theme=True),
        Link(rel="stylesheet", href="/static/css/starui.css"),
        position_handler(),
    ),
    htmlkw=dict(lang="en", dir="ltr"),
    bodykw=dict(cls="min-h-screen bg-background text-foreground"),
    plugins=get_starhtml_action_plugins(),
    lifespan=lifespan,
)

DOCS_NAV_ITEMS = [
    {"href": "/components", "label": "Components"},
    {"href": "/blocks", "label": "Blocks"},
    {"href": "/themes", "label": "Themes"},
]


@rt("/")
def home():
    """Documentation homepage."""
    return DocsLayout(
        Div(
            Div(
                H1("StarUI", cls="text-4xl font-bold tracking-tight mb-4"),
                P(
                    "Beautiful, accessible components built with StarHTML and Tailwind CSS.",
                    cls="text-xl text-muted-foreground mb-8",
                ),
                Div(
                    A(
                        "Get Started",
                        href="/installation",
                        cls="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-10 px-4 py-2 mr-4",
                    ),
                    A(
                        "View Components",
                        href="/components",
                        cls="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 border border-input bg-background hover:bg-accent hover:text-accent-foreground h-10 px-4 py-2",
                    ),
                    cls="flex gap-4",
                ),
                cls="text-center py-16",
            ),
            Div(
                H2("Features", cls="text-3xl font-bold text-center mb-12"),
                Div(
                    _feature_card(
                        "lucide:server",
                        "Python-First Architecture", 
                        "Write modern UI entirely in Python. No JSX, no build steps, no client-side frameworks. Pure server-side rendering with progressive enhancement."
                    ),
                    _feature_card(
                        "lucide:terminal",
                        "CLI-Driven Workflow",
                        "Install components instantly with `star add button`. Dependencies resolved automatically. Full type safety and IDE support out of the box."
                    ),
                    _feature_card(
                        "lucide:zap",
                        "Reactive Without React",
                        "Datastar powers reactive patterns while keeping logic server-side. Get modern UX without JavaScript complexity or hydration delays."
                    ),
                    _feature_card(
                        "lucide:shield-check",
                        "Zero Runtime Overhead",
                        "Components render complete HTML on the server. No bundle sizes, no waterfall loading, perfect SEO, and instant time-to-interactive."
                    ),
                    cls="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6",
                ),
                cls="py-16",
            ),
            cls="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8",
        ),
        layout=LayoutConfig(
            title="StarUI Documentation",
            description="A comprehensive UI component library for StarHTML applications.",
        ),
        footer=FooterConfig(
            attribution="Built with StarHTML",
            hosting_info="Component library for Python web apps",
        ),
    )


def _feature_card(icon: str, title: str, description: str) -> FT:
    """Create a feature card."""
    return Div(
        Div(
            Div(
                Icon(icon, width="32", height="32", cls="text-primary/60 dark:text-primary/70 relative z-10"),
                cls="relative mb-6 w-12 h-12 rounded-xl bg-gradient-to-br from-primary/8 via-primary/4 to-primary/12 dark:from-primary/15 dark:via-primary/8 dark:to-primary/25 shadow-inner dark:shadow-[inset_2px_2px_4px_rgba(0,0,0,0.3),inset_-1px_-1px_2px_rgba(255,255,255,0.1)] flex items-center justify-center backdrop-blur-sm border border-primary/10 dark:border-primary/20"
            ),
            H3(title, cls="text-xl font-semibold mb-2"),
            P(description, cls="text-sm text-muted-foreground"),
            cls="text-center p-6",
        ),
        cls="group hover:shadow-lg hover:border-primary/30 transition-all duration-300 cursor-pointer h-full bg-gradient-to-br from-background via-background/80 to-muted/50 backdrop-blur-sm relative overflow-hidden border rounded-lg",
    )


def _docs_feature_card(emoji: str, text: str) -> FT:
    """Create a docs feature card with emoji."""
    return Div(
        Div(
            Span(emoji, cls="text-2xl mb-2 block"),
            P(text, cls="text-sm"),
            cls="text-center p-4"
        ),
        cls="border rounded-lg bg-gradient-to-br from-background via-background/80 to-muted/50 hover:shadow-md transition-all duration-200"
    )


def _professional_feature_card(title: str, description: str, icon: str) -> FT:
    """Create a professional feature card without emojis."""
    return Div(
        Div(
            Div(
                Icon(icon, width="24", height="24", cls="text-primary/70"),
                cls="mb-6 w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center"
            ),
            H3(title, cls="text-xl font-semibold mb-4"),
            P(description, cls="text-muted-foreground leading-relaxed"),
            cls="p-4 sm:p-6"
        ),
        cls="border rounded-xl bg-gradient-to-br from-background to-muted/20 hover:shadow-lg hover:border-primary/30 transition-all duration-300 h-full"
    )


def _workflow_card(title: str, description: str, code: str, caption: str) -> FT:
    """Create a workflow step card with code example."""
    from starui.registry.components.code_block import CodeBlock
    
    return Div(
        Div(
            H3(title, cls="text-lg font-semibold mb-3"),
            P(description, cls="text-sm text-muted-foreground mb-4"),
            Div(
                CodeBlock(code, language="python", cls="text-sm border rounded-md overflow-x-auto", style="scrollbar-width: thin; scrollbar-color: transparent transparent;"),
                P(caption, cls="text-xs text-muted-foreground mt-2"),
                cls="mb-0"
            ),
            cls="p-4 sm:p-6"
        ),
        cls="border rounded-lg bg-gradient-to-br from-background to-muted/10 hover:shadow-md transition-all duration-200 h-full"
    )


def _feature_highlight_card(title: str, description: str, code: str, code_caption: str, icon: str) -> FT:
    """Create a feature highlight card with code example."""
    from starui.registry.components.code_block import CodeBlock
    
    return Div(
        Div(
            Div(
                Div(
                    Icon(icon, width="28", height="28", cls="text-primary"),
                    cls="mb-6 w-14 h-14 rounded-xl bg-primary/10 flex items-center justify-center border border-primary/20"
                ),
                H3(title, cls="text-xl font-semibold mb-4"),
                P(description, cls="text-muted-foreground mb-6 leading-relaxed"),
                cls="mb-6"
            ),
            Div(
                CodeBlock(code, language="python", cls="text-sm border rounded-md overflow-x-auto", style="scrollbar-width: thin; scrollbar-color: transparent transparent;"),
                P(code_caption, cls="text-xs text-muted-foreground mt-3"),
                cls="space-y-2"
            ),
            cls="p-4 sm:p-6"
        ),
        cls="border rounded-xl bg-gradient-to-br from-background to-muted/20 hover:shadow-lg hover:border-primary/30 transition-all duration-300 h-full"
    )


def _workflow_highlight_card(title: str, description: str, code: str, code_caption: str) -> FT:
    """Create a workflow highlight card with code example."""
    from starui.registry.components.code_block import CodeBlock
    
    return Div(
        Div(
            H3(title, cls="text-lg font-semibold mb-3"),
            P(description, cls="text-sm text-muted-foreground mb-4 leading-relaxed"),
            Div(
                CodeBlock(code, language="python", cls="text-sm border rounded-md overflow-x-auto", style="scrollbar-width: thin; scrollbar-color: transparent transparent;"),
                P(code_caption, cls="text-xs text-muted-foreground mt-2"),
                cls="space-y-2"
            ),
            cls="p-5"
        ),
        cls="border rounded-lg bg-gradient-to-br from-background to-muted/10 hover:shadow-md hover:border-primary/20 transition-all duration-200 h-full"
    )


def _performance_metric(value: str, label: str, description: str) -> FT:
    """Create a performance metric display."""
    return Div(
        Div(
            Span(value, cls="text-2xl font-bold text-primary block mb-1"),
            Span(label, cls="text-sm font-medium text-foreground block mb-2"),
            P(description, cls="text-xs text-muted-foreground leading-relaxed"),
            cls="text-center"
        ),
        cls="bg-gradient-to-br from-muted/30 to-muted/10 rounded-lg p-4 border hover:shadow-sm transition-shadow duration-200"
    )

@rt("/docs")
def docs_index():
    """Documentation index page."""
    
    return DocsLayout(
        Div(
            # Hero section
            Div(
                H1("StarUI Documentation", cls="text-4xl md:text-5xl font-bold tracking-tight mb-6"),
                P(
                    "Server-side component library that brings modern UI to Python web applications without the JavaScript complexity.",
                    cls="text-xl text-muted-foreground mb-4 max-w-3xl mx-auto",
                ),
                P(
                    "Write reactive interfaces entirely in Python using Datastar's declarative patterns.",
                    cls="text-lg text-muted-foreground/80 mb-12 max-w-2xl mx-auto",
                ),
                cls="text-center mb-20"
            ),
            
            # Core philosophy section
            Div(
                H2("The Python-Native Approach", cls="text-3xl font-bold mb-8"),
                Div(
                    _feature_highlight_card(
                        "Server-First Architecture",
                        "Components render on the server and progressively enhance with interactivity. No client-side hydration, no bundle sizes, no waterfall loading.",
                        "from starui import Button, Input, Card\n\n# Pure Python - no JSX, no build step\nCard(\n    Input(placeholder=\"Search...\"),\n    Button(\"Submit\", ds_on_click=\"$search()\")\n)",
                        "Python syntax with type safety and IDE support",
                        "lucide:server"
                    ),
                    _feature_highlight_card(
                        "Reactive Without React",
                        "Datastar provides declarative state management and reactive updates while keeping all logic server-side. Get modern UX patterns without JavaScript frameworks.",
                        "# Reactive counter - no useState, no hooks\nButton(\n    ds_text=\"'Count: ' + $count\",\n    ds_on_click=\"$count++\"\n)\n\n# State stays on the server",
                        "Reactive patterns with server-side state",
                        "lucide:zap"
                    ),
                    cls="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6 lg:gap-8 mb-16"
                ),
            ),
            
            # Developer experience section  
            Div(
                H2("Built for Python Developers", cls="text-3xl font-bold mb-8"),
                Div(
                    _workflow_highlight_card(
                        "Type-Safe Components",
                        "Python-native components with IDE autocompletion and type hints",
                        "from starui.registry.components.button import Button\n\n# IDE provides autocompletion for variants\nButton(\"Click me\", variant=\"outline\", size=\"lg\")\n# ✅ All properties properly typed",
                        "Full Python type hints and IDE support"
                    ),
                    _workflow_highlight_card(
                        "StarHTML Integration",
                        "Designed specifically for StarHTML applications with seamless interop",
                        "from starhtml import *\nfrom starui import Button, Card\n\n# Mix StarHTML and StarUI naturally\nDiv(\n    H1(\"Welcome\"),\n    Card(Button(\"Get Started\"))\n)",
                        "Native integration with StarHTML ecosystem"
                    ),
                    _workflow_highlight_card(
                        "Single Command Install",
                        "Add components with dependencies automatically resolved",
                        "star add button input card tabs\n\n# Components ready to import\nfrom starui import Button, Input, Card, Tabs",
                        "CLI handles dependency management"
                    ),
                    cls="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6 mb-16"
                ),
            ),
            
            # Performance and production section
            Div(
                H2("Production-Ready Performance", cls="text-3xl font-bold mb-8"),
                Div(
                    Div(
                        _performance_metric("Zero", "Runtime JavaScript", "Components work without any client-side JavaScript"),
                        _performance_metric("Instant", "Server Rendering", "No hydration delays or layout shifts"),
                        _performance_metric("100%", "SEO Friendly", "Fully rendered HTML for search engines"),
                        cls="grid grid-cols-1 sm:grid-cols-3 gap-4 sm:gap-6 mb-8"
                    ),
                    Div(
                        H3("Enterprise Standards", cls="text-xl font-semibold mb-4"),
                        Div(
                            Div(
                                Icon("lucide:shield-check", cls="h-5 w-5 text-green-600 mr-3"),
                                "WCAG 2.1 AA accessibility compliance",
                                cls="flex items-center mb-3"
                            ),
                            Div(
                                Icon("lucide:palette", cls="h-5 w-5 text-blue-600 mr-3"),
                                "Design tokens with light/dark theme support",
                                cls="flex items-center mb-3"
                            ),
                            Div(
                                Icon("lucide:code-2", cls="h-5 w-5 text-purple-600 mr-3"),
                                "Composable components with consistent API patterns",
                                cls="flex items-center mb-3"
                            ),
                            Div(
                                Icon("lucide:zap", cls="h-5 w-5 text-orange-600 mr-3"),
                                "Progressive enhancement for interactive features",
                                cls="flex items-center"
                            ),
                            cls="space-y-2"
                        ),
                        cls="bg-gradient-to-br from-background to-muted/20 rounded-xl p-6 border"
                    ),
                    cls="space-y-8"
                ),
            ),
            
            cls="max-w-7xl mx-auto px-4"
        ),
        layout=LayoutConfig(show_copy=False),
        sidebar=SidebarConfig(sections=DOCS_SIDEBAR_SECTIONS),
    )


@rt("/components")
def components_index():
    """Components index page."""
    registry = get_registry()
    return create_components_index(registry, DOCS_SIDEBAR_SECTIONS)


@rt("/components/{component_name}")
def component_page(component_name: str):
    """Individual component documentation page."""
    registry = get_registry()
    component = registry.get(component_name)

    if not component:
        return DocsLayout(
            Div(
                H1("Component Not Found", cls="text-3xl font-bold mb-4"),
                P(f"The component '{component_name}' was not found.", cls="text-muted-foreground"),
                A("View all components", href="/components", cls="text-primary hover:underline"),
            ),
            layout=LayoutConfig(
                title="Component Not Found",
                show_sidebar=True
            ),
            sidebar=SidebarConfig(sections=DOCS_SIDEBAR_SECTIONS),
        )

    # The component's create_docs function should handle sidebar sections
    return component.get("create_docs", lambda: None)()


@rt("/api/markdown/{component_name}")
def get_component_markdown(component_name: str):
    """Generate markdown content for a component on-demand."""
    try:
        # Import the component module dynamically
        module_name = f"pages.components.{component_name}"
        module = __import__(module_name, fromlist=["*"])
        
        # Extract component data using the same pattern as discover_components
        component_data = {
            "title": getattr(module, "TITLE", component_name.title()),
            "description": getattr(module, "DESCRIPTION", ""),
            "cli_command": f"star add {component_name}",
        }
        
        # Try to get the component creation function to extract structured data
        create_docs_func = getattr(module, f"create_{component_name}_docs", None)
        if not create_docs_func:
            return {"error": f"No documentation function found for {component_name}"}
        
        # Get examples_data, hero_example_code, usage_code, and api_reference from the component
        # We need to extract this from the function - let's call a helper to get the data
        markdown_data = _extract_component_data(module, component_name)
        
        # Generate markdown using our existing function
        from utils import generate_component_markdown
        markdown_content = generate_component_markdown(
            component_name=component_data["title"],
            description=component_data["description"],
            examples_data=markdown_data.get("examples_data", []),
            cli_command=component_data["cli_command"],
            usage_code=markdown_data.get("usage_code"),
            api_reference=markdown_data.get("api_reference"),
            hero_example_code=markdown_data.get("hero_example_code"),
        )
        
        return {"markdown": markdown_content}
        
    except Exception as e:
        return {"error": f"Failed to generate markdown for {component_name}: {str(e)}"}


def _extract_component_data(module, component_name: str) -> dict:
    """Extract structured data from a component module for markdown generation."""
    import ast
    import inspect
    import re
    
    examples_func = getattr(module, "examples", None)
    if not examples_func:
        return {}
    
    try:
        examples_data = _parse_component_previews_from_source(inspect.getsource(examples_func))
        
        create_docs_func = getattr(module, f"create_{component_name}_docs", None)
        if not create_docs_func:
            return {"examples_data": examples_data}
        
        source = inspect.getsource(create_docs_func)
        
        hero_match = re.search(r'hero_example\s*=\s*ComponentPreview\(.*?[\'\"]{3}(.*?)[\'\"]{3}', source, re.DOTALL)
        hero_example_code = hero_match.group(1).strip() if hero_match else None
        
        api_reference = getattr(module, 'api_reference', None)
        if not api_reference and 'api_reference=' in source:
            try:
                tree = ast.parse(source)
                for node in ast.walk(tree):
                    if isinstance(node, ast.Call):
                        for kw in getattr(node, 'keywords', []):
                            if kw.arg == 'api_reference':
                                api_reference = ast.literal_eval(kw.value)
                                break
            except:
                api_reference = None
        
        return {
            "examples_data": examples_data,
            "hero_example_code": hero_example_code,
            "api_reference": api_reference
        }
    
    except Exception:
        return {"examples_data": []}


def _parse_component_previews_from_source(source: str) -> list[dict]:
    """Parse ComponentPreview calls from source code to extract titles, descriptions, and code."""
    import re
    
    examples = []
    blocks = re.split(r'yield\s+ComponentPreview\s*\(', source)[1:]  # Skip content before first yield
    
    for block in blocks:
        paren_count = 1
        end_pos = 0
        for i, char in enumerate(block):
            if char == '(':
                paren_count += 1
            elif char == ')':
                paren_count -= 1
                if paren_count == 0:
                    end_pos = i
                    break
        
        if not end_pos:
            continue
            
        call = block[:end_pos]
        
        title_match = re.search(r'title\s*=\s*["\']([^"\']+)["\']', call)
        desc_match = re.search(r'description\s*=\s*["\']([^"\']*)["\']', call)
        code_match = re.search(r'[\'\"]{3}(.*?)[\'\"]{3}', call, re.DOTALL)
        
        if title_match and code_match:
            examples.append({
                "title": title_match.group(1),
                "description": desc_match.group(1) if desc_match else "",
                "code": code_match.group(1).strip()
            })
    
    return examples


@rt("/installation")
def installation():
    """Installation guide."""
    from starui.registry.components.code_block import CodeBlock as SimpleCodeBlock
    from widgets.component_preview import ComponentPreview
    from starui.registry.components.button import Button
    from starui.registry.components.input import Input
    from starui.registry.components.card import Card
    from starhtml.datastar import ds_on_click, ds_show, ds_signals, ds_text
    
    def CodeBlockWithCopy(code: str, language: str = "bash") -> FT:
        """CodeBlock with positioned copy button."""
        code_id = f"copy_{abs(hash(code))}"
        signal = f"copied_{code_id}"
        
        return Div(
            SimpleCodeBlock(code, language=language, cls="overflow-x-auto", style="scrollbar-width: thin; scrollbar-color: transparent transparent;"),
            Button(
                Span(Icon("lucide:check", cls="h-3 w-3"), ds_show(f"${signal}")),
                Span(Icon("lucide:copy", cls="h-3 w-3"), ds_show(f"!${signal}")),
                Span(ds_text(f"${signal} ? 'Copied!' : 'Copy'"), cls="sr-only"),
                ds_on_click(f'@clipboard(evt.target.closest(".relative").querySelector("code").textContent, "{signal}", 2000)'),
                variant="ghost",
                size="sm",
                cls="absolute top-3 right-3 h-7 w-7 p-0 text-muted-foreground hover:text-foreground hover:bg-muted opacity-75 hover:opacity-100 transition-all duration-200",
                type="button",
                aria_label="Copy code"
            ),
            ds_signals({signal: False}),
            cls="relative group"
        )
    
    return DocsLayout(
        Div(
            # Hero Section with Quick Start
            Div(
                P(
                    "Get started with StarUI in minutes. Build beautiful, accessible components with Python and StarHTML.",
                    cls="text-xl text-muted-foreground mb-8 max-w-3xl",
                ),
                
                # Quick Start Preview
                ComponentPreview(
                    Div(
                        Button("Get Started", variant="default", cls="mr-3"),
                        Button("View Components", variant="outline"),
                        cls="flex gap-3 items-center justify-center"
                    ),
                    '''from starui import Button

Button("Get Started")
Button("View Components", variant="outline")''',
                    title="Quick Start",
                    description="Import and use components immediately",
                    default_tab="code"
                ),
                cls="mb-12"
            ),
            
            # Installation Steps
            Div(
                H2("Installation", cls="text-3xl font-bold tracking-tight mb-8"),
                
                # Step 1: Install CLI
                Div(
                    Div(
                        Div(
                            Div(
                                Span("1", cls="flex h-10 w-10 items-center justify-center rounded-full bg-primary text-primary-foreground font-semibold"),
                                cls="flex-shrink-0"
                            ),
                            Div(
                                H3("Install the StarUI CLI", cls="text-xl font-semibold mb-2"),
                                P("Install StarUI globally using pip to access the CLI commands.", cls="text-muted-foreground mb-4"),
                                CodeBlockWithCopy("pip install starui", "bash"),
                                cls="flex-1 min-w-0 overflow-hidden"
                            ),
                            cls="flex flex-col sm:flex-row gap-4 sm:gap-6 items-start"
                        ),
                        cls="p-4 sm:p-6 border rounded-lg bg-gradient-to-br from-background to-muted/20 overflow-hidden"
                    ),
                    cls="mb-8"
                ),
                
                # Step 2: Initialize Project  
                Div(
                    Div(
                        Div(
                            Div(
                                Span("2", cls="flex h-10 w-10 items-center justify-center rounded-full bg-primary text-primary-foreground font-semibold"),
                                cls="flex-shrink-0"
                            ),
                            Div(
                                H3("Initialize your project", cls="text-xl font-semibold mb-2"),
                                P("Set up StarUI in your project directory. This creates the configuration and installs dependencies.", cls="text-muted-foreground mb-4"),
                                CodeBlockWithCopy("star init", "bash"),
                                Div(
                                    Div(
                                        Icon("lucide:file-text", cls="h-5 w-5 text-primary mr-3 flex-shrink-0"),
                                        Div(
                                            P("Creates starui.json configuration file", cls="font-medium text-sm"),
                                            P("Configures component paths and settings", cls="text-xs text-muted-foreground"),
                                        ),
                                        cls="flex items-start"
                                    ),
                                    Div(
                                        Icon("lucide:package", cls="h-5 w-5 text-primary mr-3 flex-shrink-0"),
                                        Div(
                                            P("Installs required dependencies", cls="font-medium text-sm"),
                                            P("StarHTML, Tailwind CSS, and component utilities", cls="text-xs text-muted-foreground"),
                                        ),
                                        cls="flex items-start"
                                    ),
                                    cls="space-y-3 mt-4 bg-muted/30 rounded-md p-4"
                                ),
                                cls="flex-1 min-w-0 overflow-hidden"
                            ),
                            cls="flex flex-col sm:flex-row gap-4 sm:gap-6 items-start"
                        ),
                        cls="p-4 sm:p-6 border rounded-lg bg-gradient-to-br from-background to-muted/20 overflow-hidden"
                    ),
                    cls="mb-8"
                ),
                
                # Step 3: Add Components
                Div(
                    Div(
                        Div(
                            Div(
                                Span("3", cls="flex h-10 w-10 items-center justify-center rounded-full bg-primary text-primary-foreground font-semibold"),
                                cls="flex-shrink-0"
                            ),
                            Div(
                                H3("Add components to your project", cls="text-xl font-semibold mb-2"),
                                P("Install individual components with their dependencies automatically resolved.", cls="text-muted-foreground mb-4"),
                                CodeBlockWithCopy(
                                    '''# Add a single component
star add button

# Add multiple components at once  
star add button input card tabs

# List all available components
star list''',
                                    "bash"
                                ),
                                cls="flex-1 min-w-0 overflow-hidden"
                            ),
                            cls="flex flex-col sm:flex-row gap-4 sm:gap-6 items-start"
                        ),
                        cls="p-4 sm:p-6 border rounded-lg bg-gradient-to-br from-background to-muted/20 overflow-hidden"
                    ),
                    cls="mb-12"
                ),
            ),
            
            # Usage Examples
            Div(
                H2("Usage Examples", cls="text-3xl font-bold tracking-tight mb-8"),
                
                # Basic Usage
                ComponentPreview(
                    Div(
                        Input(placeholder="Enter your email", cls="mb-3"),
                        Button("Subscribe", cls="w-full"),
                        cls="max-w-sm mx-auto space-y-3"
                    ),
                    '''from starui import Button, Input

# Use components in your StarHTML app
Div(
    Input(placeholder="Enter your email"),
    Button("Subscribe"),
    cls="space-y-3"
)''',
                    title="Basic Component Usage",
                    description="Import and use components directly in your StarHTML templates"
                ),
                
                # Interactive Features
                ComponentPreview(
                    Div(
                        Button("Click me!", ds_on_click("$count++"), cls="mb-3"),
                        P("Clicked: ", Span(ds_text("$count"), cls="font-bold text-primary")),
                        ds_signals(count=0),
                        cls="text-center space-y-3"
                    ),
                    '''from starui import Button
from starhtml.datastar import ds_on_click, ds_text, ds_signals

# Add interactivity with Datastar
Div(
    Button("Click me!", ds_on_click("$count++")),
    P("Clicked: ", Span(ds_text("$count"), cls="font-bold")),
    ds_signals(count=0)
)''',
                    title="Interactive Components",
                    description="Add reactivity using Datastar for dynamic user interfaces"
                ),
                
                cls="space-y-8"
            ),
            
            # Next Steps
            Div(
                H2("What's Next?", cls="text-3xl font-bold tracking-tight mb-8 mt-16"),
                Div(
                    _next_step_card(
                        "lucide:palette",
                        "Explore Components", 
                        "Browse our comprehensive component library with live examples and code samples.",
                        "/components",
                        "View Components"
                    ),
                    _next_step_card(
                        "lucide:book-open",
                        "Read the Documentation",
                        "Learn advanced patterns, theming, and best practices for building with StarUI.",
                        "/docs", 
                        "Read Docs"
                    ),
                    _next_step_card(
                        "lucide:github",
                        "Join the Community",
                        "Contribute to the project, report issues, or get help from other developers.",
                        "https://github.com/banditburai/starui",
                        "Visit GitHub"
                    ),
                    cls="grid grid-cols-1 md:grid-cols-3 gap-4 sm:gap-6"
                ),
            ),
        ),
        layout=LayoutConfig(
            title="Installation", 
            description="How to install and set up StarUI in your project.",
            show_sidebar=True
        ),
        sidebar=SidebarConfig(sections=DOCS_SIDEBAR_SECTIONS),
    )


def _code_block(code: str, language: str = "bash") -> FT:
    """Create a code block."""
    from starlighter import CodeBlock
    return CodeBlock(code)


def _next_step_card(icon: str, title: str, description: str, href: str, button_text: str) -> FT:
    """Create a next step card with icon, title, description, and call-to-action."""
    return Div(
        Div(
            Div(
                Icon(icon, width="28", height="28", cls="text-primary"),
                cls="mb-6 w-14 h-14 rounded-xl bg-primary/10 flex items-center justify-center border border-primary/20"
            ),
            H3(title, cls="text-xl font-semibold mb-3"),
            P(description, cls="text-muted-foreground mb-6 leading-relaxed flex-1"),
            A(
                button_text,
                href=href,
                cls="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-9 px-4 py-2"
            ),
            cls="p-6 h-full flex flex-col"
        ),
        cls="border rounded-xl bg-gradient-to-br from-background to-muted/20 hover:shadow-lg hover:border-primary/30 transition-all duration-300 h-full"
    )


# Component discovery moved to lifespan startup for proper initialization


iframe_app, iframe_rt = star_app(
    title="Component Preview",
    live=True,
    hdrs=(
        fouc_script(use_data_theme=True),
        Link(rel="stylesheet", href="/static/css/starui.css"),
        position_handler(),
    ),
    htmlkw=dict(lang="en", dir="ltr"),
    bodykw=dict(cls="min-h-screen bg-background text-foreground"),
    plugins=get_starhtml_action_plugins(),
)

@iframe_rt("/{preview_id}")
def component_preview_iframe(preview_id: str):
    from widgets.component_preview import IFRAME_PREVIEW_REGISTRY
    
    preview_data = IFRAME_PREVIEW_REGISTRY.get(preview_id)
    if not preview_data:
        return Div("Preview not found", cls="text-center p-10 text-muted-foreground")
    
    return Div(
        preview_data['content'],
        cls=f"flex min-h-[350px] w-full items-center justify-center p-10 {preview_data['class']}"
    )

app.mount("/component-preview-iframe", iframe_app)


if __name__ == "__main__":
    serve(port=5002)