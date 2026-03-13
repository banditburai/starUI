import subprocess
from contextlib import nullcontext
from dataclasses import dataclass, field
from unittest.mock import MagicMock, patch

import pytest
from click.exceptions import Exit

from starui.cli.add import (
    _build_token_rules as _build_token_rules,
)
from starui.cli.add import (
    _setup_code_highlighting as _setup_code_highlighting,
)
from starui.cli.add import (
    _setup_css_imports,
    add_command,
)


def _mock_client(resolved: dict[str, str], *, metadata_fn=None):
    client = MagicMock()
    client.get_component_with_dependencies.return_value = resolved
    default_meta = metadata_fn or (
        lambda name: {
            "name": name,
            "packages": [],
            "css_imports": [],
            "checksum": "",
        }
    )
    client.get_component_metadata.side_effect = default_meta
    client.lookup.side_effect = lambda name: ("component", default_meta(name))
    client.version = "main"
    return client


def _messages(mock) -> list[str]:
    """Extract the first positional string arg from each call to a mock."""
    return [call[0][0] for call in mock.call_args_list if call[0]]


@dataclass
class AddResult:
    """Captures the observable outcomes of an add_command invocation."""

    successes: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    infos: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    subprocess_calls: list[list[str]] = field(default_factory=list)


def _run_add(
    project,
    components,
    resolved,
    *,
    force=False,
    verbose=False,
    confirm_response=False,
    client=None,
    subprocess_side_effect=None,
):
    if client is None:
        client = _mock_client(resolved)

    with (
        patch("starui.cli.add.get_project_config", return_value=project),
        patch("starui.cli.add.RegistryClient", return_value=client),
        patch("starui.cli.add.Manifest", return_value=MagicMock()),
        patch("starui.cli.add.confirm", return_value=confirm_response),
        patch("starui.cli.add.subprocess.run", side_effect=subprocess_side_effect) as mock_subprocess,
        patch("starui.cli.add.status_context", return_value=nullcontext()),
        patch("starui.cli.add._setup_code_highlighting"),
        patch("starui.cli.add.console"),
        patch("starui.cli.add.success") as mock_success,
        patch("starui.cli.add.warning") as mock_warning,
        patch("starui.cli.add.info") as mock_info,
        patch("starui.cli.add.error") as mock_error,
    ):
        add_command(components=components, force=force, verbose=verbose, theme=None, component_dir=None)

    result = AddResult(
        successes=_messages(mock_success),
        warnings=_messages(mock_warning),
        infos=_messages(mock_info),
        errors=_messages(mock_error),
        subprocess_calls=[call[0][0] for call in mock_subprocess.call_args_list],
    )
    return result


class TestAddNewComponent:
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
        result = _run_add(
            project,
            ["dialog"],
            {"utils": "# u", "button": "# b", "dialog": "# d"},
        )
        success_text = " ".join(result.successes)
        assert "utils" in success_text
        assert "dialog" in success_text


class TestSkipExistingDeps:
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
        """If confirm were called it would return False and raise Exit -- completing is proof."""
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
    def test_prompts_for_requested_that_exists(self, project):
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
        """With force=True, confirm returning False would cause Exit -- completing is proof."""
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
        comp_dir = project.component_dir_absolute
        (comp_dir / "utils.py").write_text("# u")

        before = set(comp_dir.iterdir())
        result = _run_add(project, ["dialog"], {"utils": "# u"})
        after = set(comp_dir.iterdir())

        assert before == after
        assert any("already installed" in msg for msg in result.infos)


class TestImportPreservation:
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


def _code_block_metadata(name):
    return {
        "name": name,
        "packages": ["starlighter"] if name == "code_block" else [],
        "css_imports": [],
        "checksum": "",
    }


