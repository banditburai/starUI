"""Tests for the main CLI application."""

from typer.testing import CliRunner

from starui.cli.main import app


class TestMainCLI:
    """Test cases for the main CLI application."""

    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()

    def test_cli_app_exists(self):
        """Test that the CLI app can be imported and is a Typer app."""
        assert app is not None
        assert hasattr(app, "command")
        assert hasattr(app, "callback")

    def test_help_command(self):
        """Test that help command works."""
        result = self.runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "StarUI" in result.stdout
        assert "Python-first UI component library" in result.stdout

    def test_version_command(self):
        """Test that version command works."""
        from starui import __version__

        result = self.runner.invoke(app, ["--version"])
        assert result.exit_code == 0
        assert __version__ in result.stdout

    def test_init_command_exists(self):
        """Test that init command is registered."""
        result = self.runner.invoke(app, ["init", "--help"])
        assert result.exit_code == 0
        assert "init" in result.stdout.lower()

    def test_add_command_exists(self):
        """Test that add command is registered."""
        result = self.runner.invoke(app, ["add", "--help"])
        assert result.exit_code == 0
        assert "add" in result.stdout.lower()

    def test_dev_command_exists(self):
        """Test that dev command is registered."""
        result = self.runner.invoke(app, ["dev", "--help"])
        assert result.exit_code == 0
        assert "dev" in result.stdout.lower()

    def test_build_command_exists(self):
        """Test that build command is registered."""
        result = self.runner.invoke(app, ["build", "--help"])
        assert result.exit_code == 0
        assert "build" in result.stdout.lower()

    def test_list_command_exists(self):
        """Test that list command is registered."""
        result = self.runner.invoke(app, ["list", "--help"])
        assert result.exit_code == 0
        assert "list" in result.stdout.lower()

    def test_rich_console_integration(self):
        """Test that Rich console is properly integrated."""
        # This will be tested by checking error output formatting
        result = self.runner.invoke(app, ["nonexistent-command"])
        assert result.exit_code != 0
        # Rich should format the error nicely - check both stdout and stderr
        output = result.stdout + (result.stderr or "")
        assert "Usage:" in output or "Error:" in output or "No such command" in output

    def test_error_handling_framework(self):
        """Test that commands have proper error handling."""
        # Test that commands properly use typer.Exit for errors
        result = self.runner.invoke(app, ["add", "invalid-!@#-component"])
        assert result.exit_code != 0  # Should exit with error
        assert "Invalid component name" in result.output


class TestCLIErrorHandling:
    """Test cases for CLI error handling."""

    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()

    def test_invalid_command_error(self):
        """Test handling of invalid commands."""
        result = self.runner.invoke(app, ["invalid-command"])
        assert result.exit_code != 0
        # Check both stdout and stderr for error messages
        output = result.stdout + (result.stderr or "")
        assert "Usage:" in output or "No such command" in output or "Error" in output

    def test_missing_arguments_error(self):
        """Test handling of missing required arguments."""
        # This will be more specific once commands are implemented
        result = self.runner.invoke(app, ["add"])
        # Should fail gracefully with help message
        assert result.exit_code != 0
