from typing import Any
from uuid import uuid4

from starhtml import FT, Div, Icon, Span
from starhtml import Button as HTMLButton
from starhtml import Label as HTMLLabel
from starhtml import P as HTMLP
from starhtml.datastar import (
    ds_class,
    ds_computed,
    ds_on_click,    
    ds_position,
    ds_ref,
    ds_show,
    ds_signals,
    ds_style,
    ds_text,
    t,
    toggle_class,
    value,
)

from .utils import cn


def Select(
    *children,
    initial_value: str | None = None,
    initial_label: str | None = None,
    signal: str | None = None,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    signal = signal or f"select_{uuid4().hex[:8]}"
    return Div(
        *children,
        ds_signals(
            {
                f"{signal}_value": value(initial_value or ""),
                f"{signal}_label": value(initial_label or ""),
                f"{signal}_open": False,
            }
        ),
        cls=cn("relative", cls),
        **kwargs,
    )


def SelectTrigger(
    *children,
    signal: str | None = None,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    signal = signal or "select"
    trigger_id = kwargs.pop("id", f"{signal}-trigger")

    return HTMLButton(
        *children,
        Icon("lucide:chevron-down", cls="size-4 shrink-0 opacity-50"),
        ds_ref(f"{signal}_trigger"),
        popovertarget=f"{signal}-content",
        popoveraction="toggle",
        type="button",
        role="combobox",
        aria_haspopup="listbox",
        aria_controls=f"{signal}-content",
        data_placeholder=f"!${signal}_label",
        id=trigger_id,
        cls=cn(
            "w-[180px] flex h-9 items-center justify-between gap-2 rounded-md border border-input",
            "bg-transparent px-3 py-2 text-sm shadow-xs",
            "transition-[color,box-shadow] outline-none truncate",
            "dark:bg-input/30 dark:hover:bg-input/50",
            "focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:ring-[3px]",
            "aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40",
            "aria-invalid:border-destructive",
            "disabled:cursor-not-allowed disabled:opacity-50",
            "data-[placeholder]:text-muted-foreground",
            cls,
        ),
        **kwargs,
    )


def SelectValue(
    placeholder: str = "Select an option",
    signal: str | None = None,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    signal = signal or "select"
    return Span(
        ds_text(f"${signal}_label || '{placeholder}'"),
        toggle_class(f"${signal}_label", "", "text-muted-foreground"),
        cls=cn("pointer-events-none truncate flex-1 text-left", cls),
        **kwargs,
    )


def SelectContent(
    *children,
    signal: str | None = None,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    signal = signal or "select"

    return Div(
        Div(*children, cls="p-1 max-h-[300px] overflow-auto"),
        ds_ref(f"{signal}_content"),
        ds_computed(f"{signal}_content_min_width", f"${signal}_trigger ? ${signal}_trigger.offsetWidth + 'px' : 'auto'"),
        ds_style(min_width=f"${signal}_content_min_width"),
        ds_position(
            anchor=f"{signal}-trigger",
            placement="bottom",
            offset=4,
            flip=True,
            shift=True,
            hide=True,
        ),
        popover="auto",
        id=f"{signal}-content",
        role="listbox",
        aria_labelledby=f"{signal}-trigger",
        tabindex="-1",
        cls=cn(
            "z-50 min-w-[8rem] overflow-hidden rounded-md border bg-popover text-popover-foreground shadow-md dark:border-input",
            cls,
        ),
        **kwargs,
    )


def SelectItem(
    value: str,
    label: str | None = None,
    signal: str | None = None,
    disabled: bool = False,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    label = label or value
    signal = signal or "select"
    js_safe_label = label.replace("$", "\\u0024").replace("'", "\\'")

    return Div(
        Span(label),
        Span(
            Icon("lucide:check", cls="h-4 w-4"),
            ds_show(f"${signal}_value === '{value}'"),
            cls="absolute right-2 flex h-3.5 w-3.5 items-center justify-center",
        ),
        ds_on_click(
            f"${signal}_value='{value}';${signal}_label='{js_safe_label}';${signal}_content.hidePopover()"
        ) if not disabled else None,
        role="option",
        data_value=value,
        data_selected=f"${signal}_value === '{value}'",
        data_disabled="true" if disabled else None,
        cls=cn(
            "relative flex w-full cursor-default select-none items-center rounded-sm py-1.5 pl-2 pr-8 text-sm outline-none",
            "hover:bg-accent hover:text-accent-foreground focus:bg-accent focus:text-accent-foreground",
            "data-[disabled]:pointer-events-none data-[disabled]:opacity-50",
            cls,
        ),
        **kwargs,
    )


def SelectGroup(
    *children,
    label: str | None = None,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    return Div(
        SelectLabel(label) if label else None,
        *children,
        cls=cls,
        **kwargs,
    )


def SelectLabel(
    *children,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    return Div(
        *children,
        cls=cn("text-muted-foreground px-2 py-1.5 text-xs", cls),
        **kwargs,
    )


def _get_value_label(item: str | tuple) -> tuple[str, str]:
    """Extract value and label from an option item."""
    match item:
        case str():
            return item, item
        case (value, label):
            return value, label
        case _:
            return "", ""


def _find_initial_label(options: list, value: str | None) -> str:
    """Find the display label for a given value in options."""
    if not value:
        return ""
    
    for opt in options:
        match opt:
            case str() if opt == value:
                return opt
            case (opt_value, label) if opt_value == value:
                return label
            case {"items": items}:
                for item in items:
                    item_value, item_label = _get_value_label(item)
                    if item_value == value:
                        return item_label
    return ""


def _build_select_items(options: list, signal: str) -> list:
    """Convert options list into SelectItem components."""
    items = []
    for opt in options:
        match opt:
            case str():
                items.append(SelectItem(value=opt, label=opt, signal=signal))
            case (value, label):
                items.append(SelectItem(value=value, label=label, signal=signal))
            case {"group": group_label, "items": group_items}:
                items.append(SelectGroup(
                    *[SelectItem(*_get_value_label(item), signal=signal) 
                      for item in group_items],
                    label=group_label
                ))
    return items


def SelectWithLabel(
    *attrs: Any,
    label: str,
    options: list[str | tuple[str, str] | dict],
    value: str | None = None,
    placeholder: str = "Select an option",
    name: str | None = None,
    signal: str | None = None,
    helper_text: str | None = None,
    error_text: str | None = None,
    required: bool = False,
    disabled: bool = False,
    label_cls: str = "",
    select_cls: str = "",
    cls: str = "",
    **kwargs: Any,
) -> FT:
    signal = signal or f"select_{uuid4().hex[:8]}"
    select_id = f"{signal}-trigger"
    initial_label = _find_initial_label(options, value)

    return Div(
        HTMLLabel(
            label,
            Span(" *", cls="text-destructive") if required else "",
            for_=select_id,
            cls=cn("block text-sm font-medium mb-1.5", label_cls),
        ),
        Select(
            SelectTrigger(
                SelectValue(placeholder=placeholder, signal=signal),
                signal=signal,
                cls=select_cls,
                disabled=disabled,
                aria_invalid="true" if error_text else None,
            ),
            SelectContent(*_build_select_items(options, signal), signal=signal),
            initial_value=value,
            initial_label=initial_label,
            signal=signal,
            cls="w-full",
            *attrs,
            **kwargs,
        ),
        error_text and HTMLP(error_text, cls="text-sm text-destructive mt-1.5"),
        helper_text and not error_text and HTMLP(helper_text, cls="text-sm text-muted-foreground mt-1.5"),
        cls=cn("space-y-1.5", cls),
    )
