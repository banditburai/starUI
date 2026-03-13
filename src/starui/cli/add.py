import subprocess

import typer

from ..config import ProjectConfig, get_project_config
from ..registry.client import RegistryClient
from ..registry.manifest import Manifest
from .utils import (
    confirm,
    console,
    error,
    info,
    install_item,
    status_context,
    success,
    validate_component_name,
    warning,
)


def _build_token_rules(theme_keys: dict[str, str]) -> str:
    lines = ['[data-slot="code-block"]::-webkit-scrollbar { height: 8px; width: 8px; }']
    for suffix, extra in [
        ("track", ""),
        ("thumb", " border-radius: 4px;"),
        ("thumb-hover", ""),
    ]:
        prop = f"--scrollbar-{suffix}"
        if prop in theme_keys:
            lines.append(f'[data-slot="code-block"]::-webkit-scrollbar-{suffix} {{ background: var({prop});{extra} }}')

    for key in theme_keys:
        if not key.startswith("--token-"):
            continue
        cls_name = key.removeprefix("--")
        extra = " font-style: italic;" if key == "--token-comment" else ""
        lines.append(f".{cls_name} {{ color: var({key});{extra} }}")

    return "\n".join(lines)


def _setup_code_highlighting(config: ProjectConfig, theme: str | None) -> None:
    try:
        from starlighter import THEMES
    except ImportError:
        warning("Starlighter not installed. This should have been installed automatically. Try: uv add starlighter")
        return

    css_dir = config.css_dir_absolute
    input_css = css_dir / "input.css"

    if theme is None:
        console.print("\n[bold]Select a syntax highlighting theme:[/bold]")
        themes = [
            (
                "github-light",
                "github-dark",
                "GitHub (light/dark auto-switching) [default]",
            ),
            ("monokai", None, "Monokai (dark only)"),
            ("dracula", None, "Dracula (dark only)"),
        ]
        for i, (_, _, desc) in enumerate(themes, 1):
            console.print(f"{i}. {desc}")

        try:
            choice = int(typer.prompt("Enter choice (1-3)", default="1")) - 1
        except ValueError:
            choice = 0
        choice = max(0, min(choice, len(themes) - 1))
        light_theme, dark_theme, _ = themes[choice]
    else:
        light_theme, dark_theme = None, theme

    def _wrap_vars(selector: str, theme_name: str) -> str:
        rules = "\n    ".join(f"{k}: {v};" for k, v in THEMES[theme_name].items())
        return f"{selector} {{\n    {rules}\n}}"

    ref_theme = THEMES.get(dark_theme or light_theme, {})
    css_parts = [_build_token_rules(ref_theme)]

    if light_theme and dark_theme:
        css_parts.append(_wrap_vars(":root", light_theme))
        css_parts.append(_wrap_vars(".dark", dark_theme))
        css_parts.append(_wrap_vars("[data-theme='dark']", dark_theme))
        theme_name = f"{light_theme}/{dark_theme}"
        mode = "light/dark auto-switching"
    else:
        css_parts.append(_wrap_vars(":root", dark_theme))
        theme_name = dark_theme
        mode = "dark only"

    (css_dir / "starlighter.css").write_text("\n\n".join(css_parts) + "\n")
    success(f"Generated starlighter.css with {theme_name} theme ({mode})")

    if input_css.exists():
        content = input_css.read_text()
        if "@import './starlighter.css'" not in content:
            lines = content.split("\n")
            idx = next(
                (i + 1 for i, line in enumerate(lines) if '@import "tailwindcss"' in line),
                1,
            )
            lines.insert(idx, "@import './starlighter.css';")
            input_css.write_text("\n".join(lines))
            info("Added starlighter.css import to input.css")

    info("Run 'star build css' to rebuild your styles")


def _setup_css_imports(config: ProjectConfig, css_imports: list[str]) -> None:
    input_css = config.css_dir_absolute / "input.css"
    if not input_css.exists():
        return

    content = input_css.read_text()
    new_imports = [imp for imp in css_imports if imp not in content]

    if new_imports:
        content = content.replace(
            '@import "tailwindcss";',
            f'@import "tailwindcss";\n{"\n".join(new_imports)}',
        )
        input_css.write_text(content)


def _install_packages(packages: set[str]) -> None:
    for package in packages:
        info(f"Installing package: {package}")
        try:
            subprocess.run(
                ["uv", "add", package],
                check=True,
                capture_output=True,
                text=True,
            )
            success(f"Installed: {package}")
        except subprocess.CalledProcessError as e:
            warning(f"Failed to install {package}: {e.stderr}")