class TestPackageInstallation:
    def test_installs_required_packages(self, project):
        resolved = {"utils": "# u", "code_block": "# cb"}
        client = _mock_client(resolved, metadata_fn=_code_block_metadata)

        result = _run_add(project, ["code_block"], resolved, client=client)

        # Verify the package was installed -- check the command includes the package name
        assert len(result.subprocess_calls) == 1
        assert "starlighter" in result.subprocess_calls[0]

    def test_install_failure_warns_but_continues(self, project):
        resolved = {"utils": "# u", "code_block": "# cb"}
        client = _mock_client(resolved, metadata_fn=_code_block_metadata)

        result = _run_add(
            project,
            ["code_block"],
            resolved,
            client=client,
            subprocess_side_effect=subprocess.CalledProcessError(1, "uv", stderr="fail"),
        )

        # Component is still written despite package install failure
        assert (project.component_dir_absolute / "code_block.py").exists()
        # User sees a warning mentioning the failed package
        assert any("starlighter" in msg for msg in result.warnings)


class TestCssImports:
    def test_css_imports_added_for_typography(self, project):
        input_css = project.css_dir_absolute / "input.css"
        input_css.write_text('@import "tailwindcss";\n')

        resolved = {"utils": "# u", "typography": "# t"}
        client = _mock_client(
            resolved,
            metadata_fn=lambda name: {
                "name": name,
                "packages": [],
                "css_imports": ['@plugin "@tailwindcss/typography";'] if name == "typography" else [],
                "checksum": "",
            },
        )

        _run_add(project, ["typography"], resolved, client=client)

        content = input_css.read_text()
        assert '@plugin "@tailwindcss/typography";' in content


class TestErrorPaths:
    def test_client_failure_raises_exit_with_message(self, project):
        client = MagicMock()
        client.lookup.return_value = ("component", {"name": "button"})
        client.get_component_with_dependencies.side_effect = RuntimeError("boom")

        with (
            patch("starui.cli.add.get_project_config", return_value=project),
            patch("starui.cli.add.RegistryClient", return_value=client),
            patch("starui.cli.add.Manifest", return_value=MagicMock()),
            patch("starui.cli.add.status_context", return_value=nullcontext()),
            patch("starui.cli.add.console"),
            patch("starui.cli.add.error") as mock_error,
            pytest.raises(Exit),
        ):
            add_command(components=["button"], force=False, verbose=False, theme=None, component_dir=None)

        assert any("boom" in msg for msg in _messages(mock_error))

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
            add_command(components=["button"], force=False, verbose=False, theme=None, component_dir=None)

        assert any("no config" in msg for msg in _messages(mock_error))


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


# ── Block tests ────────────────────────────────────────────────────────────


def _mock_block_client(
    comp_deps: dict[str, str],
    block_source: str,
    *,
    registry_name: str = "user_button_01",
    install_name: str = "user_button",
    block_meta: dict | None = None,
):
    """Create a mock client that supports both component and block lookups."""
    block_entry = {
        "name": registry_name,
        "install_name": install_name,
        "packages": [],
        "css_imports": [],
        "handlers": [],
        "checksum": "",
        **(block_meta or {}),
    }

    def comp_meta_fn(name):
        return {"name": name, "packages": [], "css_imports": [], "checksum": ""}

    client = MagicMock()
    client.version = "main"
    client.get_component_metadata.side_effect = comp_meta_fn
    client.get_block_metadata.return_value = block_entry
    client.get_block_with_dependencies.return_value = (comp_deps, block_source)

    def lookup(name):
        if name in comp_deps and name != "utils":
            return ("component", comp_meta_fn(name))
        if name == registry_name:
            return ("block", block_entry)
        if name == install_name:
            return ("block", block_entry)
        raise FileNotFoundError(f"'{name}' not found")

    client.lookup.side_effect = lookup
    return client


