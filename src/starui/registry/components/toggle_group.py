from typing import Any, Literal
from uuid import uuid4

from starhtml import FT, Div
from starhtml import Button as HTMLButton
from starhtml.datastar import ds_on_click, ds_signals, value

from .toggle import toggle_variants
from .utils import cn

ToggleGroupType = Literal["single", "multiple"]
ToggleGroupVariant = Literal["default", "outline"]
ToggleGroupSize = Literal["default", "sm", "lg"]


def ToggleGroup(
    *children: Any,
    type: ToggleGroupType = "single",
    signal: str = "",
    variant: ToggleGroupVariant = "default",
    size: ToggleGroupSize = "default",
    disabled: bool = False,
    class_name: str = "",
    cls: str = "",
    **kwargs: Any,
) -> FT:
    signal = signal or f"toggle_group_{str(uuid4())[:8]}"
    value_signal = f"{signal}_value"

    initial_value = value("") if type == "single" else value([])

    processed_children = []
    for i, child in enumerate(children):
        if isinstance(child, tuple) and len(child) == 2:
            item_value, item_content = child
        else:
            item_value = str(i)
            item_content = child

        processed_children.append(
            ToggleGroupItem(
                item_content,
                value=item_value,
                group_signal=signal,
                type=type,
                variant=variant,
                size=size,
                disabled=disabled,
            )
        )

    return Div(
        *processed_children,
        ds_signals(**{value_signal: initial_value}),
        data_slot="toggle-group",
        data_variant=variant,
        data_size=size,
        data_type=type,
        role="radiogroup" if type == "single" else "group",
        aria_orientation="horizontal",
        cls=cn(
            "group/toggle-group flex w-fit items-center rounded-md",
            "data-[variant=outline]:shadow-xs" if variant == "outline" else "",
            class_name,
            cls,
        ),
        **kwargs,
    )


def ToggleGroupItem(
    *children: Any,
    value: str,
    group_signal: str,
    type: ToggleGroupType = "single",
    variant: ToggleGroupVariant = "default",
    size: ToggleGroupSize = "default",
    disabled: bool = False,
    aria_label: str | None = None,
    class_name: str = "",
    cls: str = "",
    **kwargs: Any,
) -> FT:
    value_signal = f"{group_signal}_value"
    item_id = kwargs.pop("id", f"toggle_item_{str(uuid4())[:8]}")
    aria_label = aria_label or kwargs.pop("aria_label", None)

    if type == "single":
        is_selected = f"${value_signal} === '{value}'"
        click_handler = (
            f"${value_signal} = ${value_signal} === '{value}' ? '' : '{value}'"
        )
    else:
        is_selected = f"${value_signal}.includes('{value}')"
        click_handler = (
            f"${value_signal} = ${value_signal}.includes('{value}') ? "
            f"${value_signal}.filter(v => v !== '{value}') : "
            f"[...${value_signal}, '{value}']"
        )

    return HTMLButton(
        *children,
        ds_on_click(click_handler) if not disabled else None,
        type="button",
        role="radio" if type == "single" else "checkbox",
        id=item_id,
        disabled=disabled,
        aria_label=aria_label,
        aria_checked="false",
        data_slot="toggle-group-item",
        data_variant=variant,
        data_size=size,
        data_value=value,
        data_attr_aria_checked=f"({is_selected}) ? 'true' : 'false'",
        data_attr_data_state=f"({is_selected}) ? 'on' : 'off'",
        cls=cn(
            toggle_variants(variant=variant, size=size),
            "shrink-0 rounded-none shadow-none",
            "first:rounded-l-md last:rounded-r-md",
            "focus:z-10 focus-visible:z-10",
            "data-[variant=outline]:border-l-0 data-[variant=outline]:first:border-l"
            if variant == "outline"
            else "",
            class_name,
            cls,
        ),
        **kwargs,
    )


def SingleToggleGroup(
    *children: Any,
    signal: str = "",
    variant: ToggleGroupVariant = "default",
    size: ToggleGroupSize = "default",
    disabled: bool = False,
    class_name: str = "",
    cls: str = "",
    **kwargs: Any,
) -> FT:
    return ToggleGroup(
        *children,
        type="single",
        signal=signal,
        variant=variant,
        size=size,
        disabled=disabled,
        class_name=class_name,
        cls=cls,
        **kwargs,
    )


def MultipleToggleGroup(
    *children: Any,
    signal: str = "",
    variant: ToggleGroupVariant = "default",
    size: ToggleGroupSize = "default",
    disabled: bool = False,
    class_name: str = "",
    cls: str = "",
    **kwargs: Any,
) -> FT:
    return ToggleGroup(
        *children,
        type="multiple",
        signal=signal,
        variant=variant,
        size=size,
        disabled=disabled,
        class_name=class_name,
        cls=cls,
        **kwargs,
    )
