from typing import Any, Literal

from starhtml import Div, FT, Signal, js
from starhtml import Dialog as HTMLDialog
from starhtml import H2 as HTMLH2
from starhtml import P as HTMLP

from .utils import cn, ensure_signal

AlertDialogVariant = Literal["default", "destructive"]


def AlertDialog(
    *children: Any,
    signal: str = "",
    cls: str = "",
    **kwargs: Any,
) -> FT:
    dialog_ref = ensure_signal(signal, "alert_dialog")
    open_state = Signal(f"{dialog_ref}_open", False)

    trigger = next((c for c in children if callable(c) and c.__name__ == 'trigger'), None)
    content = next((c for c in children if callable(c) and c.__name__ == 'content'), None)

    return Div(
        trigger(open_state, dialog_ref) if trigger else None,
        HTMLDialog(
            open_state,
            content(open_state, dialog_ref) if content else None,
            data_ref=dialog_ref,
            data_on_close=open_state.set(False),
            data_on_click=js(f"evt.target === evt.currentTarget && (${dialog_ref}.close(), {open_state.set(False)})"),
            id=dialog_ref,
            role="alertdialog",
            aria_labelledby=f"{dialog_ref}-title",
            aria_describedby=f"{dialog_ref}-description",
            cls=cn(
                "fixed max-h-[85vh] w-full max-w-lg overflow-auto m-auto bg-background text-foreground border rounded-lg shadow-lg p-0 backdrop:bg-black/50 backdrop:backdrop-blur-sm open:animate-in open:fade-in-0 open:zoom-in-95 open:duration-200 open:backdrop:animate-in open:backdrop:fade-in-0 open:backdrop:duration-200",
                cls,
            ),
            **kwargs,
        ),
        Div(
            data_effect=js(f"document.body.style.overflow = {open_state} ? 'hidden' : ''"),
            style="display: none;",
        ),
    )


def AlertDialogTrigger(
    *children: Any,
    variant: AlertDialogVariant = "default",
    cls: str = "",
    **kwargs: Any,
) -> FT:
    def trigger(open_state, dialog_ref):
        from .button import Button

        return Button(
            *children,
            data_on_click=[js(f"${dialog_ref}.showModal()"), open_state.set(True)],
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
    def content(open_state, dialog_ref):
        return Div(
            *[child(open_state, dialog_ref) if callable(child) else child for child in children],
            cls=cn("relative p-6", cls),
            **kwargs,
        )

    return content


def AlertDialogHeader(
    *children: Any,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    def _(open_state, dialog_ref):
        return Div(
            *[child(open_state, dialog_ref) if callable(child) else child for child in children],
            cls=cn("flex flex-col gap-2 text-center sm:text-left", cls),
            **kwargs,
        )

    return _


def AlertDialogFooter(
    *children: Any,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    def _(open_state, dialog_ref):
        return Div(
            *[child(open_state, dialog_ref) if callable(child) else child for child in children],
            cls=cn("flex flex-col-reverse gap-2 sm:flex-row sm:justify-end mt-6", cls),
            **kwargs,
        )

    return _


def AlertDialogTitle(
    *children: Any,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    def _(_open_state, dialog_ref):
        return HTMLH2(
            *children,
            id=f"{dialog_ref}-title",
            cls=cn("text-lg leading-none font-semibold text-foreground", cls),
            **kwargs,
        )

    return _


def AlertDialogDescription(
    *children: Any,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    def _(_open_state, dialog_ref):
        return HTMLP(
            *children,
            id=f"{dialog_ref}-description",
            cls=cn("text-muted-foreground text-sm", cls),
            **kwargs,
        )

    return _


def AlertDialogAction(
    *children: Any,
    action: str = "",
    variant: AlertDialogVariant = "default",
    cls: str = "",
    **kwargs: Any,
) -> FT:
    def _(open_state, dialog_ref):
        from .button import Button

        click_actions = [open_state.set(False), js(f"${dialog_ref}.close()")]
        if action:
            click_actions.insert(0, js(action))

        return Button(
            *children,
            data_on_click=click_actions,
            variant="destructive" if variant == "destructive" else "default",
            cls=cls,
            **kwargs,
        )

    return _


def AlertDialogCancel(
    *children: Any,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    def _(open_state, dialog_ref):
        from .button import Button

        return Button(
            *children,
            data_on_click=[open_state.set(False), js(f"${dialog_ref}.close()")],
            variant="outline",
            cls=cls,
            **kwargs,
        )

    return _
