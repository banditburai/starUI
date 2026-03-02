from unittest.mock import MagicMock, patch

import pytest
import typer
from typer.testing import CliRunner

from starui.cli.diff import diff_command
from starui.cli.status import status_command
from starui.cli.update import update_command
from starui.registry.checksum import compute_checksum
from starui.registry.manifest import Manifest


@pytest.fixture
def cli():
    app = typer.Typer()
    app.command("status")(status_command)
    app.command("diff")(diff_command)
    app.command("update")(update_command)
    return CliRunner(), app


@pytest.fixture
def project(tmp_path):
    comp_dir = tmp_path / "components" / "ui"
    comp_dir.mkdir(parents=True)
    return tmp_path, comp_dir


@pytest.fixture
def config(project):
    root, comp_dir = project
    cfg = MagicMock()
    cfg.project_root = root
    cfg.component_dir_absolute = comp_dir
    return cfg


def _install_component(root, comp_dir, name, source, version="0.3.0"):
    comp_file = comp_dir / f"{name}.py"
    comp_file.write_text(source)
    checksum = compute_checksum(source)

    manifest = Manifest(root)
    manifest.record_install(
        name,
        version=version,
        checksum=checksum,
        file_path=str(comp_file.relative_to(root)),
    )
    manifest.save()
    return checksum


class TestStatusCommand:
    @patch("starui.cli.status.RegistryClient")
    @patch("starui.cli.status.get_project_config")
    def test_no_manifest_shows_help(self, mock_config_fn, mock_client_cls, cli, config):
        runner, app = cli
        mock_config_fn.return_value = config

        result = runner.invoke(app, ["status"])
        assert result.exit_code == 0
        assert "star init" in result.output or "star add" in result.output

    @patch("starui.cli.status.RegistryClient")
    @patch("starui.cli.status.get_project_config")
    def test_shows_up_to_date_component(self, mock_config_fn, mock_client_cls, cli, project, config):
        runner, app = cli
        root, comp_dir = project
        mock_config_fn.return_value = config

        source = "def Button(): pass\n"
        checksum = _install_component(root, comp_dir, "button", source)

        mock_client = MagicMock()
        mock_client.get_component_metadata.return_value = {"checksum": checksum}
        mock_client_cls.return_value = mock_client

        result = runner.invoke(app, ["status"])
        assert result.exit_code == 0
        assert "button" in result.output
        assert "Up to date" in result.output

    @patch("starui.cli.status.RegistryClient")
    @patch("starui.cli.status.get_project_config")
    def test_shows_modified_component(self, mock_config_fn, mock_client_cls, cli, project, config):
        runner, app = cli
        root, comp_dir = project
        mock_config_fn.return_value = config

        _install_component(root, comp_dir, "button", "def Button(): pass\n")
        (comp_dir / "button.py").write_text("def Button(): return 'custom'\n")

        mock_client = MagicMock()
        mock_client.get_component_metadata.side_effect = FileNotFoundError
        mock_client_cls.return_value = mock_client

        result = runner.invoke(app, ["status"])
        assert result.exit_code == 0
        assert "Modified" in result.output

    @patch("starui.cli.status.RegistryClient")
    @patch("starui.cli.status.get_project_config")
    def test_shows_missing_component(self, mock_config_fn, mock_client_cls, cli, project, config):
        runner, app = cli
        root, comp_dir = project
        mock_config_fn.return_value = config

        _install_component(root, comp_dir, "button", "def Button(): pass\n")
        (comp_dir / "button.py").unlink()

        mock_client = MagicMock()
        mock_client.get_component_metadata.side_effect = FileNotFoundError
        mock_client_cls.return_value = mock_client

        result = runner.invoke(app, ["status"])
        assert result.exit_code == 0
        assert "Missing" in result.output

    @patch("starui.cli.status.RegistryClient")
    @patch("starui.cli.status.get_project_config")
    def test_shows_update_available(self, mock_config_fn, mock_client_cls, cli, project, config):
        runner, app = cli
        root, comp_dir = project
        mock_config_fn.return_value = config

        _install_component(root, comp_dir, "button", "def Button(): pass\n")

        mock_client = MagicMock()
        mock_client.get_component_metadata.return_value = {"checksum": "sha256:newer_version"}
        mock_client_cls.return_value = mock_client

        result = runner.invoke(app, ["status"])
        assert result.exit_code == 0
        assert "Update available" in result.output
        assert "star update" in result.output

    @patch("starui.cli.status.RegistryClient")
    @patch("starui.cli.status.get_project_config")
    def test_no_components_installed(self, mock_config_fn, mock_client_cls, cli, project, config):
        runner, app = cli
        root, _ = project
        mock_config_fn.return_value = config

        manifest = Manifest(root)
        manifest.save()

        result = runner.invoke(app, ["status"])
        assert result.exit_code == 0
        assert "No components installed" in result.output

    @patch("starui.cli.status.RegistryClient")
    @patch("starui.cli.status.get_project_config")
    def test_offline_mode_still_works(self, mock_config_fn, mock_client_cls, cli, project, config):
        runner, app = cli
        root, comp_dir = project
        mock_config_fn.return_value = config

        _install_component(root, comp_dir, "button", "def Button(): pass\n")
        mock_client_cls.side_effect = Exception("offline")

        result = runner.invoke(app, ["status"])
        assert result.exit_code == 0
        assert "button" in result.output

    @patch("starui.cli.status.RegistryClient")
    @patch("starui.cli.status.get_project_config")
    def test_summary_counts(self, mock_config_fn, mock_client_cls, cli, project, config):
        runner, app = cli
        root, comp_dir = project
        mock_config_fn.return_value = config

        btn_checksum = _install_component(root, comp_dir, "button", "def Button(): pass\n")
        _install_component(root, comp_dir, "dialog", "def Dialog(): pass\n")
        (comp_dir / "dialog.py").write_text("def Dialog(): return 'custom'\n")
        _install_component(root, comp_dir, "select", "def Select(): pass\n")

        mock_client = MagicMock()

        def _mock_meta(name):
            if name == "button":
                return {"checksum": btn_checksum}
            if name == "select":
                return {"checksum": "sha256:newer_version"}
            raise FileNotFoundError(name)

        mock_client.get_component_metadata.side_effect = _mock_meta
        mock_client_cls.return_value = mock_client

        result = runner.invoke(app, ["status"])
        assert "3 installed" in result.output
        assert "1 modified" in result.output
        assert "1 updates available" in result.output


