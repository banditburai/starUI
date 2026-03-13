from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from click.exceptions import Exit

from starui.cli.dev import cleanup, dev_command, get_or_create_css_input, show_status, wait_for_css
from starui.config import ProjectConfig


def test_get_or_create_css_input_existing(tmp_path):
    css_dir = tmp_path / "static" / "css"
    css_dir.mkdir(parents=True)
    input_css = css_dir / "input.css"
    input_css.write_text("/* existing */")

    config = ProjectConfig(
        project_root=tmp_path,
        css_output=Path("static/css/starui.css"),
        component_dir=Path("components/ui"),
    )

    result = get_or_create_css_input(config)
    assert result == input_css


def test_get_or_create_css_input_creates_temp(tmp_path):
    css_dir = tmp_path / "static" / "css"
    css_dir.mkdir(parents=True)

    config = ProjectConfig(
        project_root=tmp_path,
        css_output=Path("static/css/starui.css"),
        component_dir=Path("components/ui"),
    )

    with patch("starui.cli.dev.generate_css_input") as mock_gen:
        mock_gen.return_value = "/* generated */"
        result = get_or_create_css_input(config)

        assert result.exists()
        assert result.suffix == ".css"
        assert result.read_text() == "/* generated */"


def test_cleanup_deletes_files(tmp_path):
    files = [tmp_path / f"temp_{i}.css" for i in range(3)]
    for f in files:
        f.write_text("temp content")

    cleanup(*files)

    for f in files:
        assert not f.exists()


def test_cleanup_skips_nones(tmp_path):
    real_file = tmp_path / "real.css"
    real_file.write_text("content")

    cleanup(real_file, None, None)

    assert not real_file.exists()


def test_cleanup_tolerates_already_deleted(tmp_path):
    missing = tmp_path / "already_gone.css"

    # Should not raise even though file doesn't exist
    cleanup(missing)


@patch("starui.cli.dev.success")
def test_wait_for_css_returns_when_file_exists(_mock_success, tmp_path):
    css_path = tmp_path / "test.css"
    css_path.write_text("/* css */")

    # Should return without raising
    wait_for_css(css_path)


@patch("starui.cli.dev.error")
@patch("starui.cli.dev.console")
@patch("time.sleep")
def test_wait_for_css_raises_exit_on_timeout(_mock_sleep, _mock_console, _mock_error, tmp_path):
    css_path = tmp_path / "nonexistent.css"

    with pytest.raises(Exit):
        wait_for_css(css_path, timeout=0.1)


# --- wait_for_css: file appears during polling ---


@patch("starui.cli.dev.success")
@patch("starui.cli.dev.console")
def test_wait_for_css_succeeds_when_file_appears_during_poll(_mock_console, _mock_success, tmp_path):
    """CSS file created mid-poll should be detected and not time out."""
    css_path = tmp_path / "delayed.css"
    call_count = 0
    original_sleep = __import__("time").sleep

    def fake_sleep(_seconds):
        nonlocal call_count
        call_count += 1
        if call_count >= 2:
            css_path.write_text("/* built */")
        original_sleep(0.01)

    with patch("time.sleep", side_effect=fake_sleep):
        wait_for_css(css_path, timeout=5)

    assert css_path.exists()


# --- show_status ---


@patch("starui.cli.dev.console")
def test_show_status_with_hot_reload_enabled(mock_console, tmp_path):
    """show_status renders without error when hot reload is on."""
    config = ProjectConfig(
        project_root=tmp_path,
        css_output=Path("static/css/starui.css"),
        component_dir=Path("components/ui"),
    )
    show_status(config, 5000, True, "app.py")
    # Verify it called console.print with a Panel
    assert mock_console.print.called


@patch("starui.cli.dev.console")
def test_show_status_with_hot_reload_disabled(mock_console, tmp_path):
    """show_status renders without error when hot reload is off."""
    config = ProjectConfig(
        project_root=tmp_path,
        css_output=Path("static/css/starui.css"),
        component_dir=Path("components/ui"),
    )
    show_status(config, 8080, False, "main.py")
    # Verify the function called console.print (i.e. it produced output)
    assert mock_console.print.called


# --- setup_tailwind ---


@patch("starui.cli.dev.TailwindBinaryManager")
@patch("starui.cli.dev.get_or_create_css_input")
def test_setup_tailwind_with_hot_reload(mock_get_css, mock_tw_mgr, tmp_path):
    """When hot reload is enabled, a non-None callback is passed to start_tailwind_watcher."""
    from starui.cli.dev import setup_tailwind

    config = ProjectConfig(
        project_root=tmp_path,
        css_output=Path("static/css/starui.css"),
        component_dir=Path("components/ui"),
    )
    mock_get_css.return_value = tmp_path / "input.css"
    mock_tw_mgr.return_value.get_binary.return_value = "/fake/tailwind"

    manager = MagicMock()
    result = setup_tailwind(manager, config, enable_hot_reload=True)

    assert result == tmp_path / "input.css"
    # The callback (5th positional arg) should not be None
    _call_args = manager.start_tailwind_watcher.call_args
    callback_arg = _call_args[0][4]
    assert callback_arg is not None


