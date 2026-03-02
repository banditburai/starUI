import re
from typing import TYPE_CHECKING

import typer
from rich.console import Console
from rich.status import Status

if TYPE_CHECKING:
    from ..config import ProjectConfig
    from ..registry.client import RegistryClient
    from ..registry.manifest import Manifest

console = Console()


def success(message: str) -> None:
    console.print(f"[green]✓[/green] {message}")


def error(message: str) -> None:
    console.print(f"[red]❌ Error:[/red] {message}")


def warning(message: str) -> None:
    console.print(f"[yellow]⚠ Warning:[/yellow] {message}")


def info(message: str) -> None:
    console.print(f"[blue]ℹ Info:[/blue] {message}")


def confirm(message: str, default: bool = False) -> bool:
    return typer.confirm(message, default=default)


def validate_component_name(name: str) -> bool:
    return bool(name and re.match(r"^[a-z][a-z0-9_-]*$", name))


def status_context(message: str) -> Status:
    return console.status(message)


def install_component(
    name: str,
    source: str,
    *,
    config: "ProjectConfig",
    client: "RegistryClient",
    manifest: "Manifest",
) -> None:
    file_path = config.component_dir_absolute / f"{name}.py"
    file_path.write_text(source)
    try:
        meta = client.get_component_metadata(name)
        manifest.record_install(
            name,
            version=client.version,
            checksum=meta.get("checksum", ""),
            file_path=str(file_path.relative_to(config.project_root)),
        )
    except FileNotFoundError:
        pass  # Manifest recording is best-effort; component is usable without it


MSG_NO_MANIFEST = "No manifest found. Run 'star init' or 'star add' first."
MSG_NO_COMPONENTS = "No components installed."
