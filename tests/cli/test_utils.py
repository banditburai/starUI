from unittest.mock import patch

from starui.cli.utils import (
    confirm,
    error,
    info,
    success,
    validate_component_name,
    warning,
)


class TestConsoleUtilities:
    @patch("starui.cli.utils.console.print")
    def test_success_message(self, mock_print):
        success("Operation completed successfully")
        mock_print.assert_called_once()
        assert "[green]" in str(mock_print.call_args[0][0])

    @patch("starui.cli.utils.console.print")
    def test_error_message(self, mock_print):
        error("Something went wrong")
        mock_print.assert_called_once()
        assert "[red]" in str(mock_print.call_args[0][0])

    @patch("starui.cli.utils.console.print")
    def test_warning_message(self, mock_print):
        warning("This is a warning")
        mock_print.assert_called_once()
        assert "[yellow]" in str(mock_print.call_args[0][0])

    @patch("starui.cli.utils.console.print")
    def test_info_message(self, mock_print):
        info("Information message")
        mock_print.assert_called_once()
        assert "[blue]" in str(mock_print.call_args[0][0])

    @patch("starui.cli.utils.typer.confirm")
    def test_confirm_function(self, mock_confirm):
        mock_confirm.return_value = True
        result = confirm("Are you sure?")
        assert result is True
        mock_confirm.assert_called_once_with("Are you sure?", default=False)


class TestValidateComponentName:
    def test_valid_names(self):
        for name in ["button", "card", "input-field", "data-table", "date_picker"]:
            assert validate_component_name(name) is True

    def test_invalid_names(self):
        for name in ["", "Button", "123button", "button@#"]:
            assert validate_component_name(name) is False