def add_command(
    components: list[str] = typer.Argument(..., help="Components or blocks to add"),
    force: bool = typer.Option(False, "--force", help="Overwrite existing files"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show details"),
    theme: str = typer.Option(None, "--theme", help="Theme for code highlighting"),
    component_dir: str | None = typer.Option(None, "--component-dir", help="Component install directory"),
) -> None:
    """Add components and blocks to your project."""

    if invalid := [c for c in components if not validate_component_name(c)]:
        error(f"Invalid component names: {', '.join(invalid)}")
        raise typer.Exit(1)

    try:
        config = get_project_config(component_dir=component_dir)
        manifest = Manifest(config.project_root)
        client = RegistryClient(version=manifest.registry_version)
    except Exception as e:
        error(f"Initialization failed: {e}")
        raise typer.Exit(1) from e

    try:
        comp_deps: dict[str, str] = {}
        blocks_to_install: dict[str, tuple[str, str]] = {}

        for name in components:
            normalized = name.replace("-", "_")
            if verbose:
                info(f"Resolving {name} -> {normalized}...")

            try:
                kind, entry = client.lookup(normalized)
            except FileNotFoundError:
                error(f"'{name}' not found in registry")
                raise typer.Exit(1) from None

            if kind == "component":
                deps, item_source = client.get_with_dependencies(normalized)
                comp_deps.update(deps)
                comp_deps[normalized] = item_source
            else:
                registry_name = entry["name"]
                deps, block_source = client.get_with_dependencies(registry_name, kind="block")
                comp_deps.update(deps)
                install_name = entry.get("install_name", registry_name)
                blocks_to_install[registry_name] = (install_name, block_source)

        comp_dir = config.component_dir_absolute
        requested = {c.replace("-", "_") for c in components}

        conflicts = [n for n in comp_deps if n in requested and (comp_dir / f"{n}.py").exists()]
        conflicts += [
            inst
            for rn, (inst, _) in blocks_to_install.items()
            if (rn in requested or inst in requested) and (comp_dir / f"{inst}.py").exists()
        ]

        if conflicts and not force:
            warning("The following requested items already exist:")
            for name in conflicts:
                console.print(f"  • {comp_dir / f'{name}.py'}")
            if not confirm("Overwrite?", default=False):
                raise typer.Exit(0)

        if not force:
            comp_deps = {
                n: src for n, src in comp_deps.items() if n in requested or not (comp_dir / f"{n}.py").exists()
            }
            blocks_to_install = {
                rn: (inst, src)
                for rn, (inst, src) in blocks_to_install.items()
                if rn in requested or inst in requested or not (comp_dir / f"{inst}.py").exists()
            }

        packages: set[str] = set()
        css_imports: list[str] = []
        for name, kind in [*((n, "component") for n in comp_deps), *((n, "block") for n in blocks_to_install)]:
            try:
                meta = client.get_metadata(name, kind=kind)
                packages.update(meta.get("packages", []))
                css_imports.extend(meta.get("css_imports", []))
            except FileNotFoundError:
                pass

        _install_packages(packages)

        if "code_block" in comp_deps:
            _setup_code_highlighting(config, theme)

        if css_imports:
            _setup_css_imports(config, list(dict.fromkeys(css_imports)))

        with status_context("Installing..."):
            comp_dir.mkdir(parents=True, exist_ok=True)
            (comp_dir / "__init__.py").touch()

            for name, source in comp_deps.items():
                install_item(name, source, config=config, client=client, manifest=manifest)

            for reg_name, (inst_name, source) in blocks_to_install.items():
                install_item(
                    reg_name,
                    source,
                    kind="block",
                    install_name=inst_name,
                    config=config,
                    client=client,
                    manifest=manifest,
                )

            manifest.save()

        installed_names = list(comp_deps.keys()) + [inst for inst, _ in blocks_to_install.values()]
        if installed_names:
            success(f"Installed: {', '.join(installed_names)}")
        else:
            info("All items already installed (dependencies unchanged)")

        if verbose:
            info(f"Location: {comp_dir}")

        if first_name := next(iter(comp_deps or requested), None):
            class_name = first_name.title().replace("_", "")
            import_path = str(config.component_dir).replace("/", ".").replace("\\", ".")
            console.print(f"\n  Next steps:\n  • Import: from {import_path}.{first_name} import {class_name}")

    except typer.Exit:
        raise
    except Exception as e:
        error(f"Installation failed: {e}")
        raise typer.Exit(1) from e
