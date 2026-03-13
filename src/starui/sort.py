"""Tailwind class sorting engine."""

import re
import subprocess
import tempfile
from pathlib import Path

from .css import TailwindBinaryManager
from .templates import TAILWIND_CSS_TEMPLATE

_STRING_RE = re.compile(r'"[^"\n\\]*(?:\\.[^"\n\\]*)*"|\'[^\'\n\\]*(?:\\.[^\'\n\\]*)*\'')
_SELECTOR_RE = re.compile(r"\.((?:[^{}\s:,>+~\[\]\\]|\\.)+)")

THRESHOLD = 0.6


def tokenize(s: str) -> list[str]:
    """Bracket-aware whitespace splitter for Tailwind class strings."""
    tokens: list[str] = []
    i, n = 0, len(s)
    while i < n:
        while i < n and s[i] in " \t\n":
            i += 1
        if i >= n:
            break
        start = i
        depth = 0
        while i < n and (depth > 0 or s[i] not in " \t\n"):
            if s[i] in "([":
                depth += 1
            elif s[i] in ")]":
                depth = max(0, depth - 1)
            i += 1
        tokens.append(s[start:i])
    return tokens


def _is_fstring(src: str, pos: int) -> bool:
    i = pos - 1
    while i >= 0 and src[i] in "fFrRbBuU":
        if src[i] in "fF":
            return True
        i -= 1
    return False


def _extract_tokens(files: list[Path]) -> set[str]:
    tokens: set[str] = set()
    for path in files:
        src = path.read_text()
        for m in _STRING_RE.finditer(src):
            if not _is_fstring(src, m.start()):
                for tok in tokenize(m.group()[1:-1]):
                    tokens.add(tok)
    return tokens


def _build_sort_index(tokens: set[str], binary: Path) -> dict[str, int]:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        html_path = tmp_path / "tokens.html"
        token_list = sorted(tokens)
        html_path.write_text(
            "\n".join(
                f'<div class="{" ".join(token_list[i : i + 100])}"></div>' for i in range(0, len(token_list), 100)
            )
        )

        # source(none) prevents Tailwind from scanning the project tree
        css_input = TAILWIND_CSS_TEMPLATE.replace('@import "tailwindcss"', '@import "tailwindcss" source(none)')
        css_input = re.sub(r'@plugin "[^"]*";\n?', "", css_input)
        css_input += f'\n@source "./{html_path.name}";\n'

        (tmp_path / "input.css").write_text(css_input)
        output_path = tmp_path / "output.css"

        result = subprocess.run(
            [str(binary), "-i", str(tmp_path / "input.css"), "-o", str(output_path)],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=tmp,
        )
        if result.returncode != 0:
            raise RuntimeError(f"Tailwind build failed: {result.stderr}")

        css = output_path.read_text()
        layer_match = re.search(r"@layer\s+utilities\s*\{", css)
        if not layer_match:
            return {}

        start = layer_match.end()
        depth, i = 1, start
        while i < len(css) and depth > 0:
            if css[i] == "{":
                depth += 1
            elif css[i] == "}":
                depth -= 1
            i += 1

        index: dict[str, int] = {}
        pos = 0
        for m in _SELECTOR_RE.finditer(css[start : i - 1]):
            name = re.sub(r"\\(.)", r"\1", m.group(1))
            if name not in index:
                index[name] = pos
                pos += 1
        return index


def _sort_string(raw: str, index: dict[str, int]) -> str:
    quote = raw[0]
    content = raw[1:-1]
    stripped = content.strip()
    if not stripped:
        return raw

    tokens = tokenize(stripped)
    if not tokens or any("<" in t or ">" in t for t in tokens):
        return raw

    known = [(t, index[t]) for t in tokens if t in index]
    if len(known) / len(tokens) < THRESHOLD:
        return raw

    # Preserve leading/trailing whitespace for implicit string concatenation
    leading = content[: len(content) - len(content.lstrip())]
    trailing = content[len(content.rstrip()) :]

    unknown = [t for t in tokens if t not in index]
    sorted_known = [t for t, _ in sorted(known, key=lambda x: x[1])]
    return quote + leading + " ".join(sorted_known + unknown) + trailing + quote


def sort_file(path: Path, index: dict[str, int], *, check: bool = False) -> bool:
    """Sort class strings in a file. Returns True if changes were made/needed."""
    src = path.read_text()
    parts: list[str] = []
    last_end = 0
    changed = False

    for m in _STRING_RE.finditer(src):
        if _is_fstring(src, m.start()):
            continue

        original = m.group()
        sorted_str = _sort_string(original, index)

        if sorted_str != original:
            changed = True

        parts.append(src[last_end : m.start()])
        parts.append(sorted_str)
        last_end = m.end()

    if changed and not check:
        parts.append(src[last_end:])
        path.write_text("".join(parts))

    return changed


def sort_files(files: list[Path], *, check: bool = False) -> dict[Path, bool]:
    """Sort Tailwind classes in all given files. Returns {path: changed}."""
    binary = TailwindBinaryManager().get_binary()
    tokens = _extract_tokens(files)
    index = _build_sort_index(tokens, binary)
    return {path: sort_file(path, index, check=check) for path in files}
