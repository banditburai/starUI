from pathlib import Path

import typer
from rich.progress import track

from ..config import ProjectConfig, detect_project_config
from ..registry.client import RegistryClient
from ..registry.manifest import Manifest
from ..templates import generate_app_starter, generate_css_input
from .utils import confirm, console, error, info, install_component


def validate_project(root: Path, force: bool = False) -> None:
    conflicts = []

    if (root / "starui.py").exists():
        conflicts.append("starui.py configuration file")

    for comp_dir in ["components/ui", "ui"]:
        path = root / comp_dir
        if path.exists() and any(path.iterdir()):
            conflicts.append(f"{comp_dir} directory with content")
            break

    if conflicts and not force:
        error("Project appears to already be initialized. Found:\n" + "\n".join(f"  • {item}" for item in conflicts))
        info("Use --force to reinitialize anyway")
        raise typer.Exit(1)


def setup_directories(config: ProjectConfig, verbose: bool = False) -> None:
    dirs = [
        config.component_dir_absolute,
        config.css_output_absolute.parent,
        config.project_root / "static" / "css",
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
    input_path = config.project_root / "static" / "css" / "input.css"
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
        "\n# StarUI generated files",
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
        gitignore.write_text(content + "\n".join(gitignore_lines))
        if verbose:
            console.print(f"[green]{'Updated' if content else 'Created'}:[/green] .gitignore")
    elif verbose:
        console.print("[yellow]Skipped:[/yellow] .gitignore (StarUI patterns exist)")


def create_config_file(config: ProjectConfig, verbose: bool = False) -> None:
    config_path = config.project_root / "starui.py"

    if config_path.exists():
        if verbose:
            console.print("[yellow]Skipped:[/yellow] starui.py (already exists)")
        return

    config_path.write_text(f'''"""StarUI configuration."""

from pathlib import Path

CSS_OUTPUT = Path("{config.css_output}")
COMPONENT_DIR = Path("{config.component_dir}")
''')

    if verbose:
        console.print("[green]Created:[/green] starui.py")


def init_command(
    force: bool = typer.Option(False, "--force", help="Force initialization"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show details"),
    config: bool = typer.Option(False, "--config", help="Create starui.py"),
) -> None:
    """Initialize a new StarUI project."""
    try:
        root = Path.cwd()

        if verbose:
            console.print(f"[blue]Initializing StarUI in:[/blue] {root}")

        project_config = detect_project_config(root)

        if verbose:
            console.print(f"[dim]CSS output:[/dim] {project_config.css_output}")
            console.print(f"[dim]Components:[/dim] {project_config.component_dir}")

        validate_project(root, force)

        if not force and project_config.css_output_absolute.exists():
            console.print(f"\n[yellow]Will overwrite:[/yellow]\n  • {project_config.css_output}")
            if not confirm("\nProceed?", default=True):
                info("Cancelled")
                raise typer.Exit()

        console.print("\n[green]✨ Initializing StarUI...[/green]")

        def setup_and_update_config():
            nonlocal project_config
            setup_directories(project_config, verbose)
            # Re-detect config after directories are created
            project_config = detect_project_config(root)

        steps = [
            (
                "Creating directories",
                setup_and_update_config,
            ),
            ("Creating CSS input", lambda: create_css_input(project_config, verbose)),
            (
                "Adding default components",
                lambda: add_default_components(project_config, verbose),
            ),
            ("Creating starter app", lambda: create_app(project_config, verbose)),
            ("Updating .gitignore", lambda: update_gitignore(project_config, verbose)),
        ]

        if config:
            steps.append(("Creating config", lambda: create_config_file(project_config, verbose)))

        if verbose:
            for name, func in steps:
                console.print(f"[blue]{name}...[/blue]")
                func()
        else:
            for _, func in track(steps, description="Initializing..."):
                func()

        console.print("\n[green]🎉 StarUI initialized![/green]")
        console.print("\n[bold]Next steps:[/bold]")
        console.print("  1. Run [blue]star dev[/blue] to start development")
        console.print("  2. Run [blue]star add[/blue] to add components")
        console.print("  3. Run [blue]star build[/blue] for production CSS")

        if not config:
            console.print("\n[dim]💡 Use [blue]star init --config[/blue] for config file[/dim]")

    except typer.Exit:
        raise
    except Exception as e:
        error(f"Initialization failed: {e}")
        raise typer.Exit(1) from e
