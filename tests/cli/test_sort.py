"""Tests for the sort CLI command and the underlying sort library."""

from contextlib import nullcontext
from io import StringIO
from unittest.mock import patch

import pytest
from click.exceptions import Exit
from rich.console import Console

from starui.cli.sort import sort_command
from starui.sort import _extract_tokens, _is_fstring, _sort_string, sort_file, tokenize

# ---------------------------------------------------------------------------
# Library: tokenize()
# ---------------------------------------------------------------------------


class TestTokenize:
    def test_simple_classes(self):
        assert tokenize("flex items-center gap-2") == ["flex", "items-center", "gap-2"]

    def test_empty_string(self):
        assert tokenize("") == []

    def test_whitespace_only(self):
        assert tokenize("   \t\n  ") == []

    def test_single_token(self):
        assert tokenize("flex") == ["flex"]

    def test_preserves_brackets(self):
        result = tokenize("flex group-hover:text-[rgb(0,0,0)]")
        assert result == ["flex", "group-hover:text-[rgb(0,0,0)]"]

    def test_preserves_parentheses(self):
        result = tokenize("bg-[url(image.png)] p-4")
        assert result == ["bg-[url(image.png)]", "p-4"]

    def test_multiple_whitespace_between_tokens(self):
        assert tokenize("flex gap-2") == ["flex", "gap-2"]

    def test_leading_trailing_whitespace(self):
        assert tokenize("  flex gap-2  ") == ["flex", "gap-2"]

    def test_tab_and_newline_separators(self):
        assert tokenize("flex\tgap-2\np-4") == ["flex", "gap-2", "p-4"]

    def test_nested_brackets(self):
        result = tokenize("flex text-[calc(100%-2rem)]")
        assert result == ["flex", "text-[calc(100%-2rem)]"]


# ---------------------------------------------------------------------------
# Library: _is_fstring()
# ---------------------------------------------------------------------------


class TestIsFString:
    def test_plain_string(self):
        src = 'x = "hello"'
        pos = src.index('"')
        assert _is_fstring(src, pos) is False

    def test_fstring_lowercase(self):
        src = 'x = f"hello"'
        pos = src.index('"')
        assert _is_fstring(src, pos) is True

    def test_fstring_uppercase(self):
        src = 'x = F"hello"'
        pos = src.index('"')
        assert _is_fstring(src, pos) is True

    def test_rf_string(self):
        src = 'x = rf"hello"'
        pos = src.index('"')
        assert _is_fstring(src, pos) is True

    def test_fr_string(self):
        src = 'x = fr"hello"'
        pos = src.index('"')
        assert _is_fstring(src, pos) is True

    def test_raw_string_is_not_fstring(self):
        src = 'x = r"hello"'
        pos = src.index('"')
        assert _is_fstring(src, pos) is False

    def test_byte_string_is_not_fstring(self):
        src = 'x = b"hello"'
        pos = src.index('"')
        assert _is_fstring(src, pos) is False

    def test_at_start_of_string(self):
        src = '"hello"'
        assert _is_fstring(src, 0) is False

    def test_fb_string(self):
        # fb isn't valid Python but the function just checks for f/F in prefix
        src = 'x = fb"hello"'
        pos = src.index('"')
        assert _is_fstring(src, pos) is True


# ---------------------------------------------------------------------------
# Library: _sort_string()
# ---------------------------------------------------------------------------


