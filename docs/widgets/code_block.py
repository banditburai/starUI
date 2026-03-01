from starhtml import Div, FT, Icon, Span, Signal
from starhtml.datastar import js
from starui.registry.components.utils import cn
from starui.registry.components.code_block import CodeBlock as BaseCodeBlock
from .copy_button import CopyButton


def CodePanel(
    code: str,
    language: str = "python",
    show_copy: bool = True,
    collapsible: bool = True,
    default_collapsed: bool = False,
    cls: str = "",
    **attrs
) -> FT:
    code_id = f"code_{abs(hash(code))}"
    collapsed_signal_name = f"collapsed_{code_id}"
    copied_signal_name = f"copied_{code_id}"

    return Div(
        (collapsed := Signal(collapsed_signal_name, default_collapsed)),
        (copied := Signal(copied_signal_name, False)),
        Div(
            Div(
                _chevron_button(collapsed) if collapsible else Div(cls="w-6"),
                Span(language, cls="text-xs font-medium text-muted-foreground"),
                CopyButton(code_id, copied, variant="embedded", stop_propagation=True) if show_copy else Div(cls="w-8"),
                data_on_click=collapsed.toggle() if collapsible else None,
                cls=cn(
                    "flex items-center justify-between px-3 py-2",
                    collapsible and "cursor-pointer select-none hover:bg-muted/50 transition-colors",
                    not collapsible and "border-b border-border/50",
                ),
                data_attr_cls=collapsed.if_("", "border-b border-border/50") if collapsible else None
            ),
            Div(
                BaseCodeBlock(code, language, id=code_id, cls="font-mono text-sm !border-0 !border-none overflow-x-auto"),
                cls=cn("transition-all duration-300 ease-in-out", not collapsible and "max-h-[2000px]"),
                data_attr_cls=collapsed.if_("max-h-0 overflow-hidden", "max-h-[2000px]") if collapsible else None
            ),
            cls="bg-muted/30 border border-border rounded-lg overflow-hidden group"
        ),
        cls=cn("relative mb-6", cls),
        **attrs
    )


def CodeBlock(code: str, language: str = "bash", cls: str = "", center_button: bool = False, **attrs) -> FT:
    code_id = f"code_{abs(hash(code))}"
    signal_name = f"copied_{code_id}"

    return Div(
        (copied := Signal(signal_name, False)),
        BaseCodeBlock(code, language=language, id=code_id, cls="overflow-x-auto"),
        CopyButton(code_id, copied, variant="positioned", center=center_button),
        cls=cn("relative group", cls),
        **attrs
    )


def _chevron_button(collapsed: Signal) -> FT:
    return Div(
        Span(
            Icon("lucide:chevron-up", cls="h-4 w-4"),
            cls="inline-block transition-transform duration-300",
            data_attr_cls=collapsed.if_("rotate-180", "rotate-0")
        ),
        data_on_click=(js("evt.stopPropagation()"), collapsed.toggle()),
        role="button",
        tabindex="0",
        aria_label="Toggle code block",
        cls="inline-flex items-center justify-center h-6 w-6 text-muted-foreground hover:text-foreground cursor-pointer"
    )