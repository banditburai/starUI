from typing import Any

from starhtml import Div, FT, Icon, Signal, Span
from starhtml import Button as HTMLButton
from starhtml import Label as HTMLLabel
from starhtml import P as HTMLP

from .utils import cn, gen_id, inject_context


def Select(
    *children,
    value: str | None = None,
    label: str | None = None,
    signal: str | Signal = "",
    cls: str = "",
    **kwargs: Any,
) -> FT:
    sig = getattr(signal, 'id', signal) or gen_id("select")

    selected = Signal(f"{sig}_value", value or "")
    selected_label = Signal(f"{sig}_label", label or "")
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
) -> FT:
    def trigger(*, sig, selected_label, **ctx):        
        custom_id = kwargs.pop("id", None)
        trigger_id = custom_id or f"{sig}_trigger"
        trigger_ref = Signal(trigger_id, _ref_only=True)

        return HTMLButton(
            *[child(sig=sig, selected_label=selected_label, **ctx) if callable(child) else child for child in children],
            Icon("lucide:chevron-down", cls="size-4 shrink-0 opacity-50"),
            data_ref=trigger_ref,
            popovertarget=f"{sig}_content",
            popoveraction="toggle",
            type="button",
            role="combobox",
            aria_haspopup="listbox",
            aria_controls=f"{sig}_content",
            id=trigger_ref.id,
            cls=cn(
                "w-[180px] flex h-9 items-center justify-between gap-2 rounded-md border border-input",
                "bg-transparent px-3 py-2 text-sm shadow-xs",
                "transition-[color,box-shadow] outline-none truncate",
                "dark:bg-input/30 dark:hover:bg-input/50",
                "focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:ring-[3px]",
                "aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40",
                "aria-invalid:border-destructive",
                "disabled:cursor-not-allowed disabled:opacity-50",
                cls,
            ),
            data_slot="select-trigger",
            **kwargs,
        )

    return trigger


def SelectValue(
    *children,
    placeholder: str = "Select an option",
    cls: str = "",
    **kwargs: Any,
) -> FT:
    def value_component(*, selected_label, **_):
        if children:
            return Span(*children, cls=cn("pointer-events-none truncate flex-1 text-left", cls), **kwargs)

        text_expr = kwargs.pop('data_text') if 'data_text' in kwargs else selected_label.or_(placeholder)

        return Span(
            data_text=text_expr,
            cls=cn("pointer-events-none truncate flex-1 text-left", cls),
            data_class_text_muted_foreground=~selected_label,
            **kwargs,
        )

    return value_component


def SelectContent(
    *children,
    side: str = "bottom",
    align: str = "start",
    side_offset: int = 4,
    container: str = "none",
    cls: str = "",
    **kwargs: Any,
) -> FT:
    def content(*, sig, **ctx):
        trigger_ref = Signal(f"{sig}_trigger", _ref_only=True)
        content_ref = Signal(f"{sig}_content", _ref_only=True)
        placement = side if align == "center" else f"{side}-{align}"

        position_mods = {
            "placement": placement,
            "offset": side_offset,
            "flip": True,
            "shift": True,
            "hide": True,
            "container": container,
        }

        context = dict(sig=sig, **ctx)

        return Div(
            Div(*[inject_context(child, **context) for child in children], cls="p-1 max-h-[300px] overflow-auto"),
            data_ref=content_ref,
            data_style_min_width=trigger_ref.if_(trigger_ref.offsetWidth + 'px', '8rem'),
            data_position=(trigger_ref.id, position_mods),
            popover="auto",
            id=content_ref.id,
            role="listbox",
            aria_labelledby=trigger_ref.id,
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
    *children,
    value: str = "",
    disabled: bool = False,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    def item(*, sig, selected, selected_label, **_):
        content_ref = Signal(f"{sig}_content", _ref_only=True)

        item_value = value or (children[0] if children and isinstance(children[0], str) else "")
        label_text = children[0] if (children and isinstance(children[0], str)) else item_value
        is_selected = selected.eq(item_value)

        user_on_click = kwargs.pop('data_on_click', None)
        user_actions = user_on_click if isinstance(user_on_click, list) else ([user_on_click] if user_on_click else [])
        click_actions = user_actions + [selected.set(item_value), selected_label.set(label_text), content_ref.hidePopover()]

        return Div(
            *children,
            Span(
                Icon("lucide:check", cls="h-4 w-4"),
                style="opacity: 0; transition: opacity 0.15s",
                data_style_opacity=is_selected.if_("1", "0"),
                cls="absolute right-2 flex h-3.5 w-3.5 items-center justify-center",
            ),
            data_on_click=click_actions if not disabled else None,
            role="option",
            data_value=item_value,
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
) -> FT:
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
) -> FT:
    def label(**_):
        return Div(
            *children,
            cls=cn("text-muted-foreground px-2 py-1.5 text-xs", cls),
            **kwargs,
        )

    return label


def _get_value_label(item: str | tuple) -> tuple[str, str]:
    match item:
        case str():
            return item, item
        case (value, label):
            return value, label
        case _:
            return "", ""


def _find_initial_label(options: list, value: str | None) -> str:
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
    def _process_option(opt):
        match opt:
            case str():
                return SelectItem(opt)
            case (value, label):
                return SelectItem(label, value=value)
            case {"group": group_label, "items": group_items}:
                return SelectGroup(
                    *[
                        SelectItem(item_label, value=item_value)
                        for item_value, item_label in [_get_value_label(item) for item in group_items]
                    ],
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
            value=value,
            label=_find_initial_label(options, value),
            signal=sig,
            cls="w-full",
            *attrs,
            **kwargs,
        ),
        HTMLP(error_text, cls="text-sm text-destructive mt-1.5") if error_text else None,
        HTMLP(helper_text, cls="text-sm text-muted-foreground mt-1.5") if helper_text and not error_text else None,
        cls=cn("space-y-1.5", cls),
    )