class TestSortString:
    def test_sorts_known_tokens_by_index(self):
        index = {"flex": 0, "p-4": 1, "mt-2": 2}
        result = _sort_string('"mt-2 flex p-4"', index)
        assert result == '"flex p-4 mt-2"'

    def test_returns_unchanged_when_already_sorted(self):
        index = {"flex": 0, "p-4": 1, "mt-2": 2}
        result = _sort_string('"flex p-4 mt-2"', index)
        assert result == '"flex p-4 mt-2"'

    def test_unknown_tokens_placed_at_end(self):
        index = {"flex": 0, "p-4": 1}
        result = _sort_string('"custom-class flex p-4"', index)
        assert result == '"flex p-4 custom-class"'

    def test_preserves_leading_whitespace(self):
        index = {"flex": 0, "p-4": 1}
        result = _sort_string('"  p-4 flex"', index)
        assert result == '"  flex p-4"'

    def test_preserves_trailing_whitespace(self):
        index = {"flex": 0, "p-4": 1}
        result = _sort_string('"p-4 flex  "', index)
        assert result == '"flex p-4  "'

    def test_preserves_both_leading_and_trailing_whitespace(self):
        index = {"flex": 0, "p-4": 1}
        result = _sort_string('"  p-4 flex  "', index)
        assert result == '"  flex p-4  "'

    def test_returns_empty_string_unchanged(self):
        index = {"flex": 0}
        assert _sort_string('""', index) == '""'

    def test_returns_whitespace_only_string_unchanged(self):
        index = {"flex": 0}
        assert _sort_string('"   "', index) == '"   "'

    def test_skips_strings_with_angle_brackets(self):
        index = {"flex": 0, "p-4": 1}
        raw = '"<div> flex p-4"'
        assert _sort_string(raw, index) == raw

    def test_skips_when_below_threshold(self):
        # THRESHOLD is 0.6, so 1 known out of 5 = 0.2, skip
        index = {"flex": 0}
        raw = '"flex unknown1 unknown2 unknown3 unknown4"'
        assert _sort_string(raw, index) == raw

    def test_sorts_when_above_threshold(self):
        # 3 known out of 4 = 0.75, above THRESHOLD
        index = {"flex": 0, "p-4": 1, "mt-2": 2}
        result = _sort_string('"mt-2 flex p-4 custom"', index)
        assert result == '"flex p-4 mt-2 custom"'

    def test_works_with_single_quotes(self):
        index = {"flex": 0, "p-4": 1}
        result = _sort_string("'p-4 flex'", index)
        assert result == "'flex p-4'"

    def test_single_token_returns_unchanged(self):
        index = {"flex": 0}
        assert _sort_string('"flex"', index) == '"flex"'


# ---------------------------------------------------------------------------
# Library: sort_file()
# ---------------------------------------------------------------------------


class TestSortFile:
    def test_sorts_strings_in_file(self, tmp_path):
        f = tmp_path / "test.py"
        f.write_text('cls = "mt-2 flex p-4"\n')
        index = {"flex": 0, "p-4": 1, "mt-2": 2}

        changed = sort_file(f, index)

        assert changed is True
        assert f.read_text() == 'cls = "flex p-4 mt-2"\n'

    def test_check_mode_does_not_modify_file(self, tmp_path):
        f = tmp_path / "test.py"
        original = 'cls = "mt-2 flex p-4"\n'
        f.write_text(original)
        index = {"flex": 0, "p-4": 1, "mt-2": 2}

        changed = sort_file(f, index, check=True)

        assert changed is True
        assert f.read_text() == original

    def test_returns_false_when_no_changes_needed(self, tmp_path):
        f = tmp_path / "test.py"
        f.write_text('cls = "flex p-4 mt-2"\n')
        index = {"flex": 0, "p-4": 1, "mt-2": 2}

        changed = sort_file(f, index)

        assert changed is False

    def test_skips_fstrings(self, tmp_path):
        f = tmp_path / "test.py"
        original = 'cls = f"mt-2 flex {var} p-4"\n'
        f.write_text(original)
        index = {"flex": 0, "p-4": 1, "mt-2": 2}

        changed = sort_file(f, index)

        assert changed is False
        assert f.read_text() == original

    def test_sorts_multiple_strings_in_file(self, tmp_path):
        f = tmp_path / "test.py"
        f.write_text('a = "mt-2 flex"\nb = "p-4 flex"\n')
        index = {"flex": 0, "p-4": 1, "mt-2": 2}

        changed = sort_file(f, index)

        assert changed is True
        content = f.read_text()
        assert '"flex mt-2"' in content
        assert '"flex p-4"' in content

    def test_preserves_non_string_content(self, tmp_path):
        f = tmp_path / "test.py"
        f.write_text('# comment\ncls = "mt-2 flex"\nx = 42\n')
        index = {"flex": 0, "mt-2": 2}

        sort_file(f, index)

        content = f.read_text()
        assert content.startswith("# comment\n")
        assert "x = 42" in content

    def test_leaves_unrecognized_strings_alone(self, tmp_path):
        f = tmp_path / "test.py"
        original = 'msg = "hello world"\n'
        f.write_text(original)
        index = {"flex": 0, "p-4": 1}

        changed = sort_file(f, index)

        assert changed is False
        assert f.read_text() == original


