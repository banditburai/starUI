"""CSS build pipeline with Tailwind integration."""

import re
import subprocess
import tempfile
import time
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path

from ..config import ProjectConfig, get_content_patterns
from ..templates.css_input import generate_css_input
from .binary import TailwindBinaryManager


class BuildMode(StrEnum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"


class BuildError(Exception):
    pass


@dataclass
class BuildResult:
    success: bool
    css_path: Path | None = None
    build_time: float | None = None
    classes_found: int | None = None
    css_size_bytes: int | None = None
    error_message: str | None = None


def extract_classes(content: str) -> set[str]:
    patterns = [
        r'cls\s*=\s*["\']([^"\']*)["\']',
        r'class_\s*=\s*["\']([^"\']*)["\']',
        r'className\s*=\s*["\']([^"\']*)["\']',
        r'cn\s*\(\s*["\']([^"\']*)["\']',
    ]

    classes = set()
    for pattern in patterns:
        for match in re.findall(pattern, content, re.MULTILINE):
            classes.update(match.split())

    return {c for c in classes if c and re.match(r"^[a-zA-Z0-9_:-]+$", c)}


class ContentScanner:
    def __init__(self, config: ProjectConfig):
        self.config = config
        self.patterns = get_content_patterns(config.project_root)

    def scan_files(self) -> set[str]:
        all_classes: set[str] = set()
        supported_extensions = {".py", ".html", ".js", ".ts", ".jsx", ".tsx"}

        for pattern in self.patterns:
            if pattern.startswith("!"):
                continue

            for file in self.config.project_root.glob(pattern):
                if file.suffix not in supported_extensions:
                    continue

                try:
                    content = file.read_text(encoding="utf-8")
                    all_classes.update(extract_classes(content))
                except (UnicodeDecodeError, PermissionError):
                    continue

        return all_classes


class CSSBuilder:
    def __init__(self, config: ProjectConfig):
        self.config = config
        self.binary_manager = TailwindBinaryManager("latest")
        self.scanner = ContentScanner(config)

    def build(
        self,
        mode: BuildMode = BuildMode.DEVELOPMENT,
        watch: bool = False,
        scan_content: bool = True,
    ) -> BuildResult:
        start_time = time.time()

        try:
            binary_path = self.binary_manager.get_binary()

            classes_found = None
            if scan_content:
                classes_found = len(self.scanner.scan_files())

            project_input_css = (
                self.config.project_root / "static" / "css" / "input.css"
            )

            if project_input_css.exists():
                input_file = project_input_css
                use_temp = False
            else:
                css_dir = self.config.css_output_absolute.parent
                css_dir.mkdir(parents=True, exist_ok=True)

                with tempfile.NamedTemporaryFile(
                    mode="w", suffix=".css", dir=css_dir, delete=False
                ) as temp_file:
                    temp_file.write(generate_css_input(self.config))
                    input_file = Path(temp_file.name)
                    use_temp = True

            self.config.css_output_absolute.parent.mkdir(parents=True, exist_ok=True)

            cmd = [
                str(binary_path),
                "-i",
                str(input_file),
                "-o",
                str(self.config.css_output_absolute),
            ]

            if mode == BuildMode.PRODUCTION:
                cmd.append("--minify")
            if watch:
                cmd.append("--watch")

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60,
                cwd=self.config.project_root,
            )

            if use_temp and input_file.exists():
                input_file.unlink()

            if result.returncode != 0:
                raise BuildError(f"Tailwind failed: {result.stderr or 'Unknown error'}")

            build_time = time.time() - start_time
            css_size = None
            if self.config.css_output_absolute.exists():
                css_size = self.config.css_output_absolute.stat().st_size

            return BuildResult(
                success=True,
                css_path=self.config.css_output_absolute,
                build_time=build_time,
                classes_found=classes_found,
                css_size_bytes=css_size,
            )

        except Exception as e:
            if "use_temp" in locals() and use_temp and "input_file" in locals():
                input_file.unlink(missing_ok=True)
            return BuildResult(success=False, error_message=str(e))
