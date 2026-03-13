from typing import Any

import typer
from rich.table import Table
from rich.text import Text

from starui.config import get_project_config
from starui.registry.client import RegistryClient
from starui.registry.manifest import Manifest

from .utils import console, error, info


def _load_items(
    names: list[str],
    get_meta,
    installed_names: set[str],
    *,
    search: str | None = None,
    installed_only: bool = False,
) -> list[dict[str, Any]]:
    items = []
    for name in names:
        try:
            meta = get_meta(name)
            meta["installed"] = name in installed_names
            items.append(meta)
        except Exception as e:
            error(f"Failed to load {name}: {e}")

    if installed_only:
        items = [i for i in items if i["installed"]]
    if search:
        s = search.lower()
        items = [i for i in items if s in i["name"].lower() or s in i.get("description", "").lower()]
    return items


def _render_verbose(items: list[dict[str, Any]], title: str) -> None:
    console.print(f"[bold magenta]{title} (Detailed)[/bold magenta]\n")
    for i, item in enumerate(sorted(items, key=lambda x: x["name"])):
        if i > 0:
            console.print()

        is_installed = item.get("installed", False)
        icon = "[bold green]◉" if is_installed else "[bold cyan]○"
        status = "(installed)" if is_installed else "(available)"
        console.print(f"{icon} {item['name']}[/] [dim]{status}[/dim]")
        console.print(f"  {item.get('description', 'No description')}")

        if deps := item.get("dependencies", []):
            console.print(f"  [dim]Dependencies: {', '.join(deps)}[/dim]")


def _render_table(items: list[dict[str, Any]], title: str) -> None:
    table = Table(title=title, show_header=True, header_style="bold blue")
    table.add_column("Name", style="cyan")
    table.add_column("Status", justify="center", min_width=8)
    table.add_column("Description")
    table.add_column("Dependencies", style="dim")

    for item in sorted(items, key=lambda x: x["name"]):
        status = Text("✓ Installed", style="green") if item.get("installed") else Text("Available", style="yellow")
        desc = item.get("description", "")
        if len(desc) > 60:
            desc = desc[:57] + "..."

        deps = item.get("dependencies", [])
        deps_text = ", ".join(deps[:3])
        if len(deps) > 3:
            deps_text += f" +{len(deps) - 3}"
        elif not deps:
            deps_text = "None"

        table.add_row(item["name"], status, desc, deps_text)

    console.print(table)


def list_command(
    search: str | None = typer.Option(None, "--search", help="Search components"),
    installed: bool = typer.Option(False, "--installed", help="Show installed only"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show details"),
) -> None:
    """List available components and blocks."""
    try:
        installed_names: set[str] = set()
        installed_block_names: set[str] = set()
        try:
            config = get_project_config()
            manifest = Manifest(config.project_root)
            installed_names = set(manifest.get_installed())
            installed_block_names = set(manifest.get_installed_blocks())
        except Exception:
            pass

        client = RegistryClient()
        comp_names = client.list_components()
        block_names = client.list_blocks()

        components = _load_items(
            comp_names,
            client.get_component_metadata,
            installed_names,
            search=search,
            installed_only=installed,
        )
        blocks = _load_items(
            block_names,
            client.get_block_metadata,
            installed_block_names,
            search=search,
            installed_only=installed,
        )

        if not components and not blocks:
            info("No items match filters")
            return

        render = _render_verbose if verbose else _render_table
        if components:
            render(components, "Components")
        if blocks:
            if components:
                console.print()
            render(blocks, "Blocks")

        parts = [f"{len(components)} of {len(comp_names)} components"]
        if block_names:
            parts.append(f"{len(blocks)} of {len(block_names)} blocks")
        summary = f"\n[dim]Showing {', '.join(parts)}"
        installed_total = sum(1 for i in [*components, *blocks] if i.get("installed"))
        if installed_total:
            summary += f" ({installed_total} installed)"
        console.print(summary + "[/dim]")

    except typer.Exit:
        raise
    except Exception as e:
        error(f"Failed to list: {e}")
        raise typer.Exit(1) from e
