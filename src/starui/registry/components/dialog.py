from typing import Any, Literal

from starhtml import (
    FT,
    H2,
    Div,
    Icon,
    P,
    Span,
)
from starhtml import (
    Button as BaseButton,
)
from starhtml import (
    Dialog as HTMLDialog,
)
from starhtml.datastar import ds_effect, ds_on, ds_on_click, ds_ref, ds_signals

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
    class_name: str = "",
    cls: str = "",
    **attrs: Any,
) -> FT:
    signal_name = f"{ref_id}_open"

    classes = cn(dialog_variants(size=size), class_name, cls)

    dialog_attrs = [ds_ref(ref_id), ds_on("close", f"${signal_name} = false")]

    if modal:
        dialog_attrs.append(
            ds_on_click(f"""
            evt.target === evt.currentTarget &&
            (${ref_id}.close(), ${signal_name} = false)
        """)
        )

    dialog_element = HTMLDialog(content, *dialog_attrs, id=ref_id, cls=classes, **attrs)

    scroll_lock = Div(
        ds_signals(**{signal_name: False}),
        ds_effect(f"document.body.style.overflow = ${signal_name} ? 'hidden' : ''"),
        style="display: none;",
    )

    return Div(trigger, dialog_element, scroll_lock)


def DialogTrigger(
    *children: Any,
    ref_id: str,
    modal: bool = True,
    variant: str = "default",
    class_name: str = "",
    cls: str = "",
    **attrs: Any,
) -> FT:
    from .button import Button

    method = "showModal" if modal else "show"
    signal_name = f"{ref_id}_open"

    return Button(
        *children,
        ds_on_click(f"${ref_id}.{method}(), ${signal_name} = true"),
        type="button",
        aria_haspopup="dialog",
        variant=variant,
        cls=cn("", class_name, cls),
        **attrs,
    )


def DialogContent(
    *children: Any,
    show_close_button: bool = True,
    class_name: str = "",
    cls: str = "",
    **attrs: Any,
) -> FT:
    content_children = list(children)

    if show_close_button:
        close_button = BaseButton(
            Icon("lucide:x", cls="h-4 w-4"),
            Span("Close", cls="sr-only"),
            ds_on_click(
                "$[evt.target.closest('dialog').id + '_open'] = false, evt.target.closest('dialog').close()"
            ),
            cls="absolute top-4 right-4 rounded-sm opacity-70 transition-opacity hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:pointer-events-none ring-offset-background focus:ring-ring",
            type="button",
            aria_label="Close",
        )
        content_children.append(close_button)

    return Div(
        *content_children,
        cls=cn("relative p-6", class_name, cls),
        **attrs,
    )


def DialogClose(
    *children: Any,
    value: str = "",
    variant: str = "outline",
    class_name: str = "",
    cls: str = "",
    **attrs: Any,
) -> FT:
    from .button import Button

    close_expr = (
        f"$[evt.target.closest('dialog').id + '_open'] = false, evt.target.closest('dialog').close('{value}')"
        if value
        else "$[evt.target.closest('dialog').id + '_open'] = false, evt.target.closest('dialog').close()"
    )

    return Button(
        *children,
        ds_on_click(close_expr),
        cls=cn("", class_name, cls),
        type="button",
        variant=variant,
        **attrs,
    )


def DialogHeader(
    *children: Any,
    class_name: str = "",
    cls: str = "",
    **attrs: Any,
) -> FT:
    return Div(
        *children,
        cls=cn("flex flex-col gap-2 text-center sm:text-left", class_name, cls),
        **attrs,
    )


def DialogFooter(
    *children: Any,
    class_name: str = "",
    cls: str = "",
    **attrs: Any,
) -> FT:
    return Div(
        *children,
        cls=cn(
            "flex flex-col-reverse gap-2 sm:flex-row sm:justify-end mt-6",
            class_name,
            cls,
        ),
        **attrs,
    )


def DialogTitle(
    *children: Any,
    class_name: str = "",
    cls: str = "",
    **attrs: Any,
) -> FT:
    return H2(
        *children,
        cls=cn("text-lg leading-none font-semibold text-foreground", class_name, cls),
        **attrs,
    )


def DialogDescription(
    *children: Any,
    class_name: str = "",
    cls: str = "",
    **attrs: Any,
) -> FT:
    return P(
        *children,
        cls=cn("text-muted-foreground text-sm", class_name, cls),
        **attrs,
    )
