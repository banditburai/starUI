from typing import Literal

from starhtml import FT, Div, Icon, P, Signal, Span, Style
from starhtml import H2 as HTMLH2
from starhtml import Dialog as HTMLDialog
from starhtml.datastar import document, evt, seq

from .utils import cn, gen_id, inject_context, merge_actions

SheetSide = Literal["top", "right", "bottom", "left"]
SheetSize = Literal["sm", "md", "lg", "xl", "full"]

_SHEET_STYLES = """
dialog[data-side]{
  --_dur-in:500ms;--_dur-out:300ms;--_ease:cubic-bezier(0.32,0.72,0,1);
  position:fixed;margin:0;max-height:none;
  transition:translate var(--_dur-out) var(--_ease),display var(--_dur-out) allow-discrete,overlay var(--_dur-out) allow-discrete;
}
dialog[data-side][open]{transition-duration:var(--_dur-in)}
dialog[data-side]:not([open]){display:none}
dialog[data-side]::backdrop{
  background:rgb(0 0 0/.5);backdrop-filter:blur(4px);
  transition:background 200ms ease,backdrop-filter 200ms ease,display var(--_dur-out) allow-discrete,overlay var(--_dur-out) allow-discrete;
}
dialog[data-side]:not([open])::backdrop{background:rgb(0 0 0/0);backdrop-filter:blur(0)}
dialog[data-side="right"]{inset:0 0 0 auto}
dialog[data-side="right"]:not([open]){translate:100% 0}
dialog[data-side="right"][open]{@starting-style{translate:100% 0}}
dialog[data-side="left"]{inset:0 auto 0 0}
dialog[data-side="left"]:not([open]){translate:-100% 0}
dialog[data-side="left"][open]{@starting-style{translate:-100% 0}}
dialog[data-side="top"]{inset:0 0 auto 0;max-width:none}
dialog[data-side="top"]:not([open]){translate:0 -100%}
dialog[data-side="top"][open]{@starting-style{translate:0 -100%}}
dialog[data-side="bottom"]{inset:auto 0 0 0;max-width:none}
dialog[data-side="bottom"]:not([open]){translate:0 100%}
dialog[data-side="bottom"][open]{@starting-style{translate:0 100%}}
dialog[data-side][open]::backdrop{@starting-style{background:rgb(0 0 0/0);backdrop-filter:blur(0)}}
@media(prefers-reduced-motion:reduce){dialog[data-side],dialog[data-side]::backdrop{transition-duration:0ms!important}}
"""


