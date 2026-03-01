from html import escape
from typing import Any

from starhtml import FT, Code, Div, NotStr, Style

try:
    from starlighter import THEMES, highlight
except ImportError:

    def highlight(code: str, language: str = "python") -> str:
        return f'<pre><code class="language-{language}">{escape(code)}</code></pre>'

    THEMES = {}

from .utils import ALT_THEME, DEFAULT_THEME, cn

_RESIDUAL_CSS = """
[data-slot="code-block"]::-webkit-scrollbar { height: 8px; width: 8px; }
[data-slot="code-block"]::-webkit-scrollbar-track { background: var(--scrollbar-track); }
[data-slot="code-block"]::-webkit-scrollbar-thumb { background: var(--scrollbar-thumb); border-radius: 4px; }
[data-slot="code-block"]::-webkit-scrollbar-thumb:hover { background: var(--scrollbar-thumb-hover); }
.token-keyword { color: var(--token-keyword); }
.token-string { color: var(--token-string); }
.token-comment { color: var(--token-comment); font-style: italic; }
.token-number { color: var(--token-number); }
.token-operator { color: var(--token-operator); }
.token-identifier { color: var(--token-identifier); }
.token-builtin { color: var(--token-builtin); }
.token-decorator { color: var(--token-decorator); }
.token-punctuation { color: var(--token-punctuation); }
.token-starhtml-element { color: var(--token-starhtml-element); }
.token-datastar-attr { color: var(--token-datastar-attr); }
.token-css-class { color: var(--token-css-class); }
.token-css-style { color: var(--token-css-style); }
.token-signal { color: var(--token-signal); }
"""


def CodeBlockStyles(
    default_theme: str = "github-light",
    alt_theme: str = "github-dark",
    custom_vars: dict[str, str] | None = None,
    custom_css: str = "",
) -> FT:
    """Generate theme-aware styles for CodeBlock. Add once to app headers."""
    css = _RESIDUAL_CSS

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


_CODE_BLOCK_CLS = (
    "rounded-md overflow-x-auto m-0 min-w-0 px-5 py-4"
    " bg-[var(--code-bg,_var(--muted))]"
    " text-[color:var(--code-color,_var(--foreground))]"
    " border border-[var(--code-border,_var(--border))]"
    " font-mono text-sm leading-normal [tab-size:2] [font-variant-ligatures:none]"
    " [scrollbar-width:thin] [scrollbar-color:var(--scrollbar-thumb,_var(--border))_var(--scrollbar-track,_transparent)]"
    " focus-visible:outline-2 focus-visible:outline-ring/50 focus-visible:outline-offset-2"
    " [&_pre]:m-0 [&_pre]:font-[inherit] [&_pre]:text-[length:inherit] [&_pre]:leading-[inherit]"
    " [&_pre]:whitespace-pre [&_pre]:overflow-x-visible [&_pre]:min-w-0"
    " [&_code]:font-[inherit] [&_code]:bg-transparent [&_code]:p-0"
    " [&_code]:block [&_code]:whitespace-pre [&_code]:overflow-x-visible"
)


def CodeBlock(
    code: str,
    language: str = "python",
    cls: str = "",
    **kwargs: Any,
) -> FT:
    return Div(
        NotStr(highlight(code, language)),
        cls=cn(_CODE_BLOCK_CLS, cls),
        data_slot="code-block",
        tabindex="0",
        **kwargs,
    )


def InlineCode(
    text: str,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    return Code(
        text,
        cls=cn(
            "rounded bg-muted px-[0.3rem] py-[0.2rem] font-mono text-sm",
            "break-words [font-variant-ligatures:none]",
            cls,
        ),
        **kwargs,
    )


__all__ = ["CodeBlock", "CodeBlockStyles", "InlineCode"]
