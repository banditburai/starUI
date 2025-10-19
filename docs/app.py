#!/usr/bin/env python3

import sys
from pathlib import Path
from contextlib import asynccontextmanager

# Add docs directory to path so component modules can import utils
sys.path.insert(0, str(Path(__file__).parent))

from starhtml import *
from starhtml import position_handler

from component_registry import get_registry
from layouts.base import DocsLayout, LayoutConfig, FooterConfig, SidebarConfig
from pages.components_index import create_components_index
from data.constellation_components import get_constellation_components

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
        Link(rel="stylesheet", href="/static/css/gradients.css"),
        Script(src="https://cdn.jsdelivr.net/npm/motion@11.11.13/dist/motion.js"),
        position_handler(),
    ),
    htmlkw=dict(lang="en", dir="ltr"),
    bodykw=dict(cls="min-h-screen bg-background text-foreground"),
    iconify=True,
    clipboard=True,
    lifespan=lifespan,
)

DOCS_NAV_ITEMS = [
    {"href": "/components", "label": "Components"},
    # {"href": "/blocks", "label": "Blocks"},  # Coming soon
    # {"href": "/themes", "label": "Themes"},  # Coming soon
]


@rt("/")
def home():
    from starui.registry.components.button import Button

    return DocsLayout(
        Div(
            # Hero Section - Minimal, high impact
            Div(
                H1(
                    "starUI",
                    cls="text-7xl sm:text-8xl md:text-9xl font-black tracking-tight mb-6 hover:gradient-text transition-all duration-300"
                ),
                P(
                    "Python components. Zero compromise.",
                    cls="text-4xl sm:text-5xl md:text-6xl text-gray-300 leading-tight mb-12"
                ),
                Div(
                    "↓ Scroll to explore",
                    cls="text-sm text-gray-400 animate-bounce"
                ),
                cls="min-h-screen flex flex-col items-center justify-center text-center px-4"
            ),

            # Constellation Section - Scroll-driven component reveals
            Div(
                *[
                    Div(
                        comp['component'],
                        Div(
                            H3(comp['name'], cls="text-xl font-bold mb-2"),
                            Pre(comp['code'], cls="text-sm bg-gray-900 text-gray-100 p-4 rounded-md"),
                            P("View documentation →", cls="text-primary text-sm mt-2"),
                            data_demo_panel=True,
                            style="display: none;",
                            cls="mt-4 bg-white border rounded-lg p-4 shadow-lg"
                        ),
                        data_constellation_item=True,
                        data_scroll_trigger=comp['scroll_trigger'],
                        style=f"position: absolute; {'; '.join(f'{k}: {v}' for k, v in comp['position'].items())}",
                        cls="cursor-pointer transition-all gradient-glow"
                    )
                    for comp in get_constellation_components()
                ],
                id="constellation-section",
                cls="relative min-h-[300vh] py-20"
            ),

            # Value Proposition Section
            Div(
                H2(
                    "Components you own. Code you control.",
                    cls="text-4xl sm:text-5xl font-bold text-center mb-16"
                ),
                Div(
                    _value_card(
                        "lucide:folder-open",
                        "In Your Codebase",
                        "Components live in your project. Edit directly. Own the code."
                    ),
                    _value_card(
                        "lucide:code-2",
                        "Fully Customizable",
                        "Modify styles, behavior, or anything else. It's your code."
                    ),
                    _value_card(
                        "lucide:eye",
                        "Zero Abstraction",
                        "Read the code. Debug easily. Pure Python. Clean & simple."
                    ),
                    cls="grid grid-cols-1 md:grid-cols-3 gap-8"
                ),
                P(
                    "Built on Tailwind CSS and Datastar. No CSS framework conflicts. No abstraction layers. Just clean code.",
                    cls="text-center text-sm text-muted-foreground mt-12 max-w-3xl mx-auto"
                ),
                cls="max-w-6xl mx-auto px-8 py-24"
            ),

            # Quick Start Section
            Div(
                H2(
                    "From zero to components in 30 seconds",
                    cls="text-3xl sm:text-4xl font-bold text-white text-center mb-12"
                ),
                Div(
                    # Step 1
                    Div(
                        Div(
                            Span("1", cls="flex h-10 w-10 items-center justify-center rounded-full bg-gradient-to-br from-amber-500 to-orange-500 text-white font-bold text-lg mb-4"),
                            H3("Install", cls="text-xl font-bold text-white mb-3"),
                            Pre(
                                "$ pip install starui",
                                cls="bg-black/50 text-gray-100 p-4 rounded-md font-mono text-sm"
                            ),
                        ),
                        cls="text-center"
                    ),
                    # Step 2
                    Div(
                        Div(
                            Span("2", cls="flex h-10 w-10 items-center justify-center rounded-full bg-gradient-to-br from-orange-500 to-pink-500 text-white font-bold text-lg mb-4"),
                            H3("Add", cls="text-xl font-bold text-white mb-3"),
                            Pre(
                                "$ star add button",
                                cls="bg-black/50 text-gray-100 p-4 rounded-md font-mono text-sm"
                            ),
                            P("✓ Installed button + deps", cls="text-green-400 text-sm mt-2"),
                        ),
                        cls="text-center"
                    ),
                    # Step 3
                    Div(
                        Div(
                            Span("3", cls="flex h-10 w-10 items-center justify-center rounded-full bg-gradient-to-br from-pink-500 to-purple-500 text-white font-bold text-lg mb-4"),
                            H3("Use", cls="text-xl font-bold text-white mb-3"),
                            Pre(
                                "from starui import Button\n\nButton(\"Click me!\")",
                                cls="bg-black/50 text-gray-100 p-4 rounded-md font-mono text-sm mb-4"
                            ),
                            Button("Click me!", variant="default", cls="mx-auto"),
                        ),
                        cls="text-center"
                    ),
                    cls="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12"
                ),
                A(
                    "Get Started →",
                    href="/installation",
                    cls="inline-flex items-center justify-center rounded-md text-lg font-semibold bg-gradient-to-r from-amber-500 via-orange-500 to-pink-500 text-white hover:opacity-90 h-12 px-8 py-3 transition-opacity"
                ),
                cls="bg-gray-900 py-20 px-8 text-center"
            ),

            cls="max-w-7xl mx-auto"
        ),
        Script("""
document.addEventListener('DOMContentLoaded', () => {
  const { animate, scroll } = window.Motion;
  const components = document.querySelectorAll('[data-constellation-item]');

  components.forEach(component => {
    const triggerPoint = parseFloat(component.dataset.scrollTrigger);
    const targetEl = component;

    targetEl.style.opacity = '0';
    targetEl.style.transform = 'translateY(50px)';

    scroll(
      animate(
        targetEl,
        {
          opacity: [0, 1],
          transform: ['translateY(50px)', 'translateY(0)']
        },
        {
          duration: 0.6,
          easing: 'ease-out'
        }
      ),
      {
        target: document.querySelector('#constellation-section'),
        offset: [`${triggerPoint * 100}%`, `${(triggerPoint * 100) + 10}%`]
      }
    );

    setTimeout(() => {
      animate(
        targetEl,
        {
          y: [-10, 10]
        },
        {
          duration: 3,
          repeat: Infinity,
          direction: 'alternate',
          easing: 'ease-in-out'
        }
      );
    }, (triggerPoint * 2000) + 600);

    targetEl.addEventListener('mouseenter', () => {
      animate(targetEl, { scale: 1.05 }, { duration: 0.3, easing: 'ease-out' });
      targetEl.classList.add('gradient-glow-intense');
    });

    targetEl.addEventListener('mouseleave', () => {
      animate(targetEl, { scale: 1 }, { duration: 0.3, easing: 'ease-out' });
      targetEl.classList.remove('gradient-glow-intense');
    });

    targetEl.addEventListener('click', () => {
      const demoPanel = targetEl.querySelector('[data-demo-panel]');
      const allComponents = document.querySelectorAll('[data-constellation-item]');

      if (targetEl.classList.contains('isolated')) {
        allComponents.forEach(comp => {
          animate(comp, { opacity: 1, filter: 'blur(0px)' }, { duration: 0.3 });
        });
        animate(targetEl, { scale: 1 }, { duration: 0.3 });
        if (demoPanel) demoPanel.style.display = 'none';
        targetEl.classList.remove('isolated');
      } else {
        allComponents.forEach(comp => {
          if (comp !== targetEl) {
            animate(comp, { opacity: 0.15, filter: 'blur(4px)' }, { duration: 0.3 });
          }
        });
        animate(targetEl, { scale: 1.3 }, { duration: 0.3 });
        if (demoPanel) demoPanel.style.display = 'block';
        targetEl.classList.add('isolated');
      }
    });
  });
});
        """),
        layout=LayoutConfig(
            title="StarUI - Python components. Zero compromise.",
            description="Server-rendered UI components for Python. No frameworks required.",
        ),
        footer=FooterConfig(
            attribution="Built with StarHTML",
            hosting_info="Component library for Python web apps",
        ),
    )