@patch("starui.cli.dev.TailwindBinaryManager")
@patch("starui.cli.dev.get_or_create_css_input")
def test_setup_tailwind_without_hot_reload(mock_get_css, mock_tw_mgr, tmp_path):
    """When hot reload is disabled, callback should be None."""
    from starui.cli.dev import setup_tailwind

    config = ProjectConfig(
        project_root=tmp_path,
        css_output=Path("static/css/starui.css"),
        component_dir=Path("components/ui"),
    )
    mock_get_css.return_value = tmp_path / "input.css"
    mock_tw_mgr.return_value.get_binary.return_value = "/fake/tailwind"

    manager = MagicMock()
    setup_tailwind(manager, config, enable_hot_reload=False)

    _call_args = manager.start_tailwind_watcher.call_args
    callback_arg = _call_args[0][4]
    assert callback_arg is None


# --- dev_command ---


def test_dev_command_app_file_not_found(tmp_path):
    """dev_command exits when the app file does not exist."""
    with (
        patch("starui.cli.dev.error") as mock_error,
        patch("starui.cli.dev.console"),
    ):
        with pytest.raises(Exit):
            dev_command(app_file=str(tmp_path / "nonexistent.py"))
        # The error message should mention the file path
        msg = mock_error.call_args[0][0]
        assert "nonexistent.py" in msg


def test_dev_command_config_error(tmp_path):
    """dev_command exits when get_project_config raises."""
    app_file = tmp_path / "app.py"
    app_file.write_text("app = 1")

    with (
        patch("starui.cli.dev.get_project_config", side_effect=RuntimeError("bad config")),
        patch("starui.cli.dev.error") as mock_error,
        patch("starui.cli.dev.console"),
    ):
        with pytest.raises(Exit):
            dev_command(app_file=str(app_file))
        msg = mock_error.call_args[0][0]
        assert "Config error" in msg


def test_dev_command_port_resolution_fails_strict(tmp_path):
    """dev_command exits when resolve_port raises RuntimeError."""
    app_file = tmp_path / "app.py"
    app_file.write_text("app = 1")

    config = ProjectConfig(
        project_root=tmp_path,
        css_output=Path("static/css/starui.css"),
        component_dir=Path("components/ui"),
    )

    with (
        patch("starui.cli.dev.get_project_config", return_value=config),
        patch("starui.cli.dev.resolve_port", side_effect=RuntimeError("Port 5000 in use")),
        patch("starui.cli.dev.ProcessManager"),
        patch("starui.cli.dev.error") as mock_error,
        patch("starui.cli.dev.console"),
    ):
        with pytest.raises(Exit):
            dev_command(app_file=str(app_file), strict=True)
        msg = mock_error.call_args[0][0]
        assert "Port 5000 in use" in msg


def test_dev_command_port_resolution_message_printed(tmp_path):
    """When resolve_port returns a message, it gets printed."""
    app_file = tmp_path / "app.py"
    app_file.write_text("app = 1")

    config = ProjectConfig(
        project_root=tmp_path,
        css_output=Path("static/css/starui.css"),
        component_dir=Path("components/ui"),
    )

    with (
        patch("starui.cli.dev.get_project_config", return_value=config),
        patch("starui.cli.dev.resolve_port", return_value=(5001, "Port 5000 in use, using 5001")),
        patch("starui.cli.dev.setup_tailwind", return_value=tmp_path / "input.css"),
        patch("starui.cli.dev.wait_for_css"),
        patch("starui.cli.dev.show_status"),
        patch("starui.cli.dev.ProcessManager") as mock_pm_cls,
        patch("starui.cli.dev.console") as mock_console,
        patch("starui.cli.dev.success"),
        patch("starui.cli.dev.error"),
    ):
        mock_pm_cls.return_value.wait_for_any_exit.side_effect = KeyboardInterrupt
        dev_command(app_file=str(app_file))

        # Find the call that printed the port message
        printed_texts = [str(call) for call in mock_console.print.call_args_list]
        assert any("Port 5000 in use, using 5001" in text for text in printed_texts)