# ---------------------------------------------------------------------------
# Library: _extract_tokens()
# ---------------------------------------------------------------------------


class TestExtractTokens:
    def test_extracts_tokens_from_simple_strings(self, tmp_path):
        f = tmp_path / "test.py"
        f.write_text('cls = "flex p-4 mt-2"\n')

        tokens = _extract_tokens([f])

        assert "flex" in tokens
        assert "p-4" in tokens
        assert "mt-2" in tokens

    def test_skips_fstrings(self, tmp_path):
        f = tmp_path / "test.py"
        f.write_text('cls = f"flex {var} p-4"\n')

        tokens = _extract_tokens([f])

        assert tokens == set()

    def test_extracts_from_multiple_files(self, tmp_path):
        f1 = tmp_path / "a.py"
        f1.write_text('a = "flex"\n')
        f2 = tmp_path / "b.py"
        f2.write_text('b = "p-4"\n')

        tokens = _extract_tokens([f1, f2])

        assert "flex" in tokens
        assert "p-4" in tokens

    def test_extracts_from_single_quoted_strings(self, tmp_path):
        f = tmp_path / "test.py"
        f.write_text("cls = 'flex p-4'\n")

        tokens = _extract_tokens([f])

        assert "flex" in tokens
        assert "p-4" in tokens

    def test_extracts_from_multiple_strings_per_file(self, tmp_path):
        f = tmp_path / "test.py"
        f.write_text('a = "flex"\nb = "p-4"\n')

        tokens = _extract_tokens([f])

        assert "flex" in tokens
        assert "p-4" in tokens

    def test_deduplicates_tokens(self, tmp_path):
        f = tmp_path / "test.py"
        f.write_text('a = "flex flex"\n')

        tokens = _extract_tokens([f])

        # set deduplication means "flex" appears once
        assert tokens == {"flex"}


# ---------------------------------------------------------------------------
# CLI: sort_command
# ---------------------------------------------------------------------------


def _run_sort_command(
    paths=None,
    check=False,
    verbose=False,
    sort_files_return=None,
) -> str:
    """Run sort_command, capturing console output and returning it as a string.

    sort_files is mocked to avoid needing a real Tailwind binary.
    status_context is replaced with a nullcontext so no spinner is started.
    """
    if sort_files_return is None:
        sort_files_return = {}

    buf = StringIO()
    real_console = Console(file=buf, width=300, no_color=True)

    with (
        patch("starui.cli.sort.sort_files", return_value=sort_files_return),
        patch("starui.cli.sort.status_context", return_value=nullcontext()),
        patch("starui.cli.sort.console", real_console),
        patch("starui.cli.sort.success", lambda msg: real_console.print(f"OK: {msg}")),
        patch("starui.cli.sort.error", lambda msg: real_console.print(f"ERR: {msg}")),
        patch("starui.cli.sort.info", lambda msg: real_console.print(f"INFO: {msg}")),
    ):
        sort_command(paths=paths, check=check, verbose=verbose)

    return buf.getvalue()


