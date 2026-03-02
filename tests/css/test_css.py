from pathlib import Path
from unittest.mock import patch

import pytest

from starui.css import BinaryError, BuildResult, get_binary_name, get_cache_dir, get_platform_info


class TestGetPlatformInfo:
    def test_macos_arm64(self):
        with (
            patch("starui.css.platform.system", return_value="Darwin"),
            patch("starui.css.platform.machine", return_value="arm64"),
        ):
            assert get_platform_info() == ("macos", "arm64")

    def test_linux_x64(self):
        with (
            patch("starui.css.platform.system", return_value="Linux"),
            patch("starui.css.platform.machine", return_value="x86_64"),
        ):
            assert get_platform_info() == ("linux", "x64")

    def test_windows_x64(self):
        with (
            patch("starui.css.platform.system", return_value="Windows"),
            patch("starui.css.platform.machine", return_value="AMD64"),
        ):
            assert get_platform_info() == ("windows", "x64")

    def test_linux_aarch64_maps_to_arm64(self):
        with (
            patch("starui.css.platform.system", return_value="Linux"),
            patch("starui.css.platform.machine", return_value="aarch64"),
        ):
            assert get_platform_info() == ("linux", "arm64")

    def test_unsupported_platform_raises(self):
        with (
            patch("starui.css.platform.system", return_value="FreeBSD"),
            patch("starui.css.platform.machine", return_value="x86_64"),
        ):
            with pytest.raises(BinaryError, match="Unsupported platform"):
                get_platform_info()

    def test_unsupported_arch_raises(self):
        with (
            patch("starui.css.platform.system", return_value="Linux"),
            patch("starui.css.platform.machine", return_value="riscv64"),
        ):
            with pytest.raises(BinaryError, match="Unsupported architecture"):
                get_platform_info()


class TestGetBinaryName:
    def test_macos(self):
        assert get_binary_name("macos", "arm64") == "tailwindcss-macos-arm64"

    def test_linux(self):
        assert get_binary_name("linux", "x64") == "tailwindcss-linux-x64"

    def test_windows_has_exe(self):
        assert get_binary_name("windows", "x64") == "tailwindcss-windows-x64.exe"


class TestGetCacheDir:
    def test_creates_versioned_dir(self, tmp_path):
        with patch("starui.css.Path.home", return_value=tmp_path):
            result = get_cache_dir("v4.1.0")
            assert result == tmp_path / ".starui" / "cache" / "v4.1.0"
            assert result.is_dir()

    def test_idempotent(self, tmp_path):
        with patch("starui.css.Path.home", return_value=tmp_path):
            first = get_cache_dir("v4.1.0")
            second = get_cache_dir("v4.1.0")
            assert first == second


class TestBuildResult:
    def test_defaults(self):
        result = BuildResult(success=True)
        assert result.css_path is None
        assert result.build_time is None
        assert result.css_size_bytes is None
        assert result.error_message is None

    def test_failed_result(self):
        result = BuildResult(success=False, error_message="tailwind not found")
        assert not result.success
        assert result.error_message == "tailwind not found"

    def test_successful_result(self):
        result = BuildResult(
            success=True,
            css_path=Path("static/css/starui.css"),
            build_time=1.23,
            css_size_bytes=4096,
        )
        assert result.success
        assert result.css_path == Path("static/css/starui.css")
        assert result.build_time == 1.23
        assert result.css_size_bytes == 4096
