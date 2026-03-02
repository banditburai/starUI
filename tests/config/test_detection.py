"""Tests for project auto-detection logic."""

from pathlib import Path

from starui.config import (
    CONTENT_PATTERNS,
    detect_component_dir,
    detect_css_output,
    detect_project_config,
    get_project_config,
)


class TestCSSOutputDetection:
    """Test CSS output path detection logic."""

    def test_detect_css_output_static_directory_exists(self, tmp_path):
        """Test CSS output detection when static/ directory exists."""
        static_dir = tmp_path / "static"
        static_dir.mkdir()

        css_output = detect_css_output(tmp_path)
        assert css_output == Path("static/css/starui.css")

    def test_detect_css_output_assets_directory_exists(self, tmp_path):
        """Test CSS output detection when assets/ directory exists."""
        assets_dir = tmp_path / "assets"
        assets_dir.mkdir()

        css_output = detect_css_output(tmp_path)
        assert css_output == Path("assets/starui.css")

    def test_detect_css_output_no_special_directories(self, tmp_path):
        """Test CSS output detection when no special directories exist."""
        css_output = detect_css_output(tmp_path)
        assert css_output == Path("starui.css")


class TestComponentDirDetection:
    """Test component directory detection logic."""

    def test_detect_component_dir_components_ui_exists(self, tmp_path):
        """Test component dir detection when components/ui exists."""
        components_ui = tmp_path / "components" / "ui"
        components_ui.mkdir(parents=True)

        component_dir = detect_component_dir(tmp_path)
        assert component_dir == Path("components/ui")

    def test_detect_component_dir_ui_exists(self, tmp_path):
        """Test component dir detection when ui/ exists."""
        ui_dir = tmp_path / "ui"
        ui_dir.mkdir()

        component_dir = detect_component_dir(tmp_path)
        assert component_dir == Path("ui")

    def test_detect_component_dir_default(self, tmp_path):
        """Test component dir detection defaults to components/ui."""
        component_dir = detect_component_dir(tmp_path)
        assert component_dir == Path("components/ui")


class TestProjectConfigDetection:
    """Test complete project configuration detection."""

    def test_detect_project_config_with_static(self, tmp_path):
        """Test project config detection with static directory."""
        static_dir = tmp_path / "static"
        static_dir.mkdir()

        config = detect_project_config(tmp_path)

        assert config.project_root == tmp_path
        assert config.css_output == Path("static/css/starui.css")
        assert config.component_dir == Path("components/ui")

    def test_detect_project_config_with_ui_dir(self, tmp_path):
        """Test project config detection with ui directory."""
        ui_dir = tmp_path / "ui"
        ui_dir.mkdir()

        config = detect_project_config(tmp_path)

        assert config.project_root == tmp_path
        assert config.component_dir == Path("ui")

    def test_detect_project_config_defaults_to_cwd(self):
        """Test project config detection defaults to current directory."""
        config = detect_project_config()
        assert config.project_root == Path.cwd()

    def test_get_project_config_alias(self, tmp_path):
        """Test get_project_config is an alias for detect_project_config."""
        config1 = detect_project_config(tmp_path)
        config2 = get_project_config(tmp_path)

        assert config1.project_root == config2.project_root
        assert config1.css_output == config2.css_output
        assert config1.component_dir == config2.component_dir


class TestContentPatterns:
    """Test content pattern generation."""

    def test_content_patterns(self):
        assert "**/*.py" in CONTENT_PATTERNS
        assert "!**/__pycache__/**" in CONTENT_PATTERNS
        assert "!**/test_*.py" in CONTENT_PATTERNS
