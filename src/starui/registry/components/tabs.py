from itertools import count
from typing import Any, Literal

from starhtml import FT, Div, Signal
from starhtml import Button as HTMLButton

from .utils import cn, gen_id

TabsVariant = Literal["default", "plain"]


def Tabs(
    *children: Any,
    default_value: str | int = 0,
    variant: TabsVariant = "default",
    signal: str | Signal = "",
    cls: str = "",
    **kwargs: Any,
) -> FT:
    sig = getattr(signal, 'id', signal) or gen_id("tabs")

    ctx = dict(
        tabs_state=(tabs_state := Signal(sig, default_value)),
        variant=variant,
        default_value=default_value,
        _trigger_index=count(),
        _content_index=count(),
    )

    return Div(
        tabs_state,
        *[child(**ctx) if callable(child) else child for child in children],
        data_slot="tabs",
        cls=cn("w-full", cls),
        **kwargs,
    )


def TabsList(*children: Any, cls: str = "", **kwargs: Any) -> FT:
    def _(**ctx):
        variant = ctx.get("variant", "default")

        base_classes = {
            "plain": "text-muted-foreground inline-flex h-9 w-fit items-center p-[3px] justify-start gap-4 rounded-none bg-transparent px-2 md:px-0",
            "default": "bg-muted text-muted-foreground inline-flex h-9 w-fit items-center justify-center rounded-lg p-[3px]",
        }[variant]

        return Div(
            *[child(**ctx) if callable(child) else child for child in children],
            data_slot="tabs-list",
            cls=cn(base_classes, cls),
            role="tablist",
            **kwargs,
        )

    return _


def TabsTrigger(
    *children: Any,
    id: str | int | None = None,
    disabled: bool = False,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    def _(*, tabs_state, variant="default", _trigger_index, **_):
        tab_id = id if id is not None else next(_trigger_index)
        is_active = tabs_state == tab_id

        base = (
            "inline-flex h-[calc(100%-1px)] flex-1 items-center justify-center "
            "gap-1.5 rounded-md py-1 font-medium "
            "whitespace-nowrap transition-[color,box-shadow] focus-visible:ring-[3px] "
            "focus-visible:outline-1 disabled:pointer-events-none disabled:opacity-50 "
            "[&_svg]:pointer-events-none [&_svg]:shrink-0 [&_svg:not([class*='size-'])]:size-4"
        )

        variant_styles = {
            "plain": "text-muted-foreground data-[state=active]:text-foreground px-0 text-base data-[state=active]:shadow-none",
            "default": "px-2 text-sm text-foreground dark:text-muted-foreground data-[state=active]:bg-background data-[state=active]:text-foreground data-[state=active]:shadow-sm dark:data-[state=active]:border data-[state=active]:border-transparent dark:data-[state=active]:bg-input/30 dark:data-[state=active]:!border-input dark:data-[state=active]:text-foreground focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:outline-ring",
        }

        return HTMLButton(
            *children,
            data_on_click=tabs_state.set(tab_id),
            disabled=disabled,
            type="button",
            role="tab",
            aria_controls=f"panel-{tab_id}",
            id=str(tab_id),
            data_slot="tabs-trigger",
            data_attr_data_state=is_active.if_("active", "inactive"),
            data_attr_aria_selected=is_active,
            data_attr_tabindex=is_active.if_("0", "-1"),
            cls=cn(
                base,
                variant_styles[variant],
                cls,
            ),
            **kwargs,
        )

    return _


def TabsContent(*children: Any, id: str | int | None = None, cls: str = "", **kwargs: Any) -> FT:
    def _(*, tabs_state, default_value, _content_index, **_):
        tab_id = id if id is not None else next(_content_index)
        is_active = tabs_state == tab_id

        return Div(
            *children,
            data_show=is_active,
            data_slot="tabs-content",
            role="tabpanel",
            id=f"panel-{tab_id}",
            aria_labelledby=str(tab_id),
            tabindex="0",
            style="display: none" if tab_id != default_value else None,
            cls=cn("mt-2 outline-none overflow-x-auto", cls),
            **kwargs,
        )

    return _
