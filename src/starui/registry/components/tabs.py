from itertools import count
from typing import Any, Literal

from starhtml import FT, Div
from starhtml import Button as HTMLButton
from starhtml.datastar import ds_on_click, ds_show, ds_signals

from .utils import cn

TabsVariant = Literal["default", "plain"]

_tab_ids = count(1)


def Tabs(
    *children: Any,
    default_value: str,
    signal: str = "",
    variant: TabsVariant = "default",
    class_name: str = "",
    cls: str = "",
    **attrs: Any,
) -> FT:
    signal = signal or f"tabs_{next(_tab_ids)}"
    signal_value = f"{signal}_value"

    processed_children = [
        child._inject_signal(signal_value, default_value, variant)
        if hasattr(child, "_inject_signal")
        else child
        for child in children
    ]

    return Div(
        *processed_children,
        ds_signals(**{signal_value: default_value}),
        data_slot="tabs",
        cls=cn("flex flex-col gap-2", class_name, cls),
        **attrs,
    )


def TabsList(
    *children: Any,
    class_name: str = "",
    cls: str = "",
    **attrs: Any,
) -> FT:
    def _inject_signal(signal_value, default_value=None, variant="default"):
        processed_children = [
            child._inject_signal(signal_value, variant)
            if hasattr(child, "_inject_signal")
            else child
            for child in children
        ]

        base_classes = (
            "text-muted-foreground inline-flex h-9 w-fit items-center p-[3px] "
            "justify-start gap-4 rounded-none bg-transparent px-2 md:px-0"
            if variant == "plain"
            else "bg-muted text-muted-foreground inline-flex h-9 w-fit items-center "
            "justify-center rounded-lg p-[3px]"
        )

        return Div(
            *processed_children,
            data_slot="tabs-list",
            cls=cn(base_classes, class_name, cls),
            role="tablist",
            **attrs,
        )

    _inject_signal._inject_signal = _inject_signal
    return _inject_signal


def TabsTrigger(
    *children: Any,
    value: str,
    disabled: bool = False,
    class_name: str = "",
    cls: str = "",
    **attrs: Any,
) -> FT:
    def _inject_signal(signal_value, variant="default"):
        base = (
            "inline-flex h-[calc(100%-1px)] flex-1 items-center justify-center "
            "gap-1.5 rounded-md border border-transparent py-1 font-medium "
            "whitespace-nowrap transition-[color,box-shadow] focus-visible:ring-[3px] "
            "focus-visible:outline-1 disabled:pointer-events-none disabled:opacity-50 "
            "[&_svg]:pointer-events-none [&_svg]:shrink-0 [&_svg:not([class*='size-'])]:size-4"
        )

        variant_styles = {
            "plain": "text-muted-foreground data-[state=active]:text-foreground px-0 text-base data-[state=active]:shadow-none",
            "default": (
                "px-2 text-sm text-foreground dark:text-muted-foreground "
                "data-[state=active]:bg-background data-[state=active]:text-foreground "
                "data-[state=active]:shadow-sm dark:data-[state=active]:border-input "
                "dark:data-[state=active]:bg-input/30 dark:data-[state=active]:text-foreground "
                "focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:outline-ring"
            ),
        }

        return HTMLButton(
            *children,
            ds_on_click(f"${signal_value} = '{value}'"),
            disabled=disabled,
            type="button",
            role="tab",
            aria_controls=f"panel-{value}",
            id=f"tab-{value}",
            cls=cn(
                base,
                variant_styles.get(variant, variant_styles["default"]),
                class_name,
                cls,
            ),
            **{
                "data-attr-data-state": f"${signal_value} === '{value}' ? 'active' : 'inactive'",
                "data-attr-aria-selected": f"${signal_value} === '{value}'",
                **attrs,
            },
        )

    _inject_signal._inject_signal = _inject_signal
    return _inject_signal


def TabsContent(
    *children: Any,
    value: str,
    class_name: str = "",
    cls: str = "",
    **attrs: Any,
) -> FT:
    def _inject_signal(signal_value, default_value=None, variant="default"):
        return Div(
            *children,
            ds_show(f"${signal_value} === '{value}'"),
            data_slot="tabs-content",
            role="tabpanel",
            id=f"panel-{value}",
            aria_labelledby=f"tab-{value}",
            tabindex="0",
            cls=cn("mt-2 outline-none", class_name, cls),
            style=None if default_value == value else "display: none",
            **attrs,
        )

    _inject_signal._inject_signal = _inject_signal
    return _inject_signal
