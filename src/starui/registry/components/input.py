from typing import Literal

from starhtml import FT, Div, Span, js
from starhtml import Input as HTMLInput
from starhtml import Label as HTMLLabel
from starhtml import P as HTMLP

from .utils import cn, gen_id

InputType = Literal[
    "text", "password", "email", "number", "tel", "url", "search",
    "date", "datetime-local", "month", "time", "week", "color", "file",
]


def Input(
    *attrs,
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
    signal: str | None = None,
    validation: str | None = None,
    cls: str = "",
    class_name: str = "",
    **kwargs,
) -> FT:
    combined_classes = f"{class_name} {cls}".strip()
    has_width = any(c.startswith("w-") for c in combined_classes.split())
    
    classes = cn(
        "flex h-9 min-w-0 rounded-md border bg-transparent px-3 py-1 text-base shadow-xs transition-[color,box-shadow] outline-none",
        "" if has_width else "w-full",
        "border-input placeholder:text-muted-foreground selection:bg-primary selection:text-primary-foreground",
        "dark:bg-input/30",
        "file:inline-flex file:h-7 file:border-0 file:bg-transparent file:text-sm file:font-medium file:text-foreground",
        "focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:ring-[3px]",
        "aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40 aria-invalid:border-destructive",
        "disabled:pointer-events-none disabled:cursor-not-allowed disabled:opacity-50 md:text-sm",
        combined_classes,
    )

    input_attrs = {
        "type": type,
        "cls": classes,
        "data_slot": "input",
        **{k: v for k, v in {
            "placeholder": placeholder,
            "value": value,
            "name": name,
            "id": id,
            "autocomplete": autocomplete,
            "pattern": pattern,
            "min": str(min) if min is not None else None,
            "max": str(max) if max is not None else None,
            "step": str(step) if step is not None else None,
        }.items() if v is not None},
        **{k: v for k, v in {
            "disabled": disabled,
            "readonly": readonly,
            "required": required,
            "autofocus": autofocus,
        }.items() if v},
    }

    if signal:
        input_attrs["data_bind"] = signal
        if validation:
            validation_signal = f"{signal}_valid"
            validation_js = f"${validation_signal} = {validation.replace('$signal', f'${signal}')}"
            input_attrs["data_on_input"] = js(validation_js)
            input_attrs["data_on_load"] = js(validation_js)

    filtered_kwargs = {k: v for k, v in kwargs.items() if k not in {"signal", "validation"}}
    input_attrs.update(filtered_kwargs)

    return HTMLInput(*attrs, **input_attrs)


def InputWithLabel(
    *children,
    label: str,
    type: InputType = "text",
    placeholder: str | None = None,
    value: str | None = None,
    signal: str | None = None,
    validation: str | None = None,
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
    
    if error_text:
        kwargs["aria_invalid"] = "true"

    return Div(
        *children,
        HTMLLabel(
            label,
            Span(" *", cls="text-destructive") if required else "",
            for_=input_id,
            cls=cn("block text-sm font-medium mb-1.5", label_cls),
        ),
        Input(
            type=type,
            placeholder=placeholder,
            value=value,
            signal=signal,
            validation=validation,
            name=name,
            id=input_id,
            disabled=disabled,
            readonly=readonly,
            required=required,
            cls=input_cls,
            **kwargs,
        ),
        error_text and HTMLP(error_text, cls="text-sm text-destructive mt-1.5"),
        helper_text and not error_text and HTMLP(
            helper_text, cls="text-sm text-muted-foreground mt-1.5"
        ),
        cls=cn("space-y-1.5", cls),
    )
