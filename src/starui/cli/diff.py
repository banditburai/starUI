import difflib

import typer

from starui.config import get_project_config
from starui.registry.client import RegistryClient
from starui.registry.manifest import Manifest

from .utils import console, error, find_block_by_install_name, info


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
        installed_blocks = manifest.get_installed_blocks()

        record = None
        label = normalized
        is_block = False

        if normalized in installed_comps:
            record = installed_comps[normalized]
        elif normalized in installed_blocks:
            record = installed_blocks[normalized]
            is_block = True
        else:
            if match := find_block_by_install_name(normalized, installed_blocks):
                record, label, is_block = installed_blocks[match], match, True

        if record:
            recorded_file = record.get("file")
            local_file = (
                (manifest.project_root / recorded_file)
                if recorded_file
                else (config.component_dir_absolute / f"{normalized}.py")
            )
        else:
            local_file = config.component_dir_absolute / f"{normalized}.py"

        if not local_file.exists():
            error(f"'{normalized}' not found locally (not installed as component or block)")
            raise typer.Exit(1)

        try:
            registry_source = client.get_block_source(label) if is_block else client.get_component_source(label)
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
