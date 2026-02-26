#!/usr/bin/env python3

import sys
from pathlib import Path
from contextlib import asynccontextmanager

# Add docs directory to path so component modules can import utils
sys.path.insert(0, str(Path(__file__).parent))

from starhtml import *
from starhtml.plugins import motion, scroll

from component_registry import get_registry
from head import SITE_URL, hdrs
from layouts.base import DocsLayout, LayoutConfig, SidebarConfig
from layouts.landing import LandingLayout
from pages.components_index import create_components_index
from pages.landing import (
    hero_section,
    code_example_section,
    component_grid_section,
    why_starui_section,
    cta_section,
    footer_section,
)

DOCS_SIDEBAR_SECTIONS = []


@asynccontextmanager
async def lifespan(app):
    print("[STARTUP] Initializing StarUI Documentation Server...")
    await initialize_docs_sidebar()
    print(f"[STARTUP] Sidebar initialized with {len(DOCS_SIDEBAR_SECTIONS)} sections")

    from layouts.sidebar import build_sidebar_nav
    nav = build_sidebar_nav(DOCS_SIDEBAR_SECTIONS)
    print("[STARTUP] Sidebar navigation pre-built and cached")

    yield
    print("[SHUTDOWN] StarUI Documentation Server shutting down...")


async def initialize_docs_sidebar():
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
                {"href": "/installation", "label": "Installation"},
            ]
        },
        {
            "title": "Components",
            "items": all_components
        }
    ]


app, rt = star_app(
    title="StarUI",
    live=False,
    middleware=[compression()],
    hdrs=hdrs,
    htmlkw=dict(lang="en", dir="ltr"),
    bodykw=dict(cls="min-h-screen bg-background text-foreground"),
    lifespan=lifespan,
)
app.register(position, clipboard, motion, scroll)

DOCS_NAV_ITEMS = [
    {"href": "/components", "label": "Components"},
    # {"href": "/blocks", "label": "Blocks"},  # Coming soon
    # {"href": "/themes", "label": "Themes"},  # Coming soon
]


@rt("/")
def home():
    return (
        Title("StarUI \u2014 Python-First UI Components"),
        Socials(
            title="StarUI \u2014 Python-First UI Components",
            site_name="StarUI",
            description="34+ accessible UI components for Python. The shadcn/ui model, rebuilt for StarHTML. No npm. No React. Just Python.",
            image="/static/images/og/starui.jpg",
            url=SITE_URL,
            card="summary_large_image",
        ),
        LandingLayout(
            hero_section(),
            code_example_section(),
            why_starui_section(),
            component_grid_section(),
            cta_section(),
            footer_section(),
        ),
    )


@rt("/components")
def components_index():
    registry = get_registry()
    return (
        Title("Components \u2014 StarUI"),
        Socials(
            title="Components \u2014 StarUI",
            site_name="StarUI",
            description="Browse the constellation \u2014 34+ accessible, copy-paste UI components for Python and StarHTML.",
            image="/static/images/og/starui.jpg",
            url=f"{SITE_URL}/components",
            card="summary_large_image",
        ),
        create_components_index(registry, DOCS_SIDEBAR_SECTIONS),
    )


@rt("/components/{component_name}")
def component_page(component_name: str):
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

    comp_title = component.get("title", component_name.replace("_", " ").title())
    comp_desc = component.get("description", f"{comp_title} component for StarUI.")

    return (
        Title(f"{comp_title} \u2014 StarUI"),
        Socials(
            title=f"{comp_title} \u2014 StarUI",
            site_name="StarUI",
            description=comp_desc,
            image="/static/images/og/starui.jpg",
            url=f"{SITE_URL}/components/{component_name}",
            card="summary_large_image",
        ),
        component.get("create_docs", lambda: None)(),
    )


@rt("/api/markdown/{component_name}")
def get_component_markdown(component_name: str):
    try:
        # Convert hyphenated slug to Python module name (e.g., "alert-dialog" -> "alert_dialog")
        module_component_name = component_name.replace("-", "_")
        module_name = f"pages.components.{module_component_name}"
        module = __import__(module_name, fromlist=["*"])

        # Extract component data using the same pattern as discover_components
        component_data = {
            "title": getattr(module, "TITLE", component_name.title()),
            "description": getattr(module, "DESCRIPTION", ""),
            "cli_command": f"star add {component_name}",
        }

        create_docs_func = getattr(module, f"create_{module_component_name}_docs", None)
        if not create_docs_func:
            return {"error": f"No documentation function found for {component_name}"}

        markdown_data = _extract_component_data(module, module_component_name)

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
    result = {}

    # Get examples data from module-level variable and extract code from functions
    examples_data = getattr(module, "EXAMPLES_DATA", None)
    if examples_data:
        result["examples_data"] = [
            {
                "title": ex.get("title", ""),
                "description": ex.get("description", ""),
                "code": ex["fn"].code if hasattr(ex["fn"], "code") else ""
            }
            for ex in examples_data
        ]

    # Hero example is the first example in EXAMPLES_DATA
    if examples_data and len(examples_data) > 0:
        first_fn = examples_data[0].get("fn")
        if first_fn and hasattr(first_fn, 'code'):
            result["hero_example_code"] = first_fn.code

    # Get API reference from module-level variable
    api_reference = getattr(module, "API_REFERENCE", None)
    if api_reference:
        result["api_reference"] = api_reference

    return result


