from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from click.exceptions import Exit

from starui.cli.init import (
    add_default_components,
    create_app,
    create_css_input,
    init_command,
    resolve_component_dir,
    setup_directories,
    update_gitignore,
    validate_project,
)
from starui.config import ProjectConfig


class TestValidateProject:
    def test_clean_dir_passes(self, tmp_path):
        validate_project(tmp_path)

    def test_nonempty_components_ui_raises_exit(self, project):
        (project.component_dir_absolute / "button.py").write_text("# btn")

        with pytest.raises(Exit):
            validate_project(project.project_root, component_dir="components/ui")

    def test_nonempty_ui_dir_raises_exit(self, tmp_path):
        ui_dir = tmp_path / "ui"
        ui_dir.mkdir()
        (ui_dir / "button.py").write_text("# btn")

        with pytest.raises(Exit):
            validate_project(tmp_path, component_dir="ui")

    def test_empty_components_ui_passes(self, tmp_path):
        (tmp_path / "components" / "ui").mkdir(parents=True)
        validate_project(tmp_path, component_dir="components/ui")

    def test_force_skips_validation(self, project):
        (project.component_dir_absolute / "button.py").write_text("# btn")

        validate_project(project.project_root, component_dir="components/ui", force=True)

    def test_custom_component_dir(self, tmp_path):
        custom_dir = tmp_path / "custom" / "path"
        custom_dir.mkdir(parents=True)
        (custom_dir / "widget.py").write_text("# widget")

        with pytest.raises(Exit):
            validate_project(tmp_path, component_dir="custom/path")

    def test_nonexistent_dir_passes(self, tmp_path):
        validate_project(tmp_path, component_dir="does/not/exist")


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
        assert config.css_dir_absolute.is_dir()

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
        assert config.css_dir_absolute.is_dir()

    def test_respects_custom_css_dir(self, tmp_path):
        config = ProjectConfig(
            project_root=tmp_path,
            css_output=Path("dist/starui.css"),
            component_dir=Path("components/ui"),
            css_dir=Path("assets/css"),
        )

        setup_directories(config)

        assert (tmp_path / "assets" / "css").is_dir()
        assert (tmp_path / "dist").is_dir()


class TestCreateCssInput:
    def test_writes_input_css_with_template(self, project):
        create_css_input(project)

        input_css = project.css_dir_absolute / "input.css"
        assert input_css.exists()
        content = input_css.read_text()
        assert '@import "tailwindcss"' in content
        assert "@theme {" in content
        assert ":root {" in content
        assert ".dark" in content

    def test_respects_custom_css_dir(self, tmp_path):
        css_dir = tmp_path / "assets" / "styles"
        css_dir.mkdir(parents=True)

        config = ProjectConfig(
            project_root=tmp_path,
            css_output=Path("dist/starui.css"),
            component_dir=Path("components/ui"),
            css_dir=Path("assets/styles"),
        )

        create_css_input(config)

        assert (css_dir / "input.css").exists()


class TestAddDefaultComponents:
    def test_writes_utils_and_deps_with_correct_content(self, project):
        mock_client = MagicMock()
        mock_client.get_source.return_value = "# utils source"
        mock_client.version = "main"
        mock_client.get_with_dependencies.return_value = (
            {"button": "# button"},
            "# toggle",
        )

        with (
            patch("starui.cli.init.RegistryClient", return_value=mock_client),
            patch("starui.cli.init.Manifest", return_value=MagicMock()),
        ):
            add_default_components(project)

        comp_dir = project.component_dir_absolute
        assert (comp_dir / "utils.py").exists()
        assert (comp_dir / "utils.py").read_text() == "# utils source"
        assert (comp_dir / "theme_toggle.py").read_text() == "# toggle"
        assert (comp_dir / "button.py").read_text() == "# button"

    def test_exception_swallowed(self, project):
        with patch("starui.cli.init.RegistryClient", side_effect=RuntimeError("network error")):
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


