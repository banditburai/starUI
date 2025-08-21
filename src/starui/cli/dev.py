import signal
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, cast

import typer
from rich.panel import Panel
from rich.table import Table
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

from ..config import detect_project_config
from ..css.builder import BuildMode, CSSBuilder
from .utils import console, error, info, success


class RebuildHandler(FileSystemEventHandler):
    """Handler for file system events that triggers CSS rebuilds."""

    def __init__(self, builder: CSSBuilder, verbose: bool = False):
        self.builder = builder
        self.verbose = verbose
        self.last_build = time.time()

    def on_modified(self, event: FileSystemEvent) -> None:
        if event.is_directory:
            return
        path = Path(cast(str, event.src_path))
        if path.suffix in {".py", ".html", ".css", ".js"}:
            self._rebuild(path)

    def _rebuild(self, changed_path: Path) -> None:
        now = time.time()
        if now - self.last_build < 0.5:  # Debounce
            return

        if self.verbose:
            info(f"Changed: {changed_path}")

        with console.status("[bold yellow]Rebuilding CSS..."):
            result = self.builder.build(
                BuildMode.DEVELOPMENT, watch=False, scan_content=True
            )

        if result.success:
            success(f"✓ CSS rebuilt ({result.build_time:.2f}s)")
            # Force browser reload by touching the output CSS file
            if result.css_path and result.css_path.exists():
                result.css_path.touch()
        else:
            error(f"Build failed: {result.error_message}")

        self.last_build = now


def dev_command(
    app_file: str | None = typer.Argument(None, help="StarHTML app file to run"),
    port: int = typer.Option(5000, "--port", "-p", help="Port for app server"),
    watch: bool = typer.Option(True, "--watch/--no-watch", help="Watch for changes"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show details"),
) -> None:
    """Start development server with CSS watching."""

    try:
        config = detect_project_config()
        builder = CSSBuilder(config)

        # Initial build
        with console.status("[bold green]Building CSS..."):
            result = builder.build(
                BuildMode.DEVELOPMENT, watch=False, scan_content=True
            )
            if not result.success:
                error(f"Initial build failed: {result.error_message}")
                raise typer.Exit(1)

        success("✓ Initial CSS build completed")
        if verbose:
            if result.build_time:
                info(f"Build time: {result.build_time:.2f}s")
            if result.css_size_bytes:
                info(f"CSS size: {result.css_size_bytes / 1024:.1f} KB")
            if result.classes_found:
                info(f"CSS classes found: {result.classes_found}")

        # Start app server if provided
        app_process: subprocess.Popen[str] | None = None
        if app_file:
            app_path = Path(app_file)
            if not app_path.exists():
                error(f"App file not found: {app_file}")
                raise typer.Exit(1)

            app_process = subprocess.Popen(
                [
                    sys.executable,
                    "-m",
                    "uvicorn",
                    f"{app_path.stem}:app",
                    "--reload",
                    "--port",
                    str(port),
                    "--host",
                    "localhost",
                ],
                stdout=None,  # Stream to terminal
                stderr=None,  # Stream to terminal
                text=True,
            )
            success(f"✓ App server started at http://localhost:{port}")

        if watch:
            success("✓ File watcher started")

        # Display server info
        table = Table(title="Star Development Server", show_header=False)
        table.add_column(style="cyan")
        table.add_column(style="green")
        table.add_row("✓ Development server started", "")
        table.add_row("Project", str(config.project_root.name))
        table.add_row("CSS Output", str(config.css_output))
        table.add_row("Framework", "StarHTML")
        table.add_row("File Watching", "Enabled" if watch else "Disabled")
        if app_file:
            table.add_row("App Server", f"http://localhost:{port}")
            table.add_row("App File", app_file)

        console.print(Panel(table, border_style="green"))
        console.print("\nKeyboard shortcuts:")
        console.print("  Ctrl+C  Stop the server\n")

        if app_file:
            console.print("App server logs will appear below...\n")

        console.print("Press Ctrl+C to stop the development server")

        # Setup file watching
        observer = None
        if watch:
            observer = Observer()
            handler = RebuildHandler(builder, verbose)
            observer.schedule(handler, str(config.project_root), recursive=True)  # type: ignore
            observer.start()

        # Handle shutdown
        def shutdown_handler(_sig: Any, _frame: Any) -> None:
            console.print("\n[yellow]Shutting down...[/yellow]")
            if observer:
                observer.stop()
                observer.join()
            if app_process:
                app_process.terminate()
            sys.exit(0)

        signal.signal(signal.SIGINT, shutdown_handler)
        signal.signal(signal.SIGTERM, shutdown_handler)

        try:
            if app_process:
                app_process.wait()
            elif observer:
                observer.join()
            else:
                # Just wait if no watching and no app
                while True:
                    time.sleep(1)
        except KeyboardInterrupt:
            shutdown_handler(None, None)

    except Exception as e:
        error(f"Dev server error: {e}")
        raise typer.Exit(1) from e
