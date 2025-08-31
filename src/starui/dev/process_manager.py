"""Process coordination for development server."""

import os
import subprocess
import sys
import threading
import time
from collections.abc import Callable
from contextlib import suppress
from pathlib import Path
from tempfile import gettempdir
from typing import Any

from rich.console import Console

RELOAD_EXCLUDES = ["*.css", "static/**", "**/tmp*", "**/__pycache__/**", "*_dev.py"]
RENDER_PROCESSES = {"uvicorn", "tailwind"}

WRAPPER_TEMPLATE = """import sys
import warnings
sys.path.insert(0, r'{app_dir}')

warnings.filterwarnings('ignore', message='live=True requires debug=True.*', category=UserWarning)

from {app_stem} import app as original_app
from starui.dev.unified_reload import create_dev_reload_route, DevReloadJs
from starlette.routing import WebSocketRoute

if hasattr(original_app, 'debug'):
    original_app.debug = {debug}

try:
    router = getattr(original_app, 'router', original_app)

    if hasattr(router, 'routes'):
        router.routes = [
            r for r in router.routes
            if not (isinstance(r, WebSocketRoute) and r.path == '/live-reload')
        ]

    if hasattr(original_app, 'hdrs'):
        if isinstance(original_app.hdrs, list):
            original_app.hdrs = [
                h for h in original_app.hdrs
                if 'live-reload' not in str(h).lower()
                and 'LiveReloadJs' not in str(type(h).__name__)
            ]
        else:
            original_app.hdrs = []
    else:
        original_app.hdrs = []

    original_app.hdrs.append(DevReloadJs())
    route = create_dev_reload_route()

    if hasattr(router, 'routes'):
        router.routes.append(route)
    elif hasattr(router, 'mount'):
        router.mount('/live-reload', route)

    sys.stdout.write("[StarUI] ✓ Replaced StarHTML live reload with unified dev reload system\\n")
    sys.stdout.flush()

except Exception as e:
    sys.stderr.write(f"[StarUI] Warning: Could not fully replace dev reload system: {{e}}\\n")
    sys.stderr.flush()

app = original_app"""


class ProcessManager:
    def __init__(self):
        self.processes = {}
        self.threads = {}
        self.shutdown = threading.Event()
        self.console = Console()

    def start_process(
        self,
        name: str,
        cmd: list[str],
        cwd: Path | None = None,
        env: dict[str, Any] | None = None,
    ) -> subprocess.Popen[str]:
        if existing := self.processes.get(name):
            self.console.print(f"[yellow]{name} already running[/yellow]")
            return existing

        proc = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
        self.processes[name] = proc
        self._monitor(name, proc)
        return proc

    def _monitor(self, name: str, proc: subprocess.Popen[str]) -> None:
        def run() -> None:
            with suppress(Exception):
                while proc.poll() is None and not self.shutdown.is_set():
                    if line := proc.stdout.readline():
                        if clean := line.rstrip():
                            if name in RENDER_PROCESSES:
                                sys.stdout.write(f"{clean}\n")
                                sys.stdout.flush()
                            else:
                                self.console.print(
                                    f"[dim cyan][{name}][/dim cyan] {clean}"
                                )
                    else:
                        time.sleep(0.1)

        thread = threading.Thread(target=run, daemon=True)
        thread.start()
        self.threads[f"{name}_monitor"] = thread

    def start_uvicorn(
        self,
        app_file: Path,
        port: int,
        patterns: list[str],
        hot_reload: bool = True,
        debug: bool = True,
    ) -> subprocess.Popen[str]:
        module = self._get_app_module(app_file, hot_reload, debug)
        cmd = [
            sys.executable,
            "-m",
            "uvicorn",
            module,
            "--reload",
            "--port",
            str(port),
            "--host",
            "localhost",
            "--reload-delay",
            "0.1",
            "--use-colors",
        ]

        for pattern in patterns:
            cmd.extend(["--reload-include", pattern])
        for exclude in RELOAD_EXCLUDES:
            cmd.extend(["--reload-exclude", exclude])

        env = os.environ.copy()
        if hot_reload:
            temp_dir = Path(gettempdir())
            pythonpath = env.get("PYTHONPATH", "")
            env["PYTHONPATH"] = (
                f"{temp_dir}:{pythonpath}" if pythonpath else str(temp_dir)
            )

        return self.start_process("uvicorn", cmd, app_file.parent, env)

    def _get_app_module(self, app_file: Path, hot_reload: bool, debug: bool) -> str:
        if not hot_reload:
            return f"{app_file.stem}:app"

        temp_dir = Path(gettempdir())
        wrapper = temp_dir / f"starui_dev_{app_file.stem}_{os.getpid()}.py"

        wrapper.write_text(
            WRAPPER_TEMPLATE.format(
                app_dir=app_file.parent, app_stem=app_file.stem, debug=debug
            )
        )
        return f"{wrapper.stem}:app"

    def start_tailwind_watcher(
        self,
        binary: Path,
        input_css: Path,
        output_css: Path,
        project_root: Path,
        on_rebuild: Callable[[Path], None] | None = None,
    ) -> subprocess.Popen[str]:
        cmd = [
            str(binary),
            "--input",
            str(input_css),
            "--output",
            str(output_css),
            "--watch=always",
            "--cwd",
            str(project_root),
        ]

        proc = self.start_process("tailwind", cmd, project_root)
        if on_rebuild:
            self._watch(output_css, on_rebuild)
        return proc

    def _watch(self, path: Path, callback: Callable[[Path], None]) -> None:
        def run() -> None:
            last = path.stat().st_mtime if path.exists() else 0
            if last:
                callback(path)

            while not self.shutdown.is_set():
                with suppress(Exception):
                    if path.exists() and (mtime := path.stat().st_mtime) > last:
                        last = mtime
                        callback(path)
                time.sleep(0.5)

        thread = threading.Thread(target=run, daemon=True)
        thread.start()
        self.threads["tailwind_monitor"] = thread

    def is_running(self, name: str) -> bool:
        return (p := self.processes.get(name)) and p.poll() is None

    def stop_process(self, name: str, timeout: int = 2) -> bool:
        if not (proc := self.processes.get(name)):
            return True

        with suppress(Exception):
            proc.terminate()
            try:
                proc.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait(timeout=1)

        self.processes.pop(name, None)
        return True

    def stop_all(self, timeout: int = 2) -> None:
        if self.shutdown.is_set():
            return

        self.shutdown.set()
        for name in list(self.processes):
            self.stop_process(name, timeout)

        self.processes.clear()
        self.threads.clear()

    def wait_for_any_exit(self) -> None:
        while not self.shutdown.is_set():
            dead = [
                name
                for name, proc in self.processes.items()
                if proc.poll() is not None
                and not (name == "tailwind" and proc.returncode == 0)
            ]

            if dead:
                for name in dead:
                    self.console.print(f"[red]{name} died unexpectedly[/red]")
                    del self.processes[name]

                if "uvicorn" in dead:
                    break

            time.sleep(0.5)
