"""Tests for ProcessManager._find_project_root, PYTHONPATH, _get_app_module, and _resolve_module_path."""

import os
from pathlib import Path
from tempfile import gettempdir
from unittest.mock import MagicMock, patch

import pytest

from starui.dev.process_manager import ProcessManager


class TestFindProjectRoot:
    def test_finds_pyproject_in_current_dir(self, tmp_path):
        (tmp_path / "pyproject.toml").touch()
        result = ProcessManager._find_project_root(tmp_path)
        assert result == tmp_path

    def test_finds_pyproject_in_parent(self, tmp_path):
        (tmp_path / "pyproject.toml").touch()
        child = tmp_path / "src" / "app"
        child.mkdir(parents=True)
        result = ProcessManager._find_project_root(child)
        assert result == tmp_path

    def test_finds_pyproject_several_levels_up(self, tmp_path):
        (tmp_path / "pyproject.toml").touch()
        deep = tmp_path / "a" / "b" / "c" / "d"
        deep.mkdir(parents=True)
        result = ProcessManager._find_project_root(deep)
        assert result == tmp_path

    def test_returns_resolved_start_when_no_pyproject(self, tmp_path):
        child = tmp_path / "some" / "dir"
        child.mkdir(parents=True)
        result = ProcessManager._find_project_root(child)
        assert result == child.resolve()

    def test_resolves_symlinks(self, tmp_path):
        real_project = tmp_path / "real_project"
        real_project.mkdir()
        (real_project / "pyproject.toml").touch()
        sub = real_project / "src"
        sub.mkdir()

        link = tmp_path / "link_to_src"
        link.symlink_to(sub)

        result = ProcessManager._find_project_root(link)
        assert result == real_project.resolve()


class TestPythonPathConstruction:
    @patch("subprocess.Popen")
    def test_pythonpath_includes_project_root(self, mock_popen, tmp_path):
        (tmp_path / "pyproject.toml").touch()
        app_file = tmp_path / "app.py"
        app_file.write_text("app = None")

        mock_proc = MagicMock()
        mock_proc.stdout.readline.return_value = ""
        mock_proc.poll.return_value = 0
        mock_popen.return_value = mock_proc

        manager = ProcessManager()
        manager.start_uvicorn(app_file, 5000, ["*.py"], hot_reload=False)

        call_kwargs = mock_popen.call_args
        env = call_kwargs.kwargs.get("env") or call_kwargs[1].get("env", {})
        pythonpath = env.get("PYTHONPATH", "")

        assert str(tmp_path) in pythonpath

    @patch("subprocess.Popen")
    def test_pythonpath_includes_temp_dir_with_hot_reload(self, mock_popen, tmp_path):
        (tmp_path / "pyproject.toml").touch()
        app_file = tmp_path / "app.py"
        app_file.write_text("app = None")

        mock_proc = MagicMock()
        mock_proc.stdout.readline.return_value = ""
        mock_proc.poll.return_value = 0
        mock_popen.return_value = mock_proc

        manager = ProcessManager()
        manager.start_uvicorn(app_file, 5000, ["*.py"], hot_reload=True)

        call_kwargs = mock_popen.call_args
        env = call_kwargs.kwargs.get("env") or call_kwargs[1].get("env", {})
        pythonpath = env.get("PYTHONPATH", "")

        assert str(tmp_path) in pythonpath
        assert gettempdir() in pythonpath

    @patch("subprocess.Popen")
    def test_pythonpath_no_temp_dir_without_hot_reload(self, mock_popen, tmp_path):
        (tmp_path / "pyproject.toml").touch()
        app_file = tmp_path / "app.py"
        app_file.write_text("app = None")

        mock_proc = MagicMock()
        mock_proc.stdout.readline.return_value = ""
        mock_proc.poll.return_value = 0
        mock_popen.return_value = mock_proc

        manager = ProcessManager()
        manager.start_uvicorn(app_file, 5000, ["*.py"], hot_reload=False)

        call_kwargs = mock_popen.call_args
        env = call_kwargs.kwargs.get("env") or call_kwargs[1].get("env", {})
        pythonpath = env.get("PYTHONPATH", "")
        path_parts = pythonpath.split(os.pathsep)

        assert gettempdir() not in path_parts

    @patch("subprocess.Popen")
    def test_pythonpath_includes_sys_path_root_for_src_layout(self, mock_popen, tmp_path):
        (tmp_path / "pyproject.toml").touch()
        src = tmp_path / "src"
        pkg = src / "myapp"
        pkg.mkdir(parents=True)
        (pkg / "__init__.py").touch()
        app_file = pkg / "main.py"
        app_file.write_text("app = None")

        mock_proc = MagicMock()
        mock_proc.stdout.readline.return_value = ""
        mock_proc.poll.return_value = 0
        mock_popen.return_value = mock_proc

        manager = ProcessManager()
        manager.start_uvicorn(app_file, 5000, ["*.py"], hot_reload=False)

        call_kwargs = mock_popen.call_args
        env = call_kwargs.kwargs.get("env") or call_kwargs[1].get("env", {})
        pythonpath = env.get("PYTHONPATH", "")

        assert str(tmp_path) in pythonpath
        assert str(src) in pythonpath

    @patch("subprocess.Popen")
    def test_pythonpath_preserves_existing(self, mock_popen, tmp_path, monkeypatch):
        monkeypatch.setenv("PYTHONPATH", "/existing/path")
        (tmp_path / "pyproject.toml").touch()
        app_file = tmp_path / "app.py"
        app_file.write_text("app = None")

        mock_proc = MagicMock()
        mock_proc.stdout.readline.return_value = ""
        mock_proc.poll.return_value = 0
        mock_popen.return_value = mock_proc

        manager = ProcessManager()
        manager.start_uvicorn(app_file, 5000, ["*.py"], hot_reload=False)

        call_kwargs = mock_popen.call_args
        env = call_kwargs.kwargs.get("env") or call_kwargs[1].get("env", {})
        pythonpath = env.get("PYTHONPATH", "")

        assert "/existing/path" in pythonpath