class TestBlockInstallByRegistryName:
    def test_installs_block_and_component_deps(self, project):
        comp_dir = project.component_dir_absolute
        client = _mock_block_client(
            {"utils": "# u", "avatar": "# avatar", "dropdown_menu": "# dm"},
            "# user_button source",
        )

        _run_add(project, ["user-button-01"], {}, client=client)

        assert (comp_dir / "avatar.py").read_text() == "# avatar"
        assert (comp_dir / "dropdown_menu.py").read_text() == "# dm"
        assert (comp_dir / "user_button.py").read_text() == "# user_button source"

    def test_success_message_includes_block(self, project):
        client = _mock_block_client(
            {"utils": "# u"},
            "# block src",
        )
        result = _run_add(project, ["user-button-01"], {}, client=client)
        success_text = " ".join(result.successes)
        assert "user_button" in success_text


class TestBlockInstallByInstallName:
    def test_resolves_install_name_to_registry_name(self, project):
        """star add user-button should work via install_name fallback."""
        comp_dir = project.component_dir_absolute
        client = _mock_block_client(
            {"utils": "# u", "avatar": "# av"},
            "# block src",
        )

        _run_add(project, ["user-button"], {}, client=client)

        assert (comp_dir / "user_button.py").read_text() == "# block src"
        # Verify get_block_with_dependencies was called with registry name, not install name
        client.get_block_with_dependencies.assert_called_with("user_button_01")


class TestBlockConflictDetection:
    def test_conflict_detected_by_install_name(self, project):
        comp_dir = project.component_dir_absolute
        (comp_dir / "user_button.py").write_text("# existing")

        client = _mock_block_client({"utils": "# u"}, "# new block")

        # When user types the install_name, conflict should still be detected
        _run_add(project, ["user-button"], {}, client=client, confirm_response=True)
        assert (comp_dir / "user_button.py").read_text() == "# new block"

    def test_conflict_detected_by_registry_name(self, project):
        comp_dir = project.component_dir_absolute
        (comp_dir / "user_button.py").write_text("# existing")

        client = _mock_block_client({"utils": "# u"}, "# new block")

        _run_add(project, ["user-button-01"], {}, client=client, confirm_response=True)
        assert (comp_dir / "user_button.py").read_text() == "# new block"


class TestBlockPackagesAndCssImports:
    def test_block_packages_are_collected(self, project):
        client = _mock_block_client(
            {"utils": "# u"},
            "# block src",
            block_meta={"packages": ["some-pkg"]},
        )

        result = _run_add(project, ["user-button-01"], {}, client=client)
        assert len(result.subprocess_calls) == 1
        assert "some-pkg" in result.subprocess_calls[0]

    def test_block_css_imports_are_added(self, project):
        input_css = project.css_dir_absolute / "input.css"
        input_css.write_text('@import "tailwindcss";\n')

        client = _mock_block_client(
            {"utils": "# u"},
            "# block src",
            block_meta={"css_imports": ['@plugin "some-plugin";']},
        )

        _run_add(project, ["user-button-01"], {}, client=client)
        assert '@plugin "some-plugin";' in input_css.read_text()


# ── _build_token_rules tests ─────────────────────────────────────────────


class TestBuildTokenRules:
    def test_generates_scrollbar_rules_when_theme_has_scrollbar_keys(self):
        theme = {
            "--scrollbar-track": "#111",
            "--scrollbar-thumb": "#222",
            "--scrollbar-thumb-hover": "#333",
        }
        result = _build_token_rules(theme)
        assert "::-webkit-scrollbar-track" in result
        assert "::-webkit-scrollbar-thumb {" in result
        assert "border-radius: 4px;" in result
        assert "::-webkit-scrollbar-thumb-hover" in result

    def test_generates_token_rules_for_token_keys(self):
        theme = {
            "--token-keyword": "#ff0000",
            "--token-string": "#00ff00",
        }
        result = _build_token_rules(theme)
        assert ".token-keyword { color: var(--token-keyword); }" in result
        assert ".token-string { color: var(--token-string); }" in result

    def test_adds_font_style_italic_for_token_comment(self):
        theme = {
            "--token-comment": "#999",
            "--token-keyword": "#f00",
        }
        result = _build_token_rules(theme)
        assert "font-style: italic;" in result
        # Only the comment line has italic
        for line in result.split("\n"):
            if "token-keyword" in line:
                assert "italic" not in line
            if "token-comment" in line:
                assert "italic" in line

    def test_skips_non_scrollbar_and_non_token_keys(self):
        theme = {
            "--background": "#fff",
            "--foreground": "#000",
            "--some-other": "blue",
        }
        result = _build_token_rules(theme)
        # Should only have the default scrollbar size rule, nothing else
        lines = result.strip().split("\n")
        assert len(lines) == 1
        assert "scrollbar" in lines[0]
        assert "--background" not in result
        assert "--foreground" not in result


