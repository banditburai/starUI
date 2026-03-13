import re
from pathlib import Path
from typing import TYPE_CHECKING

import typer
from rich.console import Console
from rich.status import Status

from ..registry.checksum import compute_checksum
from ..registry.manifest import ItemKind

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


def rewrite_block_imports(source: str) -> str:
    """Convert absolute ``from components.`` imports to relative."""
    return re.sub(r"^from components\.", "from .", source, flags=re.MULTILINE)


def install_item(
    name: str,
    source: str,
    *,
    kind: ItemKind = "component",
    install_name: str | None = None,
    config: "ProjectConfig",
    client: "RegistryClient",
    manifest: "Manifest",
) -> None:
    effective_name = install_name or name
    if kind == "block":
        source = rewrite_block_imports(source)
    file_path = config.component_dir_absolute / f"{effective_name}.py"
    file_path.write_text(source)
    checksum = compute_checksum(file_path)
    try:
        manifest.record_install(
            name,
            version=client.version,
            checksum=checksum,
            file_path=str(file_path.relative_to(config.project_root)),
            kind=kind,
        )
    except Exception as e:
        warning(f"Failed to record {name} in manifest: {e}")


def find_block_by_install_name(name: str, installed_blocks: dict[str, dict]) -> str | None:
    return next(
        (bn for bn, rec in installed_blocks.items() if Path(rec.get("file", "")).stem == name),
        None,
    )


MSG_NO_MANIFEST = "No manifest found. Run 'star init' or 'star add' first."
MSG_NO_COMPONENTS = "No components installed."
