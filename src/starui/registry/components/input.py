from typing import Literal

from starhtml import FT, Div, Label, P, Span
from starhtml import Input as HTMLInput

from .utils import cn

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
    *datastar_attrs,
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
    class_name: str = "",
    cls: str = "",
    **attrs,
) -> FT:
    classes = cn(
        "flex h-9 w-full min-w-0 rounded-md border bg-transparent px-3 py-1 text-base shadow-xs transition-[color,box-shadow] outline-none",
        "border-input",
        "placeholder:text-muted-foreground",
        "selection:bg-primary selection:text-primary-foreground",
        "dark:bg-input/30",
        "file:inline-flex file:h-7 file:border-0 file:bg-transparent file:text-sm file:font-medium file:text-foreground",
        "focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:ring-[3px]",
        "aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40 aria-invalid:border-destructive",
        "disabled:pointer-events-none disabled:cursor-not-allowed disabled:opacity-50",
        "md:text-sm",
        class_name,
        cls,
    )

    input_attrs = {
        "type": type,
        "cls": classes,
        "data_slot": "input",
        **{
            k: v
            for k, v in {
                "placeholder": placeholder,
                "value": value,
                "name": name,
                "id": id,
                "disabled": disabled,
                "readonly": readonly,
                "required": required,
                "autofocus": autofocus,
                "autocomplete": autocomplete,
                "min": str(min) if min is not None else None,
                "max": str(max) if max is not None else None,
                "step": str(step) if step is not None else None,
                "pattern": pattern,
            }.items()
            if v is not None and v is not False
        },
        **attrs,
    }

    return HTMLInput(*datastar_attrs, **input_attrs)


def InputWithLabel(
    label: str,
    type: InputType = "text",
    placeholder: str | None = None,
    value: str | None = None,
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
    **attrs,
) -> FT:
    if not id:
        import uuid

        id = f"input_{str(uuid.uuid4())[:8]}"

    if error_text:
        attrs["aria_invalid"] = "true"

    return Div(
        Label(
            label,
            Span(" *", cls="text-destructive") if required else "",
            for_=id,
            cls=cn("block text-sm font-medium mb-1.5", label_cls),
        ),
        Input(
            type=type,
            placeholder=placeholder,
            value=value,
            name=name,
            id=id,
            disabled=disabled,
            readonly=readonly,
            required=required,
            cls=input_cls,
            **attrs,
        ),
        error_text and P(error_text, cls="text-sm text-destructive mt-1.5"),
        helper_text
        and not error_text
        and P(helper_text, cls="text-sm text-muted-foreground mt-1.5"),
        cls=cn("space-y-1.5", cls),
    )