def Sheet(
    *children,
    signal: str | Signal = "",
    modal: bool = True,
    default_open: bool = False,
    cls: str = "",
    **kwargs,
) -> FT:
    sig = getattr(signal, "_id", signal) or gen_id("sheet")
    sheet_open = Signal(f"{sig}_open", default_open)
    dialog_ref = Signal(sig, _ref_only=True)

    trigger = next(
        (c for c in children if callable(c) and getattr(c, "__name__", None) == "trigger"),
        None,
    )
    content = next(
        (c for c in children if callable(c) and getattr(c, "__name__", None) == "content"),
        None,
    )

    side = getattr(content, "_side", "right") if content else "right"
    size = getattr(content, "_size", "sm") if content else "sm"
    content_cls = getattr(content, "_cls", "") if content else ""
    content_kwargs = getattr(content, "_kwargs", {}) if content else {}

    ctx = {
        "sig": sig,
        "sheet_open": sheet_open,
        "dialog_ref": dialog_ref,
        "modal": modal,
    }

    side_cls = {
        "right": "h-full border-l",
        "left": "h-full border-r",
        "top": "w-full border-b",
        "bottom": "w-full border-t",
    }[side]

    size_cls = (
        ""
        if side in ("top", "bottom")
        else {
            "sm": "w-3/4 sm:max-w-sm",
            "md": "w-3/4 sm:max-w-md",
            "lg": "w-3/4 sm:max-w-lg",
            "xl": "w-3/4 sm:max-w-xl",
            "full": "max-w-none w-full",
        }[size]
    )

    show_action = dialog_ref.showModal() if modal else dialog_ref.show()

    return Div(
        Style(_SHEET_STYLES),
        sheet_open,
        trigger(**ctx) if trigger else None,
        HTMLDialog(
            content(**ctx) if content else None,
            data_ref=dialog_ref,
            data_on_close=sheet_open.set(False),
            data_on_click=(evt.target == evt.currentTarget).then(
                seq(dialog_ref.close(), sheet_open.set(False))
            )
            if modal
            else None,
            data_side=side,
            id=f"{sig}_content",
            aria_labelledby=f"{sig}_content-title",
            aria_describedby=f"{sig}_content-description",
            cls=cn(
                "bg-background text-foreground bg-clip-padding shadow-lg",
                "flex flex-col gap-4 p-0 outline-none",
                side_cls,
                size_cls,
                "overflow-y-auto",
                content_cls,
            ),
            **content_kwargs,
        ),
        # Sync signal → native dialog (supports external triggers like mobile menu)
        Div(
            data_effect=[
                (sheet_open & ~dialog_ref.open).then(show_action),
                (~sheet_open & dialog_ref.open).then(dialog_ref.close()),
            ],
            style="display: none;",
        ),
        Div(
            data_effect=document.body.style.overflow.set(sheet_open.if_("hidden", "")),
            style="display: none;",
        )
        if modal
        else None,
        cls=cls,
        **kwargs,
    )


def SheetTrigger(
    *children,
    variant: str = "outline",
    cls: str = "",
    **kwargs,
) -> FT:
    def trigger(*, sig, sheet_open, dialog_ref, modal, **_):
        from .button import Button

        show_method = dialog_ref.showModal() if modal else dialog_ref.show()
        click_actions = merge_actions(show_method, sheet_open.set(True), kwargs=kwargs)

        return Button(
            *children,
            data_on_click=click_actions,
            id=f"{sig}_trigger",
            data_attr_aria_expanded=sheet_open.if_("true", "false"),
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
    def content(*, sig, sheet_open, dialog_ref, **ctx):
        all_ctx = dict(sig=sig, sheet_open=sheet_open, dialog_ref=dialog_ref, **ctx)
        return Div(
            SheetClose(
                Icon("lucide:x", cls="size-4"),
                Span("Close", cls="sr-only"),
                size="icon",
                cls="absolute top-4 right-4 opacity-70 hover:opacity-100 transition-opacity",
            )(**all_ctx)
            if show_close
            else None,
            *[inject_context(child, **all_ctx) for child in children],
            cls="relative flex flex-col flex-1",
        )

    content._side = side
    content._size = size
    content._cls = cls
    content._kwargs = kwargs
    return content


def SheetClose(
    *children,
    variant: str = "ghost",
    size: str = "sm",
    cls: str = "",
    **kwargs,
) -> FT:
    def close(*, sheet_open, dialog_ref, **_):
        from .button import Button

        click_actions = merge_actions(
            kwargs=kwargs,
            after=[sheet_open.set(False), dialog_ref.close()],
        )

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
            cls=cn("flex flex-col gap-1.5 p-4", cls),
            **kwargs,
        )

    return _


def SheetFooter(*children, cls: str = "", **kwargs) -> FT:
    def _(**ctx):
        return Div(
            *[inject_context(child, **ctx) for child in children],
            data_slot="sheet-footer",
            cls=cn("mt-auto flex flex-col gap-2 p-4", cls),
            **kwargs,
        )

    return _


def SheetTitle(*children, cls: str = "", **kwargs) -> FT:
    def _(*, sig, **_):
        return HTMLH2(
            *children,
            id=f"{sig}_content-title",
            data_slot="sheet-title",
            cls=cn("text-foreground font-semibold", cls),
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
