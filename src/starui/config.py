"""Project configuration."""

import re
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


def load_pyproject_config(project_root: Path) -> ProjectConfig | None:
    pyproject_path = project_root / "pyproject.toml"
    if not pyproject_path.exists():
        return None

    with open(pyproject_path, "rb") as f:
        data = tomllib.load(f)

    starui = data.get("tool", {}).get("starui")
    if starui is None:
        return None

    return ProjectConfig(
        project_root=project_root,
        css_output=Path(starui["css_output"]) if "css_output" in starui else detect_css_output(project_root),
        component_dir=Path(starui["component_dir"])
        if "component_dir" in starui
        else detect_component_dir(project_root),
        css_dir=Path(starui["css_dir"]) if "css_dir" in starui else None,
    )


def save_config(
    project_root: Path,
    component_dir: str,
    css_output: str | None = None,
    css_dir: str | None = None,
) -> None:
    """Append [tool.starui] section to pyproject.toml."""
    pyproject_path = project_root / "pyproject.toml"
    lines = ["\n[tool.starui]", f'component_dir = "{component_dir}"']
    if css_output:
        lines.append(f'css_output = "{css_output}"')
    if css_dir:
        lines.append(f'css_dir = "{css_dir}"')
    block = "\n".join(lines) + "\n"

    if pyproject_path.exists():
        content = pyproject_path.read_text()
        if re.search(r"^\[tool\.starui\]", content, re.MULTILINE):
            return
        if not content.endswith("\n"):
            content += "\n"
        pyproject_path.write_text(content + block)
    else:
        pyproject_path.write_text(block.lstrip())


def get_project_config(
    project_root: Path | None = None,
    component_dir: str | None = None,
    css_output: str | None = None,
    css_dir: str | None = None,
) -> ProjectConfig:
    """Load project config. Resolution: CLI flag > pyproject.toml [tool.starui] > auto-detect."""
    root = project_root or Path.cwd()
    config = load_pyproject_config(root) or detect_project_config(root)
    if component_dir is not None:
        config.component_dir = Path(component_dir)
    if css_output is not None:
        config.css_output = Path(css_output)
    if css_dir is not None:
        config.css_dir = Path(css_dir)
    return config
