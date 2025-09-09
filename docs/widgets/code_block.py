from starhtml import Div, FT, Icon, Span
from starhtml.datastar import ds_on_click, ds_text, ds_signals, ds_show, ds_class, if_, toggle_signal, toggle_class
from starui.registry.components.button import Button
from starui.registry.components.utils import cn
from starui.registry.components.code_block import CodeBlock as BaseCodeBlock


def CodeBlock(
    code: str,
    language: str = "python",
    show_copy: bool = True,
    collapsible: bool = True,
    default_collapsed: bool = False,
    cls: str = "",
    **attrs
) -> FT:
    code_id = f"code_{abs(hash(code))}"
    collapsed_signal = f"collapsed_{code_id}"
    
    header_cls = cn(
        "flex items-center justify-between px-3 py-2",
        collapsible and "cursor-pointer select-none hover:bg-muted/50 transition-colors",
        if_(f"${collapsed_signal}", "", "border-b border-border/50") if collapsible else "border-b border-border/50"
    )
    
    return Div(
        Div(
            Div(
                _chevron_button(collapsed_signal) if collapsible else Div(cls="w-6"),
                Span(language, cls="text-xs font-medium text-muted-foreground"),
                _copy_button(code_id, code) if show_copy else Div(cls="w-8"),
                collapsible and ds_on_click(toggle_signal(collapsed_signal)),
                cls=header_cls
            ),
            Div(
                BaseCodeBlock(code, language, cls="font-mono text-sm !border-0 !border-none overflow-x-auto", style="scrollbar-width: thin; scrollbar-color: transparent transparent;"),
                toggle_class(
                    f"${collapsed_signal}",
                    "max-h-0 overflow-hidden",
                    "max-h-[2000px]"
                ),
                cls="transition-all duration-300 ease-in-out"
            ),
            ds_signals({
                collapsed_signal: default_collapsed,
                f"copied_{code_id}": False
            }),
            cls="bg-muted/30 border border-border rounded-lg overflow-hidden group"
        ),
        cls=cn("relative mb-6", cls),
        **attrs
    )



def _chevron_button(collapsed_signal: str) -> FT:
    return Div(
        Span(
            Icon("lucide:chevron-up", cls="h-4 w-4"),
            toggle_class(
                f"${collapsed_signal}",
                "rotate-180",
                "rotate-0"
            ),
            cls="inline-block transition-transform duration-300"
        ),
        ds_on_click(f"evt.stopPropagation(); {toggle_signal(collapsed_signal)}"),
        role="button",
        tabindex="0",
        aria_label="Toggle code block",
        cls="inline-flex items-center justify-center h-6 w-6 text-muted-foreground hover:text-foreground cursor-pointer"
    )


def _copy_button(code_id: str, code: str) -> FT:
    signal = f"copied_{code_id}"
    
    return Button(
        Span(Icon("lucide:check", cls="h-3 w-3"), ds_show(f"${signal}")),
        Span(Icon("lucide:copy", cls="h-3 w-3"), ds_show(f"!${signal}")),
        Span(ds_text(f"${signal} ? 'Copied!' : 'Copy'"), cls="sr-only"),
        ds_on_click(f'evt.stopPropagation(); @clipboard(evt.target.closest(".group").querySelector("code").textContent, "{signal}", 2000)'),
        variant="ghost",
        size="sm",
        cls="h-5 w-5 p-0 text-muted-foreground hover:text-foreground hover:bg-muted transition-all duration-200",
        type="button",
        aria_label="Copy code"
    )