"""Tailwind CSS binary management and build pipeline."""

import platform
import shutil
import subprocess
import tempfile
import time
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path

import requests

from .config import ProjectConfig
from .templates import generate_css_input


class BinaryError(Exception): ...


class NetworkError(BinaryError): ...


class BuildMode(StrEnum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"


@dataclass
class BuildResult:
    success: bool
    css_path: Path | None = None
    build_time: float | None = None
    css_size_bytes: int | None = None
    error_message: str | None = None


def get_platform_info() -> tuple[str, str]:
    system = platform.system()
    machine = platform.machine()

    platform_map = {"Darwin": "macos", "Linux": "linux", "Windows": "windows"}
    arch_map = {"arm64": "arm64", "aarch64": "arm64", "x86_64": "x64", "AMD64": "x64"}

    if system not in platform_map:
        raise BinaryError(f"Unsupported platform: {system}")
    if machine not in arch_map:
        raise BinaryError(f"Unsupported architecture: {machine}")

    return platform_map[system], arch_map[machine]


def get_binary_name(platform_name: str, arch: str) -> str:
    base = f"tailwindcss-{platform_name}-{arch}"
    return f"{base}.exe" if platform_name == "windows" else base


def get_cache_dir(version: str) -> Path:
    cache_dir = Path.home() / ".starui" / "cache" / version
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir


class TailwindBinaryManager:
    DEFAULT_VERSION = "latest"
    FALLBACK_VERSION = "v4.1.0"
    GITHUB_RELEASES_URL = "https://github.com/tailwindlabs/tailwindcss/releases/download"
    GITHUB_API_URL = "https://api.github.com/repos/tailwindlabs/tailwindcss/releases/latest"

    def __init__(self, version: str | None = None):
        self.version = version or self.DEFAULT_VERSION

    def _get_latest_version(self) -> str:
        try:
            response = requests.get(self.GITHUB_API_URL, timeout=10)
            response.raise_for_status()
            return response.json().get("tag_name", self.FALLBACK_VERSION)
        except requests.RequestException:
            # Fallback when offline — will attempt download and fail clearly
            return self.FALLBACK_VERSION

    def _get_download_url(self) -> str:
        platform_name, arch = get_platform_info()
        binary_name = get_binary_name(platform_name, arch)

        if self.version == "latest":
            version = self._get_latest_version()
            return f"{self.GITHUB_RELEASES_URL}/{version}/{binary_name}"
        return f"{self.GITHUB_RELEASES_URL}/v{self.version}/{binary_name}"

    def _get_binary_path(self) -> Path:
        cache_dir = get_cache_dir(self.version)
        platform_name, arch = get_platform_info()
        return cache_dir / get_binary_name(platform_name, arch)

    def _download_binary(self, url: str, binary_path: Path) -> None:
        try:
            response = requests.get(url, timeout=60)
            response.raise_for_status()

            binary_path.parent.mkdir(parents=True, exist_ok=True)
            binary_path.write_bytes(response.content)
            binary_path.chmod(binary_path.stat().st_mode | 0o755)

        except requests.RequestException as e:
            raise NetworkError(f"Failed to download: {e}") from e

    def get_binary(self) -> Path:
        if system_binary := shutil.which("tailwindcss"):
            return Path(system_binary)

        binary_path = self._get_binary_path()
        if binary_path.exists():
            return binary_path

        self._download_binary(self._get_download_url(), binary_path)
        return binary_path


class CSSBuilder:
    def __init__(self, config: ProjectConfig):
        self.config = config
        self.binary_manager = TailwindBinaryManager()

    def build(self, mode: BuildMode = BuildMode.DEVELOPMENT) -> BuildResult:
        start_time = time.time()
        input_file = None
        use_temp = False

        try:
            binary_path = self.binary_manager.get_binary()

            project_input_css = self.config.css_dir_absolute / "input.css"

            if project_input_css.exists():
                input_file = project_input_css
            else:
                css_dir = self.config.css_output_absolute.parent
                css_dir.mkdir(parents=True, exist_ok=True)

                with tempfile.NamedTemporaryFile(mode="w", suffix=".css", dir=css_dir, delete=False) as temp_file:
                    temp_file.write(generate_css_input(self.config))
                    input_file = Path(temp_file.name)
                    use_temp = True

            cmd = [
                str(binary_path),
                "-i",
                str(input_file),
                "-o",
                str(self.config.css_output_absolute),
            ]

            if mode == BuildMode.PRODUCTION:
                cmd.append("--minify")

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60,
                cwd=self.config.project_root,
            )

            if result.returncode != 0:
                return BuildResult(
                    success=False,
                    error_message=result.stderr or "Unknown error",
                )

            build_time = time.time() - start_time
            css_size = None
            if self.config.css_output_absolute.exists():
                css_size = self.config.css_output_absolute.stat().st_size

            return BuildResult(
                success=True,
                css_path=self.config.css_output_absolute,
                build_time=build_time,
                css_size_bytes=css_size,
            )

        except Exception as e:
            return BuildResult(success=False, error_message=str(e))

        finally:
            if use_temp and input_file:
                input_file.unlink(missing_ok=True)
