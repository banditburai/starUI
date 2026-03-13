from pathlib import Path

import typer
from rich.table import Table
from rich.text import Text

from starui.config import get_project_config
from starui.registry.client import RegistryClient
from starui.registry.manifest import Manifest

from .utils import MSG_NO_COMPONENTS, MSG_NO_MANIFEST, console, error, info


def _render_status_table(
    items: dict[str, dict],
    title: str,
    manifest: "Manifest",
    client: "RegistryClient | None",
    component_dir: Path,
    is_block: bool = False,
) -> tuple[int, int]:
    """Returns (modified_count, update_count)."""
    table = Table(title=title, show_header=True, header_style="bold blue")
    table.add_column("Block" if is_block else "Name", style="cyan")
    table.add_column("Status", justify="center", min_width=10)
    table.add_column("Version", style="dim")

    modified_count = 0
    update_count = 0

    is_modified = manifest.is_block_modified if is_block else manifest.is_modified
    get_meta = (client.get_block_metadata if is_block else client.get_component_metadata) if client else None

    for name, record in sorted(items.items()):
        recorded_file = record.get("file")
        local_file = manifest.project_root / recorded_file if recorded_file else component_dir / f"{name}.py"
        version = record.get("version", "unknown")

        if not local_file.exists():
            status = Text("Missing", style="red")
        elif is_modified(name, component_dir):
            status = Text("Modified", style="yellow")
            modified_count += 1
        elif client:
            try:
                remote_meta = get_meta(name)
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
        installed_blocks = manifest.get_installed_blocks()

        if not installed and not installed_blocks:
            info(MSG_NO_COMPONENTS)
            return

        try:
            client = RegistryClient(version=manifest.registry_version)
            client.list_components()
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
                installed_blocks, "Installed Blocks", manifest, client, component_dir, is_block=True
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
