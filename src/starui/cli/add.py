import re
import subprocess

import typer

from starui.config import get_project_config
from starui.registry.component_metadata import get_component_metadata
from starui.registry.loader import ComponentLoader

from .utils import confirm, console, error, info, status_context, success, warning


def _setup_code_highlighting(config, theme: str | None) -> None:
    try:
        from starlighter import StarlighterStyles
    except ImportError:
        warning(
            "Starlighter not installed. This should have been installed automatically. Try: uv add starlighter"
        )
        return

    css_dir = config.css_dir_absolute
    input_css = css_dir / "input.css"

    if not theme:
        console.print("\n[bold]Select a syntax highlighting theme:[/bold]")
        themes = [
            (
                "github-light",
                "github-dark",
                "GitHub (light/dark auto-switching) [default]",
            ),
            ("monokai", None, "Monokai (dark only)"),
            ("dracula", None, "Dracula (dark only)"),
        ]
        for i, (_, _, desc) in enumerate(themes, 1):
            console.print(f"{i}. {desc}")

        choice = int(typer.prompt("Enter choice (1-3)", default="1")) - 1
        light_theme, dark_theme, _ = themes[min(choice, len(themes) - 1)]
    else:
        light_theme, dark_theme = None, theme

    if light_theme and dark_theme:
        styles = StarlighterStyles(light_theme, dark_theme, auto_switch=True)
        theme_name = f"{light_theme}/{dark_theme}"
        mode = "light/dark auto-switching"
    else:
        styles = StarlighterStyles(dark_theme or theme)
        theme_name = dark_theme or theme
        mode = "dark only"

    css_content = str(styles)
    if css_content.startswith("<style>") and css_content.endswith("</style>"):
        css_content = css_content[7:-8].strip()

    (css_dir / "starlighter.css").write_text(css_content)
    success(f"Generated starlighter.css with {theme_name} theme ({mode})")

    if input_css.exists():
        content = input_css.read_text()
        if "@import './starlighter.css'" not in content:
            lines = content.split("\n")
            idx = next(
                (
                    i + 1
                    for i, line in enumerate(lines)
                    if '@import "tailwindcss"' in line
                ),
                1,
            )
            lines.insert(idx, "@import './starlighter.css';")
            input_css.write_text("\n".join(lines))
            info("Added starlighter.css import to input.css")

    info("Run 'star build css' to rebuild your styles")


def add_command(
    components: list[str] = typer.Argument(..., help="Components to add"),
    force: bool = typer.Option(False, "--force", help="Overwrite existing files"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show details"),
    theme: str = typer.Option(None, "--theme", help="Theme for code highlighting"),
) -> None:
    """Add components to your project."""

    if invalid := [c for c in components if not re.match(r"^[a-z][a-z0-9_-]*$", c)]:
        error(f"Invalid component names: {', '.join(invalid)}")
        raise typer.Exit(1)

    try:
        config = get_project_config()
        loader = ComponentLoader()
    except Exception as e:
        error(f"Initialization failed: {e}")
        raise typer.Exit(1) from e

    try:
        resolved = {}
        for component in components:
            normalized = component.replace("-", "_")
            if verbose:
                info(f"Resolving {component} -> {normalized}...")
            resolved.update(loader.load_component_with_dependencies(normalized))

        component_dir = config.component_dir_absolute
        existing = [
            component_dir / f"{name}.py"
            for name in resolved
            if (component_dir / f"{name}.py").exists()
        ]

        if existing and not force:
            warning(f"Found {len(existing)} existing files:")
            for path in existing:
                console.print(f"  • {path}")
            if not confirm("Overwrite?", default=False):
                raise typer.Exit(0)

        packages = {
            pkg
            for name in resolved
            if (metadata := get_component_metadata(name))
            for pkg in metadata.packages
        }

        for package in packages:
            info(f"Installing package: {package}")
            try:
                subprocess.run(
                    ["uv", "add", package],
                    check=True,
                    capture_output=True,
                    text=True,
                )
                success(f"Installed: {package}")
            except subprocess.CalledProcessError as e:
                warning(f"Failed to install {package}: {e.stderr}")

        if "code_block" in resolved:
            _setup_code_highlighting(config, theme)

        with status_context("Installing components..."):
            component_dir.mkdir(parents=True, exist_ok=True)
            (component_dir / "__init__.py").touch()

            for name, source in resolved.items():
                source = re.sub(
                    r"from\s+\.utils\s+import", "from starui import", source
                )
                (component_dir / f"{name}.py").write_text(source)

        success(f"Installed components: {', '.join(resolved.keys())}")

        if verbose:
            info(f"Location: {component_dir}")

        first = list(resolved)[0].title().replace("_", "")
        console.print(f"\n💡 Next steps:\n  • Import: from starui import {first}")

    except Exception as e:
        error(f"Installation failed: {e}")
        raise typer.Exit(1) from e
