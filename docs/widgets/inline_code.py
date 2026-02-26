"""Inline code widget with optional copy button - for single-line code snippets."""

from starhtml import Div, FT, NotStr, Signal
from starui.registry.components.utils import cn
from .copy_button import CopyButton

try:
    from starlighter import highlight
except ImportError:
    def highlight(code: str, language: str = "python") -> str:
        return f'<pre><code class="language-{language}">{code}</code></pre>'


def InlineCode(
    code: str,
    *,
    language: str = "bash",
    cls: str = "",
    copy_button: bool = True,
    **attrs
) -> FT:
    code_id = f"code_{abs(hash(code))}"
    signal_name = f"copied_{code_id}"

    return Div(
        copy_button and (copied := Signal(signal_name, False)),
        Div(
            Div(NotStr(highlight(code, language)), id=code_id),
            copy_button and CopyButton(code_id, copied, variant="inline"),
            cls="code-container inline-flex items-center gap-0 !py-2 !pl-4 !pr-3"
        ),
        cls=cn("inline-block", cls),
        **attrs
    )