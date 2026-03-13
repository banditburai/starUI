"""Inline code widget with optional copy button - for single-line code snippets."""

from starhtml import Div, FT, NotStr, Signal
from components.utils import cn
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
            cls="inline-flex items-center gap-0 rounded-md border border-[var(--code-border,_var(--border))] bg-[var(--code-bg,_var(--muted))] py-2 pr-3 pl-4 font-mono text-sm text-[color:var(--code-color,_var(--foreground))] [font-variant-ligatures:none]",
            data_slot="code-block"
        ),
        cls=cn("inline-block", cls),
        **attrs
    )