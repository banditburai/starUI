import typer
from rich.table import Table
from rich.text import Text

from starui.config import get_project_config
from starui.registry.client import RegistryClient
from starui.registry.manifest import Manifest

from .utils import MSG_NO_COMPONENTS, MSG_NO_MANIFEST, console, error, info


def status_command() -> None:
    """Show status of installed components."""
    try:
        config = get_project_config()
        manifest = Manifest(config.project_root)

        if not manifest.exists():
            info(MSG_NO_MANIFEST)
            return

        installed = manifest.get_installed()
        if not installed:
            info(MSG_NO_COMPONENTS)
            return

        try:
            client = RegistryClient(version=manifest.registry_version)
            client.list_components()
        except Exception:
            client = None
            info("Could not fetch remote registry; showing local status only")

        component_dir = config.component_dir_absolute

        table = Table(title="Installed Components", show_header=True, header_style="bold blue")
        table.add_column("Component", style="cyan")
        table.add_column("Status", justify="center", min_width=10)
        table.add_column("Version", style="dim")

        modified_count = 0
        update_count = 0

        for name, record in sorted(installed.items()):
            local_file = component_dir / f"{name}.py"
            version = record.get("version", "unknown")

            if not local_file.exists():
                status = Text("Missing", style="red")
            elif manifest.is_modified(name, component_dir):
                status = Text("Modified", style="yellow")
                modified_count += 1
            elif client:
                try:
                    remote_meta = client.get_component_metadata(name)
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

        summary_parts = [f"{len(installed)} installed"]
        if modified_count:
            summary_parts.append(f"{modified_count} modified")
        if update_count:
            summary_parts.append(f"{update_count} updates available")
        console.print(f"\n[dim]{', '.join(summary_parts)}[/dim]")

        if update_count:
            console.print("\n[dim]Run 'star update' to pull latest versions[/dim]")

    except Exception as e:
        error(f"Failed to check status: {e}")
        raise typer.Exit(1) from e