class TestDiffCommand:
    @patch("starui.cli.diff.RegistryClient")
    @patch("starui.cli.diff.get_project_config")
    def test_no_diff_when_identical(self, mock_config_fn, mock_client_cls, cli, project, config):
        runner, app = cli
        _, comp_dir = project
        mock_config_fn.return_value = config

        source = "def Button(): pass\n"
        (comp_dir / "button.py").write_text(source)

        mock_client = MagicMock()
        mock_client.get_component_source.return_value = source
        mock_client_cls.return_value = mock_client

        result = runner.invoke(app, ["diff", "button"])
        assert result.exit_code == 0
        assert "no differences" in result.output

    @patch("starui.cli.diff.RegistryClient")
    @patch("starui.cli.diff.get_project_config")
    def test_shows_diff_content(self, mock_config_fn, mock_client_cls, cli, project, config):
        runner, app = cli
        _, comp_dir = project
        mock_config_fn.return_value = config

        (comp_dir / "button.py").write_text("def Button(): return 'custom'\n")

        mock_client = MagicMock()
        mock_client.get_component_source.return_value = "def Button(): pass\n"
        mock_client_cls.return_value = mock_client

        result = runner.invoke(app, ["diff", "button"])
        assert result.exit_code == 0
        assert "registry/button.py" in result.output
        assert "local/button.py" in result.output
        assert "-def Button(): pass" in result.output
        assert "+def Button(): return 'custom'" in result.output

    @patch("starui.cli.diff.get_project_config")
    def test_error_when_not_installed_locally(self, mock_config_fn, cli, config):
        runner, app = cli
        mock_config_fn.return_value = config

        result = runner.invoke(app, ["diff", "nonexistent"])
        assert result.exit_code != 0

    @patch("starui.cli.diff.RegistryClient")
    @patch("starui.cli.diff.get_project_config")
    def test_error_when_not_in_registry(self, mock_config_fn, mock_client_cls, cli, project, config):
        runner, app = cli
        _, comp_dir = project
        mock_config_fn.return_value = config

        (comp_dir / "custom.py").write_text("def Custom(): pass\n")

        mock_client = MagicMock()
        mock_client.get_component_source.side_effect = FileNotFoundError("not in registry")
        mock_client_cls.return_value = mock_client

        result = runner.invoke(app, ["diff", "custom"])
        assert result.exit_code != 0

    @patch("starui.cli.diff.RegistryClient")
    @patch("starui.cli.diff.get_project_config")
    def test_hyphenated_name_normalized(self, mock_config_fn, mock_client_cls, cli, project, config):
        runner, app = cli
        _, comp_dir = project
        mock_config_fn.return_value = config

        source = "def DatePicker(): pass\n"
        (comp_dir / "date_picker.py").write_text(source)

        mock_client = MagicMock()
        mock_client.get_component_source.return_value = source
        mock_client_cls.return_value = mock_client

        result = runner.invoke(app, ["diff", "date-picker"])
        assert result.exit_code == 0
        assert "no differences" in result.output
        mock_client.get_component_source.assert_called_with("date_picker")


