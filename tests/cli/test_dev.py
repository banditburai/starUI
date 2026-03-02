from pathlib import Path
from unittest.mock import patch

import pytest
from click.exceptions import Exit

from starui.cli.dev import cleanup, get_or_create_css_input, wait_for_css
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
def test_wait_for_css_returns_when_file_exists(mock_success, tmp_path):
    css_path = tmp_path / "test.css"
    css_path.write_text("/* css */")

    # Should return without raising
    wait_for_css(css_path)


@patch("starui.cli.dev.error")
@patch("starui.cli.dev.console")
@patch("time.sleep")
def test_wait_for_css_raises_exit_on_timeout(mock_sleep, mock_console, mock_error, tmp_path):
    css_path = tmp_path / "nonexistent.css"

    with pytest.raises(Exit):
        wait_for_css(css_path, timeout=0.1)