class TestInitCommand:
    def test_full_init_creates_project_structure(self, tmp_path, monkeypatch):
        """Integration test: init_command creates all expected files using real config resolution."""
        monkeypatch.chdir(tmp_path)

        # Simulate a realistic project: pyproject.toml + static/ dir
        (tmp_path / "pyproject.toml").write_text('[project]\nname = "test"\n')
        (tmp_path / "static").mkdir()

        mock_client = MagicMock()
        mock_client.get_source.return_value = "# utils"
        mock_client.version = "main"
        mock_client.get_with_dependencies.return_value = (
            {},
            "# toggle",
        )

        # Only mock the network boundary (RegistryClient) and console output
        with (
            patch("starui.cli.init.RegistryClient", return_value=mock_client),
            patch("starui.cli.init.console"),
        ):
            init_command(force=True, verbose=True, component_dir=None, no_interaction=True)

        # Verify all expected project files were created
        assert (tmp_path / "components" / "ui").is_dir()
        assert (tmp_path / "components" / "ui" / "__init__.py").exists()
        assert (tmp_path / "components" / "ui" / "utils.py").exists()
        assert (tmp_path / "components" / "ui" / "theme_toggle.py").exists()
        assert (tmp_path / "static" / "css" / "input.css").exists()
        assert (tmp_path / "app.py").exists()
        assert (tmp_path / ".gitignore").exists()

        # Verify config was persisted to pyproject.toml
        pyproject = (tmp_path / "pyproject.toml").read_text()
        assert "[tool.starui]" in pyproject
        assert 'component_dir = "components/ui"' in pyproject

    def test_init_with_custom_component_dir(self, tmp_path, monkeypatch):
        """init_command respects --component-dir flag in the created project structure."""
        monkeypatch.chdir(tmp_path)
        (tmp_path / "pyproject.toml").write_text('[project]\nname = "test"\n')

        mock_client = MagicMock()
        mock_client.get_source.return_value = "# utils"
        mock_client.version = "main"
        mock_client.get_with_dependencies.return_value = ({}, "")

        with (
            patch("starui.cli.init.RegistryClient", return_value=mock_client),
            patch("starui.cli.init.console"),
        ):
            init_command(force=True, verbose=False, component_dir="src/ui", no_interaction=True)

        assert (tmp_path / "src" / "ui").is_dir()
        assert (tmp_path / "src" / "ui" / "__init__.py").exists()
        assert (tmp_path / "src" / "ui" / "utils.py").exists()

        pyproject = (tmp_path / "pyproject.toml").read_text()
        assert 'component_dir = "src/ui"' in pyproject

    def test_init_error_raises_exit(self, monkeypatch, tmp_path):
        monkeypatch.chdir(tmp_path)

        with (
            patch(
                "starui.cli.init.load_pyproject_config",
                side_effect=RuntimeError("boom"),
            ),
            patch("starui.cli.init.console"),
            pytest.raises(Exit),
        ):
            init_command(force=True, verbose=False, component_dir=None, no_interaction=True)


class TestResolveComponentDir:
    def test_cli_flag_takes_priority(self, tmp_path):
        existing = ProjectConfig(
            project_root=tmp_path,
            css_output=Path("static/css/starui.css"),
            component_dir=Path("from/config"),
        )
        result = resolve_component_dir(tmp_path, "from/cli", existing, no_interaction=False)
        assert result == "from/cli"

    def test_existing_config_used_when_no_flag(self, tmp_path):
        existing = ProjectConfig(
            project_root=tmp_path,
            css_output=Path("static/css/starui.css"),
            component_dir=Path("from/config"),
        )
        result = resolve_component_dir(tmp_path, None, existing, no_interaction=False)
        assert result == "from/config"

    def test_auto_detect_ui_dir(self, tmp_path):
        (tmp_path / "ui").mkdir()
        result = resolve_component_dir(tmp_path, None, None, no_interaction=True)
        assert result == "ui"

    def test_auto_detect_default(self, tmp_path):
        result = resolve_component_dir(tmp_path, None, None, no_interaction=True)
        assert result == "components/ui"

    def test_interactive_prompt(self, tmp_path):
        with patch("starui.cli.init.typer.prompt", return_value="custom/dir"):
            result = resolve_component_dir(tmp_path, None, None, no_interaction=False)
        assert result == "custom/dir"
