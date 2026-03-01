"""Shared fixtures for CLI tests."""

from pathlib import Path

import pytest

from starui.config import ProjectConfig


@pytest.fixture
def project(tmp_path) -> ProjectConfig:
    """A minimal project with components/ui dir and static/css pre-created."""
    comp_dir = tmp_path / "components" / "ui"
    comp_dir.mkdir(parents=True)
    (comp_dir / "__init__.py").touch()

    css_dir = tmp_path / "static" / "css"
    css_dir.mkdir(parents=True)

    return ProjectConfig(
        project_root=tmp_path,
        css_output=Path("static/css/starui.css"),
        component_dir=Path("components/ui"),
    )
