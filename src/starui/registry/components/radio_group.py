from itertools import count
from typing import Any
from uuid import uuid4

from starhtml import FT, Div
from starhtml import Input as HTMLInput
from starhtml import Label as HTMLLabel
from starhtml import P as HTMLP
from starhtml import Span as HTMLSpan
from starhtml.datastar import ds_class, ds_on_change, ds_signals, value, toggle_class

from .utils import cn

_radio_group_ids = count(1)


def RadioGroup(
    *children: Any,
    initial_value: str | None = None,
    signal: str = "",
    disabled: bool = False,
    required: bool = False,
    hide_indicators: bool = False,
    class_name: str = "",
    cls: str = "",
    **kwargs: Any,
) -> FT:
    signal = signal or f"radio_{next(_radio_group_ids)}"
    group_name = f"radio_group_{signal}"

    processed_children = [
        child(signal, group_name, initial_value, hide_indicators) if callable(child) else child
        for child in children
    ]

    return Div(
        *processed_children,
        ds_signals({signal: value(initial_value or "")}),
        cls=cn(class_name, cls) or "grid gap-2",
        data_slot="radio-group",
        data_radio_signal=signal,
        data_radio_name=group_name,
        role="radiogroup",
        aria_required="true" if required else None,
        **kwargs,
    )


def RadioGroupItem(
    value: str,
    label: str | None = None,
    disabled: bool = False,
    class_name: str = "",
    cls: str = "",
    indicator_cls: str = "",
    **kwargs: Any,
) -> FT:
    def create_item(signal, group_name, default_value=None, hide_indicators=False):
        radio_id = f"radio_{str(uuid4())[:8]}"
        filtered_kwargs = {k: v for k, v in kwargs.items() if k != "name"}

        radio_input = HTMLInput(
            ds_on_change(f"${signal} = '{value}'"),
            type="radio",
            id=radio_id,
            value=value,
            name=group_name,
            disabled=disabled,
            data_slot="radio-input",
            cls="sr-only peer",
            **filtered_kwargs,
        )

        # Apply sr-only to hide the visual radio if hide_indicators is True
        visual_radio_cls = cn(
            "relative aspect-square size-4 shrink-0 rounded-full border transition-all",
            "border-input bg-background dark:bg-input/30",
            "peer-disabled:cursor-not-allowed peer-disabled:opacity-50",
            "sr-only" if hide_indicators else None,
            class_name,
            cls,
        )
        
        visual_radio = Div(
            Div(
                Div(cls="size-2 rounded-full bg-primary"),
                toggle_class(
                    f"${signal}",
                    **{value: "opacity-100", "_": "opacity-0"}
                ),
                cls=cn(
                    "absolute inset-0 flex items-center justify-center",
                    "sr-only" if hide_indicators else indicator_cls,
                ),
                data_slot="radio-indicator",
            ),
            cls=visual_radio_cls,
            data_slot="radio-visual",
        )

        if not label:
            return Div(
                radio_input,
                visual_radio if not hide_indicators else None,
                cls="relative inline-flex items-center",
                data_slot="radio-container",
            )

        # When hiding indicators, use block layout for full width cards
        label_cls = "flex items-center gap-2 cursor-pointer"
        span_cls = "text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-50"
        
        if hide_indicators:
            label_cls = "block w-full cursor-pointer"
            span_cls = "block w-full"
        
        return HTMLLabel(
            radio_input,
            visual_radio if not hide_indicators else None,
            HTMLSpan(
                label,
                cls=span_cls,
            ),
            for_=radio_id,
            cls=label_cls,
            data_slot="radio-container",
        )

    return create_item


def RadioGroupWithLabel(
    *,  # Force keyword-only arguments for consistency and flexibility
    label: str,
    options: list[dict[str, Any]],
    value: str | None = None,
    signal: str | None = None,
    name: str | None = None,
    helper_text: str | None = None,
    error_text: str | None = None,
    disabled: bool = False,
    required: bool = False,
    hide_indicators: bool = False,
    orientation: str = "vertical",
    class_name: str = "",
    cls: str = "",
    **kwargs: Any,
) -> FT:
    base_id = str(uuid4())[:8]
    signal = signal or f"radio_{base_id}"
    name = name or f"radio_group_{signal}"
    group_id = f"radiogroup_{base_id}"

    radio_group_classes = cn(
        "flex gap-2",
        "flex-col" if orientation == "vertical" else "flex-row gap-6",
    )

    return Div(
        label
        and HTMLLabel(
            label,
            required and HTMLSpan(" *", cls="text-destructive") or None,
            cls="text-sm font-medium mb-3 block",
            for_=group_id,
        )
        or None,
        RadioGroup(
            *[
                RadioGroupItem(
                    value=option["value"],
                    label=option.get("label"),
                    disabled=disabled or option.get("disabled", False),
                )
                for option in options
            ],
            initial_value=value,
            signal=signal,
            name=name,
            disabled=disabled,
            required=required,
            hide_indicators=hide_indicators,
            cls=radio_group_classes,
            id=group_id,
            aria_invalid="true" if error_text else None,
        ),
        error_text and HTMLP(error_text, cls="text-sm text-destructive mt-1.5") or None,
        helper_text
        and not error_text
        and HTMLP(helper_text, cls="text-sm text-muted-foreground mt-1.5")
        or None,
        cls=cn("space-y-1.5", class_name, cls),
        **kwargs,
    )
