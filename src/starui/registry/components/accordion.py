from typing import Any, Literal
from uuid import uuid4

from starhtml import FT, Button, Div, Icon
from starhtml.datastar import ds_on_click, ds_signals, value

from .utils import cn

AccordionType = Literal["single", "multiple"]


def Accordion(
    *children: Any,
    type: AccordionType = "single",
    collapsible: bool = False,
    default_value: str | list[str] | None = None,
    signal: str = "",
    class_name: str = "",
    cls: str = "",
    **attrs: Any,
) -> FT:
    signal = signal or f"accordion_{uuid4().hex[:8]}"

    match (type, default_value):
        case ("single", _):
            initial_value = value(default_value or "")
        case ("multiple", None):
            initial_value = value([])
        case ("multiple", str() as val):
            initial_value = value([val])
        case ("multiple", val):
            initial_value = value(val)

    return Div(
        *[child(signal, type, collapsible) if callable(child) else child 
          for child in children],
        ds_signals(**{signal: initial_value}),
        cls=cn("w-full min-w-0", class_name, cls),
        **attrs,
    )


def AccordionItem(
    *children: Any,
    value: str,
    class_name: str = "",
    cls: str = "",
    **attrs: Any,
) -> FT:
    def _(signal, type="single", collapsible=False):
        return Div(
            *[child(signal, type, collapsible, value) if callable(child) else child
              for child in children],
            data_value=value,
            cls=cn("border-b", class_name, cls),
            **attrs,
        )

    return _


def AccordionTrigger(
    *children: Any,
    class_name: str = "",
    cls: str = "",
    **attrs: Any,
) -> FT:
    def _(signal, type="single", collapsible=False, item_value=None):
        if not item_value:
            raise ValueError("AccordionTrigger must be used inside AccordionItem")

        if type == "single":
            click_expr = (
                f"${signal} = ${signal} === '{item_value}' ? '' : '{item_value}'"
                if collapsible
                else f"${signal} = '{item_value}'"
            )
            is_open_expr = f"${signal} === '{item_value}'"
        else:
            click_expr = (
                f"${signal} = ${signal}.includes('{item_value}') "
                f"? ${signal}.filter(v => v !== '{item_value}') "
                f": [...${signal}, '{item_value}']"
            )
            is_open_expr = f"${signal}.includes('{item_value}')"

        return Div(
            Button(
                *children,
                Icon(
                    "lucide:chevron-down",
                    cls="h-4 w-4 shrink-0 text-muted-foreground transition-transform duration-200 ease-out",
                    data_attr_style=f"({is_open_expr}) ? 'transform: rotate(180deg)' : 'transform: rotate(0deg)'",
                ),
                ds_on_click(click_expr),
                type="button",
                cls=cn(
                    "flex w-full items-center justify-between py-4 text-sm font-medium transition-all hover:underline text-left",
                    class_name,
                    cls,
                ),
                **attrs,
            ),
            cls="flex w-full",
        )

    return _


def AccordionContent(
    *children: Any,
    class_name: str = "",
    cls: str = "",
    **attrs: Any,
) -> FT:
    def _(signal, type="single", collapsible=False, item_value=None):
        if not item_value:
            raise ValueError("AccordionContent must be used inside AccordionItem")

        show_expr = (
            f"${signal} === '{item_value}'"
            if type == "single"
            else f"${signal}.includes('{item_value}')"
        )

        return Div(
            Div(
                Div(
                    *children,
                    cls=cn("pb-4 pt-0", class_name),
                ),
                cls="overflow-hidden min-h-0"
            ),
            cls=cn(
                "text-sm grid transition-[grid-template-rows] duration-200 ease-out",
                cls
            ),
            data_attr_style=f"({show_expr}) ? 'grid-template-rows: 1fr' : 'grid-template-rows: 0fr'",
            data_state=f"({show_expr}) ? 'open' : 'closed'",
            **attrs,
        )

    return _
