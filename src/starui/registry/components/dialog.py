from typing import Any, Literal

from starhtml import FT, Div, Icon, Signal, Span, Style
from starhtml import H2 as HTMLH2
from starhtml import Button as HTMLButton
from starhtml import Dialog as HTMLDialog
from starhtml import P as HTMLP
from starhtml.datastar import document, evt, seq

from .utils import cn, cva, gen_id, inject_context, merge_actions

DialogSize = Literal["sm", "md", "lg", "xl", "full"]

_DIALOG_STYLES = """
dialog[data-dialog]{
  --_dur-in:200ms;--_dur-out:150ms;
  transition:opacity var(--_dur-out) ease,scale var(--_dur-out) ease,display var(--_dur-out) allow-discrete,overlay var(--_dur-out) allow-discrete;
}
dialog[data-dialog][open]{transition-duration:var(--_dur-in);transition-timing-function:cubic-bezier(0.16,1,0.3,1)}
dialog[data-dialog]:not([open]){opacity:0;scale:0.95}
dialog[data-dialog][open]{@starting-style{opacity:0;scale:0.95}}
dialog[data-dialog]::backdrop{
  background:rgb(0 0 0/.5);backdrop-filter:blur(4px);
  transition:background var(--_dur-out) ease,backdrop-filter var(--_dur-out) ease,display var(--_dur-out) allow-discrete,overlay var(--_dur-out) allow-discrete;
}
dialog[data-dialog]:not([open])::backdrop{background:rgb(0 0 0/0);backdrop-filter:blur(0)}
dialog[data-dialog][open]::backdrop{transition-timing-function:cubic-bezier(0.16,1,0.3,1);@starting-style{background:rgb(0 0 0/0);backdrop-filter:blur(0)}}
@media(prefers-reduced-motion:reduce){dialog[data-dialog],dialog[data-dialog]::backdrop{transition-duration:0ms!important}}
"""

dialog_variants = cva(
    base="fixed inset-0 z-50 max-h-[85vh] max-w-[calc(100%-2rem)] w-full overflow-auto m-auto bg-background text-foreground border rounded-lg shadow-lg p-0 outline-none",
    config={
        "variants": {
            "size": {
                "sm": "sm:max-w-sm",
                "md": "sm:max-w-lg",
                "lg": "sm:max-w-2xl",
                "xl": "sm:max-w-4xl",
                "full": "max-w-[95vw]",
            }
        },
        "defaultVariants": {"size": "md"},
    },
)


def Dialog(
    *children: Any,
    signal: str | Signal = "",
    modal: bool = True,
    size: DialogSize = "md",
    cls: str = "",
    **kwargs: Any,
) -> FT:
    sig = getattr(signal, "_id", signal) or gen_id("dialog")
    open_state = Signal(f"{sig}_open", False)
    dialog_ref = Signal(sig, _ref_only=True)

    trigger = next(
        (
            c
            for c in children
            if callable(c) and getattr(c, "__name__", None) == "trigger"
        ),
        None,
    )
    content = next(
        (
            c
            for c in children
            if callable(c) and getattr(c, "__name__", None) == "content"
        ),
        None,
    )

    ctx = {
        "open_state": open_state,
        "dialog_ref": dialog_ref,
        "sig": sig,
        "modal": modal,
    }

    return Div(
        Style(_DIALOG_STYLES),
        trigger(**ctx) if trigger else None,
        HTMLDialog(
            content(**ctx) if content else None,
            data_ref=dialog_ref,
            data_on_close=open_state.set(False),
            data_on_click=(evt.target == evt.currentTarget)
            & seq(dialog_ref.close(), open_state.set(False))
            if modal
            else None,
            data_dialog="",
            id=sig,
            aria_labelledby=f"{sig}-title",
            aria_describedby=f"{sig}-description",
            cls=cn(dialog_variants(size=size), cls),
            **kwargs,
        ),
        Div(
            data_effect=document.body.style.overflow.set(open_state.if_("hidden", "")),
            style="display: none;",
        )
        if modal
        else None,
    )


def DialogTrigger(
    *children: Any,
    variant: str = "default",
    cls: str = "",
    **kwargs: Any,
) -> FT:
    def trigger(*, open_state, dialog_ref, modal, **_):
        from .button import Button

        show_method = dialog_ref.showModal() if modal else dialog_ref.show()
        click_actions = merge_actions(show_method, open_state.set(True), kwargs=kwargs)

        return Button(
            *children,
            data_on_click=click_actions,
            type="button",
            aria_haspopup="dialog",
            variant=variant,
            cls=cls,
            **kwargs,
        )

    return trigger


def DialogContent(
    *children: Any,
    show_close_button: bool = True,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    def content(**ctx):
        open_state = ctx["open_state"]
        dialog_ref = ctx["dialog_ref"]

        return Div(
            *[inject_context(child, **ctx) for child in children],
            HTMLButton(
                Icon("lucide:x", cls="size-4"),
                Span("Close", cls="sr-only"),
                data_on_click=[open_state.set(False), dialog_ref.close()],
                cls="absolute top-4 right-4 rounded-sm opacity-70 transition-opacity hover:opacity-100 outline-none focus-visible:ring-ring/50 focus-visible:ring-[3px] disabled:pointer-events-none [&_svg]:pointer-events-none [&_svg]:shrink-0",
                type="button",
                aria_label="Close",
            )
            if show_close_button
            else None,
            cls=cn("relative grid gap-4 p-6", cls),
            **kwargs,
        )

    return content


def DialogClose(
    *children: Any,
    value: str = "",
    variant: str = "outline",
    cls: str = "",
    **kwargs: Any,
) -> FT:
    def _(*, open_state, dialog_ref, **_):
        from .button import Button

        close_actions = merge_actions(
            kwargs=kwargs,
            after=[
                open_state.set(False),
                dialog_ref.close(value) if value else dialog_ref.close(),
            ],
        )

        return Button(
            *children,
            data_on_click=close_actions,
            type="button",
            variant=variant,
            cls=cls,
            **kwargs,
        )

    return _


def DialogHeader(
    *children: Any,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    def _(**ctx):
        return Div(
            *[inject_context(child, **ctx) for child in children],
            cls=cn("flex flex-col gap-2 text-center sm:text-left", cls),
            **kwargs,
        )

    return _


def DialogFooter(
    *children: Any,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    def _(**ctx):
        return Div(
            *[inject_context(child, **ctx) for child in children],
            cls=cn("flex flex-col-reverse gap-2 sm:flex-row sm:justify-end", cls),
            **kwargs,
        )

    return _


def DialogTitle(
    *children: Any,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    def _(*, sig, **_):
        return HTMLH2(
            *children,
            id=f"{sig}-title",
            cls=cn("text-lg leading-none font-semibold", cls),
            **kwargs,
        )

    return _


def DialogDescription(
    *children: Any,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    def _(*, sig, **_):
        return HTMLP(
            *children,
            id=f"{sig}-description",
            cls=cn("text-muted-foreground text-sm", cls),
            **kwargs,
        )

    return _