def _parse_component_previews_from_source(source: str) -> list[dict]:
    import re

    examples = []
    blocks = re.split(r'yield\s+ComponentPreview\s*\(', source)[1:]
    
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
    from widgets.component_preview import ComponentPreview
    from widgets.code_block import CodeBlock
    from starui.registry.components.button import Button
    from starui.registry.components.input import Input
    
    return (
        Title("Installation \u2014 StarUI"),
        Socials(
            title="Installation \u2014 StarUI",
            site_name="StarUI",
            description="Get started with StarUI in minutes. Install the CLI, initialize your project, and add components.",
            image="/static/images/og/starui.jpg",
            url=f"{SITE_URL}/installation",
            card="summary_large_image",
        ),
        DocsLayout(
        Div(
            Div(
                P(
                    "Get started with StarUI in minutes. Build beautiful, accessible components with Python and StarHTML.",
                    cls="text-xl text-muted-foreground mb-8 max-w-3xl",
                ),
                
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
            
            Div(
                H2("Installation", cls="text-3xl font-bold tracking-tight mb-8"),
                
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
                                CodeBlock("pip install starui", language="bash"),
                                cls="flex-1 min-w-0 overflow-hidden"
                            ),
                            cls="flex flex-col sm:flex-row gap-4 sm:gap-6 items-start"
                        ),
                        cls="p-4 sm:p-6 border rounded-lg bg-gradient-to-br from-background to-muted/20 overflow-hidden"
                    ),
                    cls="mb-8"
                ),

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
                                CodeBlock("star init", language="bash"),
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
                                CodeBlock(
                                    '''# Add a single component
star add button

# Add multiple components at once
star add button input card tabs

# List all available components
star list''',
                                    language="bash"
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
            
            Div(
                H2("Usage Examples", cls="text-3xl font-bold tracking-tight mb-8"),
                
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
                
                ComponentPreview(
                    Div(
                        (count := Signal("count", 0)),
                        Button("Click me!", data_on_click=count.add(1), cls="mb-3"),
                        P("Clicked: ", Span(data_text=count, cls="font-bold text-primary")),
                        cls="text-center space-y-3"
                    ),
                    '''from starui import Button
from starhtml import Signal

# Add interactivity with Datastar
Div(
    (count := Signal("count", 0)),
    Button("Click me!", data_on_click=count.add(1)),
    P("Clicked: ", Span(data_text=count, cls="font-bold"))
)''',
                    title="Interactive Components",
                    description="Add reactivity using Datastar for dynamic user interfaces"
                ),
                
                cls="space-y-8"
            ),
            
            Div(
                H2("Onwards", cls="text-2xl font-semibold tracking-tight mb-8 mt-16"),
                Div(
                    _next_step_card(
                        "01",
                        "The Constellation",
                        "34+ components. Every one interactive, every one yours to modify.",
                        "/components",
                        "Browse Components",
                    ),
                    _next_step_card(
                        "02",
                        "The Field Guide",
                        "Signals, reactivity, the server-first model \u2014 learn the framework beneath the components.",
                        "https://starhtml.com",
                        "Visit StarHTML",
                    ),
                    _next_step_card(
                        "03",
                        "The Source",
                        "Apache 2.0. Read the code, open an issue, send a patch.",
                        "https://github.com/banditburai/starui",
                        "View on GitHub",
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
    ),
    )


def _next_step_card(num: str, title: str, description: str, href: str, button_text: str) -> FT:
    return A(
        Div(
            Span(num, cls="text-xs font-mono text-muted-foreground tracking-widest"),
            H3(title, cls="text-base font-medium mt-2 mb-2 group-hover:text-primary transition-colors"),
            P(description, cls="text-sm text-muted-foreground leading-relaxed flex-1"),
            Span(button_text, " \u2192", cls="text-sm font-medium text-primary mt-4 inline-block"),
            cls="p-5 h-full flex flex-col",
        ),
        href=href,
        cls="group border rounded-lg hover:border-primary/30 transition-colors h-full block",
    )


@rt("/sitemap.xml")
def sitemap():
    from starlette.responses import Response

    registry = get_registry()
    paths = ["/", "/installation", "/components"]
    paths += [f"/components/{name}" for name in registry.components]

    urls = "\n".join(
        f"  <url><loc>{SITE_URL}{p}</loc></url>"
        for p in paths
    )
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{urls}\n"
        "</urlset>"
    )
    return Response(content=xml, media_type="application/xml")


iframe_app, iframe_rt = star_app(
    title="Component Preview",
    live=False,
    hdrs=(
        Script("""
            (function() {
                const iframeId = window.location.pathname.split('/').pop();
                const iframeKey = 'iframe-theme-' + iframeId;

                // Try iframe-specific key first, then parent key, then system preference
                const theme = localStorage.getItem(iframeKey) ||
                              localStorage.getItem('theme') ||
                              (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');

                document.documentElement.setAttribute('data-theme', theme);
            })();
        """),
        Style("""
            [data-theme="light"] .theme-icon-alt,
            [data-theme="dark"] .theme-icon-default {
                display: none;
            }
        """),
        Link(rel="stylesheet", href="/static/css/starui.css"),
    ),
    htmlkw=dict(lang="en", dir="ltr"),
    bodykw=dict(cls="min-h-screen bg-background text-foreground"),
)
iframe_app.register(position, clipboard)

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