# ── Verbose mode and lookup failure tests ─────────────────────────────────


class TestVerboseModeAndLookupFailure:
    def test_verbose_shows_file_location(self, project):
        result = _run_add(
            project,
            ["button"],
            {"utils": "# u", "button": "# btn"},
            verbose=True,
        )
        info_text = " ".join(result.infos)
        assert "Location" in info_text or str(project.component_dir_absolute) in info_text

    def test_component_not_found_in_registry_shows_error_and_exits(self, project):
        client = MagicMock()
        client.lookup.side_effect = FileNotFoundError("'nonexistent' not found")
        client.version = "main"

        with (
            patch("starui.cli.add.get_project_config", return_value=project),
            patch("starui.cli.add.RegistryClient", return_value=client),
            patch("starui.cli.add.Manifest", return_value=MagicMock()),
            patch("starui.cli.add.status_context", return_value=nullcontext()),
            patch("starui.cli.add.console"),
            patch("starui.cli.add.error") as mock_error,
            pytest.raises(Exit),
        ):
            add_command(components=["nonexistent"], force=False, verbose=False, theme=None, component_dir=None)

        assert any("not found" in msg for msg in _messages(mock_error))

    def test_verbose_shows_resolving_message(self, project):
        result = _run_add(
            project,
            ["button"],
            {"utils": "# u", "button": "# btn"},
            verbose=True,
        )
        info_text = " ".join(result.infos)
        assert "Resolving" in info_text


class TestMetadataFetchFailure:
    def test_component_metadata_not_found_still_installs(self, project):
        """If get_component_metadata raises FileNotFoundError during package collection,
        the component should still be installed."""
        comp_dir = project.component_dir_absolute

        client = MagicMock()
        client.version = "main"
        client.lookup.return_value = (
            "component",
            {"name": "button", "packages": [], "css_imports": [], "checksum": ""},
        )
        client.get_component_with_dependencies.return_value = {"button": "# btn source"}
        # Metadata fetch fails during package collection phase
        client.get_component_metadata.side_effect = FileNotFoundError("no metadata")

        _run_add(project, ["button"], {"button": "# btn source"}, client=client)
        assert (comp_dir / "button.py").exists()

    def test_block_metadata_not_found_still_installs(self, project):
        """If get_block_metadata raises FileNotFoundError during package collection,
        the block should still be installed."""
        comp_dir = project.component_dir_absolute

        client = _mock_block_client({"utils": "# u"}, "# block src")
        # Override get_block_metadata to always fail — the package-collection loop
        # on lines 222-228 catches FileNotFoundError and continues
        client.get_block_metadata.side_effect = FileNotFoundError("metadata vanished")

        _run_add(project, ["user-button-01"], {}, client=client)
        assert (comp_dir / "user_button.py").exists()


# ── _setup_code_highlighting tests ────────────────────────────────────────

FAKE_THEMES = {
    "github-light": {"--token-keyword": "#cf222e", "--token-string": "#0a3069"},
    "github-dark": {"--token-keyword": "#ff7b72", "--token-string": "#a5d6ff", "--token-comment": "#8b949e"},
    "monokai": {"--token-keyword": "#f92672", "--token-comment": "#75715e"},
}


