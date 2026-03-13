from starhtml import *
from widgets.code_block import CodeBlock
from widgets.onwards import onwards_card, onwards_section
from layouts.base import DocsLayout, LayoutConfig, SidebarConfig


def _command_card(
    num: str,
    title: str,
    description: str,
    *body,
) -> FT:
    return Div(
        Div(
            Div(
                Div(
                    Span(num, cls="flex h-10 w-10 items-center justify-center rounded-full bg-primary font-mono text-sm font-semibold text-primary-foreground"),
                    cls="flex-shrink-0"
                ),
                Div(
                    H3(title, cls="mb-2 font-mono text-xl font-semibold"),
                    P(description, cls="mb-4 text-muted-foreground"),
                    *body,
                    cls="min-w-0 flex-1 overflow-hidden"
                ),
                cls="flex flex-col items-start gap-4 sm:flex-row sm:gap-6"
            ),
            cls="overflow-hidden rounded-lg border bg-gradient-to-br from-background to-muted/20 p-4 sm:p-6"
        ),
        cls="mb-8"
    )


def _options_table(*rows) -> FT:
    return Div(
        Div(
            *[
                Div(
                    Span(flag, cls="font-mono text-sm font-medium text-primary"),
                    P(desc, cls="mt-0.5 text-sm text-muted-foreground"),
                    cls="py-2"
                )
                for flag, desc in rows
            ],
            cls="divide-y divide-border"
        ),
        cls="mt-4 rounded-md border border-border bg-muted/20 px-4"
    )


def _callout(text: str, icon: str = "lucide:info") -> FT:
    return Div(
        Icon(icon, cls="mt-0.5 mr-3 h-5 w-5 flex-shrink-0 text-primary"),
        P(text, cls="text-sm text-muted-foreground"),
        cls="mt-4 flex items-start rounded-md bg-muted/30 p-4"
    )


