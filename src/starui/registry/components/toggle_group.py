from typing import Any, Literal

from starhtml import FT, Div, Signal
from starhtml import Button as HTMLButton

from .toggle import toggle_variants
from .utils import cn, gen_id, inject_context

ToggleGroupType = Literal["single", "multiple"]
ToggleGroupVariant = Literal["default", "outline"]
ToggleGroupSize = Literal["default", "sm", "lg"]


def ToggleGroup(
    *children: Any,
    type: ToggleGroupType = "single",
    signal: str | Signal = "",
    value: str | list[str] | None = None,
    variant: ToggleGroupVariant = "default",
    size: ToggleGroupSize = "default",
    disabled: bool = False,
    orientation: Literal["horizontal", "vertical"] = "horizontal",
    cls: str = "",
    **kwargs: Any,
) -> FT:
    sig = getattr(signal, "_id", signal) or gen_id("toggle_group")
    initial = value if value is not None else ("" if type == "single" else [])
    is_vertical = orientation == "vertical"
    ctx = {
        "type": type,
        "variant": variant,
        "size": size,
        "disabled": disabled,
        "orientation": orientation,
    }

    items = [
        ToggleGroupItem(child[1], value=child[0])
        if isinstance(child, tuple) and len(child) == 2
        else child
        for child in children
    ]

    return Div(
        (selected_state := Signal(sig, initial)),
        *[inject_context(item, selected=selected_state, **ctx) for item in items],
        data_slot="toggle-group",
        data_variant=variant,
        data_size=size,
        data_type=type,
        data_orientation=orientation,
        role="radiogroup" if type == "single" else "group",
        aria_orientation=orientation if type == "single" else None,
        cls=cn(
            "group/toggle-group flex w-fit rounded-md",
            "flex-col items-stretch" if is_vertical else "items-center",
            "data-[variant=outline]:shadow-xs" if variant == "outline" else "",
            cls,
        ),
        **kwargs,
    )


def ToggleGroupItem(
    *children: Any,
    value: str,
    aria_label: str | None = None,
    cls: str = "",
    **kwargs: Any,
):
    def _(*, selected, type, variant, size, disabled, orientation="horizontal", **_):
        item_id = kwargs.pop("id", gen_id("toggle_item"))
        is_vertical = orientation == "vertical"
        is_selected = (
            selected.eq(value) if type == "single" else selected.contains(value)
        )
        click_handler = (
            selected.toggle(value, "")
            if type == "single"
            else selected.toggle_in(value)
        )

        return HTMLButton(
            *children,
            data_on_click=click_handler if not disabled else None,
            type="button",
            role="radio" if type == "single" else "checkbox",
            id=item_id,
            disabled=disabled,
            aria_label=aria_label or value,
            data_attr_aria_checked=is_selected.if_("true", "false"),
            data_attr_data_state=is_selected.if_("on", "off"),
            data_slot="toggle-group-item",
            data_variant=variant,
            data_size=size,
            data_value=value,
            cls=cn(
                toggle_variants(variant=variant, size=size),
                "w-auto min-w-0 shrink-0 px-3 rounded-none shadow-none",
                "first:rounded-t-md last:rounded-b-md"
                if is_vertical
                else "first:rounded-l-md last:rounded-r-md",
                "focus:z-10 focus-visible:z-10",
                (
                    "data-[variant=outline]:border-t-0 data-[variant=outline]:first:border-t"
                    if is_vertical
                    else "data-[variant=outline]:border-l-0 data-[variant=outline]:first:border-l"
                )
                if variant == "outline"
                else "",
                cls,
            ),
        )

    return _
