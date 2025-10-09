from starhtml import FT, Icon, Span, Signal
from starhtml.datastar import clipboard, js
from starui.registry.components.button import Button


def CopyButton(
    code_id: str,
    copied: Signal,
    variant: str = "positioned",
    stop_propagation: bool = False,
    center: bool = False
) -> FT:
    """Copy button with context-specific positioning: embedded, positioned, group-hover, inline.

    Args:
        center: If True, vertically centers the button (for single-line code).
               If False, positions at top (for multi-line code blocks).
    """
    vertical_pos = "top-1/2 -translate-y-1/2" if center else "top-3"

    variants = {
        "embedded": "h-5 w-5 p-0 text-muted-foreground hover:text-foreground hover:bg-muted transition-all duration-200",
        "positioned": f"absolute {vertical_pos} right-3 h-7 w-7 p-0 text-muted-foreground hover:text-foreground hover:bg-muted opacity-75 hover:opacity-100 transition-all duration-200",
        "group-hover": f"absolute {vertical_pos} right-3 h-7 w-7 p-0 text-muted-foreground hover:text-foreground hover:bg-muted opacity-0 group-hover:opacity-100 transition-all duration-200",
        "inline": "h-6 w-6 p-0 ml-3 text-muted-foreground hover:text-foreground transition-colors flex-shrink-0",
    }

    click_handler = clipboard(element=f'#{code_id}', signal=copied.id)
    if stop_propagation:
        click_handler = (js("evt.stopPropagation()"), click_handler)

    return Button(
        Span(Icon("lucide:check", cls="h-3 w-3"), data_show=copied),
        Span(Icon("lucide:copy", cls="h-3 w-3"), data_show=~copied),
        Span(data_text=copied.if_("Copied!", "Copy"), cls="sr-only"),
        data_on_click=click_handler,
        variant="ghost",
        size="sm",
        cls=variants.get(variant, variants["positioned"]),
        type="button",
        aria_label="Copy code"
    )