class TestSortCommandFileCollection:
    def test_collects_py_files_from_directory(self, tmp_path):
        (tmp_path / "a.py").write_text("")
        (tmp_path / "b.py").write_text("")
        (tmp_path / "readme.txt").write_text("")

        output = _run_sort_command(
            paths=[str(tmp_path)],
            sort_files_return={},
        )

        assert "already sorted" in output

    def test_accepts_specific_file_path(self, tmp_path):
        f = tmp_path / "test.py"
        f.write_text("")

        output = _run_sort_command(
            paths=[str(f)],
            sort_files_return={f: False},
        )

        assert "already sorted" in output

    def test_ignores_non_py_file(self, tmp_path):
        f = tmp_path / "readme.txt"
        f.write_text("")

        with pytest.raises(Exit):
            _run_sort_command(paths=[str(f)])

    def test_skips_venv_directory(self, tmp_path):
        venv_dir = tmp_path / ".venv"
        venv_dir.mkdir()
        (venv_dir / "module.py").write_text("")
        # No other .py files => should error
        with pytest.raises(Exit):
            _run_sort_command(paths=[str(tmp_path)])

    def test_skips_plain_venv_directory(self, tmp_path):
        venv_dir = tmp_path / "venv"
        venv_dir.mkdir()
        (venv_dir / "module.py").write_text("")
        with pytest.raises(Exit):
            _run_sort_command(paths=[str(tmp_path)])

    def test_skips_pycache_directory(self, tmp_path):
        cache_dir = tmp_path / "__pycache__"
        cache_dir.mkdir()
        (cache_dir / "module.py").write_text("")
        with pytest.raises(Exit):
            _run_sort_command(paths=[str(tmp_path)])

    def test_skips_node_modules_directory(self, tmp_path):
        nm_dir = tmp_path / "node_modules"
        nm_dir.mkdir()
        (nm_dir / "module.py").write_text("")
        with pytest.raises(Exit):
            _run_sort_command(paths=[str(tmp_path)])

    def test_skips_git_directory(self, tmp_path):
        git_dir = tmp_path / ".git"
        git_dir.mkdir()
        (git_dir / "hook.py").write_text("")
        with pytest.raises(Exit):
            _run_sort_command(paths=[str(tmp_path)])

    def test_skips_nested_excluded_directory(self, tmp_path):
        # .py file in a deeply nested excluded directory should be skipped
        nested = tmp_path / "sub" / "__pycache__"
        nested.mkdir(parents=True)
        (nested / "cached.py").write_text("")
        # Only excluded dirs, no valid files
        with pytest.raises(Exit):
            _run_sort_command(paths=[str(tmp_path)])

    def test_collects_files_from_subdirectories(self, tmp_path):
        sub = tmp_path / "pkg"
        sub.mkdir()
        (sub / "mod.py").write_text("")
        (tmp_path / "top.py").write_text("")

        output = _run_sort_command(
            paths=[str(tmp_path)],
            sort_files_return={},
        )

        assert "already sorted" in output


class TestSortCommandExitCodes:
    def test_exits_1_when_no_py_files_found(self, tmp_path):
        # Empty directory
        with pytest.raises(Exit):
            _run_sort_command(paths=[str(tmp_path)])

    def test_exits_1_in_check_mode_when_files_need_sorting(self, tmp_path):
        f = tmp_path / "test.py"
        f.write_text("")

        with pytest.raises(Exit):
            _run_sort_command(
                paths=[str(f)],
                check=True,
                sort_files_return={f: True},
            )

    def test_check_mode_exits_0_when_all_sorted(self, tmp_path):
        f = tmp_path / "test.py"
        f.write_text("")

        output = _run_sort_command(
            paths=[str(f)],
            check=True,
            sort_files_return={f: False},
        )

        assert "already sorted" in output


