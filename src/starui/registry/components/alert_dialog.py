from typing import Any, Literal

from starhtml import FT, Div, Signal, Style
from starhtml import H2 as HTMLH2
from starhtml import Dialog as HTMLDialog
from starhtml import P as HTMLP
from starhtml.datastar import document

from .utils import cn, gen_id, inject_context, merge_actions

AlertDialogVariant = Literal["default", "destructive"]

_ALERT_DIALOG_STYLES = """
dialog[data-alert-dialog]{
  --_dur-in:200ms;--_dur-out:150ms;
  transition:opacity var(--_dur-out) ease,scale var(--_dur-out) ease,display var(--_dur-out) allow-discrete,overlay var(--_dur-out) allow-discrete;
}
dialog[data-alert-dialog][open]{transition-duration:var(--_dur-in);transition-timing-function:cubic-bezier(0.16,1,0.3,1)}
dialog[data-alert-dialog]:not([open]){opacity:0;scale:0.95}
dialog[data-alert-dialog][open]{@starting-style{opacity:0;scale:0.95}}
dialog[data-alert-dialog]::backdrop{
  background:rgb(0 0 0/.5);backdrop-filter:blur(4px);
  transition:background var(--_dur-out) ease,backdrop-filter var(--_dur-out) ease,display var(--_dur-out) allow-discrete,overlay var(--_dur-out) allow-discrete;
}
dialog[data-alert-dialog]:not([open])::backdrop{background:rgb(0 0 0/0);backdrop-filter:blur(0)}
dialog[data-alert-dialog][open]::backdrop{transition-timing-function:cubic-bezier(0.16,1,0.3,1);@starting-style{background:rgb(0 0 0/0);backdrop-filter:blur(0)}}
@media(prefers-reduced-motion:reduce){dialog[data-alert-dialog],dialog[data-alert-dialog]::backdrop{transition-duration:0ms!important}}
"""


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
        (c for c in children if callable(c) and getattr(c, "__name__", None) == "trigger"), None,
    )
    content = next(
        (c for c in children if callable(c) and getattr(c, "__name__", None) == "content"), None,
    )

    ctx = {"open_state": open_state, "dialog_ref": dialog_ref, "sig": sig}

    return Div(
        Style(_ALERT_DIALOG_STYLES),
        trigger(**ctx) if trigger else None,
        HTMLDialog(
            content(**ctx) if content else None,
            data_ref=dialog_ref,
            data_on_close=open_state.set(False),
            data_alert_dialog="",
            id=sig,
            role="alertdialog",
            aria_labelledby=f"{sig}-title",
            aria_describedby=f"{sig}-description",
            cls=cn(
                "fixed inset-0 z-50 max-h-[85vh] max-w-[calc(100%-2rem)] sm:max-w-lg w-full overflow-auto m-auto bg-background text-foreground border rounded-lg shadow-lg p-0 outline-none",
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
            *[inject_context(child, **ctx) for child in children],
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
            *[inject_context(child, **ctx) for child in children],
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
            *[inject_context(child, **ctx) for child in children],
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
