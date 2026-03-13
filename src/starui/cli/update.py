import typer

from ..config import get_project_config
from ..registry.client import RegistryClient
from ..registry.manifest import ItemKind, Manifest
from .utils import (
    MSG_NO_COMPONENTS,
    MSG_NO_MANIFEST,
    error,
    find_block_by_install_name,
    info,
    install_item,
    success,
    warning,
)


def update_command(
    components: list[str] = typer.Argument(None, help="Components/blocks to update (all if omitted)"),
    force: bool = typer.Option(False, "--force", help="Overwrite locally modified files"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show details"),
) -> None:
    """Update installed components and blocks to latest registry versions."""
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

        if components:
            targets = [c.replace("-", "_") for c in components]
            comp_targets = [t for t in targets if t in installed]
            block_targets = [t for t in targets if t in installed_blocks]
            unknown = [t for t in targets if t not in installed and t not in installed_blocks]
            still_unknown = []
            for t in unknown:
                if match := find_block_by_install_name(t, installed_blocks):
                    block_targets.append(match)
                else:
                    still_unknown.append(t)
            if still_unknown:
                error(f"Not installed: {', '.join(still_unknown)}")
                raise typer.Exit(1)
        else:
            comp_targets = list(installed)
            block_targets = list(installed_blocks)

        client = RegistryClient(version=manifest.registry_version)
        component_dir = config.component_dir_absolute

        updated: list[str] = []
        skipped: list[str] = []

        all_targets: list[tuple[str, ItemKind]] = [
            *((n, "component") for n in comp_targets),
            *((n, "block") for n in block_targets),
        ]

        for name, kind in all_targets:
            items = installed_blocks if kind == "block" else installed

            try:
                remote_meta = client.get_metadata(name, kind=kind)
            except FileNotFoundError:
                if verbose:
                    info(f"{name}: not in registry, skipping")
                continue

            remote_checksum = remote_meta.get("checksum", "")
            local_checksum = items[name].get("checksum", "")
            if remote_checksum == local_checksum:
                if verbose:
                    info(f"{name}: already up to date")
                continue

            if manifest.is_modified(name, component_dir, kind=kind) and not force:
                warning(f"{name}: locally modified, skipping (use --force to overwrite)")
                skipped.append(name)
                continue

            source = client.get_source(name, kind=kind)
            iname = remote_meta.get("install_name") if kind == "block" else None
            install_item(name, source, kind=kind, install_name=iname, config=config, client=client, manifest=manifest)
            updated.append(name)

            if kind == "block":
                try:
                    for dep_name in client.resolve_dependencies(name, kind="block"):
                        if not (component_dir / f"{dep_name}.py").exists():
                            dep_source = client.get_source(dep_name)
                            install_item(dep_name, dep_source, config=config, client=client, manifest=manifest)
                            updated.append(dep_name)
                except Exception as e:
                    warning(f"Could not install dependency for {name}: {e}")

        if updated:
            manifest.save()
            success(f"Updated {len(updated)} item(s): {', '.join(updated)}")
        elif skipped:
            warning(f"Skipped {len(skipped)} modified item(s)")
        else:
            info("Everything is up to date")

    except typer.Exit:
        raise
    except Exception as e:
        error(f"Update failed: {e}")
        raise typer.Exit(1) from e
