import re
import subprocess

import typer

from starui.config import get_project_config
from starui.registry.component_metadata import get_component_metadata
from starui.registry.loader import ComponentLoader

from .utils import confirm, console, error, info, status_context, success, warning


def _setup_code_highlighting(config, theme: str | None) -> None:
    try:
        from starlighter import THEMES
    except ImportError:
        warning(
            "Starlighter not installed. This should have been installed automatically. Try: uv add starlighter"
        )
        return

    from starui.registry.components.code_block import _RESIDUAL_CSS

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

    def _wrap_vars(selector: str, theme_name: str) -> str:
        rules = "\n    ".join(f"{k}: {v};" for k, v in THEMES[theme_name].items())
        return f"{selector} {{\n    {rules}\n}}"

    css_parts = [_RESIDUAL_CSS.strip()]

    if light_theme and dark_theme:
        css_parts.append(_wrap_vars(":root", light_theme))
        css_parts.append(_wrap_vars(".dark", dark_theme))
        css_parts.append(_wrap_vars("[data-theme='dark']", dark_theme))
        theme_name = f"{light_theme}/{dark_theme}"
        mode = "light/dark auto-switching"
    else:
        selected = dark_theme or theme
        css_parts.append(_wrap_vars(":root", selected))
        theme_name = selected
        mode = "dark only"

    (css_dir / "starlighter.css").write_text("\n\n".join(css_parts) + "\n")
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


def _setup_css_imports(config, css_imports: list[str]) -> None:
    input_css = config.css_dir_absolute / "input.css"
    if not input_css.exists():
        return

    content = input_css.read_text()
    new_imports = [imp for imp in css_imports if imp not in content]

    if new_imports:
        content = content.replace(
            '@import "tailwindcss";',
            f'@import "tailwindcss";\n{"\n".join(new_imports)}',
        )
        input_css.write_text(content)


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
        requested = {c.replace("-", "_") for c in components}

        def exists(n):
            return (component_dir / f"{n}.py").exists()

        conflicts = [n for n in resolved if n in requested and exists(n)]
        if conflicts and not force:
            warning("The following requested components already exist:")
            for name in conflicts:
                console.print(f"  • {component_dir / f'{name}.py'}")
            if not confirm("Overwrite?", default=False):
                raise typer.Exit(0)

        if not force:
            resolved = {
                n: src for n, src in resolved.items() if n in requested or not exists(n)
            }

        packages = {
            pkg
            for name in resolved
            if (metadata := get_component_metadata(name))
            for pkg in metadata.packages
        }

        css_imports = [
            css_import
            for name in resolved
            if (metadata := get_component_metadata(name))
            for css_import in metadata.css_imports
        ]

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

        if css_imports:
            _setup_css_imports(config, css_imports)

        with status_context("Installing components..."):
            component_dir.mkdir(parents=True, exist_ok=True)
            (component_dir / "__init__.py").touch()

            for name, source in resolved.items():
                (component_dir / f"{name}.py").write_text(source)

        if resolved:
            success(f"Installed components: {', '.join(resolved.keys())}")
        else:
            info("All components already installed (dependencies unchanged)")

        if verbose:
            info(f"Location: {component_dir}")

        first = (list(resolved) or list(requested))[0].title().replace("_", "")
        console.print(f"\n💡 Next steps:\n  • Import: from starui import {first}")

    except Exception as e:
        error(f"Installation failed: {e}")
        raise typer.Exit(1) from e
