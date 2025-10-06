from typing import Any, Literal
from uuid import uuid4

from starhtml import FT, Div, Signal
from starhtml import Button as HTMLButton

from .toggle import toggle_variants
from .utils import cn, gen_id

ToggleGroupType = Literal["single", "multiple"]
ToggleGroupVariant = Literal["default", "outline"]
ToggleGroupSize = Literal["default", "sm", "lg"]


def ToggleGroup(
    *children: Any,
    type: ToggleGroupType = "single",
    signal: str | Signal = "",
    default_value: str | list[str] | None = None,
    variant: ToggleGroupVariant = "default",
    size: ToggleGroupSize = "default",
    disabled: bool = False,
    orientation: Literal["horizontal", "vertical"] = "horizontal",
    cls: str = "",
    **kwargs: Any,
) -> FT:
    sig = getattr(signal, 'id', signal) or gen_id("toggle_group")
    initial = default_value if default_value is not None else ("" if type == "single" else [])
    selected = Signal(sig, initial)

    ctx = dict(selected=selected, type=type, variant=variant, size=size, disabled=disabled, initial=initial)

    processed_children = []
    for i, child in enumerate(children):
        if isinstance(child, tuple) and len(child) == 2:
            item_value, item_content = child
            processed_children.append(
                ToggleGroupItem(item_content, value=item_value)
            )
        else:
            # If not a tuple, assume it's already a component
            processed_children.append(child)

    return Div(
        selected,
        *[c(**ctx) if callable(c) else c for c in processed_children],
        data_slot="toggle-group",
        data_variant=variant,
        data_size=size,
        data_type=type,
        data_orientation=orientation,
        role="radiogroup" if type == "single" else "group",
        aria_orientation=orientation,
        cls=cn(
            "group/toggle-group flex w-fit items-center rounded-md",
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
    def _(*, selected, type, variant, size, disabled, initial, **_):
        from starhtml.datastar import js

        item_id = kwargs.pop("id", f"toggle_item_{str(uuid4())[:8]}")

        if type == "single":
            is_selected = selected.eq(value)
            click_handler = selected.set(is_selected.if_('', value))
        else:
            is_selected = selected.contains(value)
            # For arrays, we need to filter or append - requires raw JS for filter
            click_handler = js(
                f"{selected.to_js()} = {is_selected.to_js()} ? "
                f"{selected.to_js()}.filter(v => v !== '{value}') : "
                f"[...{selected.to_js()}, '{value}']"
            )

        is_initially_selected = initial == value if type == "single" else value in (initial or [])

        return HTMLButton(
            *children,
            data_on_click=click_handler if not disabled else None,
            type="button",
            role="radio" if type == "single" else "checkbox",
            id=item_id,
            disabled=disabled,
            aria_label=aria_label,
            aria_checked="true" if is_initially_selected else "false",
            data_slot="toggle-group-item",
            data_variant=variant,
            data_size=size,
            data_value=value,
            data_disabled="" if disabled else None,
            data_attr_aria_checked=is_selected.if_('true', 'false'),
            data_attr_data_state=is_selected.if_('on', 'off'),
            data_state="on" if is_initially_selected else "off",
            cls=cn(
                toggle_variants(variant=variant, size=size),
                "shrink-0 rounded-none shadow-none",
                "first:rounded-l-md last:rounded-r-md",
                "focus:z-10 focus-visible:z-10",
                "data-[variant=outline]:border-l-0 data-[variant=outline]:first:border-l"
                if variant == "outline"
                else "",
                cls,
            ),
        )

    return _