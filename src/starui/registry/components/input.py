"""Input component matching shadcn/ui styling and behavior."""

from typing import Literal
from uuid import uuid4

from starhtml import FT, Div, Span
from starhtml import Input as HTMLInput
from starhtml import Label as HTMLLabel
from starhtml import P as HTMLP

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
    *args,
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
    **attrs,
) -> FT:
    """
    Input component with optional reactive binding and validation.
    
    Args:
        type: Input type (text, email, password, etc.)
        placeholder: Placeholder text
        value: Initial value (for non-reactive inputs)
        name: Form field name (for traditional forms)
        id: Element ID
        disabled: Whether input is disabled
        readonly: Whether input is read-only
        required: Whether input is required
        autofocus: Whether to autofocus
        autocomplete: Autocomplete hint
        min: Minimum value (for number/date inputs)
        max: Maximum value (for number/date inputs)
        step: Step value (for number inputs)
        pattern: HTML5 validation pattern
        signal: Datastar signal name for reactive binding (enables reactivity)
        validation: JavaScript validation expression (e.g., '/^[a-z]+$/.test($signal)')
        cls: CSS classes (alias for class_name)
        class_name: CSS classes
        **attrs: Additional HTML attributes
    
    Returns:
        FT: Input element with proper attributes
    """
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

    # Build base input attributes
    input_attrs = {"type": type, "cls": classes, "data_slot": "input"}
    
    # Add optional attributes only if provided
    if placeholder:
        input_attrs["placeholder"] = placeholder
    if value is not None:
        input_attrs["value"] = value
    if name:
        input_attrs["name"] = name
    if id:
        input_attrs["id"] = id
    if disabled:
        input_attrs["disabled"] = disabled
    if readonly:
        input_attrs["readonly"] = readonly
    if required:
        input_attrs["required"] = required
    if autofocus:
        input_attrs["autofocus"] = autofocus
    if autocomplete:
        input_attrs["autocomplete"] = autocomplete
    if min is not None:
        input_attrs["min"] = str(min)
    if max is not None:
        input_attrs["max"] = str(max)
    if step is not None:
        input_attrs["step"] = str(step)
    if pattern:
        input_attrs["pattern"] = pattern

    # Handle reactive functionality
    if signal:
        from starhtml.datastar import ds_bind, ds_on_input, ds_on_load
        
        # Add reactive binding
        bind_attrs = ds_bind(signal)
        input_attrs.update(bind_attrs.attrs)
        
        # Add validation if specified
        if validation:
            validation_signal = f"{signal}Valid"
            validation_expr = validation.replace('$signal', f'${signal}')
            
            # Add validation on input (ds_bind handles basic value syncing)
            input_js = f"${validation_signal} = {validation_expr}"
            input_handler = ds_on_input(input_js)
            input_attrs.update(input_handler.attrs)
            
            # Add initial validation on load
            load_js = f"${validation_signal} = {validation_expr}"
            load_handler = ds_on_load(load_js)
            input_attrs.update(load_handler.attrs)

    # Merge any additional attributes (excluding signal and validation which are not HTML attrs)
    clean_attrs = {k: v for k, v in attrs.items() if k not in ['signal', 'validation']}
    input_attrs.update(clean_attrs)

    # Create the base input with positional args first
    base_input = HTMLInput(*args, **input_attrs)
    
    # CRITICAL FIX: Remove auto-generated name attribute for reactive inputs
    # StarHTML automatically sets name=id, which conflicts with ds_bind
    if signal and 'name' in base_input.attrs and base_input.attrs.get('name') == base_input.attrs.get('id'):
        base_input.attrs = {k: v for k, v in base_input.attrs.items() if k != 'name'}

    return base_input


def InputWithLabel(
    *,  # Force keyword-only arguments for consistency and flexibility
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
    **attrs,
) -> FT:
    """
    Input with label component that uses the new reactive API.
    """
    id = id or f"input_{str(uuid4())[:8]}"
    
    if error_text:
        attrs["aria_invalid"] = "true"

    return Div(
        HTMLLabel(
            label,
            Span(" *", cls="text-destructive") if required else "",
            for_=id,
            cls=cn("block text-sm font-medium mb-1.5", label_cls),
        ),
        Input(
            type=type,
            placeholder=placeholder,
            value=value,
            signal=signal,  # Now using the new API
            validation=validation,  # And validation support
            name=name,
            id=id,
            disabled=disabled,
            readonly=readonly,
            required=required,
            cls=input_cls,
            **attrs,
        ),
        error_text and HTMLP(error_text, cls="text-sm text-destructive mt-1.5"),
        helper_text
        and not error_text
        and HTMLP(helper_text, cls="text-sm text-muted-foreground mt-1.5"),
        cls=cn("space-y-1.5", cls),
    )
