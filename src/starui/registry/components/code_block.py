from typing import Any

from starhtml import FT, Code, Div, NotStr, Style

try:
    from starlighter import highlight, get_theme_css, THEMES
except ImportError:
    def highlight(code: str, language: str = "python") -> str:
        return f'<pre><code class="language-{language}">{code}</code></pre>'

    def get_theme_css(theme: str = "github-dark") -> str:
        return ""

    THEMES = {}

from .utils import cn, DEFAULT_THEME, ALT_THEME


def CodeBlockStyles(
    default_theme: str = "github-light",
    alt_theme: str = "github-dark",
    custom_vars: dict[str, str] | None = None,
    custom_css: str = "",
) -> FT:
    """Generate theme-aware styles for CodeBlock. Add once to app headers."""
    css = get_theme_css(default_theme)

    if THEMES:
        if default_vars := THEMES.get(default_theme):
            rules = "\n".join(f"  {k}: {v};" for k, v in default_vars.items())
            css += f"\n:root, [data-theme='{DEFAULT_THEME}'] {{\n{rules}\n}}"

        if alt_vars := THEMES.get(alt_theme):
            rules = "\n".join(f"  {k}: {v};" for k, v in alt_vars.items())
            css += f"\n[data-theme='{ALT_THEME}'] {{\n{rules}\n}}"

    if custom_vars:
        rules = "\n".join(f"  {k}: {v};" for k, v in custom_vars.items())
        css += f"\n:root {{\n{rules}\n}}"

    if custom_css:
        css += f"\n{custom_css}"

    return Style(NotStr(css))


def CodeBlock(
    code: str,
    language: str = "python",
    cls: str = "",
    **kwargs: Any,
) -> FT:
    return Div(
        NotStr(highlight(code, language)),
        cls=cn("code-container", cls),
        **kwargs
    )


def InlineCode(
    text: str,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    return Code(
        text,
        cls=cn("rounded bg-muted px-[0.3rem] py-[0.2rem] font-mono text-sm", cls),
        **kwargs
    )


__all__ = ["CodeBlock", "CodeBlockStyles", "InlineCode"]
