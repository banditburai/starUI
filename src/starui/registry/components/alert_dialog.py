from typing import Any, Literal

from starhtml import FT, Div
from starhtml import H2 as HTMLH2
from starhtml import Dialog as HTMLDialog
from starhtml import P as HTMLP
from starhtml.datastar import ds_effect, ds_on_click, ds_on_close, ds_ref, ds_signals

from .utils import cn

AlertDialogVariant = Literal["default", "destructive"]


def _close_dialog_expr(ref_id: str, action: str = "") -> str:
    """Generate dialog close expression with optional action."""
    close_expr = f"${ref_id}_open = false; ${ref_id}.close()"
    return f"{action}; {close_expr}" if action else close_expr


def AlertDialog(
    trigger: FT,
    content: FT,
    ref_id: str,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    signal_name = f"{ref_id}_open"

    dialog_element = HTMLDialog(
        content,
        ds_ref(ref_id),
        ds_on_close(f"${signal_name} = false"),
        ds_on_click(f"evt.target === evt.currentTarget && (${ref_id}.close(), ${signal_name} = false)"),
        id=ref_id,
        cls=cn(
            "fixed max-h-[85vh] w-full max-w-lg overflow-auto m-auto bg-background text-foreground border border-input rounded-lg shadow-lg p-0 backdrop:bg-black/50 backdrop:backdrop-blur-sm open:animate-in open:fade-in-0 open:zoom-in-95 open:duration-200 open:backdrop:animate-in open:backdrop:fade-in-0 open:backdrop:duration-200",
            cls,
        ),
        **kwargs,
    )

    scroll_lock = Div(
        ds_signals(**{signal_name: False}),
        ds_effect(f"document.body.style.overflow = ${signal_name} ? 'hidden' : ''"),
        style="display: none;",
    )

    return Div(trigger, dialog_element, scroll_lock)


def AlertDialogTrigger(
    *children: Any,
    ref_id: str,
    variant: AlertDialogVariant = "default",
    cls: str = "",
    **kwargs: Any,
) -> FT:
    from .button import Button

    return Button(
        *children,
        ds_on_click(f"${ref_id}.showModal(); ${ref_id}_open = true"),
        aria_haspopup="dialog",
        variant=variant,
        cls=cls,
        **kwargs,
    )


def AlertDialogContent(
    *children: Any,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    return Div(
        *children,
        cls=cn("relative p-6", cls),
        **kwargs,
    )


def AlertDialogHeader(
    *children: Any,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    return Div(
        *children,
        cls=cn("flex flex-col gap-2 text-center sm:text-left", cls),
        **kwargs,
    )


def AlertDialogFooter(
    *children: Any,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    return Div(
        *children,
        cls=cn("flex flex-col-reverse gap-2 sm:flex-row sm:justify-end mt-6", cls),
        **kwargs,
    )


def AlertDialogTitle(
    *children: Any,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    return HTMLH2(
        *children,
        cls=cn("text-lg leading-none font-semibold text-foreground", cls),
        **kwargs,
    )


def AlertDialogDescription(
    *children: Any,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    return HTMLP(
        *children,
        cls=cn("text-muted-foreground text-sm", cls),
        **kwargs,
    )


def AlertDialogAction(
    *children: Any,
    ref_id: str,
    action: str = "",
    variant: AlertDialogVariant = "default",
    cls: str = "",
    **kwargs: Any,
) -> FT:
    from .button import Button

    return Button(
        *children,
        ds_on_click(_close_dialog_expr(ref_id, action)),
        variant="destructive" if variant == "destructive" else "default",
        cls=cls,
        **kwargs,
    )


def AlertDialogCancel(
    *children: Any,
    ref_id: str,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    from .button import Button

    return Button(
        *children,
        ds_on_click(_close_dialog_expr(ref_id)),
        variant="outline",
        cls=cls,
        **kwargs,
    )
