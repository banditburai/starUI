from typing import Any, Literal

from starhtml import FT, Div, Signal
from starhtml import H2 as HTMLH2
from starhtml import Dialog as HTMLDialog
from starhtml import P as HTMLP
from starhtml.datastar import document, evt, seq

from .utils import cn, gen_id, merge_actions

AlertDialogVariant = Literal["default", "destructive"]


def AlertDialog(
    *children: Any,
    signal: str | Signal = "",
    cls: str = "",
    **kwargs: Any,
) -> FT:
    sig = getattr(signal, "_id", signal) or gen_id("alert_dialog")
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

    ctx = {"open_state": open_state, "dialog_ref": dialog_ref, "sig": sig}

    return Div(
        trigger(**ctx) if trigger else None,
        HTMLDialog(
            content(**ctx) if content else None,
            data_ref=dialog_ref,
            data_on_close=open_state.set(False),
            data_on_click=(evt.target == evt.currentTarget)
            & seq(dialog_ref.close(), open_state.set(False)),
            id=sig,
            role="alertdialog",
            aria_labelledby=f"{sig}-title",
            aria_describedby=f"{sig}-description",
            cls=cn(
                "fixed max-h-[85vh] w-full max-w-lg overflow-auto m-auto bg-background text-foreground border rounded-lg shadow-lg p-0 backdrop:bg-black/50 backdrop:backdrop-blur-sm open:animate-in open:fade-in-0 open:zoom-in-95 open:duration-200 open:backdrop:animate-in open:backdrop:fade-in-0 open:backdrop:duration-200",
                cls,
            ),
            **kwargs,
        ),
        Div(
            data_effect=document.body.style.overflow.set(open_state.if_("hidden", "")),
            style="display: none;",
        ),
    )


def AlertDialogTrigger(
    *children: Any,
    variant: AlertDialogVariant = "default",
    cls: str = "",
    **kwargs: Any,
) -> FT:
    def trigger(*, open_state, dialog_ref, **_):
        from .button import Button

        click_actions = merge_actions(
            dialog_ref.showModal(), open_state.set(True), kwargs=kwargs
        )

        return Button(
            *children,
            data_on_click=click_actions,
            aria_haspopup="dialog",
            variant=variant,
            cls=cls,
            **kwargs,
        )

    return trigger


def AlertDialogContent(
    *children: Any,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    def content(**ctx):
        return Div(
            *[child(**ctx) if callable(child) else child for child in children],
            cls=cn("relative p-6", cls),
            **kwargs,
        )

    return content


def AlertDialogHeader(
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


def AlertDialogFooter(
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


def AlertDialogTitle(
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


def AlertDialogDescription(
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


def AlertDialogAction(
    *children: Any,
    action: Any = None,
    variant: AlertDialogVariant = "default",
    cls: str = "",
    **kwargs: Any,
) -> FT:
    def _(*, open_state, dialog_ref, **_):
        from .button import Button

        click_actions = merge_actions(
            action, after=[open_state.set(False), dialog_ref.close()]
        )

        return Button(
            *children,
            data_on_click=click_actions,
            variant=variant,
            cls=cls,
            **kwargs,
        )

    return _


def AlertDialogCancel(
    *children: Any,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    def _(*, open_state, dialog_ref, **_):
        from .button import Button

        click_actions = merge_actions(
            kwargs=kwargs, after=[open_state.set(False), dialog_ref.close()]
        )

        return Button(
            *children,
            data_on_click=click_actions,
            variant="outline",
            cls=cls,
            **kwargs,
        )

    return _
