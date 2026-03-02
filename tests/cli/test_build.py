from io import StringIO
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from click.exceptions import Exit
from rich.console import Console

from starui.cli.build import build_command, format_size
from starui.config import ProjectConfig
from starui.css import BuildMode, BuildResult


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


def _capture_build_output(config, result, *, output=None, minify=True, verbose=False) -> str:
    """Run build_command capturing all console output to a string."""
    mock_builder = MagicMock()
    mock_builder.build.return_value = result

    buf = StringIO()
    real_console = Console(file=buf, width=300, no_color=True)

    with (
        patch("starui.cli.build.get_project_config", return_value=config),
        patch("starui.cli.build.CSSBuilder", return_value=mock_builder),
        patch("starui.cli.build.console", real_console),
        patch("starui.cli.build.success", lambda msg: real_console.print(f"OK: {msg}")),
        patch("starui.cli.build.error", lambda msg: real_console.print(f"ERR: {msg}")),
        patch("starui.cli.build.info", lambda msg: real_console.print(f"INFO: {msg}")),
    ):
        build_command(output=output, minify=minify, verbose=verbose)

    return buf.getvalue()


class TestBuildCommand:
    def test_success_reports_build_stats(self, tmp_path):
        config = _make_config(tmp_path)
        result = BuildResult(
            success=True,
            css_path=config.css_output_absolute,
            build_time=0.5,
            css_size_bytes=1024,
        )

        output = _capture_build_output(config, result)

        assert "0.5s" in output
        assert "1.0 KB" in output

    def test_failure_raises_exit_with_error_message(self, tmp_path):
        config = _make_config(tmp_path)
        result = BuildResult(success=False, error_message="tailwind not found")

        with pytest.raises(Exit):
            _capture_build_output(config, result)

    def test_cleans_existing_output_before_build(self, tmp_path):
        config = _make_config(tmp_path)
        config.css_output_absolute.write_text("old css")
        result = BuildResult(success=True)

        _capture_build_output(config, result)

        assert not config.css_output_absolute.exists()

    def test_creates_parent_dir(self, tmp_path):
        config = ProjectConfig(
            project_root=tmp_path,
            css_output=Path("dist/css/starui.css"),
            component_dir=Path("components/ui"),
        )
        result = BuildResult(success=True)

        _capture_build_output(config, result)

        assert config.css_output_absolute.parent.is_dir()

    def test_no_minify_uses_development_mode(self, tmp_path):
        config = _make_config(tmp_path)
        result = BuildResult(success=True)

        mock_builder = MagicMock()
        mock_builder.build.return_value = result

        with (
            patch("starui.cli.build.get_project_config", return_value=config),
            patch("starui.cli.build.CSSBuilder", return_value=mock_builder),
            patch("starui.cli.build.console"),
            patch("starui.cli.build.success"),
            patch("starui.cli.build.error"),
            patch("starui.cli.build.info"),
        ):
            build_command(output=None, minify=False, verbose=False)

        assert mock_builder.build.call_args.kwargs["mode"] == BuildMode.DEVELOPMENT

    def test_minify_uses_production_mode(self, tmp_path):
        config = _make_config(tmp_path)
        result = BuildResult(success=True)

        mock_builder = MagicMock()
        mock_builder.build.return_value = result

        with (
            patch("starui.cli.build.get_project_config", return_value=config),
            patch("starui.cli.build.CSSBuilder", return_value=mock_builder),
            patch("starui.cli.build.console"),
            patch("starui.cli.build.success"),
            patch("starui.cli.build.error"),
            patch("starui.cli.build.info"),
        ):
            build_command(output=None, minify=True, verbose=False)

        assert mock_builder.build.call_args.kwargs["mode"] == BuildMode.PRODUCTION

    def test_output_flag_appends_css_suffix(self, tmp_path):
        config = _make_config(tmp_path)
        result = BuildResult(success=True)

        mock_builder = MagicMock()
        mock_builder.build.return_value = result

        with (
            patch("starui.cli.build.get_project_config", return_value=config),
            patch("starui.cli.build.CSSBuilder") as MockCSSBuilder,
            patch("starui.cli.build.console"),
            patch("starui.cli.build.success"),
            patch("starui.cli.build.info"),
        ):
            MockCSSBuilder.return_value = mock_builder
            build_command(output="dist/styles", minify=True, verbose=False)

        assert config.css_output.suffix == ".css"

    def test_verbose_shows_output_path(self, tmp_path):
        config = _make_config(tmp_path)
        result = BuildResult(success=True)

        output = _capture_build_output(config, result, verbose=True)

        assert str(config.css_output_absolute) in output

    def test_config_error_raises_exit(self):
        with (
            patch(
                "starui.cli.build.get_project_config",
                side_effect=RuntimeError("no project"),
            ),
            patch("starui.cli.build.console"),
            patch("starui.cli.build.error"),
            pytest.raises(Exit),
        ):
            build_command(output=None, minify=True, verbose=False)
