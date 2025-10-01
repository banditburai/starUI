from typing import Any, Literal

from starhtml import FT, Button, Div, Icon, Signal, js

from .utils import cn, ensure_signal

AccordionType = Literal["single", "multiple"]


def Accordion(
    *children: Any,
    type: AccordionType = "single",
    collapsible: bool = False,
    default_value: str | list[str] | None = None,
    signal: str = "",
    cls: str = "",
    **kwargs: Any,
) -> FT:
    sig_name = ensure_signal(signal, "accordion")

    if type == "single":
        initial = default_value or ""
    else:
        initial = [default_value] if isinstance(default_value, str) else (default_value or [])

    return Div(
        (sig := Signal(sig_name, initial)),
        *[child(sig, type, collapsible) if callable(child) else child for child in children],
        cls=cn("w-full min-w-0", cls),
        **kwargs,
    )


def AccordionItem(
    *children: Any,
    value: str,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    def _(sig, type="single", collapsible=False):
        return Div(
            *[child(sig, type, collapsible, value) if callable(child) else child for child in children],
            data_value=value,
            cls=cn("border-b", cls),
            **kwargs,
        )

    return _


def AccordionTrigger(
    *children: Any,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    def _(sig, type="single", collapsible=False, item_value=None):
        if not item_value:
            raise ValueError("AccordionTrigger must be used inside AccordionItem")

        is_open = (sig == item_value) if type == "single" else sig.contains(item_value)

        if type == "single":
            click_action = sig.toggle(item_value, "") if collapsible else sig.set(item_value)
        else:
            click_action = js(f"{sig} = {sig}.includes('{item_value}') ? {sig}.filter(v => v !== '{item_value}') : [...{sig}, '{item_value}']")

        return Div(
            Button(
                *children,
                Icon(
                    "lucide:chevron-down",
                    cls="h-4 w-4 shrink-0 text-muted-foreground transition-transform duration-200 ease-out",
                    data_attr_style=is_open.if_("transform: rotate(180deg)", "transform: rotate(0deg)"),
                ),
                data_on_click=click_action,
                type="button",
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
    def _(sig, type="single", _collapsible=False, item_value=None):
        if not item_value:
            raise ValueError("AccordionContent must be used inside AccordionItem")

        is_open = (sig == item_value) if type == "single" else sig.contains(item_value)

        return Div(
            Div(
                Div(*children, cls="pb-4 pt-0"),
                cls="overflow-hidden min-h-0"
            ),
            cls=cn("text-sm grid transition-[grid-template-rows] duration-200 ease-out", cls),
            data_attr_style=is_open.if_("grid-template-rows: 1fr", "grid-template-rows: 0fr"),
            data_attr_state=is_open.if_("open", "closed"),
            **kwargs,
        )

    return _
