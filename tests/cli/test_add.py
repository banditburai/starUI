"""Tests for the add command."""

import subprocess
from contextlib import nullcontext
from unittest.mock import MagicMock, patch

import pytest
from click.exceptions import Exit

from starui.cli.add import _setup_css_imports, add_command


def _mock_loader(resolved: dict[str, str]):
    """Create a mock loader that returns resolved sources."""
    loader = MagicMock()
    loader.load_component_with_dependencies.return_value = resolved
    return loader


def _run_add(
    project, components, resolved, *, force=False, verbose=False, confirm_response=False
):
    """Run add_command with mocked dependencies. Returns captured mocks."""
    loader = _mock_loader(resolved)

    mocks = {}
    with (
        patch("starui.cli.add.get_project_config", return_value=project),
        patch("starui.cli.add.ComponentLoader", return_value=loader),
        patch("starui.cli.add.confirm", return_value=confirm_response),
        patch("starui.cli.add.subprocess.run") as mock_subprocess,
        patch("starui.cli.add.status_context", return_value=nullcontext()),
        patch("starui.cli.add.console"),
        patch("starui.cli.add.success") as mock_success,
        patch("starui.cli.add.warning") as mock_warning,
        patch("starui.cli.add.info") as mock_info,
        patch("starui.cli.add.error") as mock_error,
    ):
        mocks["loader"] = loader
        mocks["subprocess"] = mock_subprocess
        mocks["success"] = mock_success
        mocks["warning"] = mock_warning
        mocks["info"] = mock_info
        mocks["error"] = mock_error
        add_command(components=components, force=force, verbose=verbose, theme=None)

    return mocks


class TestAddNewComponent:
    """Adding a component that doesn't exist yet."""

    def test_writes_component_file(self, project):
        comp_dir = project.component_dir_absolute
        _run_add(
            project,
            ["dialog"],
            {
                "utils": "# utils source",
                "button": "# button source",
                "dialog": "# dialog source",
            },
        )
        assert (comp_dir / "dialog.py").read_text() == "# dialog source"

    def test_writes_deps_that_dont_exist(self, project):
        comp_dir = project.component_dir_absolute
        _run_add(
            project,
            ["dialog"],
            {
                "utils": "# utils",
                "button": "# button",
                "dialog": "# dialog",
            },
        )
        assert (comp_dir / "utils.py").read_text() == "# utils"
        assert (comp_dir / "button.py").read_text() == "# button"

    def test_creates_init_py(self, project):
        comp_dir = project.component_dir_absolute
        (comp_dir / "__init__.py").unlink()
        _run_add(project, ["badge"], {"utils": "# u", "badge": "# b"})
        assert (comp_dir / "__init__.py").exists()

    def test_multiple_components_in_one_call(self, project):
        comp_dir = project.component_dir_absolute
        _run_add(
            project,
            ["button", "badge"],
            {"utils": "# u", "button": "# btn", "badge": "# bdg"},
        )
        assert (comp_dir / "button.py").read_text() == "# btn"
        assert (comp_dir / "badge.py").read_text() == "# bdg"

    def test_success_message_lists_installed_components(self, project):
        mocks = _run_add(
            project,
            ["dialog"],
            {"utils": "# u", "button": "# b", "dialog": "# d"},
        )
        msg = mocks["success"].call_args[0][0]
        assert "utils" in msg
        assert "dialog" in msg


class TestSkipExistingDeps:
    """Dependencies already installed by init should be silently skipped."""

    def test_skips_existing_deps(self, project):
        comp_dir = project.component_dir_absolute
        (comp_dir / "utils.py").write_text("# local utils")
        (comp_dir / "button.py").write_text("# local button")

        _run_add(
            project,
            ["dialog"],
            {
                "utils": "# registry utils",
                "button": "# registry button",
                "dialog": "# dialog source",
            },
        )

        assert (comp_dir / "utils.py").read_text() == "# local utils"
        assert (comp_dir / "button.py").read_text() == "# local button"
        assert (comp_dir / "dialog.py").read_text() == "# dialog source"

    def test_no_prompt_when_only_deps_exist(self, project):
        """If confirm were called it would return False and raise Exit — completing is proof."""
        comp_dir = project.component_dir_absolute
        (comp_dir / "utils.py").write_text("# local")

        _run_add(
            project,
            ["dialog"],
            {"utils": "# u", "dialog": "# d"},
            confirm_response=False,
        )

        assert (comp_dir / "dialog.py").read_text() == "# d"


