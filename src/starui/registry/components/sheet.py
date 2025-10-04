from typing import Literal

from starhtml import FT, Div, P, Span, Signal
from starhtml import H2 as HTMLH2
from starhtml.datastar import js

from .utils import cn

SheetSide = Literal["top", "right", "bottom", "left"]
SheetSize = Literal["sm", "md", "lg", "xl", "full"]


def Sheet(
    *children,
    signal: str,
    modal: bool = True,
    default_open: bool = False,
    cls: str = "",
    **kwargs,
) -> FT:
    signal_name = f"{signal}_open"
    sheet_open = Signal(signal_name, default_open)

    return Div(
        sheet_open,
        Div(data_effect=js(f"document.body.style.overflow = ${signal_name} ? 'hidden' : ''")) if modal else None,
        *children,
        **{"data-on-keydown__window__key.Escape": sheet_open.set(False)} if modal else {},
        data_slot="sheet",
        data_sheet_root=signal,
        data_attr_state=sheet_open.if_("open", "closed"),
        cls=cn("relative", cls),
        **kwargs,
    )


def SheetTrigger(
    *children,
    signal: str,
    variant: str = "outline",
    cls: str = "",
    **kwargs,
) -> FT:
    from .button import Button

    signal_name = f"{signal}_open"
    content_id = f"{signal}_content"

    return Button(
        *children,
        data_on_click=js(f"${signal_name} = true"),
        id=f"{signal}_trigger",
        data_attr_aria_expanded=js(f"${signal_name}"),
        aria_haspopup="dialog",
        aria_controls=content_id,
        data_slot="sheet-trigger",
        variant=variant,
        cls=cls,
        **kwargs,
    )


def SheetContent(
    *children,
    signal: str,
    side: SheetSide = "right",
    size: SheetSize = "sm",
    modal: bool = True,
    show_close: bool = True,
    cls: str = "",
    **kwargs,
) -> FT:
    signal_name = f"{signal}_open"
    content_id = f"{signal}_content"

    side_classes = {
        "right": "inset-y-0 right-0 h-full border-l data-[state=closed]:slide-out-to-right data-[state=open]:slide-in-from-right",
        "left": "inset-y-0 left-0 h-full border-r data-[state=closed]:slide-out-to-left data-[state=open]:slide-in-from-left",
        "top": "inset-x-0 top-0 w-full border-b data-[state=closed]:slide-out-to-top data-[state=open]:slide-in-from-top",
        "bottom": "inset-x-0 bottom-0 w-full border-t data-[state=closed]:slide-out-to-bottom data-[state=open]:slide-in-from-bottom",
    }

    size_classes = (
        {
            "sm": "max-w-sm",
            "md": "max-w-md",
            "lg": "max-w-lg",
            "xl": "max-w-xl",
            "full": "max-w-none w-full",
        }
        if side in ["left", "right"]
        else {}
    )

    close_button = (
        SheetClose(
            Span("×", aria_hidden="true", cls="text-2xl font-light leading-none -mt-0.5"),
            signal=signal,
            size="icon",
            cls="absolute right-4 top-4 rounded-sm opacity-70 ring-offset-background transition-opacity hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:pointer-events-none data-[state=open]:bg-secondary",
        )
        if show_close
        else None
    )

    overlay = (
        Div(
            data_show=js(f"${signal_name}"),
            data_on_click=js(f"${signal_name} = false"),
            data_attr_state=js(f"${signal_name} ? 'open' : 'closed'"),
            cls="fixed inset-0 z-[100] bg-black/50 backdrop-blur-sm animate-in fade-in-0",
            data_slot="sheet-overlay",
            style="display: none;",
        )
        if modal
        else None
    )

    content_panel = Div(
        close_button,
        *children,
        data_show=js(f"${signal_name}"),
        id=content_id,
        role="dialog",
        aria_modal="true" if modal else None,
        aria_labelledby=f"{content_id}-title",
        aria_describedby=f"{content_id}-description",
        data_attr_state=js(f"${signal_name} ? 'open' : 'closed'"),
        data_slot="sheet-content",
        cls=cn(
            "fixed z-[110] bg-background shadow-lg border flex flex-col",
            "transition-all duration-300 ease-in-out",
            "data-[state=open]:animate-in data-[state=closed]:animate-out",
            "data-[state=closed]:duration-300 data-[state=open]:duration-500",
            side_classes.get(side, ""),
            size_classes.get(size, ""),
            "overflow-y-auto",
            cls,
        ),
        style="display: none;",
        **kwargs,
    )

    return Div(overlay, content_panel, data_slot="sheet-content-wrapper")


def SheetClose(
    *children,
    signal: str,
    variant: str = "ghost",
    size: str = "sm",
    cls: str = "",
    **kwargs,
) -> FT:
    from .button import Button

    signal_name = f"{signal}_open"
    return Button(
        *children,
        data_on_click=js(f"${signal_name} = false"),
        data_slot="sheet-close",
        variant=variant,
        size=size,
        cls=cls,
        **kwargs,
    )


def SheetHeader(*children, cls: str = "", **kwargs) -> FT:
    return Div(
        *children,
        data_slot="sheet-header",
        cls=cn("flex flex-col space-y-1.5 p-6", cls),
        **kwargs,
    )


def SheetFooter(*children, cls: str = "", **kwargs) -> FT:
    return Div(
        *children,
        data_slot="sheet-footer",
        cls=cn(
            "flex flex-col-reverse sm:flex-row sm:justify-end sm:space-x-2 p-6",
            cls,
        ),
        **kwargs,
    )


def SheetTitle(
    *children, signal: str, cls: str = "", **kwargs
) -> FT:
    content_id = f"{signal}_content"
    return HTMLH2(
        *children,
        id=f"{content_id}-title",
        data_slot="sheet-title",
        cls=cn("text-lg font-semibold text-foreground", cls),
        **kwargs,
    )


def SheetDescription(
    *children, signal: str, cls: str = "", **kwargs
) -> FT:
    content_id = f"{signal}_content"
    return P(
        *children,
        id=f"{content_id}-description",
        data_slot="sheet-description",
        cls=cn("text-sm text-muted-foreground", cls),
        **kwargs,
    )
