"""Tests for the list command."""

from io import StringIO
from unittest.mock import MagicMock, patch

import pytest
from click.exceptions import Exit
from rich.console import Console

from starui.cli.list import get_category, is_installed, list_command


class TestGetCategory:
    def test_name_match(self):
        assert get_category({"name": "button", "description": ""}) == "ui"

    def test_description_match(self):
        assert (
            get_category({"name": "my_widget", "description": "A toast notification"})
            == "feedback"
        )

    def test_returns_none_for_unknown(self):
        assert (
            get_category({"name": "utils", "description": "Utility functions"}) is None
        )

    def test_overlay_category(self):
        assert (
            get_category({"name": "dialog", "description": "Modal dialog"}) == "overlay"
        )


class TestIsInstalled:
    def test_returns_true_when_file_exists(self, tmp_path, monkeypatch):
        (tmp_path / "components" / "ui").mkdir(parents=True)
        (tmp_path / "components" / "ui" / "button.py").write_text("# btn")
        monkeypatch.chdir(tmp_path)

        assert is_installed("button") is True

    def test_returns_false_when_not_found(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)

        assert is_installed("button") is False

    def test_finds_in_alternative_ui_dir(self, tmp_path, monkeypatch):
        (tmp_path / "ui").mkdir()
        (tmp_path / "ui" / "card.py").write_text("# card")
        monkeypatch.chdir(tmp_path)

        assert is_installed("card") is True


def _mock_client(components: list[dict]):
    """Create a mock RegistryClient with given component metadata."""
    client = MagicMock()
    client.list_components.return_value = [c["name"] for c in components]
    client.get_component_metadata.side_effect = lambda name: next(
        c for c in components if c["name"] == name
    )
    return client


def _render_console(mock_console) -> str:
    """Render all console.print calls to a plain-text string."""
    buf = StringIO()
    real_console = Console(file=buf, width=120, no_color=True)
    for call in mock_console.print.call_args_list:
        real_console.print(*call.args, **call.kwargs)
    return buf.getvalue()


TWO_COMPONENTS = [
    {
        "name": "button",
        "description": "Button with variants",
        "dependencies": ["utils"],
    },
    {"name": "badge", "description": "Badge for labels", "dependencies": ["utils"]},
]


class TestListCommand:
    def test_displays_all_components(self):
        client = _mock_client(TWO_COMPONENTS)

        with (
            patch("starui.cli.list.RegistryClient", return_value=client),
            patch("starui.cli.list.is_installed", return_value=False),
            patch("starui.cli.list.console") as mock_console,
        ):
            list_command(category=None, search=None, installed=False, verbose=False)

        output = _render_console(mock_console)
        assert "button" in output
        assert "badge" in output

    def test_empty_registry_shows_info_message(self):
        client = MagicMock()
        client.list_components.return_value = []

        with (
            patch("starui.cli.list.RegistryClient", return_value=client),
            patch("starui.cli.list.console"),
            patch("starui.cli.list.info") as mock_info,
        ):
            list_command(category=None, search=None, installed=False, verbose=False)

        mock_info.assert_called_once_with("No components found")

    def test_search_filters_by_name(self):
        client = _mock_client(TWO_COMPONENTS)

        with (
            patch("starui.cli.list.RegistryClient", return_value=client),
            patch("starui.cli.list.is_installed", return_value=False),
            patch("starui.cli.list.console") as mock_console,
        ):
            list_command(category=None, search="button", installed=False, verbose=False)

        output = _render_console(mock_console)
        assert "button" in output
        assert "badge" not in output.split("Showing")[0]

    def test_search_matches_description(self):
        client = _mock_client(TWO_COMPONENTS)

        with (
            patch("starui.cli.list.RegistryClient", return_value=client),
            patch("starui.cli.list.is_installed", return_value=False),
            patch("starui.cli.list.console") as mock_console,
        ):
            list_command(category=None, search="labels", installed=False, verbose=False)

        output = _render_console(mock_console)
        assert "badge" in output
        assert "button" not in output.split("Showing")[0]

    def test_installed_filter_shows_only_installed(self):
        client = _mock_client(TWO_COMPONENTS)

        with (
            patch("starui.cli.list.RegistryClient", return_value=client),
            patch("starui.cli.list.is_installed", side_effect=lambda n: n == "button"),
            patch("starui.cli.list.console") as mock_console,
        ):
            list_command(category=None, search=None, installed=True, verbose=False)

        output = _render_console(mock_console)
        assert "button" in output
        assert "badge" not in output.split("Showing")[0]

    def test_category_filter(self):
        components = [
            {"name": "button", "description": "A button", "dependencies": []},
            {"name": "dialog", "description": "Modal dialog", "dependencies": []},
        ]
        client = _mock_client(components)

        with (
            patch("starui.cli.list.RegistryClient", return_value=client),
            patch("starui.cli.list.is_installed", return_value=False),
            patch("starui.cli.list.console") as mock_console,
        ):
            list_command(
                category="overlay", search=None, installed=False, verbose=False
            )

        output = _render_console(mock_console)
        assert "dialog" in output
        assert "button" not in output.split("Showing")[0]

    def test_no_matches_shows_info(self):
        client = _mock_client(TWO_COMPONENTS)

        with (
            patch("starui.cli.list.RegistryClient", return_value=client),
            patch("starui.cli.list.is_installed", return_value=False),
            patch("starui.cli.list.console"),
            patch("starui.cli.list.info") as mock_info,
        ):
            list_command(
                category=None, search="zzz_nonexistent", installed=False, verbose=False
            )

        mock_info.assert_called_with("No components match filters")

    def test_metadata_error_skips_component_and_continues(self):
        client = MagicMock()
        client.list_components.return_value = ["good", "bad"]

        def get_meta(name):
            if name == "bad":
                raise RuntimeError("fail")
            return {"name": "good", "description": "Good one", "dependencies": []}

        client.get_component_metadata.side_effect = get_meta

        with (
            patch("starui.cli.list.RegistryClient", return_value=client),
            patch("starui.cli.list.is_installed", return_value=False),
            patch("starui.cli.list.console") as mock_console,
            patch("starui.cli.list.error") as mock_error,
        ):
            list_command(category=None, search=None, installed=False, verbose=False)

        mock_error.assert_called_once()
        assert "bad" in mock_error.call_args[0][0]
        output = _render_console(mock_console)
        assert "good" in output

    def test_registry_error_raises_exit(self):
        with (
            patch(
                "starui.cli.list.RegistryClient",
                side_effect=RuntimeError("network error"),
            ),
            patch("starui.cli.list.console"),
            patch("starui.cli.list.error"),
            pytest.raises(Exit),
        ):
            list_command(category=None, search=None, installed=False, verbose=False)

    def test_verbose_shows_detailed_output(self):
        client = _mock_client(TWO_COMPONENTS)

        with (
            patch("starui.cli.list.RegistryClient", return_value=client),
            patch("starui.cli.list.is_installed", return_value=True),
            patch("starui.cli.list.console") as mock_console,
        ):
            list_command(category=None, search=None, installed=False, verbose=True)

        output = _render_console(mock_console)
        assert "button" in output
        assert "(installed)" in output