class TestOverwriteConflicts:
    """Explicitly requested components that already exist trigger a prompt."""

    def test_prompts_for_requested_that_exists(self, project):
        """confirm returns True → file should be overwritten with new content."""
        comp_dir = project.component_dir_absolute
        (comp_dir / "utils.py").write_text("# u")
        (comp_dir / "button.py").write_text("# old button")

        _run_add(
            project,
            ["button"],
            {"utils": "# u", "button": "# new button"},
            confirm_response=True,
        )

        assert (comp_dir / "button.py").read_text() == "# new button"

    def test_decline_overwrite_exits_cleanly(self, project):
        comp_dir = project.component_dir_absolute
        (comp_dir / "button.py").write_text("# old")

        with pytest.raises(Exit):
            _run_add(
                project,
                ["button"],
                {"utils": "# u", "button": "# new"},
                confirm_response=False,
            )

        assert (comp_dir / "button.py").read_text() == "# old"

    def test_force_overwrites_requested_and_dependencies(self, project):
        """With force=True, confirm returning False would cause Exit — completing is proof."""
        comp_dir = project.component_dir_absolute
        (comp_dir / "utils.py").write_text("# old utils")
        (comp_dir / "button.py").write_text("# old button")

        _run_add(
            project,
            ["button"],
            {"utils": "# new utils", "button": "# new button"},
            force=True,
            confirm_response=False,
        )

        assert (comp_dir / "utils.py").read_text() == "# new utils"
        assert (comp_dir / "button.py").read_text() == "# new button"


class TestAllComponentsAlreadyInstalled:
    def test_no_new_files_written(self, project):
        """All deps exist, nothing new requested — no new files."""
        comp_dir = project.component_dir_absolute
        (comp_dir / "utils.py").write_text("# u")

        before = set(comp_dir.iterdir())
        mocks = _run_add(project, ["dialog"], {"utils": "# u"})
        after = set(comp_dir.iterdir())

        assert before == after
        mocks["info"].assert_any_call(
            "All components already installed (dependencies unchanged)"
        )


class TestImportPreservation:
    """Source is written verbatim — no import rewriting."""

    def test_preserves_relative_utils_import(self, project):
        source = "from .utils import cn, cva\n\ndef Button(): pass"
        _run_add(project, ["button"], {"utils": "# u", "button": source})

        written = (project.component_dir_absolute / "button.py").read_text()
        assert "from .utils import cn, cva" in written
        assert "from starui import" not in written

    def test_preserves_relative_sibling_imports(self, project):
        source = "from .button import Button\nfrom .utils import cn"
        _run_add(
            project,
            ["dialog"],
            {"utils": "# u", "button": "# b", "dialog": source},
        )

        written = (project.component_dir_absolute / "dialog.py").read_text()
        assert "from .button import Button" in written
        assert "from .utils import cn" in written


class TestHyphenNormalization:
    def test_hyphen_to_underscore(self, project):
        _run_add(
            project,
            ["alert-dialog"],
            {"utils": "# u", "button": "# b", "alert_dialog": "# ad"},
        )
        assert (project.component_dir_absolute / "alert_dialog.py").exists()


class TestInvalidComponentNames:
    @pytest.mark.parametrize(
        "name",
        [
            "Invalid!Name",
            "123start",
            "_underscore",
            "UPPER",
            "has space",
        ],
    )
    def test_rejects_invalid_names(self, project, name):
        with pytest.raises(Exit):
            _run_add(project, [name], {})