def test_dev_command_setup_tailwind_fails_cleanup_runs(tmp_path):
    """When setup_tailwind raises, dev_command exits with error and cleanup still runs."""
    app_file = tmp_path / "app.py"
    app_file.write_text("app = 1")

    config = ProjectConfig(
        project_root=tmp_path,
        css_output=Path("static/css/starui.css"),
        component_dir=Path("components/ui"),
    )

    with (
        patch("starui.cli.dev.get_project_config", return_value=config),
        patch("starui.cli.dev.resolve_port", return_value=(5000, None)),
        patch("starui.cli.dev.setup_tailwind", side_effect=RuntimeError("tailwind broke")),
        patch("starui.cli.dev.ProcessManager") as mock_pm_cls,
        patch("starui.cli.dev.error") as mock_error,
        patch("starui.cli.dev.console"),
    ):
        manager = mock_pm_cls.return_value
        with pytest.raises(Exit):
            dev_command(app_file=str(app_file))

        msg = mock_error.call_args[0][0]
        assert "Dev server error" in msg
        # Cleanup should have been called (stop_all runs in finally block)
        assert manager.stop_all.called


def test_dev_command_keyboard_interrupt_graceful_shutdown(tmp_path):
    """KeyboardInterrupt during wait_for_any_exit triggers graceful shutdown."""
    app_file = tmp_path / "app.py"
    app_file.write_text("app = 1")

    config = ProjectConfig(
        project_root=tmp_path,
        css_output=Path("static/css/starui.css"),
        component_dir=Path("components/ui"),
    )

    with (
        patch("starui.cli.dev.get_project_config", return_value=config),
        patch("starui.cli.dev.resolve_port", return_value=(5000, None)),
        patch("starui.cli.dev.setup_tailwind", return_value=tmp_path / "input.css"),
        patch("starui.cli.dev.wait_for_css"),
        patch("starui.cli.dev.show_status"),
        patch("starui.cli.dev.ProcessManager") as mock_pm_cls,
        patch("starui.cli.dev.console") as mock_console,
        patch("starui.cli.dev.success"),
        patch("starui.cli.dev.error"),
    ):
        manager = mock_pm_cls.return_value
        manager.wait_for_any_exit.side_effect = KeyboardInterrupt

        dev_command(app_file=str(app_file))

        # Verify shutdown message was printed
        printed_texts = [str(call) for call in mock_console.print.call_args_list]
        assert any("Shutting down" in text for text in printed_texts)
        # Verify stop_all was called for cleanup
        assert manager.stop_all.called


def test_dev_command_temp_files_cleaned_up(tmp_path):
    """Temp CSS files in the output directory are cleaned up on exit."""
    app_file = tmp_path / "app.py"
    app_file.write_text("app = 1")

    css_dir = tmp_path / "static" / "css"
    css_dir.mkdir(parents=True)

    # Create a temp file that matches the cleanup glob pattern
    temp_css = css_dir / "tmpABCDEF.css"
    temp_css.write_text("/* temp */")

    config = ProjectConfig(
        project_root=tmp_path,
        css_output=Path("static/css/starui.css"),
        component_dir=Path("components/ui"),
    )

    with (
        patch("starui.cli.dev.get_project_config", return_value=config),
        patch("starui.cli.dev.resolve_port", return_value=(5000, None)),
        patch("starui.cli.dev.setup_tailwind", return_value=tmp_path / "input.css"),
        patch("starui.cli.dev.wait_for_css"),
        patch("starui.cli.dev.show_status"),
        patch("starui.cli.dev.ProcessManager") as mock_pm_cls,
        patch("starui.cli.dev.console"),
        patch("starui.cli.dev.success"),
        patch("starui.cli.dev.error"),
    ):
        manager = mock_pm_cls.return_value
        manager.wait_for_any_exit.side_effect = KeyboardInterrupt

        dev_command(app_file=str(app_file))

    # The temp file should have been cleaned up
    assert not temp_css.exists()


def test_dev_command_tmp_input_css_tracked_for_cleanup(tmp_path):
    """If setup_tailwind returns a path starting with 'tmp', it gets cleaned up."""
    app_file = tmp_path / "app.py"
    app_file.write_text("app = 1")

    css_dir = tmp_path / "static" / "css"
    css_dir.mkdir(parents=True)
    tmp_input = css_dir / "tmpXYZ123.css"
    tmp_input.write_text("/* temp input */")

    config = ProjectConfig(
        project_root=tmp_path,
        css_output=Path("static/css/starui.css"),
        component_dir=Path("components/ui"),
    )

    with (
        patch("starui.cli.dev.get_project_config", return_value=config),
        patch("starui.cli.dev.resolve_port", return_value=(5000, None)),
        patch("starui.cli.dev.setup_tailwind", return_value=tmp_input),
        patch("starui.cli.dev.wait_for_css"),
        patch("starui.cli.dev.show_status"),
        patch("starui.cli.dev.ProcessManager") as mock_pm_cls,
        patch("starui.cli.dev.console"),
        patch("starui.cli.dev.success"),
        patch("starui.cli.dev.error"),
    ):
        manager = mock_pm_cls.return_value
        manager.wait_for_any_exit.side_effect = KeyboardInterrupt

        dev_command(app_file=str(app_file))

    # The tmp input CSS should be removed by cleanup
    assert not tmp_input.exists()
