from typing import Any, Literal

from starhtml import FT, Div
from starhtml import Label as HTMLLabel
from starhtml import P as HTMLP
from starhtml import Span as HTMLSpan
from starhtml import Textarea as HTMLTextarea
from starhtml.datastar import ds_bind

from .utils import cn

ResizeType = Literal["none", "both", "horizontal", "vertical"]


def Textarea(
    *datastar_attrs,
    placeholder: str | None = None,
    value: str | None = None,
    signal: str | None = None,
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
    class_name: str = "",
    cls: str = "",
    **attrs: Any,
) -> FT:
    resize_classes = {
        "none": "resize-none",
        "both": "resize",
        "horizontal": "resize-x",
        "vertical": "resize-y",
    }

    classes = cn(
        "flex min-h-16 w-full rounded-md border bg-transparent px-3 py-2",
        "text-base shadow-xs transition-[color,box-shadow] outline-none",
        "border-input placeholder:text-muted-foreground",
        "dark:bg-input/30",
        "focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:ring-[3px]",
        "aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40 aria-invalid:border-destructive",
        "disabled:cursor-not-allowed disabled:opacity-50",
        "md:text-sm",
        "field-sizing-content" if rows is None else "",
        resize_classes.get(resize, "") if resize else "",
        class_name,
        cls,
    )

    textarea_attrs = {
        "cls": classes,
        "data_slot": "textarea",
        **{
            k: v
            for k, v in {
                "id": id,
                "placeholder": placeholder,
                "value": value if not signal else None,
                "name": name,
                "disabled": disabled,
                "readonly": readonly,
                "required": required,
                "autofocus": autofocus,
                "rows": rows,
                "cols": cols,
                "maxlength": maxlength,
                "wrap": wrap,
            }.items()
            if v is not None and v is not False
        },
        **attrs,
    }

    if signal:
        # Add reactive binding (following the input component pattern)
        bind_attrs = ds_bind(signal)
        textarea_attrs.update(bind_attrs.attrs)
        # NOTE: Don't add bind_attrs to datastar_attrs - it's already in textarea_attrs!

    # For HTML textarea, the initial value should be passed as children content
    initial_content = value if value and not signal else None
    
    # Create the base textarea
    if initial_content:
        base_textarea = HTMLTextarea(initial_content, *datastar_attrs, **textarea_attrs)
    else:
        base_textarea = HTMLTextarea(*datastar_attrs, **textarea_attrs)
    
    # CRITICAL FIX: Remove auto-generated name attribute for reactive textareas
    # StarHTML automatically sets name=id, which conflicts with ds_bind
    if signal and 'name' in base_textarea.attrs and base_textarea.attrs.get('name') == base_textarea.attrs.get('id'):
        base_textarea.attrs = {k: v for k, v in base_textarea.attrs.items() if k != 'name'}
    
    return base_textarea


def TextareaWithLabel(
    *,  # Force keyword-only arguments for consistency and flexibility
    label: str,
    placeholder: str | None = None,
    value: str | None = None,
    signal: str | None = None,
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
    **attrs: Any,
) -> FT:
    if not id:
        import uuid

        id = f"textarea_{str(uuid.uuid4())[:8]}"

    if error_text:
        attrs["aria_invalid"] = "true"

    return Div(
        HTMLLabel(
            label,
            HTMLSpan(" *", cls="text-destructive") if required else "",
            for_=id,
            cls=cn("block text-sm font-medium mb-1.5", label_cls),
        ),
        Textarea(
            placeholder=placeholder,
            value=value,
            signal=signal,
            name=name,
            id=id,
            disabled=disabled,
            readonly=readonly,
            required=required,
            rows=rows,
            cls=textarea_cls,
            **attrs,
        ),
        error_text and HTMLP(error_text, cls="text-sm text-destructive mt-1.5"),
        helper_text
        and not error_text
        and HTMLP(helper_text, cls="text-sm text-muted-foreground mt-1.5"),
        cls=cn("space-y-1.5", cls),
    )
