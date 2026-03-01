from typing import Any, Literal

from starhtml import FT, Div, Signal
from starhtml import Input as HTMLInput
from starhtml import Label as HTMLLabel
from starhtml import P as HTMLP
from starhtml import Span as HTMLSpan

from .utils import cn, gen_id, inject_context


def RadioGroup(
    *children: Any,
    value: str = "",
    signal: str | Signal = "",
    name: str = "",
    required: bool = False,
    hide_indicators: bool = False,
    aria_label: str = "",
    cls: str = "",
    **kwargs: Any,
) -> FT:
    sig = getattr(signal, "_id", signal) or gen_id("radio")
    group_name = name or f"radio_group_{sig}"
    selected = Signal(sig, value)

    ctx = {
        "sig": sig,
        "selected": selected,
        "group_name": group_name,
        "hide_indicators": hide_indicators,
        "initial_value": value,
    }

    return Div(
        selected,
        *[inject_context(child, **ctx) for child in children],
        cls=cn("grid gap-2", cls),
        data_slot="radio-group",
        role="radiogroup",
        aria_label=aria_label or None,
        aria_required="true" if required else None,
        **kwargs,
    )


def RadioGroupItem(
    value: str,
    label: str = "",
    disabled: bool = False,
    cls: str = "",
    indicator_cls: str = "",
    **kwargs: Any,
):
    def item(*, sig, selected, group_name, hide_indicators, initial_value="", **_):
        radio_id = gen_id("radio")
        is_checked = selected.eq(value)

        radio_input = HTMLInput(
            data_on_change=selected.set(value),
            type="radio",
            id=radio_id,
            value=value,
            name=group_name,
            checked=(value == initial_value) or None,
            disabled=disabled,
            data_attr_data_state=is_checked.if_("checked", "unchecked"),
            data_disabled="" if disabled else None,
            data_slot="radio-input",
            cls="sr-only peer",
            **kwargs,
        )

        if hide_indicators:
            return (
                HTMLLabel(
                    radio_input,
                    HTMLSpan(label, cls="block w-full"),
                    fr=radio_id,
                    cls="block w-full cursor-pointer",
                    data_slot="radio-container",
                )
                if label
                else Div(
                    radio_input,
                    cls="relative inline-flex items-center",
                    data_slot="radio-container",
                )
            )

        visual_radio = Div(
            Div(
                cls="absolute -inset-px rounded-full bg-primary",
                style="opacity: 0; transition: opacity 0.15s",
                data_style_opacity=is_checked.if_("1", "0"),
            ),
            Div(
                Div(cls="size-2 rounded-full bg-primary-foreground"),
                cls=cn(
                    "absolute inset-0 flex items-center justify-center pointer-events-none",
                    indicator_cls,
                ),
                style="opacity: 0; transition: opacity 0.15s",
                data_style_opacity=is_checked.if_("1", "0"),
                data_slot="radio-group-indicator",
            ),
            cls=cn(
                "relative flex aspect-square size-4 shrink-0 rounded-full border outline-none",
                "border-input bg-background dark:bg-input/30",
                "peer-focus-visible:border-ring peer-focus-visible:ring-ring/50 peer-focus-visible:ring-3",
                "peer-aria-[invalid]:ring-destructive/20 dark:peer-aria-[invalid]:ring-destructive/40",
                "dark:peer-aria-[invalid]:border-destructive/50 peer-aria-[invalid]:border-destructive peer-aria-[invalid]:ring-3",
                "peer-disabled:cursor-not-allowed peer-disabled:opacity-50",
                cls,
            ),
            data_slot="radio-group-item",
        )

        if not label:
            return Div(
                radio_input,
                visual_radio,
                cls="relative inline-flex items-center",
                data_slot="radio-container",
            )

        return HTMLLabel(
            radio_input,
            visual_radio,
            HTMLSpan(
                label,
                cls="text-sm font-medium leading-none select-none peer-disabled:cursor-not-allowed peer-disabled:opacity-50",
            ),
            fr=radio_id,
            cls="flex items-center gap-3 cursor-pointer",
            data_slot="radio-container",
        )

    return item


def RadioGroupWithLabel(
    *attrs: Any,
    label: str,
    options: list[dict[str, Any]],
    value: str = "",
    signal: str | Signal = "",
    name: str = "",
    id: str = "",
    helper_text: str = "",
    error_text: str = "",
    disabled: bool = False,
    required: bool = False,
    hide_indicators: bool = False,
    orientation: Literal["vertical", "horizontal"] = "vertical",
    cls: str = "",
    **kwargs: Any,
) -> FT:
    sig = getattr(signal, "_id", signal) or gen_id("radio")
    group_name = name or f"radio_group_{sig}"
    group_id = id or gen_id("radiogroup")

    return Div(
        HTMLLabel(
            label,
            HTMLSpan(" *", cls="text-destructive") if required else None,
            cls="text-sm font-medium mb-3 block",
            fr=group_id,
        ),
        RadioGroup(
            *[
                RadioGroupItem(
                    value=option["value"],
                    label=option.get("label", ""),
                    disabled=disabled or option.get("disabled", False),
                )
                for option in options
            ],
            *attrs,
            value=value,
            signal=sig,
            name=group_name,
            required=required,
            hide_indicators=hide_indicators,
            cls=cn(
                "flex gap-2",
                "flex-col" if orientation == "vertical" else "flex-row gap-6",
            ),
            id=group_id,
            aria_invalid="true" if error_text else None,
            **kwargs,
        ),
        HTMLP(error_text, cls="text-sm text-destructive mt-1.5")
        if error_text
        else None,
        HTMLP(helper_text, cls="text-sm text-muted-foreground mt-1.5")
        if helper_text and not error_text
        else None,
        cls=cn("space-y-1.5", cls),
    )
