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
            cls="inline-flex items-center gap-0 rounded-md bg-[var(--code-bg,_var(--muted))] text-[color:var(--code-color,_var(--foreground))] border border-[var(--code-border,_var(--border))] font-mono text-sm [font-variant-ligatures:none] py-2 pl-4 pr-3",
            data_slot="code-block"
        ),
        cls=cn("inline-block", cls),
        **attrs
    )