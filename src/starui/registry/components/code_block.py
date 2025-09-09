from typing import Any

from starhtml import FT, Code, Div, NotStr

try:
    from starlighter import highlight
except ImportError:
    def highlight(code: str, language: str = "python") -> str:
        return f'<pre><code class="language-{language}">{code}</code></pre>'

from .utils import cn


def CodeBlock(
    code: str,
    language: str = "python",
    class_name: str = "",
    cls: str = "",
    **kwargs: Any,
) -> FT:
    return Div(
        NotStr(highlight(code, language)),
        cls=cn("code-container", class_name, cls),
        **kwargs
    )


def InlineCode(
    text: str,
    class_name: str = "",
    cls: str = "",
    **kwargs: Any,
) -> FT:
    return Code(
        text,
        cls=cn("rounded bg-muted px-[0.3rem] py-[0.2rem] font-mono text-sm", class_name, cls),
        **kwargs
    )


__all__ = ["CodeBlock", "InlineCode"]
