"""Templates for StarUI project scaffolding."""

from pathlib import Path

from .config import ProjectConfig

APP_TEMPLATE = """\
from starhtml import *
from {component_import}.theme_toggle import ThemeToggle

styles = Link(rel="stylesheet", href="{css_path}", type="text/css")

app, rt = star_app(
    hdrs=(
        theme_script(use_data_theme=True),
        styles,
    ),
    htmlkw=dict(lang="en", dir="ltr"),
    bodykw=dict(cls="min-h-screen bg-background text-foreground")
)

@rt("/")
def get():
    return Div(
        Div(ThemeToggle(), cls="absolute top-4 right-4"),
        Div(
            H1("Nothing to see here yet...", cls="mb-2 text-2xl font-bold text-foreground"),
            P("But your StarHTML app is running!", cls="text-base text-muted-foreground"),
            P("Theme toggle in top right →", cls="mt-4 text-sm text-muted-foreground"),
            cls="text-center"
        ),
        cls="relative flex min-h-screen items-center justify-center"
    )

if __name__ == "__main__":
    serve(port=8000)
"""

TAILWIND_CSS_TEMPLATE = """\
@import "tailwindcss";
@plugin "@tailwindcss/typography";

@custom-variant dark (&:where(.dark, .dark *, [data-theme="dark"], [data-theme="dark"] *));

@theme {
  --radius: 0.65rem;
  --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", "Oxygen", "Ubuntu", "Cantarell", "Fira Sans", "Droid Sans", "Helvetica Neue", sans-serif;
  --font-mono: ui-monospace, "SF Mono", "Monaco", "Inconsolata", "Fira Code", "Fira Mono", "Roboto Mono", monospace;
}
:root {
  --radius: 0.625rem;
  --background: oklch(1 0 0);
  --foreground: oklch(0.145 0 0);
  --card: oklch(1 0 0);
  --card-foreground: oklch(0.145 0 0);
  --popover: oklch(1 0 0);
  --popover-foreground: oklch(0.145 0 0);
  --primary: oklch(0.205 0 0);
  --primary-foreground: oklch(0.985 0 0);
  --secondary: oklch(0.97 0 0);
  --secondary-foreground: oklch(0.205 0 0);
  --muted: oklch(0.97 0 0);
  --muted-foreground: oklch(0.556 0 0);
  --accent: oklch(0.97 0 0);
  --accent-foreground: oklch(0.205 0 0);
  --destructive: oklch(0.577 0.245 27.325);
  --border: oklch(0.922 0 0);
  --input: oklch(0.922 0 0);
  --ring: oklch(0.708 0 0);
  --chart-1: oklch(0.646 0.222 41.116);
  --chart-2: oklch(0.6 0.118 184.704);
  --chart-3: oklch(0.398 0.07 227.392);
  --chart-4: oklch(0.828 0.189 84.429);
  --chart-5: oklch(0.769 0.188 70.08);
  --sidebar: oklch(0.985 0 0);
  --sidebar-foreground: oklch(0.145 0 0);
  --sidebar-primary: oklch(0.205 0 0);
  --sidebar-primary-foreground: oklch(0.985 0 0);
  --sidebar-accent: oklch(0.97 0 0);
  --sidebar-accent-foreground: oklch(0.205 0 0);
  --sidebar-border: oklch(0.922 0 0);
  --sidebar-ring: oklch(0.708 0 0);
}

.dark, [data-theme="dark"] {
  --background: oklch(0.145 0 0);
  --foreground: oklch(0.985 0 0);
  --card: oklch(0.205 0 0);
  --card-foreground: oklch(0.985 0 0);
  --popover: oklch(0.205 0 0);
  --popover-foreground: oklch(0.985 0 0);
  --primary: oklch(0.985 0 0);
  --primary-foreground: oklch(0.145 0 0);
  --secondary: oklch(0.31 0 0);
  --secondary-foreground: oklch(0.985 0 0);
  --muted: oklch(0.31 0 0);
  --muted-foreground: oklch(0.708 0 0);
  --accent: oklch(0.31 0 0);
  --accent-foreground: oklch(0.985 0 0);
  --destructive: oklch(0.521 0.245 27.325);
  --destructive-foreground: oklch(0.985 0 0);
  --border: oklch(1 0 0 / 10%);
  --input: oklch(1 0 0 / 15%);
  --ring: oklch(0.556 0 0);
  --chart-1: oklch(0.828 0.189 84.429);
  --chart-2: oklch(0.769 0.188 70.08);
  --chart-3: oklch(0.646 0.222 41.116);
  --chart-4: oklch(0.6 0.118 184.704);
  --chart-5: oklch(0.398 0.07 227.392);
  --sidebar: oklch(0.205 0 0);
  --sidebar-foreground: oklch(0.985 0 0);
  --sidebar-primary: oklch(0.985 0 0);
  --sidebar-primary-foreground: oklch(0.145 0 0);
  --sidebar-accent: oklch(0.31 0 0);
  --sidebar-accent-foreground: oklch(0.985 0 0);
  --sidebar-border: oklch(0.31 0 0);
  --sidebar-ring: oklch(0.851 0 0);
}

[data-theme="blue"] { --primary: oklch(59.2% 0.221 239.314); --primary-foreground: oklch(98.5% 0 0); }
[data-theme="green"] { --primary: oklch(46.3% 0.154 154.893); --primary-foreground: oklch(98.5% 0 0); }

@theme inline {
  --color-background: var(--background);
  --color-foreground: var(--foreground);
  --color-card: var(--card);
  --color-card-foreground: var(--card-foreground);
  --color-popover: var(--popover);
  --color-popover-foreground: var(--popover-foreground);
  --color-primary: var(--primary);
  --color-primary-foreground: var(--primary-foreground);
  --color-secondary: var(--secondary);
  --color-secondary-foreground: var(--secondary-foreground);
  --color-muted: var(--muted);
  --color-muted-foreground: var(--muted-foreground);
  --color-accent: var(--accent);
  --color-accent-foreground: var(--accent-foreground);
  --color-destructive: var(--destructive);
  --color-destructive-foreground: var(--destructive-foreground);
  --color-border: var(--border);
  --color-input: var(--input);
  --color-ring: var(--ring);
  --color-chart-1: var(--chart-1);
  --color-chart-2: var(--chart-2);
  --color-chart-3: var(--chart-3);
  --color-chart-4: var(--chart-4);
  --color-chart-5: var(--chart-5);
  --color-sidebar: var(--sidebar);
  --color-sidebar-foreground: var(--sidebar-foreground);
  --color-sidebar-primary: var(--sidebar-primary);
  --color-sidebar-primary-foreground: var(--sidebar-primary-foreground);
  --color-sidebar-accent: var(--sidebar-accent);
  --color-sidebar-accent-foreground: var(--sidebar-accent-foreground);
  --color-sidebar-border: var(--sidebar-border);
  --color-sidebar-ring: var(--sidebar-ring);
  --radius: var(--radius);
}

@layer base {
  * {
    @apply border-border;
  }
  body {
    @apply bg-background text-foreground;
  }
}"""


def generate_app_starter(config: ProjectConfig | None = None, **_) -> str:
    """Generate StarHTML app starter with theme system."""
    if config is None:
        config = ProjectConfig(
            project_root=Path.cwd(),
            css_output=Path("starui.css"),
            component_dir=Path("components/ui"),
        )

    css_path = str(config.css_output)
    if not css_path.startswith("/"):
        css_path = "/" + css_path

    component_import = str(config.component_dir).replace("/", ".").replace("\\", ".")
    return APP_TEMPLATE.format(css_path=css_path, component_import=component_import)


def generate_css_input(config: ProjectConfig | None = None) -> str:
    """Generate CSS input file with hybrid theming for Tailwind v4."""
    return TAILWIND_CSS_TEMPLATE
