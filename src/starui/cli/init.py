from pathlib import Path

import typer
from rich.progress import track

from ..config import ProjectConfig, detect_component_dir, get_project_config, load_pyproject_config, save_config
from ..registry.client import RegistryClient
from ..registry.manifest import Manifest
from ..templates import generate_app_starter, generate_css_input
from .utils import confirm, console, error, info, install_component


def validate_project(root: Path, component_dir: str = "components/ui", force: bool = False) -> None:
    path = root / component_dir
    if path.exists() and any(path.iterdir()) and not force:
        error(f"Project appears to already be initialized. Found:\n  • {component_dir} directory with content")
        info("Use --force to reinitialize anyway")
        raise typer.Exit(1)


def setup_directories(config: ProjectConfig, verbose: bool = False) -> None:
    dirs = [
        config.component_dir_absolute,
        config.css_output_absolute.parent,
        config.css_dir_absolute,
    ]

    for dir_path in dirs:
        dir_path.mkdir(parents=True, exist_ok=True)
        if verbose:
            console.print(f"[green]Created:[/green] {dir_path.relative_to(config.project_root)}")

    component_init = config.component_dir_absolute / "__init__.py"
    if not component_init.exists():
        component_init.touch()
        if verbose:
            console.print(f"[green]Created:[/green] {component_init.relative_to(config.project_root)}")


def create_css_input(config: ProjectConfig, verbose: bool = False) -> None:
    input_path = config.css_dir_absolute / "input.css"
    input_path.write_text(generate_css_input(config))
    if verbose:
        console.print("[green]Created:[/green] input.css")


def add_default_components(config: ProjectConfig, verbose: bool = False) -> None:
    try:
        client = RegistryClient()
        manifest = Manifest(config.project_root)

        utils_source = client.get_component_source("utils")
        install_component("utils", utils_source, config=config, client=client, manifest=manifest)
        if verbose:
            console.print("[green]Added:[/green] utils.py")

        components = client.get_component_with_dependencies("theme_toggle")
        for name, source in components.items():
            install_component(name, source, config=config, client=client, manifest=manifest)
            if verbose:
                console.print(f"[green]Added component:[/green] {name}")

        manifest.save()
    except Exception as e:
        console.print(f"[yellow]Could not add default components:[/yellow] {e}")


def create_app(config: ProjectConfig, verbose: bool = False) -> None:
    app_path = config.project_root / "app.py"
    if app_path.exists():
        if verbose:
            console.print("[yellow]Skipped:[/yellow] app.py (already exists)")
        return

    app_path.write_text(generate_app_starter(config, include_theme_system=True))
    if verbose:
        console.print("[green]Created:[/green] app.py")


def update_gitignore(config: ProjectConfig, verbose: bool = False) -> None:
    gitignore = config.project_root / ".gitignore"
    gitignore_lines = [
        "# StarUI generated files",
        str(config.css_output),
        "*.css.map",
        "",
        "# StarUI cache",
        ".starui/",
        "",
    ]

    content = gitignore.read_text() if gitignore.exists() else ""

    if "# StarUI generated files" not in content:
        if content and not content.endswith("\n"):
            content += "\n"
        block = "\n".join(gitignore_lines)
        gitignore.write_text(content + ("\n" if content else "") + block)
        if verbose:
            console.print(f"[green]{'Updated' if content else 'Created'}:[/green] .gitignore")
    elif verbose:
        console.print("[yellow]Skipped:[/yellow] .gitignore (StarUI patterns exist)")


def resolve_component_dir(
    root: Path, component_dir: str | None, existing: ProjectConfig | None, no_interaction: bool
) -> str:
    if component_dir:
        return component_dir
    if existing:
        return str(existing.component_dir)

    default = str(detect_component_dir(root))
    if no_interaction:
        return default

    return typer.prompt("Where should components be installed?", default=default)


def init_command(
    force: bool = typer.Option(False, "--force", help="Force initialization"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show details"),
    component_dir: str | None = typer.Option(None, "--component-dir", help="Component install directory"),
    no_interaction: bool = typer.Option(False, "--no-interaction", help="Non-interactive mode for CI"),
) -> None:
    """Initialize a new StarUI project."""
    try:
        root = Path.cwd()

        if verbose:
            console.print(f"[blue]Initializing StarUI in:[/blue] {root}")

        existing = load_pyproject_config(root)
        chosen_dir = resolve_component_dir(root, component_dir, existing, no_interaction)

        validate_project(root, component_dir=chosen_dir, force=force)

        if existing:
            info(f"Using existing config (component_dir: {existing.component_dir})")
        else:
            save_config(root, chosen_dir)
            info("Wrote [tool.starui] config to pyproject.toml")

        project_config = get_project_config(root, component_dir=chosen_dir)

        if verbose:
            console.print(f"[dim]CSS output:[/dim] {project_config.css_output}")
            console.print(f"[dim]Components:[/dim] {project_config.component_dir}")

        if not force and project_config.css_output_absolute.exists():
            console.print(f"\n[yellow]Will overwrite:[/yellow]\n  • {project_config.css_output}")
            if not confirm("\nProceed?", default=True):
                info("Cancelled")
                raise typer.Exit()

        console.print("\n[green]Initializing StarUI...[/green]")

        steps = [
            ("Creating directories", lambda: setup_directories(project_config, verbose)),
            ("Creating CSS input", lambda: create_css_input(project_config, verbose)),
            ("Adding default components", lambda: add_default_components(project_config, verbose)),
            ("Creating starter app", lambda: create_app(project_config, verbose)),
            ("Updating .gitignore", lambda: update_gitignore(project_config, verbose)),
        ]

        if verbose:
            for name, func in steps:
                console.print(f"[blue]{name}...[/blue]")
                func()
        else:
            for _, func in track(steps, description="Initializing..."):
                func()

        console.print("\n[green]StarUI initialized![/green]")
        console.print("\n[bold]Next steps:[/bold]")
        console.print("  1. Run [blue]star dev[/blue] to start development")
        console.print("  2. Run [blue]star add[/blue] to add components")
        console.print("  3. Run [blue]star build[/blue] for production CSS")

    except typer.Exit:
        raise
    except Exception as e:
        error(f"Initialization failed: {e}")
        raise typer.Exit(1) from e
