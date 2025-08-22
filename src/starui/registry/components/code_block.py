from typing import Any

from starhtml import Code, Div, NotStr

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
    **attrs: Any,
):
    """Syntax-highlighted code block that auto-switches with theme."""
    highlighted_html = highlight(code, language)
    classes = cn("code-container", class_name, cls)

    return Div(NotStr(highlighted_html), cls=classes, **attrs)


def InlineCode(text: str, class_name: str = "", cls: str = "", **attrs: Any):
    """Inline code snippet without syntax highlighting."""
    classes = cn(
        "rounded bg-muted px-[0.3rem] py-[0.2rem] font-mono text-sm", class_name, cls
    )

    return Code(text, cls=classes, **attrs)


__all__ = ["CodeBlock", "InlineCode"]
