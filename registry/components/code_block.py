from html import escape
from typing import Any

from starhtml import FT, Code, Div, NotStr

try:
    from starlighter import highlight
except ImportError:

    def highlight(code: str, language: str = "python") -> str:
        return f'<pre><code class="language-{language}">{escape(code)}</code></pre>'


from .utils import cn

__metadata__ = {"description": "Code block with syntax highlighting", "packages": ["starlighter"]}


_CODE_BLOCK_CLS = (
    "m-0 min-w-0 overflow-x-auto rounded-md px-5 py-4"
    " bg-[var(--code-bg,_var(--muted))]"
    " text-[color:var(--code-color,_var(--foreground))]"
    " border border-[var(--code-border,_var(--border))]"
    " font-mono text-sm leading-normal [font-variant-ligatures:none] [tab-size:2]"
    " [scrollbar-color:var(--scrollbar-thumb,_var(--border))_var(--scrollbar-track,_transparent)] [scrollbar-width:thin]"
    " focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring/50"
    " [&_pre]:m-0 [&_pre]:font-[inherit] [&_pre]:text-[length:inherit] [&_pre]:leading-[inherit]"
    " [&_pre]:min-w-0 [&_pre]:overflow-x-visible [&_pre]:whitespace-pre"
    " [&_code]:bg-transparent [&_code]:p-0 [&_code]:font-[inherit]"
    " [&_code]:block [&_code]:overflow-x-visible [&_code]:whitespace-pre"
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


__all__ = ["CodeBlock", "InlineCode"]
