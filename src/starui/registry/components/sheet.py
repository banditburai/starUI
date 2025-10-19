from typing import Any, Literal

from starhtml import FT, Div, P, Span, Signal
from starhtml import H2 as HTMLH2
from starhtml.datastar import document, evt

from .utils import cn, gen_id, with_signals, inject_context

SheetSide = Literal["top", "right", "bottom", "left"]
SheetSize = Literal["sm", "md", "lg", "xl", "full"]


def Sheet(
    *children: Any,
    signal: str | Signal = "",
    modal: bool = True,
    default_open: bool = False,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    sig = getattr(signal, 'id', signal) or gen_id("sheet")
    sheet_open = Signal(f"{sig}_open", default_open)

    escape_handler = (evt.key == "Escape").then(sheet_open.set(False))

    ctx = dict(sig=sig, sheet_open=sheet_open, modal=modal)

    return with_signals(
        Div(
            sheet_open,
            Div(data_effect=document.body.style.overflow.set(sheet_open.if_('hidden')), style="display: none;") if modal else None,
            *[child(**ctx) if callable(child) else child for child in children],
            data_on_keydown=(escape_handler, dict(window=True)) if modal else None,
            data_attr_state=sheet_open.if_("open", "closed"),
            cls=cn("relative", cls),
            **kwargs,
        ),
        open=sheet_open,
    )


def SheetTrigger(
    *children,
    variant: str = "outline",
    cls: str = "",
    **kwargs,
) -> FT:
    def trigger(*, sig, sheet_open, **_):
        from .button import Button

        user_on_click = kwargs.pop('data_on_click', None)
        user_actions = user_on_click if isinstance(user_on_click, list) else ([user_on_click] if user_on_click else [])
        click_actions = [sheet_open.set(True)] + user_actions

        return Button(
            *children,
            data_on_click=click_actions,
            id=f"{sig}_trigger",
            data_attr_aria_expanded=sheet_open,
            aria_haspopup="dialog",
            aria_controls=f"{sig}_content",
            data_slot="sheet-trigger",
            variant=variant,
            cls=cls,
            **kwargs,
        )

    return trigger


def SheetContent(
    *children,
    side: SheetSide = "right",
    size: SheetSize = "sm",
    show_close: bool = True,
    cls: str = "",
    **kwargs,
) -> FT:
    def content(*, sig, sheet_open, modal, **ctx):
        side_cls = {
            "right": "inset-y-0 right-0 h-full border-l data-[state=closed]:slide-out-to-right data-[state=open]:slide-in-from-right",
            "left": "inset-y-0 left-0 h-full border-r data-[state=closed]:slide-out-to-left data-[state=open]:slide-in-from-left",
            "top": "inset-x-0 top-0 w-full border-b data-[state=closed]:slide-out-to-top data-[state=open]:slide-in-from-top",
            "bottom": "inset-x-0 bottom-0 w-full border-t data-[state=closed]:slide-out-to-bottom data-[state=open]:slide-in-from-bottom",
        }[side]

        size_cls = "" if side in ("top", "bottom") else {
            "sm": "max-w-sm",
            "md": "max-w-md",
            "lg": "max-w-lg",
            "xl": "max-w-xl",
            "full": "max-w-none w-full",
        }[size]

        overlay = Div(
            data_show=sheet_open,
            data_on_click=sheet_open.set(False),
            data_attr_state=sheet_open.if_("open", "closed"),
            cls="fixed inset-0 z-[100] bg-black/50 backdrop-blur-sm animate-in fade-in-0",
            style="display: none;",
        ) if modal else None

        return Div(
            overlay,
            Div(
                SheetClose(
                    Span("×", aria_hidden="true", cls="text-2xl font-light leading-none -mt-0.5"),
                    size="icon",
                    cls="absolute right-4 top-4 rounded-sm opacity-70 ring-offset-background transition-opacity hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:pointer-events-none data-[state=open]:bg-secondary",
                )(sig=sig, sheet_open=sheet_open, **ctx) if show_close else None,
                *[inject_context(child, sig=sig, sheet_open=sheet_open, **ctx) for child in children],
                data_show=sheet_open,
                id=f"{sig}_content",
                role="dialog",
                aria_modal=modal,
                aria_labelledby=f"{sig}_content-title",
                aria_describedby=f"{sig}_content-description",
                data_attr_state=sheet_open.if_("open", "closed"),
                cls=cn(
                    "fixed z-[110] bg-background shadow-lg border flex flex-col",
                    "transition-all duration-300 ease-in-out",
                    "data-[state=open]:animate-in data-[state=closed]:animate-out",
                    "data-[state=closed]:duration-300 data-[state=open]:duration-500",
                    side_cls,
                    size_cls,
                    "overflow-y-auto",
                    cls,
                ),
                style="display: none;",
                **kwargs,
            ),
        )

    return content


def SheetClose(
    *children,
    variant: str = "ghost",
    size: str = "sm",
    cls: str = "",
    **kwargs,
) -> FT:
    def close(*, sheet_open, **_):
        from .button import Button

        user_on_click = kwargs.pop('data_on_click', None)
        user_actions = user_on_click if isinstance(user_on_click, list) else ([user_on_click] if user_on_click else [])
        click_actions = user_actions + [sheet_open.set(False)]

        return Button(
            *children,
            data_on_click=click_actions,
            data_slot="sheet-close",
            variant=variant,
            size=size,
            cls=cls,
            **kwargs,
        )

    return close


def SheetHeader(*children, cls: str = "", **kwargs) -> FT:
    def _(**ctx):
        return Div(
            *[inject_context(child, **ctx) for child in children],
            data_slot="sheet-header",
            cls=cn("flex flex-col space-y-1.5 p-6", cls),
            **kwargs,
        )

    return _


def SheetFooter(*children, cls: str = "", **kwargs) -> FT:
    def _(**ctx):
        return Div(
            *[inject_context(child, **ctx) for child in children],
            data_slot="sheet-footer",
            cls=cn(
                "flex flex-col-reverse sm:flex-row sm:justify-end sm:space-x-2 p-6",
                cls,
            ),
            **kwargs,
        )

    return _


def SheetTitle(*children, cls: str = "", **kwargs) -> FT:
    def _(*, sig, **_):
        return HTMLH2(
            *children,
            id=f"{sig}_content-title",
            data_slot="sheet-title",
            cls=cn("text-lg font-semibold text-foreground", cls),
            **kwargs,
        )

    return _


def SheetDescription(*children, cls: str = "", **kwargs) -> FT:
    def _(*, sig, **_):
        return P(
            *children,
            id=f"{sig}_content-description",
            data_slot="sheet-description",
            cls=cn("text-sm text-muted-foreground", cls),
            **kwargs,
        )

    return _
