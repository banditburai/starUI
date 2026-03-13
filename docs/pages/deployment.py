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


def create_deployment_docs(sidebar_sections: list) -> FT:
    return DocsLayout(
        Div(
            # Production Build
            _section(
                "Production Build",
                _card(
                    H3("star build", cls="mb-2 text-xl font-semibold"),
                    P(
                        "Build optimized, minified CSS for production. The CLI downloads a standalone Tailwind binary automatically \u2014 no Node.js or npm required.",
                        cls="mb-4 text-muted-foreground",
                    ),
                    CodeBlock(
                        """# Build minified CSS (default)
star build

# Custom output path, unminified
star build --output static/css/app.css --no-minify""",
                        language="bash",
                    ),
                    _callout(
                        "The Tailwind binary is resolved in order: system PATH \u2192 ~/.starui/cache/ \u2192 auto-download. "
                        "Once cached, builds run entirely offline."
                    ),
                ),
            ),

            # CI/CD Pipeline
            _section(
                "CI/CD Pipeline",
                _card(
                    H3("Minimum Required Steps", cls="mb-2 text-xl font-semibold"),
                    P("A CI pipeline needs just two commands after installing dependencies:", cls="mb-4 text-muted-foreground"),
                    CodeBlock(
                        """# 1. Install dependencies
uv sync

# 2. Build production CSS
uv run star build

# 3. (Optional) Lint Tailwind class ordering
uv run star sort --check""",
                        language="bash",
                    ),
                    _callout(
                        "star sort --check exits with code 1 if any files have unsorted Tailwind classes, "
                        "without modifying them. Use it as a CI gate alongside your other linters."
                    ),
                ),
            ),

            # Caching the Tailwind Binary
            _section(
                "Caching the Tailwind Binary",
                _card(
                    H3("Why Cache?", cls="mb-2 text-xl font-semibold"),
                    P(
                        "The standalone Tailwind binary is ~40 MB. Without caching, every CI run downloads it fresh. "
                        "Cache the ", Code("~/.starui/cache", cls="text-sm"), " directory to skip this.",
                        cls="mb-4 text-muted-foreground",
                    ),
                    H3("GitHub Actions", cls="mt-6 mb-4 text-lg font-semibold"),
                    CodeBlock(
                        """- uses: actions/cache@v4
  with:
    path: ~/.starui/cache
    key: starui-tailwind-${{ runner.os }}-${{ runner.arch }}""",
                        language="yaml",
                    ),
                    H3("Other CI Systems", cls="mt-6 mb-4 text-lg font-semibold"),
                    P("Cache the directory ", Code("~/.starui/cache", cls="text-sm"), " using your provider's cache mechanism. The key should include OS and architecture since the binary is platform-specific.", cls="text-muted-foreground"),
                ),
            ),

            # Example GitHub Actions Workflow
            _section(
                "Example GitHub Actions Workflow",
                _card(
                    P("A complete workflow that installs dependencies, caches the Tailwind binary, builds CSS, and lints class ordering:", cls="mb-4 text-muted-foreground"),
                    CodeBlock(
                        """name: Build & Lint

on:
  push:
    branches: [main]
  pull_request:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: astral-sh/setup-uv@v5
        with:
          enable-cache: true

      - run: uv sync

      - uses: actions/cache@v4
        with:
          path: ~/.starui/cache
          key: starui-tailwind-${{ runner.os }}-${{ runner.arch }}

      - run: uv run star build

      - run: uv run star sort --check""",
                        language="yaml",
                    ),
                ),
            ),

        ),
        layout=LayoutConfig(
            title="Deployment",
            description="Build for production and set up CI/CD pipelines.",
            show_sidebar=True,
        ),
        sidebar=SidebarConfig(sections=sidebar_sections),
    )
