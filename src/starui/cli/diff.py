import difflib

import typer

from starui.config import get_project_config
from starui.registry.client import RegistryClient
from starui.registry.manifest import Manifest

from .utils import console, error, info


def diff_command(
    component: str = typer.Argument(..., help="Component to diff"),
) -> None:
    """Show diff between local component and registry version."""
    try:
        config = get_project_config()
        manifest = Manifest(config.project_root)
        component_name = component.replace("-", "_")

        local_file = config.component_dir_absolute / f"{component_name}.py"
        if not local_file.exists():
            error(f"Component '{component_name}' not found locally")
            raise typer.Exit(1)

        client = RegistryClient(version=manifest.registry_version)
        try:
            registry_source = client.get_component_source(component_name)
        except FileNotFoundError:
            error(f"Component '{component_name}' not found in registry")
            raise typer.Exit(1) from None

        local_source = local_file.read_text()

        if local_source == registry_source:
            info(f"{component_name}: no differences")
            return

        diff = difflib.unified_diff(
            registry_source.splitlines(keepends=True),
            local_source.splitlines(keepends=True),
            fromfile=f"registry/{component_name}.py",
            tofile=f"local/{component_name}.py",
        )

        console.print("".join(diff), highlight=False)

    except typer.Exit:
        raise
    except Exception as e:
        error(f"Failed to diff component: {e}")
        raise typer.Exit(1) from e
