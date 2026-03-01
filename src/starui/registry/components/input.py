from typing import Literal

from starhtml import FT, Div, Signal, Span
from starhtml import Input as HTMLInput
from starhtml import Label as HTMLLabel
from starhtml import P as HTMLP

from .utils import cn, gen_id

InputType = Literal[
    "text",
    "password",
    "email",
    "number",
    "tel",
    "url",
    "search",
    "date",
    "datetime-local",
    "month",
    "time",
    "week",
    "color",
    "file",
]


def Input(
    type: InputType = "text",
    placeholder: str | None = None,
    value: str | None = None,
    name: str | None = None,
    id: str | None = None,
    disabled: bool = False,
    readonly: bool = False,
    required: bool = False,
    autofocus: bool = False,
    autocomplete: str | None = None,
    min: str | int | None = None,
    max: str | int | None = None,
    step: str | int | None = None,
    pattern: str | None = None,
    signal: str | Signal | None = None,
    cls: str = "",
    **kwargs,
) -> FT:
    return HTMLInput(
        type=type,
        placeholder=placeholder,
        value=value,
        name=name,
        id=id,
        autocomplete=autocomplete,
        pattern=pattern,
        min=str(min) if min is not None else None,
        max=str(max) if max is not None else None,
        step=str(step) if step is not None else None,
        disabled=disabled or None,
        readonly=readonly or None,
        required=required or None,
        autofocus=autofocus or None,
        data_bind=signal,
        data_slot="input",
        cls=cn(
            "peer flex h-9 w-full min-w-0 rounded-md border bg-transparent px-3 py-1 text-base shadow-xs transition-[color,box-shadow] outline-none",
            "border-input placeholder:text-muted-foreground selection:bg-primary selection:text-primary-foreground",
            "dark:bg-input/30",
            "file:inline-flex file:h-7 file:border-0 file:bg-transparent file:text-sm file:font-medium file:text-foreground",
            "focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:ring-[3px]",
            "aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40 aria-invalid:border-destructive",
            "disabled:pointer-events-none disabled:cursor-not-allowed disabled:opacity-50 md:text-sm",
            cls,
        ),
        **kwargs,
    )


def InputWithLabel(
    *children,
    label: str,
    type: InputType = "text",
    placeholder: str | None = None,
    value: str | None = None,
    signal: str | None = None,
    name: str | None = None,
    id: str | None = None,
    disabled: bool = False,
    readonly: bool = False,
    required: bool = False,
    helper_text: str | None = None,
    error_text: str | None = None,
    label_cls: str = "",
    input_cls: str = "",
    cls: str = "",
    **kwargs,
) -> FT:
    input_id = id or gen_id("input")

    return Div(
        *children,
        HTMLLabel(
            label,
            Span(" *", cls="text-destructive") if required else None,
            fr=input_id,
            cls=cn("block text-sm font-medium mb-1.5", label_cls),
        ),
        Input(
            type=type,
            placeholder=placeholder,
            value=value,
            signal=signal,
            name=name,
            id=input_id,
            disabled=disabled,
            readonly=readonly,
            required=required,
            aria_invalid="true" if error_text else None,
            cls=input_cls,
            **kwargs,
        ),
        HTMLP(error_text, cls="text-sm text-destructive mt-1.5")
        if error_text
        else None,
        HTMLP(helper_text, cls="text-sm text-muted-foreground mt-1.5")
        if helper_text and not error_text
        else None,
        data_slot="input-with-label",
        cls=cn("space-y-1.5", cls),
    )
