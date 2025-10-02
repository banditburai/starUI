from typing import Any, Literal

from starhtml import FT, Div, Icon, Signal, Span, js
from starhtml import Button as HTMLButton
from starhtml import Dialog as HTMLDialog
from starhtml import H2 as HTMLH2, P as HTMLP

from .button import Button
from .utils import cn, cva, ensure_signal

DialogSize = Literal["sm", "md", "lg", "xl", "full"]

dialog_variants = cva(
    base="fixed max-h-[85vh] w-full overflow-auto m-auto bg-background text-foreground border rounded-lg shadow-lg p-0 backdrop:bg-black/50 backdrop:backdrop-blur-sm open:animate-in open:fade-in-0 open:zoom-in-95 open:duration-200 open:backdrop:animate-in open:backdrop:fade-in-0 open:backdrop:duration-200",
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
    signal: str = "",
    modal: bool = True,
    size: DialogSize = "md",
    cls: str = "",
    **kwargs: Any,
) -> FT:
    dialog_ref = ensure_signal(signal, "dialog")
    open_state = Signal(f"{dialog_ref}_open", False)

    trigger = next((c for c in children if callable(c) and c.__name__ == 'trigger'), None)
    content = next((c for c in children if callable(c) and c.__name__ == 'content'), None)

    return Div(
        trigger(open_state, dialog_ref, modal) if trigger else None,
        HTMLDialog(
            open_state,
            content(open_state, dialog_ref) if content else None,
            data_ref=dialog_ref,
            data_on_close=open_state.set(False),
            data_on_click=js(f"evt.target === evt.currentTarget && (${dialog_ref}.close(), {open_state.set(False)})") if modal else None,
            id=dialog_ref,
            aria_labelledby=f"{dialog_ref}-title",
            aria_describedby=f"{dialog_ref}-description",
            cls=cn(dialog_variants(size=size), cls),
            **kwargs,
        ),
        Div(
            data_effect=js(f"document.body.style.overflow = {open_state} ? 'hidden' : ''"),
            style="display: none;",
        ),
    )


def DialogTrigger(
    *children: Any,
    variant: str = "default",
    cls: str = "",
    **kwargs: Any,
) -> FT:
    def trigger(open_state, dialog_ref, modal):
        method = "showModal" if modal else "show"
        return Button(
            *children,
            data_on_click=[js(f"${dialog_ref}.{method}()"), open_state.set(True)],
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
    def content(open_state, dialog_ref):
        close_button = (
            HTMLButton(
                Icon("lucide:x", cls="h-4 w-4"),
                Span("Close", cls="sr-only"),
                data_on_click=[open_state.set(False), js(f"${dialog_ref}.close()")],
                cls="absolute top-4 right-4 rounded-sm opacity-70 transition-opacity hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:pointer-events-none ring-offset-background focus:ring-ring",
                type="button",
                aria_label="Close",
            )
            if show_close_button else None
        )

        return Div(
            *[child(open_state, dialog_ref) if callable(child) else child for child in children],
            close_button,
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
    def _(open_state, dialog_ref):
        close_actions = [open_state.set(False), js(f"${dialog_ref}.close('{value}')" if value else f"${dialog_ref}.close()")]
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
    def _(open_state, dialog_ref):
        return Div(
            *[child(open_state, dialog_ref) if callable(child) else child for child in children],
            cls=cn("flex flex-col gap-2 text-center sm:text-left", cls),
            **kwargs,
        )

    return _


def DialogFooter(
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


def DialogTitle(
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


def DialogDescription(
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