class TestGetAppModule:
    def test_without_hot_reload_returns_simple_module(self, tmp_path):
        (tmp_path / "pyproject.toml").touch()
        app_file = tmp_path / "main.py"
        app_file.write_text("app = None")

        manager = ProcessManager()
        result = manager._get_app_module(app_file, hot_reload=False, debug=True)
        assert result == "main:app"

    def test_with_hot_reload_creates_wrapper_file(self, tmp_path):
        (tmp_path / "pyproject.toml").touch()
        app_file = tmp_path / "main.py"
        app_file.write_text("app = None")

        manager = ProcessManager()
        result = manager._get_app_module(app_file, hot_reload=True, debug=True)

        assert result.endswith(":app")
        wrapper_stem = result.split(":")[0]
        wrapper_path = Path(gettempdir()) / f"{wrapper_stem}.py"
        assert wrapper_path.exists()

        content = wrapper_path.read_text()
        assert "from main import app" in content
        assert str(tmp_path) in content
        wrapper_path.unlink()

    @pytest.mark.parametrize("debug", [True, False])
    def test_with_hot_reload_debug_flag_propagated(self, tmp_path, debug):
        (tmp_path / "pyproject.toml").touch()
        app_file = tmp_path / "app.py"
        app_file.write_text("app = None")

        manager = ProcessManager()
        result = manager._get_app_module(app_file, hot_reload=True, debug=debug)
        wrapper_stem = result.split(":")[0]
        wrapper = Path(gettempdir()) / f"{wrapper_stem}.py"
        content = wrapper.read_text()
        assert f"original_app.debug = {debug}" in content
        wrapper.unlink()


class TestResolveModulePath:
    def test_flat_layout_returns_stem(self, tmp_path):
        (tmp_path / "pyproject.toml").touch()
        app_file = tmp_path / "app.py"
        app_file.touch()

        module, sys_root = ProcessManager._resolve_module_path(app_file, tmp_path)
        assert module == "app"
        assert sys_root == tmp_path.resolve()

    def test_package_layout_returns_dotted_path(self, tmp_path):
        (tmp_path / "pyproject.toml").touch()
        pkg = tmp_path / "mypkg" / "web"
        pkg.mkdir(parents=True)
        (tmp_path / "mypkg" / "__init__.py").touch()
        (pkg / "__init__.py").touch()
        app_file = pkg / "app.py"
        app_file.touch()

        module, sys_root = ProcessManager._resolve_module_path(app_file, tmp_path)
        assert module == "mypkg.web.app"
        assert sys_root == tmp_path.resolve()

    def test_partial_package_stops_at_missing_init(self, tmp_path):
        (tmp_path / "pyproject.toml").touch()
        # src/ has no __init__.py, but src/myapp/ does
        src = tmp_path / "src"
        pkg = src / "myapp"
        pkg.mkdir(parents=True)
        (pkg / "__init__.py").touch()
        app_file = pkg / "main.py"
        app_file.touch()

        module, sys_root = ProcessManager._resolve_module_path(app_file, tmp_path)
        assert module == "myapp.main"
        assert sys_root == src.resolve()

    def test_single_level_package(self, tmp_path):
        (tmp_path / "pyproject.toml").touch()
        pkg = tmp_path / "myapp"
        pkg.mkdir()
        (pkg / "__init__.py").touch()
        app_file = pkg / "main.py"
        app_file.touch()

        module, sys_root = ProcessManager._resolve_module_path(app_file, tmp_path)
        assert module == "myapp.main"
        assert sys_root == tmp_path.resolve()


class TestGetAppModulePackageAware:
    def test_package_layout_without_hot_reload(self, tmp_path):
        (tmp_path / "pyproject.toml").touch()
        pkg = tmp_path / "mypkg" / "web"
        pkg.mkdir(parents=True)
        (tmp_path / "mypkg" / "__init__.py").touch()
        (pkg / "__init__.py").touch()
        app_file = pkg / "app.py"
        app_file.touch()

        manager = ProcessManager()
        result = manager._get_app_module(app_file, hot_reload=False, debug=True)
        assert result == "mypkg.web.app:app"

    def test_package_layout_with_hot_reload_wrapper(self, tmp_path):
        (tmp_path / "pyproject.toml").touch()
        pkg = tmp_path / "mypkg" / "web"
        pkg.mkdir(parents=True)
        (tmp_path / "mypkg" / "__init__.py").touch()
        (pkg / "__init__.py").touch()
        app_file = pkg / "app.py"
        app_file.touch()

        manager = ProcessManager()
        result = manager._get_app_module(app_file, hot_reload=True, debug=True)

        wrapper_stem = result.split(":")[0]
        wrapper = Path(gettempdir()) / f"{wrapper_stem}.py"
        content = wrapper.read_text()

        assert "from mypkg.web.app import app as original_app" in content
        assert str(tmp_path.resolve()) in content
        wrapper.unlink()
