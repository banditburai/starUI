from typing import Any, Literal

from starhtml import FT, Div, Icon, Signal, Span
from starhtml import H2 as HTMLH2
from starhtml import Button as HTMLButton
from starhtml import Dialog as HTMLDialog
from starhtml import P as HTMLP
from starhtml.datastar import document, evt, seq

from .utils import cn, cva, gen_id, merge_actions

DialogSize = Literal["sm", "md", "lg", "xl", "full"]

dialog_variants = cva(
    base="fixed max-h-[85vh] w-full overflow-auto m-auto bg-background text-foreground border rounded-lg shadow-lg p-0 backdrop:bg-black/50 backdrop:backdrop-blur-sm open:animate-in open:fade-in-0 open:zoom-in-95 open:duration-200 open:backdrop:animate-in open:backdrop:fade-in-0 open:backdrop:duration-200 outline-none",
    config={
        "variants": {
            "size": {
                "sm": "max-w-sm",
                "md": "max-w-lg",
                "lg": "max-w-2xl",
                "xl": "max-w-4xl",
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
        (c for c in children if callable(c) and c.__name__ == "trigger"), None
    )
    content = next(
        (c for c in children if callable(c) and c.__name__ == "content"), None
    )

    ctx = {
        "open_state": open_state,
        "dialog_ref": dialog_ref,
        "sig": sig,
        "modal": modal,
    }

    return Div(
        trigger(**ctx) if trigger else None,
        HTMLDialog(
            content(**ctx) if content else None,
            data_ref=dialog_ref,
            data_on_close=open_state.set(False),
            data_on_click=(evt.target == evt.currentTarget)
            & seq(dialog_ref.close(), open_state.set(False))
            if modal
            else None,
            id=sig,
            aria_labelledby=f"{sig}-title",
            aria_describedby=f"{sig}-description",
            cls=cn(dialog_variants(size=size), cls),
            **kwargs,
        ),
        Div(
            data_effect=document.body.style.overflow.set(open_state.if_("hidden", "")),
            style="display: none;",
        ),
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
            *[child(**ctx) if callable(child) else child for child in children],
            HTMLButton(
                Icon("lucide:x", cls="h-4 w-4"),
                Span("Close", cls="sr-only"),
                data_on_click=[open_state.set(False), dialog_ref.close()],
                cls="absolute top-4 right-4 rounded-sm opacity-70 transition-opacity hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:pointer-events-none ring-offset-background focus:ring-ring",
                type="button",
                aria_label="Close",
            )
            if show_close_button
            else None,
            cls=cn("relative p-6", cls),
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
            *[child(**ctx) if callable(child) else child for child in children],
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
            *[child(**ctx) if callable(child) else child for child in children],
            cls=cn("flex flex-col-reverse gap-2 sm:flex-row sm:justify-end mt-6", cls),
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
            cls=cn("text-lg leading-none font-semibold text-foreground", cls),
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
