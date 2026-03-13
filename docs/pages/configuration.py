from starhtml import *
from widgets.code_block import CodeBlock
from layouts.base import DocsLayout, LayoutConfig, SidebarConfig


def _section(title: str, *children) -> FT:
    return Div(
        H2(title, cls="mb-8 text-3xl font-bold tracking-tight"),
        *children,
        cls="mb-12"
    )


def _card(*children) -> FT:
    return Div(
        Div(*children, cls="overflow-hidden rounded-lg border bg-gradient-to-br from-background to-muted/20 p-4 sm:p-6"),
        cls="mb-8"
    )


def _callout(text: str, icon: str = "lucide:info") -> FT:
    return Div(
        Icon(icon, cls="mt-0.5 mr-3 h-5 w-5 flex-shrink-0 text-primary"),
        P(text, cls="text-sm text-muted-foreground"),
        cls="mt-4 flex items-start rounded-md bg-muted/30 p-4"
    )


def _config_key(name: str, description: str) -> FT:
    return Div(
        Span(name, cls="font-mono text-sm font-medium text-primary"),
        P(description, cls="mt-0.5 text-sm text-muted-foreground"),
        cls="py-2"
    )


def create_configuration_docs(sidebar_sections: list) -> FT:
    return DocsLayout(
        Div(
            # Project Configuration
            _section(
                "Project Configuration",
                _card(
                    H3("pyproject.toml", cls="mb-2 text-xl font-semibold"),
                    P(
                        "StarUI reads its settings from the ",
                        Code("[tool.starui]", cls="text-sm"),
                        " section in your project's ",
                        Code("pyproject.toml", cls="text-sm"),
                        ".",
                        cls="mb-4 text-muted-foreground",
                    ),
                    CodeBlock(
                        """[tool.starui]
component_dir = "components/ui"
css_output = "static/css/starui.css"
css_dir = "static/css" """,
                        language="toml",
                    ),
                    Div(
                        _config_key("component_dir", "Directory where components are installed. Relative to project root."),
                        _config_key("css_output", "Path for the generated CSS file."),
                        _config_key("css_dir", "Directory containing input.css. Defaults to the parent directory of css_output."),
                        cls="mt-4 divide-y divide-border rounded-md border border-border bg-muted/20 px-4"
                    ),
                ),
            ),

            # Configuration Resolution
            _section(
                "Configuration Resolution",
                _card(
                    H3("Priority Order", cls="mb-2 text-xl font-semibold"),
                    P("When resolving settings, StarUI checks these sources in order:", cls="mb-4 text-muted-foreground"),
                    Div(
                        Div(
                            Span("1", cls="flex h-7 w-7 items-center justify-center rounded-full bg-primary text-xs font-semibold text-primary-foreground"),
                            Div(
                                Span("CLI flags", cls="text-sm font-medium"),
                                P("e.g. --component-dir, --output", cls="text-xs text-muted-foreground"),
                            ),
                            cls="flex items-center gap-3 py-2"
                        ),
                        Div(
                            Span("2", cls="flex h-7 w-7 items-center justify-center rounded-full bg-primary text-xs font-semibold text-primary-foreground"),
                            Div(
                                Span("pyproject.toml", cls="text-sm font-medium"),
                                P("[tool.starui] section", cls="text-xs text-muted-foreground"),
                            ),
                            cls="flex items-center gap-3 py-2"
                        ),
                        Div(
                            Span("3", cls="flex h-7 w-7 items-center justify-center rounded-full bg-primary text-xs font-semibold text-primary-foreground"),
                            Div(
                                Span("Auto-detection", cls="text-sm font-medium"),
                                P("Scans project structure for common patterns", cls="text-xs text-muted-foreground"),
                            ),
                            cls="flex items-center gap-3 py-2"
                        ),
                        cls="space-y-1"
                    ),
                ),
                _card(
                    H3("Auto-Detection Defaults", cls="mb-2 text-xl font-semibold"),
                    P("When no explicit config is found, StarUI infers paths from your project layout:", cls="mb-4 text-muted-foreground"),
                    Div(
                        Div(
                            Span("component_dir", cls="font-mono text-sm font-medium text-primary"),
                            P(
                                Code("ui/", cls="text-sm"), " if it exists, otherwise ",
                                Code("components/ui/", cls="text-sm"),
                                cls="mt-0.5 text-sm text-muted-foreground",
                            ),
                            cls="py-2"
                        ),
                        Div(
                            Span("css_output", cls="font-mono text-sm font-medium text-primary"),
                            P(
                                Code("static/css/starui.css", cls="text-sm"), " if ",
                                Code("static/", cls="text-sm"), " exists, ",
                                Code("assets/starui.css", cls="text-sm"), " if ",
                                Code("assets/", cls="text-sm"), " exists, otherwise ",
                                Code("starui.css", cls="text-sm"),
                                cls="mt-0.5 text-sm text-muted-foreground",
                            ),
                            cls="py-2"
                        ),
                        Div(
                            Span("css_dir", cls="font-mono text-sm font-medium text-primary"),
                            P("Parent directory of css_output", cls="mt-0.5 text-sm text-muted-foreground"),
                            cls="py-2"
                        ),
                        cls="divide-y divide-border rounded-md border border-border bg-muted/20 px-4"
                    ),
                ),
            ),

            # Project Structure
            _section(
                "Project Structure",
                _card(
                    H3("What star init creates", cls="mb-2 text-xl font-semibold"),
                    P("Running ", Code("star init", cls="text-sm"), " scaffolds the following structure:", cls="mb-4 text-muted-foreground"),
                    CodeBlock(
                        """my-project/
\u251c\u2500\u2500 pyproject.toml          # [tool.starui] section added
\u251c\u2500\u2500 app.py                  # Starter StarHTML app
\u251c\u2500\u2500 components/
\u2502   \u2514\u2500\u2500 ui/
\u2502       \u251c\u2500\u2500 __init__.py
\u2502       \u251c\u2500\u2500 utils.py        # cn() and shared utilities
\u2502       \u2514\u2500\u2500 theme_toggle.py # Theme toggle + dependencies
\u251c\u2500\u2500 static/
\u2502   \u2514\u2500\u2500 css/
\u2502       \u251c\u2500\u2500 input.css       # Tailwind v4 input
\u2502       \u2514\u2500\u2500 starui.css      # Generated output (git-ignored)
\u2514\u2500\u2500 .starui/
    \u2514\u2500\u2500 manifest.json       # Component tracking""",
                        language="text",
                    ),
                ),
                _card(
                    H3("input.css", cls="mb-2 text-xl font-semibold"),
                    P("The generated input.css uses Tailwind v4 syntax with the StarUI theme system:", cls="mb-4 text-muted-foreground"),
                    CodeBlock(
                        """@import "tailwindcss";
@plugin "@tailwindcss/typography";

@custom-variant dark (&:where(.dark, .dark *, [data-theme="dark"], ...));

@theme {
  --radius: 0.65rem;
  --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", ...;
  --font-mono: ui-monospace, "SF Mono", "Monaco", ...;
}

:root {
  /* Light theme: background, foreground, primary, etc. */
}

.dark, [data-theme="dark"] {
  /* Dark theme overrides */
}""",
                        language="css",
                    ),
                    _callout("Colors use OKLch color space for perceptually uniform theming. Named theme variants like [data-theme=\"blue\"] are included for easy customization."),
                ),
            ),

            # Manifest
            _section(
                "Manifest",
                _card(
                    H3(".starui/manifest.json", cls="mb-2 text-xl font-semibold"),
                    P("The manifest tracks every component and block installed in your project:", cls="mb-4 text-muted-foreground"),
                    CodeBlock(
                        """{
  "registry_version": "main",
  "components": {
    "button": {
      "version": "0.3.2",
      "checksum": "a1b2c3d4...",
      "file": "components/ui/button.py"
    }
  },
  "blocks": {
    "user_button_01": {
      "version": "0.3.2",
      "checksum": "e5f6a7b8...",
      "file": "blocks/user_button_01/user_button.py"
    }
  }
}""",
                        language="json",
                    ),
                    _callout(
                        "Checksums enable modification detection. When you edit a component locally, "
                        "star status will flag it as modified and star update will skip it unless --force is used."
                    ),
                ),
            ),

            # Cache
            _section(
                "Cache",
                _card(
                    H3("~/.starui/cache/", cls="mb-2 font-mono text-xl font-semibold"),
                    P("StarUI maintains a global cache for the Tailwind binary and registry index. Component sources are cached on-demand as you install them:", cls="mb-4 text-muted-foreground"),
                    CodeBlock(
                        """~/.starui/cache/
\u251c\u2500\u2500 latest/                       # Tailwind binary version
\u2502   \u2514\u2500\u2500 tailwindcss-macos-arm64   # Platform-specific binary (~40 MB)
\u2514\u2500\u2500 registry/
    \u251c\u2500\u2500 main/
    \u2502   \u251c\u2500\u2500 index.json            # Component registry index
    \u2502   \u251c\u2500\u2500 index.meta.json       # Cache timestamp
    \u2502   \u251c\u2500\u2500 components/           # Sources fetched during star add
    \u2502   \u2514\u2500\u2500 blocks/               # Block sources fetched during star add
    \u2514\u2500\u2500 v0.3.2/                   # Pinned version (immutable)
        \u2514\u2500\u2500 ...""",
                        language="text",
                    ),
                ),
                _card(
                    H3("Cache TTL", cls="mb-2 text-xl font-semibold"),
                    P("Cache freshness depends on the registry version:", cls="mb-4 text-muted-foreground"),
                    Div(
                        Div(
                            Span("Mutable versions", cls="text-sm font-medium"),
                            P(
                                "e.g. ", Code("main", cls="text-sm"),
                                " \u2014 index re-fetched after 1 hour",
                                cls="mt-0.5 text-sm text-muted-foreground",
                            ),
                            cls="py-2"
                        ),
                        Div(
                            Span("Immutable versions", cls="text-sm font-medium"),
                            P(
                                "e.g. ", Code("v0.3.2", cls="text-sm"),
                                " \u2014 cached permanently, never re-fetched",
                                cls="mt-0.5 text-sm text-muted-foreground",
                            ),
                            cls="py-2"
                        ),
                        cls="divide-y divide-border rounded-md border border-border bg-muted/20 px-4"
                    ),
                    _callout("Component source files are validated by checksum. If the cached file matches the registry checksum, it's served from cache regardless of age."),
                ),
            ),
        ),
        layout=LayoutConfig(
            title="Configuration",
            description="How StarUI discovers and uses project configuration.",
            show_sidebar=True,
        ),
        sidebar=SidebarConfig(sections=sidebar_sections),
    )
