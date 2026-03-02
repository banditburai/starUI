from io import StringIO
from unittest.mock import MagicMock, patch

import pytest
from click.exceptions import Exit
from rich.console import Console

from starui.cli.list import list_command


def _mock_client(components: list[dict]):
    client = MagicMock()
    client.list_components.return_value = [c["name"] for c in components]
    client.get_component_metadata.side_effect = lambda name: next(c for c in components if c["name"] == name)
    return client


def _render_console(mock_console) -> str:
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


def _mock_manifest(installed_names: set[str] | None = None):
    manifest = MagicMock()
    manifest.get_installed.return_value = {n: {} for n in (installed_names or set())}
    return manifest


class TestListCommand:
    def test_displays_all_components(self):
        client = _mock_client(TWO_COMPONENTS)

        with (
            patch("starui.cli.list.get_project_config"),
            patch("starui.cli.list.Manifest", return_value=_mock_manifest()),
            patch("starui.cli.list.RegistryClient", return_value=client),
            patch("starui.cli.list.console") as mock_console,
        ):
            list_command(search=None, installed=False, verbose=False)

        output = _render_console(mock_console)
        assert "button" in output
        assert "badge" in output

    def test_empty_registry_shows_info_message(self):
        client = MagicMock()
        client.list_components.return_value = []

        with (
            patch("starui.cli.list.get_project_config"),
            patch("starui.cli.list.Manifest", return_value=_mock_manifest()),
            patch("starui.cli.list.RegistryClient", return_value=client),
            patch("starui.cli.list.console"),
            patch("starui.cli.list.info") as mock_info,
        ):
            list_command(search=None, installed=False, verbose=False)

        mock_info.assert_called_once_with("No components found")

    def test_search_filters_by_name(self):
        client = _mock_client(TWO_COMPONENTS)

        with (
            patch("starui.cli.list.get_project_config"),
            patch("starui.cli.list.Manifest", return_value=_mock_manifest()),
            patch("starui.cli.list.RegistryClient", return_value=client),
            patch("starui.cli.list.console") as mock_console,
        ):
            list_command(search="button", installed=False, verbose=False)

        output = _render_console(mock_console)
        assert "button" in output
        assert "badge" not in output.split("Showing")[0]

    def test_search_matches_description(self):
        client = _mock_client(TWO_COMPONENTS)

        with (
            patch("starui.cli.list.get_project_config"),
            patch("starui.cli.list.Manifest", return_value=_mock_manifest()),
            patch("starui.cli.list.RegistryClient", return_value=client),
            patch("starui.cli.list.console") as mock_console,
        ):
            list_command(search="labels", installed=False, verbose=False)

        output = _render_console(mock_console)
        assert "badge" in output
        assert "button" not in output.split("Showing")[0]

    def test_installed_filter_shows_only_installed(self):
        client = _mock_client(TWO_COMPONENTS)

        with (
            patch("starui.cli.list.get_project_config"),
            patch("starui.cli.list.Manifest", return_value=_mock_manifest({"button"})),
            patch("starui.cli.list.RegistryClient", return_value=client),
            patch("starui.cli.list.console") as mock_console,
        ):
            list_command(search=None, installed=True, verbose=False)

        output = _render_console(mock_console)
        assert "button" in output
        assert "badge" not in output.split("Showing")[0]

    def test_no_matches_shows_info(self):
        client = _mock_client(TWO_COMPONENTS)

        with (
            patch("starui.cli.list.get_project_config"),
            patch("starui.cli.list.Manifest", return_value=_mock_manifest()),
            patch("starui.cli.list.RegistryClient", return_value=client),
            patch("starui.cli.list.console"),
            patch("starui.cli.list.info") as mock_info,
        ):
            list_command(search="zzz_nonexistent", installed=False, verbose=False)

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
            patch("starui.cli.list.get_project_config"),
            patch("starui.cli.list.Manifest", return_value=_mock_manifest()),
            patch("starui.cli.list.RegistryClient", return_value=client),
            patch("starui.cli.list.console") as mock_console,
            patch("starui.cli.list.error") as mock_error,
        ):
            list_command(search=None, installed=False, verbose=False)

        mock_error.assert_called_once()
        assert "bad" in mock_error.call_args[0][0]
        output = _render_console(mock_console)
        assert "good" in output

    def test_registry_error_raises_exit(self):
        with (
            patch("starui.cli.list.get_project_config"),
            patch("starui.cli.list.Manifest", return_value=_mock_manifest()),
            patch(
                "starui.cli.list.RegistryClient",
                side_effect=RuntimeError("network error"),
            ),
            patch("starui.cli.list.console"),
            patch("starui.cli.list.error"),
            pytest.raises(Exit),
        ):
            list_command(search=None, installed=False, verbose=False)

    def test_verbose_shows_detailed_output(self):
        client = _mock_client(TWO_COMPONENTS)

        with (
            patch("starui.cli.list.get_project_config"),
            patch("starui.cli.list.Manifest", return_value=_mock_manifest({"button", "badge"})),
            patch("starui.cli.list.RegistryClient", return_value=client),
            patch("starui.cli.list.console") as mock_console,
        ):
            list_command(search=None, installed=False, verbose=True)

        output = _render_console(mock_console)
        assert "button" in output
        assert "(installed)" in output