class TestPackageInstallation:
    def test_installs_packages_via_subprocess(self, project):
        loader = _mock_loader({"utils": "# u", "code_block": "# cb"})

        with (
            patch("starui.cli.add.get_project_config", return_value=project),
            patch("starui.cli.add.ComponentLoader", return_value=loader),
            patch("starui.cli.add.confirm", return_value=False),
            patch("starui.cli.add.subprocess.run") as mock_run,
            patch("starui.cli.add.status_context", return_value=nullcontext()),
            patch("starui.cli.add.console"),
            patch("starui.cli.add.success"),
            patch("starui.cli.add.warning"),
            patch("starui.cli.add.info"),
            patch("starui.cli.add.error"),
            patch("starui.cli.add._setup_code_highlighting"),
        ):
            add_command(
                components=["code_block"], force=False, verbose=False, theme=None
            )

        mock_run.assert_called_once_with(
            ["uv", "add", "starlighter"],
            check=True,
            capture_output=True,
            text=True,
        )

    def test_install_failure_warns_but_continues(self, project):
        """If uv add fails, component is still installed."""
        loader = _mock_loader({"utils": "# u", "code_block": "# cb"})

        with (
            patch("starui.cli.add.get_project_config", return_value=project),
            patch("starui.cli.add.ComponentLoader", return_value=loader),
            patch("starui.cli.add.confirm", return_value=False),
            patch(
                "starui.cli.add.subprocess.run",
                side_effect=subprocess.CalledProcessError(1, "uv", stderr="fail"),
            ),
            patch("starui.cli.add.status_context", return_value=nullcontext()),
            patch("starui.cli.add.console"),
            patch("starui.cli.add.success"),
            patch("starui.cli.add.warning") as mock_warning,
            patch("starui.cli.add.info"),
            patch("starui.cli.add.error"),
            patch("starui.cli.add._setup_code_highlighting"),
        ):
            add_command(
                components=["code_block"], force=False, verbose=False, theme=None
            )

        # Component was still written despite package install failure
        assert (project.component_dir_absolute / "code_block.py").exists()
        mock_warning.assert_called_once()
        assert "starlighter" in mock_warning.call_args[0][0]


class TestCssImports:
    def test_css_imports_added_for_typography(self, project):
        input_css = project.css_dir_absolute / "input.css"
        input_css.write_text('@import "tailwindcss";\n')

        _run_add(project, ["typography"], {"utils": "# u", "typography": "# t"})

        content = input_css.read_text()
        assert '@plugin "@tailwindcss/typography";' in content


class TestErrorPaths:
    def test_loader_failure_raises_exit_with_message(self, project):
        loader = MagicMock()
        loader.load_component_with_dependencies.side_effect = RuntimeError("boom")

        with (
            patch("starui.cli.add.get_project_config", return_value=project),
            patch("starui.cli.add.ComponentLoader", return_value=loader),
            patch("starui.cli.add.status_context", return_value=nullcontext()),
            patch("starui.cli.add.console"),
            patch("starui.cli.add.error") as mock_error,
            pytest.raises(Exit),
        ):
            add_command(components=["button"], force=False, verbose=False, theme=None)

        assert "boom" in mock_error.call_args[0][0]

    def test_config_failure_raises_exit(self):
        with (
            patch(
                "starui.cli.add.get_project_config",
                side_effect=RuntimeError("no config"),
            ),
            patch("starui.cli.add.console"),
            patch("starui.cli.add.error") as mock_error,
            pytest.raises(Exit),
        ):
            add_command(components=["button"], force=False, verbose=False, theme=None)

        assert "no config" in mock_error.call_args[0][0]


class TestSetupCssImports:
    def test_adds_new_css_imports(self, project):
        input_css = project.css_dir_absolute / "input.css"
        input_css.write_text('@import "tailwindcss";\n')

        _setup_css_imports(project, ['@plugin "@tailwindcss/typography";'])

        content = input_css.read_text()
        assert '@plugin "@tailwindcss/typography";' in content

    def test_skips_existing_css_imports(self, project):
        input_css = project.css_dir_absolute / "input.css"
        original = '@import "tailwindcss";\n@plugin "@tailwindcss/typography";\n'
        input_css.write_text(original)

        _setup_css_imports(project, ['@plugin "@tailwindcss/typography";'])

        assert input_css.read_text() == original

    def test_noop_without_input_css(self, project):
        _setup_css_imports(project, ['@plugin "@tailwindcss/typography";'])
