import difflib

import typer

from ..config import get_project_config
from ..registry.client import RegistryClient
from ..registry.manifest import Manifest
from .utils import (
    console,
    error,
    find_block_by_install_name,
    info,
    resolve_local_path,
    rewrite_block_imports,
)


def diff_command(
    component: str = typer.Argument(..., help="Component or block to diff"),
) -> None:
    """Show diff between local component/block and registry version."""
    try:
        config = get_project_config()
        manifest = Manifest(config.project_root)
        normalized = component.replace("-", "_")
        client = RegistryClient(version=manifest.registry_version)

        installed_comps = manifest.get_installed()
        installed_blocks = manifest.get_installed(kind="block")

        record = None
        label = normalized
        kind = "component"

        if normalized in installed_comps:
            record = installed_comps[normalized]
        elif normalized in installed_blocks:
            record = installed_blocks[normalized]
            kind = "block"
        elif match := find_block_by_install_name(normalized, installed_blocks):
            record, label, kind = installed_blocks[match], match, "block"
        else:
            error(f"'{normalized}' is not installed (use 'star add {component}' first)")
            raise typer.Exit(1)

        local_file = resolve_local_path(
            record, normalized, manifest=manifest, component_dir=config.component_dir_absolute
        )

        if not local_file.exists():
            error(f"'{normalized}' is installed but the file is missing: {local_file}")
            raise typer.Exit(1)

        try:
            registry_source = client.get_source(label, kind=kind)
            if kind == "block":
                registry_source = rewrite_block_imports(registry_source)
        except FileNotFoundError:
            error(f"'{label}' not found in registry")
            raise typer.Exit(1) from None

        local_source = local_file.read_text()

        if local_source == registry_source:
            info(f"{label}: no differences")
            return

        diff = difflib.unified_diff(
            registry_source.splitlines(keepends=True),
            local_source.splitlines(keepends=True),
            fromfile=f"registry/{label}.py",
            tofile=f"local/{label}.py",
        )

        console.print("".join(diff), highlight=False)

    except typer.Exit:
        raise
    except Exception as e:
        error(f"Failed to diff: {e}")
        raise typer.Exit(1) from e