class TestSortCommandOutput:
    def test_reports_sorted_count_in_normal_mode(self, tmp_path):
        f1 = tmp_path / "a.py"
        f2 = tmp_path / "b.py"
        f1.write_text("")
        f2.write_text("")

        output = _run_sort_command(
            paths=[str(f1), str(f2)],
            sort_files_return={f1: True, f2: True},
        )

        assert "Sorted 2 file(s)" in output

    def test_reports_all_sorted_when_nothing_changed(self, tmp_path):
        f = tmp_path / "test.py"
        f.write_text("")

        output = _run_sort_command(
            paths=[str(f)],
            sort_files_return={f: False},
        )

        assert "All files already sorted" in output

    def test_check_mode_uses_would_sort_verb(self, tmp_path):
        f = tmp_path / "test.py"
        f.write_text("")

        buf = StringIO()
        real_console = Console(file=buf, width=300, no_color=True)

        with (
            patch("starui.cli.sort.sort_files", return_value={f: True}),
            patch("starui.cli.sort.status_context", return_value=nullcontext()),
            patch("starui.cli.sort.console", real_console),
            patch("starui.cli.sort.success", lambda msg: real_console.print(f"OK: {msg}")),
            patch("starui.cli.sort.error", lambda msg: real_console.print(f"ERR: {msg}")),
            patch("starui.cli.sort.info", lambda msg: real_console.print(f"INFO: {msg}")),
            pytest.raises(Exit),
        ):
            sort_command(paths=[str(f)], check=True, verbose=False)

        output = buf.getvalue()
        assert "would sort" in output

    def test_normal_mode_uses_sorted_verb(self, tmp_path):
        f = tmp_path / "test.py"
        f.write_text("")

        buf = StringIO()
        real_console = Console(file=buf, width=300, no_color=True)

        with (
            patch("starui.cli.sort.sort_files", return_value={f: True}),
            patch("starui.cli.sort.status_context", return_value=nullcontext()),
            patch("starui.cli.sort.console", real_console),
            patch("starui.cli.sort.success", lambda msg: real_console.print(f"OK: {msg}")),
            patch("starui.cli.sort.error", lambda msg: real_console.print(f"ERR: {msg}")),
            patch("starui.cli.sort.info", lambda msg: real_console.print(f"INFO: {msg}")),
        ):
            sort_command(paths=[str(f)], check=False, verbose=False)

        output = buf.getvalue()
        assert "sorted" in output.lower()
        assert "would sort" not in output

    def test_check_mode_reports_file_count_needing_sort(self, tmp_path):
        f = tmp_path / "test.py"
        f.write_text("")

        buf = StringIO()
        real_console = Console(file=buf, width=300, no_color=True)

        with (
            patch("starui.cli.sort.sort_files", return_value={f: True}),
            patch("starui.cli.sort.status_context", return_value=nullcontext()),
            patch("starui.cli.sort.console", real_console),
            patch("starui.cli.sort.success", lambda msg: real_console.print(f"OK: {msg}")),
            patch("starui.cli.sort.error", lambda msg: real_console.print(f"ERR: {msg}")),
            patch("starui.cli.sort.info", lambda msg: real_console.print(f"INFO: {msg}")),
            pytest.raises(Exit),
        ):
            sort_command(paths=[str(f)], check=True, verbose=False)

        output = buf.getvalue()
        assert "1 file(s) need sorting" in output

    def test_verbose_shows_file_count(self, tmp_path):
        f = tmp_path / "test.py"
        f.write_text("")

        output = _run_sort_command(
            paths=[str(f)],
            verbose=True,
            sort_files_return={f: False},
        )

        assert "Processing 1 file(s)" in output

    def test_verbose_not_shown_by_default(self, tmp_path):
        f = tmp_path / "test.py"
        f.write_text("")

        output = _run_sort_command(
            paths=[str(f)],
            verbose=False,
            sort_files_return={f: False},
        )

        assert "Processing" not in output

    def test_no_py_files_shows_error_message(self, tmp_path):
        buf = StringIO()
        real_console = Console(file=buf, width=300, no_color=True)

        with (
            patch("starui.cli.sort.sort_files"),
            patch("starui.cli.sort.status_context", return_value=nullcontext()),
            patch("starui.cli.sort.console", real_console),
            patch("starui.cli.sort.success", lambda msg: real_console.print(f"OK: {msg}")),
            patch("starui.cli.sort.error", lambda msg: real_console.print(f"ERR: {msg}")),
            patch("starui.cli.sort.info", lambda msg: real_console.print(f"INFO: {msg}")),
            pytest.raises(Exit),
        ):
            sort_command(paths=[str(tmp_path)], check=False, verbose=False)

        output = buf.getvalue()
        assert "No .py files found" in output
