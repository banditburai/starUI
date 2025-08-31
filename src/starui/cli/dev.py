"""Development server with hot reload and Tailwind CSS."""

import asyncio
import tempfile
import time
from contextlib import suppress
from pathlib import Path

import typer
from rich.panel import Panel
from rich.table import Table

from ..config import detect_project_config
from ..css.binary import TailwindBinaryManager
from ..dev.analyzer import resolve_port
from ..dev.process_manager import ProcessManager
from ..templates.css_input import generate_css_input
from .utils import console, error, success


def get_or_create_css_input(config) -> Path:
    if (existing := config.project_root / "static" / "css" / "input.css").exists():
        return existing

    css_dir = config.css_output_absolute.parent
    css_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".css", dir=css_dir, delete=False
    ) as tmp:
        tmp.write(generate_css_input(config))
        return Path(tmp.name)


def setup_tailwind(manager: ProcessManager, config, enable_hot_reload: bool = True):
    from ..dev.unified_reload import DevReloadHandler

    input_css = get_or_create_css_input(config)
    binary = Path(TailwindBinaryManager("latest").get_binary())

    async def notify(path: Path):
        with suppress(Exception):
            await DevReloadHandler.notify_css_update(path, time.time())

    manager.start_tailwind_watcher(
        binary,
        input_css,
        config.css_output_absolute,
        config.project_root,
        lambda p: asyncio.run(notify(p)) if enable_hot_reload else None,
    )
    return input_css


def wait_for_css(css_path: Path, timeout: int = 10):
    if css_path.exists():
        return success("CSS ready")

    console.print("[cyan]Building CSS...[/cyan]")

    deadline = time.time() + timeout
    while time.time() < deadline:
        if css_path.exists():
            return success("CSS built")
        time.sleep(0.5)

    error("CSS build timed out")
    raise typer.Exit(1)


def cleanup(*paths: Path):
    for path in filter(None, paths):
        path.unlink(missing_ok=True)


def show_status(config, port: int, hot_reload: bool, app_file: str):
    table = Table(title="StarUI Development Server", show_header=False)
    table.add_column(style="cyan")
    table.add_column(style="green")

    for label, value in [
        ("App", f"http://localhost:{port}"),
        ("File", app_file),
        ("CSS", str(config.css_output)),
        ("Hot Reload", f"✓ (Unified WebSocket on port {port})" if hot_reload else "✗"),
    ]:
        table.add_row(label, value)

    console.print(Panel(table, border_style="green"))


def dev_command(
    app_file: str = typer.Argument(..., help="StarHTML app file to run"),
    port: int = typer.Option(5000, "--port", "-p"),
    css_hot_reload: bool = typer.Option(True, "--css-hot/--no-css-hot"),
    strict: bool = typer.Option(False, "--strict"),
    debug: bool = typer.Option(True, "--debug/--no-debug"),
    verbose: bool = typer.Option(False, "--verbose", "-v"),
):
    """Start development server with hot reload."""

    app_path = Path(app_file)
    if not app_path.exists():
        error(f"App file not found: {app_file}")
        raise typer.Exit(1)

    config = detect_project_config()
    manager = ProcessManager()
    temp_files = []

    try:
        app_port, msg = resolve_port(port, strict, app_path)
        if msg:
            console.print(f"[blue]{msg}[/blue]")
    except RuntimeError as e:
        error(str(e))
        raise typer.Exit(1) from e

    try:
        console.print("[cyan]Starting tailwind...[/cyan]")
        input_css = setup_tailwind(manager, config, css_hot_reload)
        if input_css.name.startswith("tmp"):
            temp_files.append(input_css)
        wait_for_css(config.css_output_absolute)

        console.print("[cyan]Starting uvicorn...[/cyan]")
        manager.start_uvicorn(
            app_path,
            app_port,
            ["*.py", "*.html"],
            css_hot_reload,
            debug,
        )

        # Collect wrapper files for cleanup
        temp_files.extend(app_path.parent.glob(f"{app_path.stem}_dev*.py"))
        temp_files.extend(config.css_output_absolute.parent.glob("tmp*.css"))

        success(f"Server running at http://localhost:{app_port}")
        show_status(config, app_port, css_hot_reload, app_file)
        console.print("[dim]Press Ctrl+C to stop[/dim]\n")

        try:
            manager.wait_for_any_exit()
        except KeyboardInterrupt:
            console.print("\n[yellow]Shutting down...[/yellow]")

    except Exception as e:
        error(f"Dev server error: {e}")
        raise typer.Exit(1) from e
    finally:
        manager.stop_all()
        cleanup(*temp_files)