def create_cli_docs(sidebar_sections: list) -> FT:
    return DocsLayout(
        Div(
            # Overview
            Div(
                P(
                    "The ", Code("star", cls="text-sm"), " CLI manages your StarUI components, builds production CSS, and runs the dev server.",
                    cls="mb-4 text-muted-foreground",
                ),
                CodeBlock("star --version", language="bash"),
                cls="mb-12"
            ),

            H2("Commands", cls="mb-8 text-3xl font-bold tracking-tight"),

            # 1. star init
            _command_card(
                "1", "star init",
                "Initialize a new StarUI project. Creates configuration, component directory, Tailwind input CSS, and a starter app file.",
                CodeBlock("star init", language="bash"),
                _options_table(
                    ("--force", "Force initialization even if project already set up"),
                    ("--verbose, -v", "Show detailed output"),
                    ("--component-dir DIR", "Set the component install directory"),
                    ("--no-interaction", "Non-interactive mode for CI environments"),
                ),
                _callout("In non-interactive mode, all prompts are skipped and sensible defaults are used. Useful for CI pipelines and scripted setups."),
            ),

            # 2. star add
            _command_card(
                "2", "star add",
                "Add components and blocks to your project. Dependencies are resolved and installed automatically.",
                CodeBlock(
                    """# Add a single component
star add button

# Add multiple components at once
star add button input card tabs

# Add a block
star add user-button-01

# Overwrite existing files
star add button --force""",
                    language="bash",
                ),
                _options_table(
                    ("<components>", "One or more component or block names (required)"),
                    ("--force", "Overwrite existing files"),
                    ("--verbose, -v", "Show detailed output"),
                    ("--theme THEME", "Theme for code highlighting components"),
                    ("--component-dir DIR", "Override the component install directory"),
                ),
            ),

            # 3. star dev
            _command_card(
                "3", "star dev",
                "Start the development server with dual hot reload: Tailwind CSS rebuilds on class changes, and Python code reloads on file saves.",
                CodeBlock(
                    """# Start dev server (default port 5000)
star dev app.py

# Specify a port
star dev app.py --port 8000

# Disable CSS hot reload
star dev app.py --no-css-hot""",
                    language="bash",
                ),
                _options_table(
                    ("<app_file>", "StarHTML app file to run (required)"),
                    ("--port, -p PORT", "Port number (default: 5000)"),
                    ("--css-hot / --no-css-hot", "Enable or disable CSS hot reload (default: enabled)"),
                    ("--strict", "Fail if the detected port is unavailable instead of auto-finding one"),
                    ("--debug / --no-debug", "Enable or disable debug mode (default: enabled)"),
                ),
                _callout(
                    "Port detection reads your app file for patterns like serve(port=...) and uvicorn.run(port=...). "
                    "If that port is busy and --strict is off, the next available port is used automatically."
                ),
            ),

            # 4. star build
            _command_card(
                "4", "star build",
                "Build production CSS. Downloads a standalone Tailwind binary automatically \u2014 no Node.js required.",
                CodeBlock(
                    """# Build with defaults (minified)
star build

# Custom output path, unminified
star build --output static/css/app.css --no-minify""",
                    language="bash",
                ),
                _options_table(
                    ("--output, -o PATH", "CSS output path (default: from config or auto-detected)"),
                    ("--minify / --no-minify", "Minify the output CSS (default: minified)"),
                    ("--verbose, -v", "Show detailed output"),
                ),
                _callout(
                    "The Tailwind binary is downloaded once and cached at ~/.starui/cache/. "
                    "Subsequent builds reuse the cached binary with zero network overhead."
                ),
            ),

            # 5. star list
            _command_card(
                "5", "star list",
                "List all available components and blocks from the registry.",
                CodeBlock(
                    """# List everything
star list

# Search by name
star list --search button

# Show only installed components
star list --installed""",
                    language="bash",
                ),
                _options_table(
                    ("--search QUERY", "Filter components by name"),
                    ("--installed", "Show only installed components"),
                    ("--verbose, -v", "Show detailed output with descriptions"),
                ),
            ),

            # 6. star status
            _command_card(
                "6", "star status",
                "Show the status of installed components and blocks. Detects local modifications using checksum comparison against the registry version.",
                CodeBlock("star status", language="bash"),
                _callout(
                    "Checksums are computed at install time and stored in .starui/manifest.json. "
                    "Any local edits to component files will be flagged as modified."
                ),
            ),

            # 7. star diff
            _command_card(
                "7", "star diff",
                "Show a diff between your local component file and the latest registry version. Useful for reviewing what you've changed.",
                CodeBlock(
                    """# See what changed in your local button
star diff button""",
                    language="bash",
                ),
                _options_table(
                    ("<component>", "Component or block name to diff (required)"),
                ),
            ),

            # 8. star update
            _command_card(
                "8", "star update",
                "Update installed components and blocks to the latest registry versions. Skips locally modified files unless forced.",
                CodeBlock(
                    """# Update all components
star update

# Update specific components
star update button card

# Force-update even if locally modified
star update button --force""",
                    language="bash",
                ),
                _options_table(
                    ("<components>", "Specific components to update (optional \u2014 updates all if omitted)"),
                    ("--force", "Overwrite locally modified files"),
                    ("--verbose, -v", "Show detailed output"),
                ),
            ),

            # 9. star sort
            _command_card(
                "9", "star sort",
                "Sort Tailwind classes in Python source files for consistent ordering.",
                CodeBlock(
                    """# Sort all Python files in the current directory
star sort

# Sort specific files or directories
star sort components/ app.py

# Check mode for CI (exits code 1 if changes needed)
star sort --check""",
                    language="bash",
                ),
                _options_table(
                    ("<paths>", "Files or directories to sort (optional \u2014 defaults to current directory)"),
                    ("--check", "Check only \u2014 exit code 1 if any changes would be made"),
                    ("--verbose, -v", "Show detailed output"),
                ),
                _callout(
                    "Use --check in CI pipelines as a lint gate. It exits with code 1 if any files have unsorted classes, without modifying them."
                ),
            ),

            onwards_section(
                onwards_card("01", "Configuration", "Project settings, auto-detection, manifest, and cache.", "/configuration", "View Configuration"),
                onwards_card("02", "Deployment", "Production builds, CI/CD pipelines, and GitHub Actions.", "/deployment", "View Deployment"),
                onwards_card("03", "Components", "Browse the full constellation of UI components.", "/components", "Browse Components"),
            ),
        ),
        layout=LayoutConfig(
            title="CLI Reference",
            description="Complete reference for the star command-line interface.",
            show_sidebar=True,
        ),
        sidebar=SidebarConfig(sections=sidebar_sections),
    )