class TestUpdateCommand:
    @patch("starui.cli.update.RegistryClient")
    @patch("starui.cli.update.get_project_config")
    def test_no_manifest_shows_help(self, mock_config_fn, mock_client_cls, cli, config):
        runner, app = cli
        mock_config_fn.return_value = config

        result = runner.invoke(app, ["update"])
        assert result.exit_code == 0
        assert "star init" in result.output or "star add" in result.output

    @patch("starui.cli.update.RegistryClient")
    @patch("starui.cli.update.get_project_config")
    def test_updates_component_on_disk(self, mock_config_fn, mock_client_cls, cli, project, config):
        runner, app = cli
        root, comp_dir = project
        mock_config_fn.return_value = config

        old_source = "def Button(): pass  # v1\n"
        new_source = "def Button(): pass  # v2\n"
        _install_component(root, comp_dir, "button", old_source, version="0.2.0")

        mock_client = MagicMock()
        mock_client.version = "main"
        mock_client.get_component_metadata.return_value = {"checksum": compute_checksum(new_source)}
        mock_client.get_component_source.return_value = new_source
        mock_client_cls.return_value = mock_client

        result = runner.invoke(app, ["update", "button"])
        assert result.exit_code == 0
        assert (comp_dir / "button.py").read_text() == new_source

        manifest = Manifest(root)
        assert manifest.get_installed()["button"]["checksum"] == compute_checksum(new_source)

    @patch("starui.cli.update.RegistryClient")
    @patch("starui.cli.update.get_project_config")
    def test_skips_modified_without_force(self, mock_config_fn, mock_client_cls, cli, project, config):
        runner, app = cli
        root, comp_dir = project
        mock_config_fn.return_value = config

        _install_component(root, comp_dir, "button", "def Button(): pass\n")
        modified = "def Button(): return 'my custom logic'\n"
        (comp_dir / "button.py").write_text(modified)

        mock_client = MagicMock()
        mock_client.version = "main"
        mock_client.get_component_metadata.return_value = {"checksum": "sha256:newer"}
        mock_client_cls.return_value = mock_client

        result = runner.invoke(app, ["update", "button"])
        assert result.exit_code == 0
        assert (comp_dir / "button.py").read_text() == modified
        assert "modified" in result.output.lower() or "skipping" in result.output.lower()

    @patch("starui.cli.update.RegistryClient")
    @patch("starui.cli.update.get_project_config")
    def test_force_overwrites_modified(self, mock_config_fn, mock_client_cls, cli, project, config):
        runner, app = cli
        root, comp_dir = project
        mock_config_fn.return_value = config

        _install_component(root, comp_dir, "button", "def Button(): pass\n")
        (comp_dir / "button.py").write_text("def Button(): return 'custom'\n")

        new_source = "def Button(): pass  # v2\n"
        mock_client = MagicMock()
        mock_client.version = "main"
        mock_client.get_component_metadata.return_value = {"checksum": compute_checksum(new_source)}
        mock_client.get_component_source.return_value = new_source
        mock_client_cls.return_value = mock_client

        result = runner.invoke(app, ["update", "button", "--force"])
        assert result.exit_code == 0
        assert (comp_dir / "button.py").read_text() == new_source

    @patch("starui.cli.update.RegistryClient")
    @patch("starui.cli.update.get_project_config")
    def test_already_up_to_date(self, mock_config_fn, mock_client_cls, cli, project, config):
        runner, app = cli
        root, comp_dir = project
        mock_config_fn.return_value = config

        source = "def Button(): pass\n"
        checksum = _install_component(root, comp_dir, "button", source)

        mock_client = MagicMock()
        mock_client.get_component_metadata.return_value = {"checksum": checksum}
        mock_client_cls.return_value = mock_client

        result = runner.invoke(app, ["update"])
        assert result.exit_code == 0
        assert "up to date" in result.output

    @patch("starui.cli.update.RegistryClient")
    @patch("starui.cli.update.get_project_config")
    def test_unknown_component_errors(self, mock_config_fn, mock_client_cls, cli, project, config):
        runner, app = cli
        root, comp_dir = project
        mock_config_fn.return_value = config

        _install_component(root, comp_dir, "button", "def Button(): pass\n")

        result = runner.invoke(app, ["update", "nonexistent"])
        assert result.exit_code != 0
        assert "Not installed" in result.output

    @patch("starui.cli.update.RegistryClient")
    @patch("starui.cli.update.get_project_config")
    def test_component_not_in_registry_skips(self, mock_config_fn, mock_client_cls, cli, project, config):
        runner, app = cli
        root, comp_dir = project
        mock_config_fn.return_value = config

        original_source = "def Custom(): pass\n"
        _install_component(root, comp_dir, "custom", original_source)

        mock_client = MagicMock()
        mock_client.get_component_metadata.side_effect = FileNotFoundError("not in registry")
        mock_client_cls.return_value = mock_client

        result = runner.invoke(app, ["update"])
        assert result.exit_code == 0
        assert (comp_dir / "custom.py").read_text() == original_source

    @patch("starui.cli.update.RegistryClient")
    @patch("starui.cli.update.get_project_config")
    def test_updates_multiple_components(self, mock_config_fn, mock_client_cls, cli, project, config):
        runner, app = cli
        root, comp_dir = project
        mock_config_fn.return_value = config

        _install_component(root, comp_dir, "button", "# v1\n", version="0.2.0")
        _install_component(root, comp_dir, "dialog", "# v1\n", version="0.2.0")

        new_button = "# v2 button\n"
        new_dialog = "# v2 dialog\n"

        def mock_metadata(name):
            return {"checksum": compute_checksum(new_button if name == "button" else new_dialog)}

        def mock_source(name):
            return new_button if name == "button" else new_dialog

        mock_client = MagicMock()
        mock_client.version = "main"
        mock_client.get_component_metadata.side_effect = mock_metadata
        mock_client.get_component_source.side_effect = mock_source
        mock_client_cls.return_value = mock_client

        result = runner.invoke(app, ["update", "button", "dialog"])
        assert result.exit_code == 0
        assert (comp_dir / "button.py").read_text() == new_button
        assert (comp_dir / "dialog.py").read_text() == new_dialog
