from pathlib import Path

from starui.config import (
    detect_component_dir,
    detect_css_output,
    detect_project_config,
    get_project_config,
    load_pyproject_config,
    save_config,
)


class TestCSSOutputDetection:
    def test_detect_css_output_static_directory_exists(self, tmp_path):
        (tmp_path / "static").mkdir()

        css_output = detect_css_output(tmp_path)
        assert css_output == Path("static/css/starui.css")

    def test_detect_css_output_assets_directory_exists(self, tmp_path):
        (tmp_path / "assets").mkdir()

        css_output = detect_css_output(tmp_path)
        assert css_output == Path("assets/starui.css")

    def test_detect_css_output_no_special_directories(self, tmp_path):
        css_output = detect_css_output(tmp_path)
        assert css_output == Path("starui.css")


class TestComponentDirDetection:
    def test_detect_component_dir_components_ui_exists(self, tmp_path):
        (tmp_path / "components" / "ui").mkdir(parents=True)

        component_dir = detect_component_dir(tmp_path)
        assert component_dir == Path("components/ui")

    def test_detect_component_dir_ui_exists(self, tmp_path):
        (tmp_path / "ui").mkdir()

        component_dir = detect_component_dir(tmp_path)
        assert component_dir == Path("ui")

    def test_detect_component_dir_default(self, tmp_path):
        component_dir = detect_component_dir(tmp_path)
        assert component_dir == Path("components/ui")


class TestProjectConfigDetection:
    def test_detect_project_config_with_static(self, tmp_path):
        (tmp_path / "static").mkdir()

        config = detect_project_config(tmp_path)

        assert config.project_root == tmp_path
        assert config.css_output == Path("static/css/starui.css")
        assert config.component_dir == Path("components/ui")

    def test_detect_project_config_with_ui_dir(self, tmp_path):
        (tmp_path / "ui").mkdir()

        config = detect_project_config(tmp_path)

        assert config.project_root == tmp_path
        assert config.component_dir == Path("ui")

    def test_detect_project_config_defaults_to_cwd(self):
        config = detect_project_config()
        assert config.project_root == Path.cwd()

    def test_get_project_config_falls_back_to_detect(self, tmp_path):
        config1 = detect_project_config(tmp_path)
        config2 = get_project_config(tmp_path)

        assert config1.project_root == config2.project_root
        assert config1.css_output == config2.css_output
        assert config1.component_dir == config2.component_dir

    def test_get_project_config_reads_pyproject_toml(self, tmp_path):
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text('[tool.starui]\ncomponent_dir = "custom/components"\n')

        config = get_project_config(tmp_path)
        assert config.component_dir == Path("custom/components")

    def test_get_project_config_cli_override(self, tmp_path):
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text('[tool.starui]\ncomponent_dir = "custom/components"\n')

        config = get_project_config(tmp_path, component_dir="override/path")
        assert config.component_dir == Path("override/path")

    def test_get_project_config_css_output_override(self, tmp_path):
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text('[tool.starui]\ncss_output = "dist/app.css"\n')

        config = get_project_config(tmp_path, css_output="build/styles.css")
        assert config.css_output == Path("build/styles.css")

    def test_get_project_config_css_dir_override(self, tmp_path):
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text('[tool.starui]\ncss_dir = "assets/css"\n')

        config = get_project_config(tmp_path, css_dir="custom/css")
        assert config.css_dir == Path("custom/css")

    def test_pyproject_takes_precedence_over_detect(self, tmp_path):
        """pyproject.toml values override filesystem auto-detection."""
        (tmp_path / "static").mkdir()
        (tmp_path / "ui").mkdir()

        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text('[tool.starui]\ncomponent_dir = "lib/widgets"\ncss_output = "build/out.css"\n')

        config = get_project_config(tmp_path)
        assert config.component_dir == Path("lib/widgets")
        assert config.css_output == Path("build/out.css")


class TestLoadPyprojectConfig:
    def test_returns_none_without_pyproject(self, tmp_path):
        assert load_pyproject_config(tmp_path) is None

    def test_returns_none_without_starui_section(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text('[project]\nname = "myapp"\n')
        assert load_pyproject_config(tmp_path) is None

    def test_reads_all_fields(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text(
            '[tool.starui]\ncomponent_dir = "lib/ui"\ncss_output = "dist/app.css"\ncss_dir = "styles"\n'
        )
        config = load_pyproject_config(tmp_path)
        assert config is not None
        assert config.component_dir == Path("lib/ui")
        assert config.css_output == Path("dist/app.css")
        assert config.css_dir == Path("styles")

    def test_falls_back_to_detect_for_missing_fields(self, tmp_path):
        (tmp_path / "static").mkdir()
        (tmp_path / "pyproject.toml").write_text('[tool.starui]\ncomponent_dir = "custom/ui"\n')

        config = load_pyproject_config(tmp_path)
        assert config is not None
        assert config.component_dir == Path("custom/ui")
        assert config.css_output == Path("static/css/starui.css")
        assert config.css_dir is None

    def test_css_dir_defaults_to_none(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text('[tool.starui]\ncomponent_dir = "ui"\n')
        config = load_pyproject_config(tmp_path)
        assert config is not None
        assert config.css_dir is None

    def test_empty_starui_section(self, tmp_path):
        """Empty [tool.starui] with no keys still returns a config using auto-detect."""
        (tmp_path / "pyproject.toml").write_text("[tool.starui]\n")
        config = load_pyproject_config(tmp_path)
        assert config is not None
        assert config.component_dir == Path("components/ui")


class TestSaveConfig:
    def test_creates_new_pyproject(self, tmp_path):
        save_config(tmp_path, "components/ui")
        content = (tmp_path / "pyproject.toml").read_text()
        assert "[tool.starui]" in content
        assert 'component_dir = "components/ui"' in content

    def test_appends_to_existing_pyproject(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text('[project]\nname = "myapp"\n')
        save_config(tmp_path, "lib/ui")

        content = (tmp_path / "pyproject.toml").read_text()
        assert '[project]\nname = "myapp"' in content
        assert "[tool.starui]" in content
        assert 'component_dir = "lib/ui"' in content

    def test_skips_if_section_exists(self, tmp_path):
        original = '[project]\nname = "myapp"\n\n[tool.starui]\ncomponent_dir = "old"\n'
        (tmp_path / "pyproject.toml").write_text(original)

        save_config(tmp_path, "new/path")
        assert (tmp_path / "pyproject.toml").read_text() == original

    def test_writes_css_output(self, tmp_path):
        save_config(tmp_path, "ui", css_output="dist/styles.css")
        content = (tmp_path / "pyproject.toml").read_text()
        assert 'css_output = "dist/styles.css"' in content

    def test_writes_css_dir(self, tmp_path):
        save_config(tmp_path, "ui", css_dir="assets/css")
        content = (tmp_path / "pyproject.toml").read_text()
        assert 'css_dir = "assets/css"' in content

    def test_regex_match_not_substring(self, tmp_path):
        """Ensure [tool.starui] detection uses proper regex, not substring match."""
        content = '# This mentions [tool.starui] in a comment\n[project]\nname = "test"\n'
        (tmp_path / "pyproject.toml").write_text(content)

        save_config(tmp_path, "ui")
        updated = (tmp_path / "pyproject.toml").read_text()
        assert updated.count("[tool.starui]") == 2  # comment + new section

    def test_no_trailing_newline_handled(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text('[project]\nname = "test"')
        save_config(tmp_path, "ui")
        content = (tmp_path / "pyproject.toml").read_text()
        assert "[tool.starui]" in content
        assert 'name = "test"' in content
