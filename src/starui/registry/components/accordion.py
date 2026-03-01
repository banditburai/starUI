from itertools import count
from typing import Any, Literal

from starhtml import FT, Button, Div, Icon, Signal

from .utils import cn, gen_id, inject_context, merge_actions

AccordionType = Literal["single", "multiple"]


def Accordion(
    *children: Any,
    type: AccordionType = "single",
    collapsible: bool = False,
    value: str | int | list[str | int] | None = None,
    signal: str | Signal = "",
    cls: str = "",
    **kwargs: Any,
) -> FT:
    sig = getattr(signal, "_id", signal) or gen_id("accordion")

    if type == "single":
        initial = "" if value is None else value
    else:
        initial = (
            []
            if value is None
            else list(value)
            if isinstance(value, list | tuple)
            else [value]
        )

    accordion_state = Signal(sig, initial)
    ctx = {
        "accordion_state": accordion_state,
        "id": sig,
        "type": type,
        "collapsible": collapsible,
        "initial_value": value,
        "_item_index": count(),
    }

    return Div(
        accordion_state,
        *[inject_context(child, **ctx) for child in children],
        cls=cn("w-full min-w-0", cls),
        **kwargs,
    )


def AccordionItem(
    *children: Any,
    value: str | int | None = None,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    def _(*, accordion_state, id, type, collapsible, initial_value, _item_index, **_):
        item_value = value if value is not None else next(_item_index)
        is_open = (
            (accordion_state == item_value)
            if type == "single"
            else accordion_state.contains(item_value)
        )
        is_default_open = (
            (item_value == initial_value)
            if type == "single"
            else isinstance(initial_value, list) and item_value in initial_value
        )

        if type == "single":
            click_action = (
                accordion_state.toggle(item_value, "")
                if collapsible
                else accordion_state.set(item_value)
            )
        else:
            click_action = accordion_state.toggle_in(item_value)

        child_ctx = {
            "id": id,
            "item_value": item_value,
            "is_open": is_open,
            "is_default_open": is_default_open,
            "click_action": click_action,
        }

        return Div(
            *[inject_context(child, **child_ctx) for child in children],
            data_value=str(item_value),
            # SSR initial + reactive binding (prevents FOUC before Datastar hydrates)
            data_state="open" if is_default_open else "closed",
            data_attr_data_state=is_open.if_("open", "closed"),
            cls=cn("border-b", cls),
            **kwargs,
        )

    return _


def AccordionTrigger(
    *children: Any,
    cls: str = "",
    icon: str | None = "lucide:chevron-down",
    icon_cls: str = "h-4 w-4 shrink-0 text-muted-foreground transition-transform duration-200 ease-out",
    icon_rotation: int = 180,
    **kwargs: Any,
) -> FT:
    def _(*, id, item_value, is_open, is_default_open, click_action, **_):
        click_actions = merge_actions(click_action, kwargs=kwargs)

        icon_el = (
            (
                Icon(
                    icon,
                    cls=icon_cls,
                    style=f"transform: rotate({icon_rotation}deg)"
                    if is_default_open
                    else None,
                    data_attr_style=is_open.if_(
                        f"transform: rotate({icon_rotation}deg)",
                        "transform: rotate(0deg)",
                    ),
                ),
            )
            if icon
            else ()
        )

        return Div(
            Button(
                *children,
                *icon_el,
                data_on_click=click_actions,
                type="button",
                id=f"{id}-{item_value}-trigger",
                aria_controls=f"{id}-{item_value}-content",
                aria_expanded="true" if is_default_open else "false",
                data_attr_aria_expanded=is_open.if_("true", "false"),
                data_state="open" if is_default_open else "closed",
                data_attr_data_state=is_open.if_("open", "closed"),
                cls=cn(
                    "flex w-full items-center justify-between py-4 text-sm font-medium transition-all hover:underline text-left",
                    cls,
                ),
                **kwargs,
            ),
            cls="flex w-full",
        )

    return _


def AccordionContent(
    *children: Any,
    cls: str = "",
    role: str = "region",
    **kwargs: Any,
) -> FT:
    def _(*, id, item_value, is_open, is_default_open, **_):
        return Div(
            Div(
                Div(*children, cls="pb-4 pt-0"),
                cls="overflow-hidden min-h-0",
            ),
            role=role,
            id=f"{id}-{item_value}-content",
            aria_labelledby=f"{id}-{item_value}-trigger",
            style="grid-template-rows: 1fr"
            if is_default_open
            else "grid-template-rows: 0fr",
            data_state="open" if is_default_open else "closed",
            cls=cn(
                "text-sm grid transition-[grid-template-rows] duration-200 ease-out",
                cls,
            ),
            data_attr_style=is_open.if_(
                "grid-template-rows: 1fr", "grid-template-rows: 0fr"
            ),
            data_attr_data_state=is_open.if_("open", "closed"),
            **kwargs,
        )

    return _
