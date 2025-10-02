from typing import Any, Literal

from starhtml import FT, Div, Icon, Span
from starhtml import Button as HTMLButton
from starhtml import Dialog as HTMLDialog
from starhtml import H2 as HTMLH2, P as HTMLP
from starhtml.datastar import ds_effect, ds_on_click, ds_on_close, ds_ref, ds_signals

from .button import Button
from .utils import cn, cva

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
    trigger: FT,
    content: FT,
    ref_id: str,
    modal: bool = True,
    size: DialogSize = "md",
    cls: str = "",
    **kwargs: Any,
) -> FT:
    signal_name = f"{ref_id}_open"
    
    dialog_attrs = [
        ds_ref(ref_id),
        ds_on_close(f"${signal_name} = false"),
    ]
    if modal:
        dialog_attrs.append(
            ds_on_click(f"evt.target === evt.currentTarget && (${ref_id}.close(), ${signal_name} = false)")
        )
    
    return Div(
        trigger,
        HTMLDialog(
            content,
            *dialog_attrs,
            id=ref_id,
            cls=cn(dialog_variants(size=size), cls),
            **kwargs
        ),
        Div(
            ds_signals(**{signal_name: False}),
            ds_effect(f"document.body.style.overflow = ${signal_name} ? 'hidden' : ''"),
            style="display: none;",
        ),
    )


def DialogTrigger(
    *children: Any,
    ref_id: str,
    modal: bool = True,
    variant: str = "default",
    cls: str = "",
    **kwargs: Any,
) -> FT:
    signal_name = f"{ref_id}_open"
    method = "showModal" if modal else "show"
    
    return Button(
        *children,
        ds_on_click(f"${ref_id}.{method}(), ${signal_name} = true"),
        type="button",
        aria_haspopup="dialog",
        variant=variant,
        cls=cls,
        **kwargs,
    )


def DialogContent(
    *children: Any,
    show_close_button: bool = True,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    close_button = (
        HTMLButton(
            Icon("lucide:x", cls="h-4 w-4"),
            Span("Close", cls="sr-only"),
            ds_on_click("$[evt.target.closest('dialog').id + '_open'] = false, evt.target.closest('dialog').close()"),
            cls="absolute top-4 right-4 rounded-sm opacity-70 transition-opacity hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:pointer-events-none ring-offset-background focus:ring-ring",
            type="button",
            aria_label="Close",
        )
        if show_close_button else None
    )
    
    return Div(
        *children,
        close_button,
        cls=cn("relative p-6", cls),
        **kwargs,
    )


def DialogClose(
    *children: Any,
    value: str = "",
    variant: str = "outline",
    cls: str = "",
    **kwargs: Any,
) -> FT:
    close_arg = f"'{value}'" if value else ""
    return Button(
        *children,
        ds_on_click(f"$[evt.target.closest('dialog').id + '_open'] = false, evt.target.closest('dialog').close({close_arg})"),
        type="button",
        variant=variant,
        cls=cls,
        **kwargs,
    )


def DialogHeader(
    *children: Any,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    return Div(
        *children,
        cls=cn("flex flex-col gap-2 text-center sm:text-left", cls),
        **kwargs,
    )


def DialogFooter(
    *children: Any,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    return Div(
        *children,
        cls=cn("flex flex-col-reverse gap-2 sm:flex-row sm:justify-end mt-6", cls),
        **kwargs,
    )


def DialogTitle(
    *children: Any,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    return HTMLH2(
        *children,
        cls=cn("text-lg leading-none font-semibold text-foreground", cls),
        **kwargs,
    )


def DialogDescription(
    *children: Any,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    return HTMLP(
        *children,
        cls=cn("text-muted-foreground text-sm", cls),
        **kwargs,
    )
