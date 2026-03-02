import typer

from starui.config import get_project_config
from starui.registry.client import RegistryClient
from starui.registry.manifest import Manifest

from .utils import MSG_NO_COMPONENTS, MSG_NO_MANIFEST, error, info, success, warning


def update_command(
    components: list[str] = typer.Argument(None, help="Components to update (all if omitted)"),
    force: bool = typer.Option(False, "--force", help="Overwrite locally modified components"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show details"),
) -> None:
    """Update installed components to latest registry versions."""
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

        if components:
            targets = [c.replace("-", "_") for c in components]
            unknown = [t for t in targets if t not in installed]
            if unknown:
                error(f"Not installed: {', '.join(unknown)}")
                raise typer.Exit(1)
        else:
            targets = list(installed.keys())

        client = RegistryClient(version=manifest.registry_version)
        component_dir = config.component_dir_absolute

        updated = []
        skipped = []

        for name in targets:
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

        if updated:
            manifest.save()
            success(f"Updated {len(updated)} component(s): {', '.join(updated)}")
        elif skipped:
            warning(f"Skipped {len(skipped)} modified component(s)")
        else:
            info("All components are up to date")

    except typer.Exit:
        raise
    except Exception as e:
        error(f"Update failed: {e}")
        raise typer.Exit(1) from e
