from io import StringIO
from unittest.mock import MagicMock, patch

from rich.console import Console

import starui.cli.utils as utils_module
from starui.cli.utils import (
    confirm,
    error,
    info,
    install_component,
    success,
    validate_component_name,
    warning,
)


def _capture_output(func, message):
    """Call a console function and return the rendered text output."""
    buf = StringIO()
    capture_console = Console(file=buf, force_terminal=False)
    original = utils_module.console
    utils_module.console = capture_console
    try:
        func(message)
    finally:
        utils_module.console = original
    return buf.getvalue()


class TestConsoleUtilities:
    def test_success_includes_message_and_checkmark(self):
        output = _capture_output(success, "Operation completed successfully")
        assert "Operation completed successfully" in output
        assert "\u2713" in output  # checkmark prefix

    def test_error_includes_message_and_label(self):
        output = _capture_output(error, "Something went wrong")
        assert "Something went wrong" in output
        assert "Error" in output

    def test_warning_includes_message_and_label(self):
        output = _capture_output(warning, "This is a warning")
        assert "This is a warning" in output
        assert "Warning" in output

    def test_info_includes_message_and_label(self):
        output = _capture_output(info, "Information message")
        assert "Information message" in output
        assert "Info" in output

    def test_confirm_returns_user_response(self):
        with patch("starui.cli.utils.typer.confirm", return_value=True):
            assert confirm("Are you sure?") is True

        with patch("starui.cli.utils.typer.confirm", return_value=False):
            assert confirm("Are you sure?") is False

    def test_confirm_defaults_to_false(self):
        with patch("starui.cli.utils.typer.confirm", return_value=False) as mock_confirm:
            confirm("Are you sure?")
            _, kwargs = mock_confirm.call_args
            assert kwargs["default"] is False


class TestInstallComponent:
    def test_writes_file_and_records_manifest(self, project):
        client = MagicMock()
        client.version = "1.0.0"
        client.get_component_metadata.return_value = {"checksum": "abc123"}
        manifest = MagicMock()

        install_component("button", "# button source", config=project, client=client, manifest=manifest)

        written = (project.component_dir_absolute / "button.py").read_text()
        assert written == "# button source"
        manifest.record_install.assert_called_once_with(
            "button",
            version="1.0.0",
            checksum="abc123",
            file_path=str(project.component_dir_absolute.relative_to(project.project_root) / "button.py"),
        )

    def test_writes_file_even_when_metadata_missing(self, project):
        client = MagicMock()
        client.get_component_metadata.side_effect = FileNotFoundError("not in registry")
        manifest = MagicMock()

        install_component("custom", "# custom source", config=project, client=client, manifest=manifest)

        assert (project.component_dir_absolute / "custom.py").read_text() == "# custom source"
        manifest.record_install.assert_not_called()

    def test_non_file_not_found_errors_propagate(self, project):
        client = MagicMock()
        client.get_component_metadata.side_effect = RuntimeError("unexpected")
        manifest = MagicMock()

        try:
            install_component("broken", "# src", config=project, client=client, manifest=manifest)
            raise AssertionError("Should have raised")
        except RuntimeError:
            pass

        assert (project.component_dir_absolute / "broken.py").exists()


class TestValidateComponentName:
    def test_valid_names(self):
        for name in ["button", "card", "input-field", "data-table", "date_picker"]:
            assert validate_component_name(name) is True

    def test_invalid_names(self):
        for name in ["", "Button", "123button", "button@#"]:
            assert validate_component_name(name) is False