class TestSetupCodeHighlighting:
    def test_warns_when_starlighter_not_installed(self, project):
        """If starlighter is not importable, shows a warning and returns early."""
        with (
            patch("starui.cli.add.warning") as mock_warning,
            patch.dict("sys.modules", {"starlighter": None}),
        ):
            _setup_code_highlighting(project, theme="monokai")
            assert any("Starlighter" in msg for msg in _messages(mock_warning))

        # No starlighter.css should be generated
        assert not (project.css_dir_absolute / "starlighter.css").exists()

    def test_explicit_theme_generates_dark_only_css(self, project):
        """Passing --theme monokai generates a dark-only starlighter.css."""
        mock_starlighter = MagicMock()
        mock_starlighter.THEMES = FAKE_THEMES

        with (
            patch.dict("sys.modules", {"starlighter": mock_starlighter}),
            patch("starui.cli.add.console"),
            patch("starui.cli.add.success"),
            patch("starui.cli.add.info"),
        ):
            _setup_code_highlighting(project, theme="monokai")

        css_file = project.css_dir_absolute / "starlighter.css"
        assert css_file.exists()
        content = css_file.read_text()
        assert ":root" in content
        # Dark-only mode: no .dark selector
        assert ".dark" not in content

    def test_interactive_theme_default_generates_light_dark_css(self, project):
        """Interactive selection defaulting to choice 1 generates light/dark auto-switching."""
        mock_starlighter = MagicMock()
        mock_starlighter.THEMES = FAKE_THEMES

        with (
            patch.dict("sys.modules", {"starlighter": mock_starlighter}),
            patch("starui.cli.add.typer.prompt", return_value="1"),
            patch("starui.cli.add.console"),
            patch("starui.cli.add.success"),
            patch("starui.cli.add.info"),
        ):
            _setup_code_highlighting(project, theme=None)

        css_file = project.css_dir_absolute / "starlighter.css"
        assert css_file.exists()
        content = css_file.read_text()
        # Light/dark mode has both :root and .dark selectors
        assert ":root" in content
        assert ".dark" in content

    def test_interactive_invalid_choice_defaults_to_first(self, project):
        """Non-numeric input falls back to choice 0 (GitHub light/dark)."""
        mock_starlighter = MagicMock()
        mock_starlighter.THEMES = FAKE_THEMES

        with (
            patch.dict("sys.modules", {"starlighter": mock_starlighter}),
            patch("starui.cli.add.typer.prompt", return_value="abc"),
            patch("starui.cli.add.console"),
            patch("starui.cli.add.success"),
            patch("starui.cli.add.info"),
        ):
            _setup_code_highlighting(project, theme=None)

        css_file = project.css_dir_absolute / "starlighter.css"
        assert css_file.exists()
        content = css_file.read_text()
        assert ".dark" in content

    def test_adds_import_to_input_css(self, project):
        """starlighter.css import is added to input.css after the tailwindcss import."""
        input_css = project.css_dir_absolute / "input.css"
        input_css.write_text('@import "tailwindcss";\n')

        mock_starlighter = MagicMock()
        mock_starlighter.THEMES = FAKE_THEMES

        with (
            patch.dict("sys.modules", {"starlighter": mock_starlighter}),
            patch("starui.cli.add.console"),
            patch("starui.cli.add.success"),
            patch("starui.cli.add.info"),
        ):
            _setup_code_highlighting(project, theme="monokai")

        content = input_css.read_text()
        assert "@import './starlighter.css';" in content

    def test_skips_import_if_already_present(self, project):
        """If input.css already has the import, don't add it again."""
        input_css = project.css_dir_absolute / "input.css"
        original = "@import \"tailwindcss\";\n@import './starlighter.css';\n"
        input_css.write_text(original)

        mock_starlighter = MagicMock()
        mock_starlighter.THEMES = FAKE_THEMES

        with (
            patch.dict("sys.modules", {"starlighter": mock_starlighter}),
            patch("starui.cli.add.console"),
            patch("starui.cli.add.success"),
            patch("starui.cli.add.info"),
        ):
            _setup_code_highlighting(project, theme="monokai")

        assert input_css.read_text() == original
