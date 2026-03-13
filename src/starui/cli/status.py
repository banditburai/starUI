from pathlib import Path

import typer
from rich.table import Table
from rich.text import Text

from ..config import get_project_config
from ..registry.client import RegistryClient
from ..registry.manifest import ItemKind, Manifest
from .utils import MSG_NO_COMPONENTS, MSG_NO_MANIFEST, console, error, info, resolve_local_path


def _render_status_table(
    items: dict[str, dict],
    title: str,
    manifest: "Manifest",
    client: "RegistryClient | None",
    component_dir: Path,
    kind: ItemKind = "component",
) -> tuple[int, int]:
    table = Table(title=title, show_header=True, header_style="bold blue")
    table.add_column("Block" if kind == "block" else "Name", style="cyan")
    table.add_column("Status", justify="center", min_width=10)
    table.add_column("Version", style="dim")

    modified_count = 0
    update_count = 0

    for name, record in sorted(items.items()):
        local_file = resolve_local_path(record, name, manifest=manifest, component_dir=component_dir)
        version = record.get("version", "unknown")

        if not local_file.exists():
            status = Text("Missing", style="red")
        elif manifest.is_modified(name, component_dir, kind=kind):
            status = Text("Modified", style="yellow")
            modified_count += 1
        elif client:
            try:
                remote_meta = client.get_metadata(name, kind=kind)
                remote_checksum = remote_meta.get("checksum", "")
            except FileNotFoundError:
                remote_checksum = ""
            if remote_checksum and remote_checksum != record.get("checksum", ""):
                status = Text("Update available", style="magenta")
                update_count += 1
            else:
                status = Text("Up to date", style="green")
        else:
            status = Text("Installed", style="dim")

        table.add_row(name, status, version)

    console.print(table)
    return modified_count, update_count


def status_command() -> None:
    """Show status of installed components and blocks."""
    try:
        config = get_project_config()
        manifest = Manifest(config.project_root)

        if not manifest.exists():
            info(MSG_NO_MANIFEST)
            return

        installed = manifest.get_installed()
        installed_blocks = manifest.get_installed(kind="block")

        if not installed and not installed_blocks:
            info(MSG_NO_COMPONENTS)
            return

        try:
            client = RegistryClient(version=manifest.registry_version)
            client.list_items("component")
        except Exception:
            client = None
            info("Could not fetch remote registry; showing local status only")

        component_dir = config.component_dir_absolute

        total_modified = 0
        total_updates = 0

        if installed:
            m, u = _render_status_table(installed, "Installed Components", manifest, client, component_dir)
            total_modified += m
            total_updates += u

        if installed_blocks:
            m, u = _render_status_table(
                installed_blocks, "Installed Blocks", manifest, client, component_dir, kind="block"
            )
            total_modified += m
            total_updates += u

        total = len(installed) + len(installed_blocks)
        summary_parts = [f"{total} installed"]
        if total_modified:
            summary_parts.append(f"{total_modified} modified")
        if total_updates:
            summary_parts.append(f"{total_updates} updates available")
        console.print(f"\n[dim]{', '.join(summary_parts)}[/dim]")

        if total_updates:
            console.print("\n[dim]Run 'star update' to pull latest versions[/dim]")

    except typer.Exit:
        raise
    except Exception as e:
        error(f"Failed to check status: {e}")
        raise typer.Exit(1) from e
