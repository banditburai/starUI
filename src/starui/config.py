"""Project configuration."""

import tomllib
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ProjectConfig:
    """StarUI project configuration."""

    project_root: Path
    css_output: Path
    component_dir: Path
    css_dir: Path | None = None

    def _absolute(self, path: Path) -> Path:
        """Convert relative path to absolute."""
        return path if path.is_absolute() else self.project_root / path

    @property
    def css_output_absolute(self) -> Path:
        return self._absolute(self.css_output)

    @property
    def component_dir_absolute(self) -> Path:
        return self._absolute(self.component_dir)

    @property
    def css_dir_absolute(self) -> Path:
        if self.css_dir is None:
            return self.css_output_absolute.parent
        return self._absolute(self.css_dir)


def detect_css_output(root: Path) -> Path:
    if (root / "static").exists():
        return Path("static/css/starui.css")
    if (root / "assets").exists():
        return Path("assets/starui.css")
    return Path("starui.css")


def detect_component_dir(root: Path) -> Path:
    if (root / "components" / "ui").exists():
        return Path("components/ui")
    if (root / "ui").exists():
        return Path("ui")
    return Path("components/ui")


def detect_project_config(project_root: Path | None = None) -> ProjectConfig:
    root = project_root or Path.cwd()
    return ProjectConfig(
        project_root=root,
        css_output=detect_css_output(root),
        component_dir=detect_component_dir(root),
    )


def get_content_patterns(project_root: Path) -> list[str]:
    return ["**/*.py", "!**/__pycache__/**", "!**/test_*.py"]


def load_toml_config(project_root: Path) -> ProjectConfig | None:
    toml_path = project_root / "starui.toml"
    if not toml_path.exists():
        return None

    with open(toml_path, "rb") as f:
        data = tomllib.load(f)

    project = data.get("project", {})
    return ProjectConfig(
        project_root=project_root,
        css_output=Path(project.get("css_output", "starui.css")),
        component_dir=Path(project.get("component_dir", "components/ui")),
        css_dir=Path(project["css_dir"]) if "css_dir" in project else None,
    )


def get_project_config(project_root: Path | None = None) -> ProjectConfig:
    root = project_root or Path.cwd()
    return load_toml_config(root) or detect_project_config(root)
