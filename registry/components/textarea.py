from typing import Any, Literal

from starhtml import FT, Div, Signal, Span
from starhtml import Label as HTMLLabel
from starhtml import P as HTMLP
from starhtml import Textarea as HTMLTextarea

from .utils import cn, gen_id

__metadata__ = {"description": "Multi-line text input"}


ResizeType = Literal["none", "both", "horizontal", "vertical"]


def Textarea(
    placeholder: str | None = None,
    value: str | None = None,
    signal: str | Signal | None = None,
    name: str | None = None,
    id: str | None = None,
    disabled: bool = False,
    readonly: bool = False,
    required: bool = False,
    autofocus: bool = False,
    rows: int | None = None,
    cols: int | None = None,
    maxlength: int | None = None,
    wrap: str | None = None,
    resize: ResizeType | None = None,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    return HTMLTextarea(
        value if value and not signal else None,
        placeholder=placeholder,
        name=name,
        id=id,
        disabled=disabled or None,
        readonly=readonly or None,
        required=required or None,
        autofocus=autofocus or None,
        rows=rows,
        cols=cols,
        maxlength=maxlength,
        wrap=wrap,
        data_bind=signal,
        data_slot="textarea",
        cls=cn(
            "flex min-h-16 w-full rounded-md border bg-transparent px-3 py-2",
            "text-base shadow-xs transition-[color,box-shadow] outline-none",
            "border-input selection:bg-primary selection:text-primary-foreground placeholder:text-muted-foreground",
            "dark:bg-input/30",
            "focus-visible:border-ring focus-visible:ring-[3px] focus-visible:ring-ring/50",
            "aria-invalid:border-destructive aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40",
            "disabled:cursor-not-allowed disabled:opacity-50",
            "md:text-sm",
            "field-sizing-content" if rows is None else "",
            {
                "none": "resize-none",
                "both": "resize",
                "horizontal": "resize-x",
                "vertical": "resize-y",
            }[resize]
            if resize
            else "",
            cls,
        ),
        **kwargs,
    )


def TextareaWithLabel(
    *children,
    label: str,
    placeholder: str | None = None,
    value: str | None = None,
    signal: str | Signal | None = None,
    name: str | None = None,
    id: str | None = None,
    disabled: bool = False,
    readonly: bool = False,
    required: bool = False,
    rows: int | None = None,
    helper_text: str | None = None,
    error_text: str | None = None,
    label_cls: str = "",
    textarea_cls: str = "",
    cls: str = "",
    **kwargs: Any,
) -> FT:
    textarea_id = id or gen_id("textarea")

    return Div(
        *children,
        HTMLLabel(
            label,
            Span(" *", cls="text-destructive") if required else None,
            fr=textarea_id,
            cls=cn("mb-1.5 block text-sm font-medium", label_cls),
        ),
        Textarea(
            placeholder=placeholder,
            value=value,
            signal=signal,
            name=name,
            id=textarea_id,
            disabled=disabled,
            readonly=readonly,
            required=required,
            rows=rows,
            aria_invalid="true" if error_text else None,
            cls=textarea_cls,
            **kwargs,
        ),
        HTMLP(error_text, cls="mt-1.5 text-sm text-destructive") if error_text else None,
        HTMLP(helper_text, cls="mt-1.5 text-sm text-muted-foreground") if helper_text and not error_text else None,
        data_slot="textarea-with-label",
        cls=cn("space-y-1.5", cls),
    )
