from pathlib import Path

from starui.config import ProjectConfig


class TestProjectConfig:
    def test_config_creation(self):
        config = ProjectConfig(
            project_root=Path("/test/path"),
            css_output=Path("static/css/app.css"),
            component_dir=Path("src/ui"),
        )

        assert config.project_root == Path("/test/path")
        assert config.css_output == Path("static/css/app.css")
        assert config.component_dir == Path("src/ui")

    def test_css_output_absolute_path(self):
        config = ProjectConfig(
            project_root=Path("/project"),
            css_output=Path("static/css/app.css"),
            component_dir=Path("src/ui"),
        )

        assert config.css_output_absolute == Path("/project/static/css/app.css")

        config2 = ProjectConfig(
            project_root=Path("/project"),
            css_output=Path("/absolute/path/app.css"),
            component_dir=Path("src/ui"),
        )

        assert config2.css_output_absolute == Path("/absolute/path/app.css")

    def test_component_dir_absolute_path(self):
        config = ProjectConfig(
            project_root=Path("/project"),
            css_output=Path("static/css/app.css"),
            component_dir=Path("src/ui"),
        )

        assert config.component_dir_absolute == Path("/project/src/ui")

        config2 = ProjectConfig(
            project_root=Path("/project"),
            css_output=Path("static/css/app.css"),
            component_dir=Path("/absolute/ui"),
        )

        assert config2.component_dir_absolute == Path("/absolute/ui")

    def test_css_dir_absolute_defaults_to_css_output_parent(self):
        """Falls back to css_output parent when css_dir is None."""
        config = ProjectConfig(
            project_root=Path("/project"),
            css_output=Path("static/css/app.css"),
            component_dir=Path("ui"),
        )
        assert config.css_dir is None
        assert config.css_dir_absolute == Path("/project/static/css")

    def test_css_dir_absolute_with_explicit_css_dir(self):
        config = ProjectConfig(
            project_root=Path("/project"),
            css_output=Path("dist/app.css"),
            component_dir=Path("ui"),
            css_dir=Path("assets/styles"),
        )
        assert config.css_dir_absolute == Path("/project/assets/styles")

    def test_css_dir_absolute_with_absolute_css_dir(self):
        config = ProjectConfig(
            project_root=Path("/project"),
            css_output=Path("dist/app.css"),
            component_dir=Path("ui"),
            css_dir=Path("/absolute/styles"),
        )
        assert config.css_dir_absolute == Path("/absolute/styles")
