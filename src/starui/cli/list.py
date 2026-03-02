from typing import Any

import typer
from rich.table import Table
from rich.text import Text

from starui.config import get_project_config
from starui.registry.client import RegistryClient
from starui.registry.manifest import Manifest

from .utils import console, error, info


def render_verbose(components: list[dict[str, Any]]) -> None:
    console.print("[bold magenta]Components (Detailed)[/bold magenta]\n")
    for i, comp in enumerate(sorted(components, key=lambda x: x["name"])):
        if i > 0:
            console.print()

        is_installed = comp.get("installed", False)
        icon = "[bold green]◉" if is_installed else "[bold cyan]○"
        status = "(installed)" if is_installed else "(available)"
        console.print(f"{icon} {comp['name']}[/] [dim]{status}[/dim]")
        console.print(f"  {comp.get('description', 'No description')}")

        if deps := comp.get("dependencies", []):
            console.print(f"  [dim]Dependencies: {', '.join(deps)}[/dim]")


def render_table(components: list[dict[str, Any]]) -> None:
    table = Table(title="Components", show_header=True, header_style="bold blue")
    table.add_column("Name", style="cyan")
    table.add_column("Status", justify="center", min_width=8)
    table.add_column("Description")
    table.add_column("Dependencies", style="dim")

    for comp in sorted(components, key=lambda x: x["name"]):
        status = Text("✓ Installed", style="green") if comp.get("installed") else Text("Available", style="yellow")
        desc = comp.get("description", "")
        if len(desc) > 60:
            desc = desc[:57] + "..."

        deps = comp.get("dependencies", [])
        deps_text = ", ".join(deps[:3])
        if len(deps) > 3:
            deps_text += f" +{len(deps) - 3}"
        elif not deps:
            deps_text = "None"

        table.add_row(comp["name"], status, desc, deps_text)

    console.print(table)


def list_command(
    search: str | None = typer.Option(None, "--search", help="Search components"),
    installed: bool = typer.Option(False, "--installed", help="Show installed only"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show details"),
) -> None:
    """List available components."""
    try:
        installed_names: set[str] = set()
        try:
            config = get_project_config()
            manifest = Manifest(config.project_root)
            installed_names = set(manifest.get_installed().keys())
        except Exception:
            pass

        client = RegistryClient()
        names = client.list_components()

        if not names:
            info("No components found")
            return

        components: list[dict[str, Any]] = []
        for name in names:
            try:
                meta = client.get_component_metadata(name)
                meta["installed"] = name in installed_names
                components.append(meta)
            except Exception as e:
                error(f"Failed to load {name}: {e}")

        if installed:
            components = [c for c in components if c["installed"]]

        if search:
            search = search.lower()
            components = [
                c for c in components if search in c["name"].lower() or search in c.get("description", "").lower()
            ]

        if not components:
            info("No components match filters")
            return

        if verbose:
            render_verbose(components)
        else:
            render_table(components)

        total = len(names)
        shown = len(components)
        installed_count = sum(1 for c in components if c.get("installed"))

        summary = f"\n[dim]Showing {shown} of {total} components"
        if installed_count:
            summary += f" ({installed_count} installed)"
        console.print(summary + "[/dim]")

    except Exception as e:
        error(f"Failed to list components: {e}")
        raise typer.Exit(1) from e
