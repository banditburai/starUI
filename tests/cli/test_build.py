"""Tests for the build command."""

from io import StringIO
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from click.exceptions import Exit
from rich.console import Console

from starui.cli.build import build_command, format_size
from starui.config import ProjectConfig
from starui.css.builder import BuildMode, BuildResult


class TestFormatSize:
    def test_bytes(self):
        assert format_size(500) == "500 B"

    def test_kilobytes(self):
        assert format_size(2048) == "2.0 KB"

    def test_megabytes(self):
        assert format_size(1_500_000) == "1.4 MB"


def _make_config(tmp_path) -> ProjectConfig:
    (tmp_path / "static" / "css").mkdir(parents=True)
    return ProjectConfig(
        project_root=tmp_path,
        css_output=Path("static/css/starui.css"),
        component_dir=Path("components/ui"),
    )


def _run_build(config, result, *, output=None, minify=True, verbose=False):
    """Run build_command and return captured mocks for assertion."""
    mock_builder = MagicMock()
    mock_builder.build.return_value = result

    mocks = {}
    with (
        patch("starui.cli.build.detect_project_config", return_value=config),
        patch("starui.cli.build.CSSBuilder", return_value=mock_builder),
        patch("starui.cli.build.console") as mock_console,
        patch("starui.cli.build.success") as mock_success,
        patch("starui.cli.build.error") as mock_error,
        patch("starui.cli.build.info") as mock_info,
    ):
        mocks["console"] = mock_console
        mocks["success"] = mock_success
        mocks["error"] = mock_error
        mocks["info"] = mock_info
        mocks["builder"] = mock_builder
        build_command(output=output, minify=minify, verbose=verbose)

    return mocks


class TestBuildCommand:
    def test_success_prints_completion(self, tmp_path):
        config = _make_config(tmp_path)
        result = BuildResult(
            success=True,
            css_path=config.css_output_absolute,
            build_time=0.5,
            css_size_bytes=1024,
        )

        mocks = _run_build(config, result)

        mocks["success"].assert_called_once_with("Build completed!")
        # Verify the stats table was printed with our values
        buf = StringIO()
        real_console = Console(file=buf, width=120, no_color=True)
        for call in mocks["console"].print.call_args_list:
            real_console.print(*call.args, **call.kwargs)
        output = buf.getvalue()
        assert "0.5s" in output
        assert "1.0 KB" in output

    def test_failure_raises_exit_with_error_message(self, tmp_path):
        config = _make_config(tmp_path)
        result = BuildResult(success=False, error_message="tailwind not found")

        mock_builder = MagicMock()
        mock_builder.build.return_value = result

        with (
            patch("starui.cli.build.detect_project_config", return_value=config),
            patch("starui.cli.build.CSSBuilder", return_value=mock_builder),
            patch("starui.cli.build.console"),
            patch("starui.cli.build.success"),
            patch("starui.cli.build.error") as mock_error,
            patch("starui.cli.build.info"),
            pytest.raises(Exit),
        ):
            build_command(output=None, minify=True, verbose=False)

        # First error call is the specific failure message
        assert mock_error.call_args_list[0][0][0] == "Build failed: tailwind not found"

    def test_cleans_existing_output_before_build(self, tmp_path):
        config = _make_config(tmp_path)
        config.css_output_absolute.write_text("old css")
        result = BuildResult(success=True)

        _run_build(config, result)

        assert not config.css_output_absolute.exists()

    def test_creates_parent_dir(self, tmp_path):
        config = ProjectConfig(
            project_root=tmp_path,
            css_output=Path("dist/css/starui.css"),
            component_dir=Path("components/ui"),
        )
        result = BuildResult(success=True)

        _run_build(config, result)

        assert config.css_output_absolute.parent.is_dir()

    def test_no_minify_passes_development_mode(self, tmp_path):
        config = _make_config(tmp_path)
        result = BuildResult(success=True)

        mocks = _run_build(config, result, minify=False)

        mocks["builder"].build.assert_called_once_with(
            mode=BuildMode.DEVELOPMENT, watch=False, scan_content=True
        )

    def test_minify_passes_production_mode(self, tmp_path):
        config = _make_config(tmp_path)
        result = BuildResult(success=True)

        mocks = _run_build(config, result, minify=True)

        mocks["builder"].build.assert_called_once_with(
            mode=BuildMode.PRODUCTION, watch=False, scan_content=True
        )

    def test_output_flag_appends_css_suffix(self, tmp_path):
        config = _make_config(tmp_path)
        result = BuildResult(success=True)

        mock_builder = MagicMock()
        mock_builder.build.return_value = result

        with (
            patch("starui.cli.build.detect_project_config", return_value=config),
            patch("starui.cli.build.CSSBuilder") as MockCSSBuilder,
            patch("starui.cli.build.console"),
            patch("starui.cli.build.success"),
            patch("starui.cli.build.info"),
        ):
            MockCSSBuilder.return_value = mock_builder
            build_command(output="dist/styles", minify=True, verbose=False)

        # The config passed to CSSBuilder should have .css suffix
        assert config.css_output.suffix == ".css"

    def test_verbose_prints_output_path(self, tmp_path):
        config = _make_config(tmp_path)
        result = BuildResult(success=True)

        mocks = _run_build(config, result, verbose=True)

        mocks["info"].assert_called_once()
        assert str(config.css_output_absolute) in mocks["info"].call_args[0][0]

    def test_config_error_raises_exit(self):
        with (
            patch(
                "starui.cli.build.detect_project_config",
                side_effect=RuntimeError("no project"),
            ),
            patch("starui.cli.build.console"),
            patch("starui.cli.build.error"),
            pytest.raises(Exit),
        ):
            build_command(output=None, minify=True, verbose=False)
