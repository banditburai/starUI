from itertools import count
from typing import Any, Literal

from starhtml import FT, Button, Div, Icon, Signal

from .utils import cn, gen_id

AccordionType = Literal["single", "multiple"]


def _is_default_open(item_value: str | int, initial_value: Any, type: AccordionType) -> bool:
    if type == "single":
        return item_value == initial_value
    return isinstance(initial_value, list) and item_value in initial_value


def Accordion(
    *children: Any,
    type: AccordionType = "single",
    collapsible: bool = False,
    value: str | int | list[str | int] | None = None,
    signal: str | Signal = "",
    cls: str = "",
    **kwargs: Any,
) -> FT:
    sig = getattr(signal, '_id', signal) or gen_id("accordion")

    if type == "single":
        initial = "" if value is None else value
    else:
        initial = (
            [] if value is None
            else list(value) if isinstance(value, (list, tuple))
            else [value]
        )

    accordion_state = Signal(sig, initial)
    ctx = dict(
        accordion_state=accordion_state,
        type=type,
        collapsible=collapsible,
        initial_value=value,
        _item_index=count()
    )

    return Div(
        accordion_state,
        *[child(**ctx) if callable(child) else child for child in children],
        cls=cn("w-full min-w-0", cls),
        **kwargs,
    )


def AccordionItem(
    *children: Any,
    value: str | int | None = None,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    def _(*, _item_index, **ctx):
        item_value = value if value is not None else next(_item_index)
        return Div(
            *[child(item_value=item_value, **ctx) if callable(child) else child for child in children],
            data_value=str(item_value),
            cls=cn("border-b", cls),
            **kwargs,
        )

    return _


def AccordionTrigger(
    *children: Any,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    def _(*, accordion_state, type, collapsible, item_value, initial_value, **_):
        if item_value is None:
            raise ValueError("AccordionTrigger must be used inside AccordionItem")

        is_open = (accordion_state == item_value) if type == "single" else accordion_state.contains(item_value)
        is_default_open = _is_default_open(item_value, initial_value, type)

        if type == "single":
            click_action = accordion_state.toggle(item_value, "") if collapsible else accordion_state.set(item_value)
        else:
            click_action = accordion_state.toggle_in(item_value)

        user_on_click = kwargs.pop('data_on_click', None)
        user_actions = user_on_click if isinstance(user_on_click, list) else ([user_on_click] if user_on_click else [])
        click_actions = [click_action] + user_actions

        return Div(
            Button(
                *children,
                Icon(
                    "lucide:chevron-down",
                    cls="h-4 w-4 shrink-0 text-muted-foreground transition-transform duration-200 ease-out",
                    style=f"transform: rotate({'180deg' if is_default_open else '0deg'})",
                    data_attr_style=is_open.if_("transform: rotate(180deg)", "transform: rotate(0deg)"),
                ),
                data_on_click=click_actions,
                type="button",
                id=f"{item_value}-trigger",
                aria_controls=f"{item_value}-content",
                aria_expanded="true" if is_default_open else "false",
                data_attr_aria_expanded=is_open,
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
    **kwargs: Any,
) -> FT:
    def _(*, accordion_state, type, item_value, initial_value, **_):
        if item_value is None:
            raise ValueError("AccordionContent must be used inside AccordionItem")

        is_open = (accordion_state == item_value) if type == "single" else accordion_state.contains(item_value)
        is_default_open = _is_default_open(item_value, initial_value, type)
        initial_style = "grid-template-rows: 1fr" if is_default_open else "grid-template-rows: 0fr"

        return Div(
            Div(
                Div(*children, cls="pb-4 pt-0"),
                cls="overflow-hidden min-h-0"
            ),
            role="region",
            id=f"{item_value}-content",
            aria_labelledby=f"{item_value}-trigger",
            style=initial_style,
            cls=cn("text-sm grid transition-[grid-template-rows] duration-200 ease-out", cls),
            data_attr_style=is_open.if_("grid-template-rows: 1fr", "grid-template-rows: 0fr"),
            data_attr_state=is_open.if_("open", "closed"),
            **kwargs,
        )

    return _
