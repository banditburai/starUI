from typing import Any

from starhtml import Div, FT, Icon, Signal, Span
from starhtml import Button as HTMLButton
from starhtml import Label as HTMLLabel
from starhtml import P as HTMLP

from .utils import cn, gen_id, inject_signal_recursively, js_literal


def Select(
    *children,
    initial_value: str | None = None,
    initial_label: str | None = None,
    signal: str | Signal = "",
    cls: str = "",
    **kwargs: Any,
) -> FT:
    sig = getattr(signal, 'id', signal) or gen_id("select")

    selected = Signal(f"{sig}_value", initial_value or "")
    selected_label = Signal(f"{sig}_label", initial_label or "")
    open_state = Signal(f"{sig}_open", False)

    ctx = dict(sig=sig, selected=selected, selected_label=selected_label, open_state=open_state)

    return Div(
        selected,
        selected_label,
        open_state,
        *[child(**ctx) if callable(child) else child for child in children],
        cls=cn("relative", cls),
        data_slot="select",
        **kwargs,
    )


def SelectTrigger(
    *children,
    cls: str = "",
    **kwargs: Any,
):
    def trigger(*, sig, selected_label, **ctx):
        trigger_id = kwargs.pop("id", f"{sig}_trigger")

        return HTMLButton(
            *[child(sig=sig, selected_label=selected_label, **ctx) if callable(child) else child for child in children],
            Icon("lucide:chevron-down", cls="size-4 shrink-0 opacity-50"),
            data_ref=f"{sig}_trigger",
            popovertarget=f"{sig}_content",
            popoveraction="toggle",
            type="button",
            role="combobox",
            aria_haspopup="listbox",
            aria_controls=f"{sig}_content",
            data_placeholder=~selected_label,
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
            data_slot="select-trigger",
            **kwargs,
        )

    return trigger


def SelectValue(
    placeholder: str = "Select an option",
    cls: str = "",
    **kwargs: Any,
):
    def value_component(*, selected_label, **_):
        from starhtml.datastar import js

        return Span(
            data_text=js(f"${selected_label.name} || '{placeholder}'"),
            data_attr_class=selected_label.if_("", "text-muted-foreground"),
            cls=cn("pointer-events-none truncate flex-1 text-left", cls),
            **kwargs,
        )

    return value_component


def SelectContent(
    *children,
    cls: str = "",
    **kwargs: Any,
):
    def content(*, sig, **ctx):
        from starhtml.datastar import js

        content_min_width = Signal(
            f"{sig}_content_min_width",
            js(f"${sig}_trigger ? ${sig}_trigger.offsetWidth + 'px' : 'auto'")
        )

        return Div(
            content_min_width,
            Div(*[inject_signal_recursively(child, sig) for child in children], cls="p-1 max-h-[300px] overflow-auto"),
            data_ref=f"{sig}_content",
            data_style_min_width=content_min_width,
            data_position=(
                f"{sig}_trigger",
                {
                    "placement": "bottom",
                    "offset": 4,
                    "flip": True,
                    "shift": True,
                    "hide": True,
                }
            ),
            popover="auto",
            id=f"{sig}_content",
            role="listbox",
            aria_labelledby=f"{sig}_trigger",
            tabindex="-1",
            cls=cn(
                "z-50 min-w-[8rem] overflow-hidden rounded-md border bg-popover text-popover-foreground shadow-md dark:border-input",
                cls,
            ),
            data_slot="select-content",
            **kwargs,
        )

    return content


def SelectItem(
    value: str,
    label: str | None = None,
    disabled: bool = False,
    cls: str = "",
    **kwargs: Any,
):
    def item(*, sig, selected, selected_label, **_):
        from starhtml.datastar import js

        label_text = label or value
        js_safe_label = js_literal(label_text)
        is_selected = selected.eq(value)

        return Div(
            Span(label_text),
            Span(
                Icon("lucide:check", cls="h-4 w-4"),
                style="opacity: 0; transition: opacity 0.15s",
                data_style_opacity=is_selected.if_("1", "0"),
                cls="absolute right-2 flex h-3.5 w-3.5 items-center justify-center",
            ),
            data_on_click=[
                selected.set(value),
                selected_label.set(js_safe_label),
                js(f"${sig}_content.hidePopover()")
            ] if not disabled else None,
            role="option",
            data_value=value,
            data_selected=is_selected,
            data_disabled="true" if disabled else None,
            cls=cn(
                "relative flex w-full cursor-default select-none items-center rounded-sm py-1.5 pl-2 pr-8 text-sm outline-none",
                "hover:bg-accent hover:text-accent-foreground focus:bg-accent focus:text-accent-foreground",
                "data-[disabled]:pointer-events-none data-[disabled]:opacity-50",
                cls,
            ),
            data_slot="select-item",
            **kwargs,
        )

    return item


def SelectGroup(
    *children,
    label: str | None = None,
    cls: str = "",
    **kwargs: Any,
):
    def group(*, sig, **ctx):
        return Div(
            SelectLabel(label)(sig=sig, **ctx) if label else None,
            *[child(sig=sig, **ctx) if callable(child) else child for child in children],
            cls=cls,
            **kwargs,
        )

    return group


def SelectLabel(
    *children,
    cls: str = "",
    **kwargs: Any,
):
    def label(**_):
        return Div(
            *children,
            cls=cn("text-muted-foreground px-2 py-1.5 text-xs", cls),
            **kwargs,
        )

    return label


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


def _build_select_items(options: list) -> list:
    """Convert options list into SelectItem components."""
    def _process_option(opt):
        match opt:
            case str():
                return SelectItem(value=opt, label=opt)
            case (value, label):
                return SelectItem(value=value, label=label)
            case {"group": group_label, "items": group_items}:
                return SelectGroup(
                    *[SelectItem(*_get_value_label(item)) for item in group_items],
                    label=group_label
                )
    
    return [_process_option(opt) for opt in options]


def SelectWithLabel(
    *attrs: Any,
    label: str,
    options: list[str | tuple[str, str] | dict],
    value: str | None = None,
    placeholder: str = "Select an option",
    name: str | None = None,
    signal: str | Signal = "",
    id: str = "",
    helper_text: str = "",
    error_text: str = "",
    required: bool = False,
    disabled: bool = False,
    label_cls: str = "",
    select_cls: str = "",
    cls: str = "",
    **kwargs: Any,
) -> FT:
    sig = getattr(signal, 'id', signal) or gen_id("select")
    trigger_id = id or f"{sig}_trigger"

    return Div(
        HTMLLabel(
            label,
            Span(" *", cls="text-destructive") if required else None,
            fr=trigger_id,
            cls=cn("block text-sm font-medium mb-1.5", label_cls),
        ),
        Select(
            SelectTrigger(
                SelectValue(placeholder=placeholder),
                cls=select_cls,
                disabled=disabled or None,
                aria_invalid="true" if error_text else None,
                id=trigger_id,
            ),
            SelectContent(*_build_select_items(options)),
            initial_value=value,
            initial_label=_find_initial_label(options, value),
            signal=sig,
            cls="w-full",
            *attrs,
            **kwargs,
        ),
        HTMLP(error_text, cls="text-sm text-destructive mt-1.5") if error_text else None,
        HTMLP(helper_text, cls="text-sm text-muted-foreground mt-1.5") if helper_text and not error_text else None,
        cls=cn("space-y-1.5", cls),
    )
