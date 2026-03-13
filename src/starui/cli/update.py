import typer

from starui.config import get_project_config
from starui.registry.client import RegistryClient
from starui.registry.manifest import Manifest

from .utils import (
    MSG_NO_COMPONENTS,
    MSG_NO_MANIFEST,
    error,
    find_block_by_install_name,
    info,
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
        installed_blocks = manifest.get_installed_blocks()

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

        updated = []
        skipped = []

        for name in comp_targets:
            try:
                remote_meta = client.get_component_metadata(name)
            except FileNotFoundError:
                if verbose:
                    info(f"{name}: not in registry, skipping")
                continue

            remote_checksum = remote_meta.get("checksum", "")
            local_checksum = installed[name].get("checksum", "")
            if remote_checksum == local_checksum:
                if verbose:
                    info(f"{name}: already up to date")
                continue

            if manifest.is_modified(name, component_dir) and not force:
                warning(f"{name}: locally modified, skipping (use --force to overwrite)")
                skipped.append(name)
                continue

            source = client.get_component_source(name)
            file_path = component_dir / f"{name}.py"
            file_path.write_text(source)

            manifest.record_install(
                name,
                version=client.version,
                checksum=remote_checksum,
                file_path=str(file_path.relative_to(config.project_root)),
            )

            updated.append(name)

        for name in block_targets:
            try:
                remote_meta = client.get_block_metadata(name)
            except FileNotFoundError:
                if verbose:
                    info(f"{name}: not in registry, skipping")
                continue

            remote_checksum = remote_meta.get("checksum", "")
            local_checksum = installed_blocks[name].get("checksum", "")
            if remote_checksum == local_checksum:
                if verbose:
                    info(f"{name}: already up to date")
                continue

            install_name = remote_meta.get("install_name", name)
            if manifest.is_block_modified(name, component_dir) and not force:
                warning(f"{name}: locally modified, skipping (use --force to overwrite)")
                skipped.append(name)
                continue

            source = client.get_block_source(name)
            file_path = component_dir / f"{install_name}.py"
            file_path.write_text(source)

            manifest.record_block_install(
                name,
                version=client.version,
                checksum=remote_checksum,
                file_path=str(file_path.relative_to(config.project_root)),
            )

            updated.append(name)

            # Ensure block's component deps are installed
            try:
                for dep_name in client.resolve_block_dependencies(name):
                    dep_file = component_dir / f"{dep_name}.py"
                    if not dep_file.exists():
                        dep_source = client.get_component_source(dep_name)
                        dep_file.write_text(dep_source)
                        dep_meta = client.get_component_metadata(dep_name)
                        manifest.record_install(
                            dep_name,
                            version=client.version,
                            checksum=dep_meta.get("checksum", ""),
                            file_path=str(dep_file.relative_to(config.project_root)),
                        )
                        updated.append(dep_name)
            except Exception:
                pass

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
