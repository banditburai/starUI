"""Tests for the init command."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from click.exceptions import Exit

from starui.cli.init import (
    create_app,
    create_config_file,
    create_css_input,
    setup_directories,
    update_gitignore,
    validate_project,
)
from starui.config import ProjectConfig


class TestValidateProject:
    def test_clean_dir_passes(self, tmp_path):
        validate_project(tmp_path)

    def test_existing_starui_py_raises_exit(self, project):
        (project.project_root / "starui.py").write_text("# config")

        with pytest.raises(Exit):
            validate_project(project.project_root)

    def test_nonempty_components_ui_raises_exit(self, project):
        (project.component_dir_absolute / "button.py").write_text("# btn")

        with pytest.raises(Exit):
            validate_project(project.project_root)

    def test_nonempty_ui_dir_raises_exit(self, tmp_path):
        ui_dir = tmp_path / "ui"
        ui_dir.mkdir()
        (ui_dir / "button.py").write_text("# btn")

        with pytest.raises(Exit):
            validate_project(tmp_path)

    def test_empty_components_ui_passes(self, tmp_path):
        (tmp_path / "components" / "ui").mkdir(parents=True)
        validate_project(tmp_path)

    def test_force_skips_validation(self, project):
        (project.project_root / "starui.py").write_text("# config")
        (project.component_dir_absolute / "button.py").write_text("# btn")

        validate_project(project.project_root, force=True)


class TestSetupDirectories:
    def test_creates_all_dirs_and_init_py(self, tmp_path):
        config = ProjectConfig(
            project_root=tmp_path,
            css_output=Path("static/css/starui.css"),
            component_dir=Path("components/ui"),
        )

        setup_directories(config)

        assert config.component_dir_absolute.is_dir()
        assert (config.component_dir_absolute / "__init__.py").exists()
        assert config.css_output_absolute.parent.is_dir()
        assert (tmp_path / "static" / "css").is_dir()

    def test_idempotent(self, tmp_path):
        config = ProjectConfig(
            project_root=tmp_path,
            css_output=Path("static/css/starui.css"),
            component_dir=Path("components/ui"),
        )

        setup_directories(config)
        setup_directories(config)

        assert config.component_dir_absolute.is_dir()
        assert (config.component_dir_absolute / "__init__.py").exists()
        assert config.css_output_absolute.parent.is_dir()
        assert (tmp_path / "static" / "css").is_dir()


class TestCreateCssInput:
    def test_writes_input_css_with_template(self, project):
        create_css_input(project)

        input_css = project.project_root / "static" / "css" / "input.css"
        assert input_css.exists()
        content = input_css.read_text()
        assert '@import "tailwindcss"' in content
        assert "@theme {" in content
        assert ":root {" in content
        assert ".dark" in content


class TestAddDefaultComponents:
    def test_writes_utils_and_deps_with_correct_content(self, project):
        from starui.cli.init import add_default_components

        mock_client = MagicMock()
        mock_client.get_component_source.return_value = "# utils source"

        mock_loader = MagicMock()
        mock_loader.load_component_with_dependencies.return_value = {
            "theme_toggle": "# toggle",
            "button": "# button",
        }

        with (
            patch("starui.cli.init.RegistryClient", return_value=mock_client),
            patch("starui.cli.init.ComponentLoader", return_value=mock_loader),
        ):
            add_default_components(project)

        comp_dir = project.component_dir_absolute
        assert comp_dir / "utils.py"
        assert (comp_dir / "utils.py").read_text() == "# utils source"
        assert (comp_dir / "theme_toggle.py").read_text() == "# toggle"
        assert (comp_dir / "button.py").read_text() == "# button"

    def test_exception_swallowed(self, project):
        from starui.cli.init import add_default_components

        with patch(
            "starui.cli.init.RegistryClient", side_effect=RuntimeError("network error")
        ):
            add_default_components(project, verbose=True)

        assert not (project.component_dir_absolute / "utils.py").exists()


class TestCreateApp:
    def test_creates_app_py_with_correct_css_path(self, project):
        create_app(project)

        app_path = project.project_root / "app.py"
        assert app_path.exists()
        content = app_path.read_text()
        assert "star_app" in content
        assert "/static/css/starui.css" in content

    def test_skips_if_app_exists(self, project):
        app_path = project.project_root / "app.py"
        app_path.write_text("# my existing app")

        create_app(project)

        assert app_path.read_text() == "# my existing app"


class TestUpdateGitignore:
    def test_creates_new_gitignore(self, project):
        update_gitignore(project)

        gitignore = project.project_root / ".gitignore"
        assert gitignore.exists()
        content = gitignore.read_text()
        assert "# StarUI generated files" in content
        assert ".starui/" in content
        assert "static/css/starui.css" in content

    def test_appends_without_duplicating(self, project):
        gitignore = project.project_root / ".gitignore"
        gitignore.write_text("__pycache__/\n")

        update_gitignore(project)

        content = gitignore.read_text()
        assert content.startswith("__pycache__/\n")
        assert "# StarUI generated files" in content

    def test_appends_newline_if_missing(self, project):
        gitignore = project.project_root / ".gitignore"
        gitignore.write_text("__pycache__")  # no trailing newline

        update_gitignore(project)

        content = gitignore.read_text()
        # Should have newline between old content and StarUI block
        assert "__pycache__\n" in content
        assert "# StarUI generated files" in content

    def test_skips_if_patterns_already_present(self, project):
        gitignore = project.project_root / ".gitignore"
        original = "# StarUI generated files\n.starui/\n"
        gitignore.write_text(original)

        update_gitignore(project)

        assert gitignore.read_text() == original


class TestCreateConfigFile:
    def test_creates_starui_py_with_correct_paths(self, project):
        create_config_file(project)

        config_path = project.project_root / "starui.py"
        assert config_path.exists()
        content = config_path.read_text()
        assert 'CSS_OUTPUT = Path("static/css/starui.css")' in content
        assert 'COMPONENT_DIR = Path("components/ui")' in content

    def test_skips_if_already_exists(self, project):
        config_path = project.project_root / "starui.py"
        config_path.write_text("# existing config")

        create_config_file(project)

        assert config_path.read_text() == "# existing config"


class TestInitCommand:
    def test_full_init_creates_all_files(self, project, monkeypatch):
        from starui.cli.init import init_command

        monkeypatch.chdir(project.project_root)

        mock_client = MagicMock()
        mock_client.get_component_source.return_value = "# utils"

        mock_loader = MagicMock()
        mock_loader.load_component_with_dependencies.return_value = {
            "theme_toggle": "# toggle",
        }

        with (
            patch("starui.cli.init.detect_project_config", return_value=project),
            patch("starui.cli.init.RegistryClient", return_value=mock_client),
            patch("starui.cli.init.ComponentLoader", return_value=mock_loader),
            patch("starui.cli.init.console"),
        ):
            init_command(force=True, verbose=True, config=False)

        root = project.project_root
        assert (root / "static" / "css" / "input.css").exists()
        assert (root / "app.py").exists()
        assert (root / ".gitignore").exists()
        assert (root / "components" / "ui" / "utils.py").exists()
        assert (root / "components" / "ui" / "theme_toggle.py").exists()
        assert not (root / "starui.py").exists()

    def test_init_with_config_flag_creates_starui_py(self, project, monkeypatch):
        from starui.cli.init import init_command

        monkeypatch.chdir(project.project_root)

        mock_client = MagicMock()
        mock_client.get_component_source.return_value = "# utils"

        mock_loader = MagicMock()
        mock_loader.load_component_with_dependencies.return_value = {}

        with (
            patch("starui.cli.init.detect_project_config", return_value=project),
            patch("starui.cli.init.RegistryClient", return_value=mock_client),
            patch("starui.cli.init.ComponentLoader", return_value=mock_loader),
            patch("starui.cli.init.console"),
        ):
            init_command(force=True, verbose=True, config=True)

        config_path = project.project_root / "starui.py"
        assert config_path.exists()
        assert "CSS_OUTPUT" in config_path.read_text()

    def test_init_error_raises_exit(self, monkeypatch, tmp_path):
        from starui.cli.init import init_command

        monkeypatch.chdir(tmp_path)

        with (
            patch(
                "starui.cli.init.detect_project_config",
                side_effect=RuntimeError("boom"),
            ),
            patch("starui.cli.init.console"),
            pytest.raises(Exit),
        ):
            init_command(force=True, verbose=False, config=False)