def _value_card(icon: str, title: str, description: str) -> FT:
    """Value proposition card with gradient icon."""
    return Div(
        Div(
            Icon(icon, width="32", height="32", cls="text-primary"),
            cls="mb-6 w-16 h-16 rounded-xl bg-gradient-to-br from-amber-500/10 via-orange-500/10 to-pink-500/10 flex items-center justify-center border border-primary/20"
        ),
        H3(title, cls="text-2xl font-bold mb-4"),
        P(description, cls="text-muted-foreground leading-relaxed"),
        cls="p-8 text-left"
    )


def _feature_card(icon: str, title: str, description: str) -> FT:
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
    return Div(
        Div(
            Span(emoji, cls="text-2xl mb-2 block"),
            P(text, cls="text-sm"),
            cls="text-center p-4"
        ),
        cls="border rounded-lg bg-gradient-to-br from-background via-background/80 to-muted/50 hover:shadow-md transition-all duration-200"
    )


def _professional_feature_card(title: str, description: str, icon: str) -> FT:
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
    
    return DocsLayout(
        Div(
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
            
            Div(
                H2("The Python-Native Approach", cls="text-3xl font-bold mb-8"),
                Div(
                    _feature_highlight_card(
                        "Server-First Architecture",
                        "Components render on the server and progressively enhance with interactivity. No client-side hydration, no bundle sizes, no waterfall loading.",
                        "from starui import Button, Input, Card\n\n# Pure Python - no JSX, no build step\nCard(\n    Input(placeholder=\"Search...\"),\n    Button(\"Submit\", data_on_click=\"search()\")\n)",
                        "Python syntax with type safety and IDE support",
                        "lucide:server"
                    ),
                    _feature_highlight_card(
                        "Reactive Without React",
                        "Datastar provides declarative state management and reactive updates while keeping all logic server-side. Get modern UX patterns without JavaScript frameworks.",
                        "# Reactive counter - no useState, no hooks\nButton(\n    (count := Signal(\"count\", 0)),\n    data_text=\"Count: \" + count,\n    data_on_click=count.add(1)\n)\n\n# State stays on the server",
                        "Reactive patterns with server-side state",
                        "lucide:zap"
                    ),
                    cls="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6 lg:gap-8 mb-16"
                ),
            ),

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
    registry = get_registry()
    return create_components_index(registry, DOCS_SIDEBAR_SECTIONS)


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

    # The component's create_docs function should handle sidebar sections
    return component.get("create_docs", lambda: None)()


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
    
    return DocsLayout(
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


def _next_step_card(icon: str, title: str, description: str, href: str, button_text: str) -> FT:
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


iframe_app, iframe_rt = star_app(
    title="Component Preview",
    live=True,
    hdrs=(
        # Inherit parent theme with iframe-specific fallback support
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
        # Add CSS for theme toggle icon switching
        Style("""
            [data-theme="light"] .theme-icon-alt,
            [data-theme="dark"] .theme-icon-default {
                display: none;
            }
        """),
        Link(rel="stylesheet", href="/static/css/starui.css"),
        position_handler(),
    ),
    htmlkw=dict(lang="en", dir="ltr"),
    bodykw=dict(cls="min-h-screen bg-background text-foreground"),
    iconify=True,
    clipboard=True,
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