"""Tests for ProcessManager._find_project_root, PYTHONPATH, and _get_app_module."""

import os
from pathlib import Path
from tempfile import gettempdir
from unittest.mock import MagicMock, patch

from starui.dev.process_manager import ProcessManager


class TestFindProjectRoot:
    """Test _find_project_root static method."""

    def test_finds_pyproject_in_current_dir(self, tmp_path):
        """Finds pyproject.toml in the start directory."""
        (tmp_path / "pyproject.toml").touch()
        result = ProcessManager._find_project_root(tmp_path)
        assert result == tmp_path

    def test_finds_pyproject_in_parent(self, tmp_path):
        """Walks up to find pyproject.toml in parent directory."""
        (tmp_path / "pyproject.toml").touch()
        child = tmp_path / "src" / "app"
        child.mkdir(parents=True)
        result = ProcessManager._find_project_root(child)
        assert result == tmp_path

    def test_finds_pyproject_several_levels_up(self, tmp_path):
        """Walks up multiple levels to find pyproject.toml."""
        (tmp_path / "pyproject.toml").touch()
        deep = tmp_path / "a" / "b" / "c" / "d"
        deep.mkdir(parents=True)
        result = ProcessManager._find_project_root(deep)
        assert result == tmp_path

    def test_returns_resolved_start_when_no_pyproject(self, tmp_path):
        """Falls back to resolved start path when no pyproject.toml found."""
        child = tmp_path / "some" / "dir"
        child.mkdir(parents=True)
        result = ProcessManager._find_project_root(child)
        assert result == child.resolve()

    def test_resolves_symlinks(self, tmp_path):
        """Resolves symlinks when finding project root."""
        real_project = tmp_path / "real_project"
        real_project.mkdir()
        (real_project / "pyproject.toml").touch()
        sub = real_project / "src"
        sub.mkdir()

        # Create a symlink pointing to the subdirectory
        link = tmp_path / "link_to_src"
        link.symlink_to(sub)

        result = ProcessManager._find_project_root(link)
        assert result == real_project.resolve()


class TestPythonPathConstruction:
    """Test PYTHONPATH in start_uvicorn."""

    @patch("subprocess.Popen")
    def test_pythonpath_includes_project_root(self, mock_popen, tmp_path):
        """PYTHONPATH should include the project root."""
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
        """PYTHONPATH should include temp dir when hot_reload is True."""
        from tempfile import gettempdir

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
        """PYTHONPATH should not include temp dir when hot_reload is False."""
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
    def test_pythonpath_preserves_existing(self, mock_popen, tmp_path, monkeypatch):
        """Existing PYTHONPATH entries are preserved."""
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
    """Test _get_app_module wrapper generation."""

    def test_without_hot_reload_returns_simple_module(self, tmp_path):
        """Without hot_reload, returns '{stem}:app'."""
        app_file = tmp_path / "main.py"
        app_file.write_text("app = None")

        manager = ProcessManager()
        result = manager._get_app_module(app_file, hot_reload=False, debug=True)
        assert result == "main:app"

    def test_with_hot_reload_creates_wrapper_file(self, tmp_path):
        """With hot_reload, creates a wrapper file in temp dir."""
        app_file = tmp_path / "main.py"
        app_file.write_text("app = None")

        manager = ProcessManager()
        result = manager._get_app_module(app_file, hot_reload=True, debug=True)

        # Result should be 'wrapper_stem:app'
        assert result.endswith(":app")
        wrapper_stem = result.split(":")[0]

        # Wrapper file should exist in temp dir
        wrapper_path = Path(gettempdir()) / f"{wrapper_stem}.py"
        assert wrapper_path.exists()

        # Wrapper should reference the original app
        content = wrapper_path.read_text()
        assert "main" in content  # references app_stem
        assert str(tmp_path) in content  # references app_dir

        # Cleanup
        wrapper_path.unlink()

    def test_with_hot_reload_debug_flag_propagated(self, tmp_path):
        """Debug flag is propagated to the wrapper template."""
        app_file = tmp_path / "app.py"
        app_file.write_text("app = None")

        manager = ProcessManager()

        # debug=True
        result = manager._get_app_module(app_file, hot_reload=True, debug=True)
        wrapper_stem = result.split(":")[0]
        wrapper = Path(gettempdir()) / f"{wrapper_stem}.py"
        content = wrapper.read_text()
        assert "original_app.debug = True" in content
        wrapper.unlink()

        # debug=False
        result = manager._get_app_module(app_file, hot_reload=True, debug=False)
        wrapper_stem = result.split(":")[0]
        wrapper = Path(gettempdir()) / f"{wrapper_stem}.py"
        content = wrapper.read_text()
        assert "original_app.debug = False" in content
        wrapper.unlink()
