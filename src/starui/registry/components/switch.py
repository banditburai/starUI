from typing import Literal

from starhtml import FT, Div, Signal
from starhtml import Button as HTMLButton
from starhtml import Label as HTMLLabel
from starhtml import P as HTMLP
from starhtml import Span as HTMLSpan

from .utils import cn, cva, gen_id, merge_actions

SwitchSize = Literal["default", "sm"]

switch_variants = cva(
    base=(
        "peer inline-flex shrink-0 items-center rounded-full "
        "border border-transparent shadow-xs transition-all outline-none "
        "focus-visible:ring-[3px] focus-visible:border-ring focus-visible:ring-ring/50 "
        "disabled:cursor-not-allowed disabled:opacity-50"
    ),
    config={
        "variants": {
            "size": {
                "default": "h-[1.15rem] w-8",
                "sm": "h-3.5 w-6",
            },
        },
        "defaultVariants": {"size": "default"},
    },
)

switch_thumb_variants = cva(
    base="pointer-events-none block rounded-full bg-background ring-0 transition-transform",
    config={
        "variants": {
            "size": {
                "default": "size-4",
                "sm": "size-3",
            },
        },
        "defaultVariants": {"size": "default"},
    },
)

# Thumb translate per size — dynamic Datastar binding can't go through CVA
_THUMB_TRANSLATE = {"default": "translate-x-3.5", "sm": "translate-x-2.5"}


def Switch(
    checked: bool | None = None,
    signal: str | Signal | None = None,
    disabled: bool = False,
    required: bool = False,
    size: SwitchSize = "default",
    cls: str = "",
    **kwargs,
) -> FT:
    sig = getattr(signal, "_id", signal) or gen_id("switch")
    switch_id = kwargs.pop("id", sig)

    checked_state = Signal(sig, checked or False)
    click_actions = merge_actions(checked_state.toggle(), kwargs=kwargs)
    translate = _THUMB_TRANSLATE[size]

    return Div(
        checked_state,
        HTMLButton(
            HTMLSpan(
                cls=switch_thumb_variants(size=size),
                data_attr_cls=checked_state.if_(
                    f"{translate} dark:bg-primary-foreground",
                    "translate-x-0 dark:bg-foreground",
                ),
                data_slot="switch-thumb",
            ),
            data_on_click=click_actions,
            cls=cn(switch_variants(size=size), cls),
            data_attr_cls=checked_state.if_("bg-primary", "bg-input dark:bg-input/80"),
            type="button",
            role="switch",
            id=switch_id,
            disabled=disabled,
            data_attr_aria_checked=checked_state.if_("true", "false"),
            aria_required="true" if required else None,
            data_slot="switch",
            **kwargs,
        ),
    )


def SwitchWithLabel(
    *attrs,
    label: str,
    checked: bool | None = None,
    signal: str | Signal | None = None,
    helper_text: str | None = None,
    error_text: str | None = None,
    disabled: bool = False,
    required: bool = False,
    size: SwitchSize = "default",
    cls: str = "",
    label_cls: str = "",
    switch_cls: str = "",
    **kwargs,
) -> FT:
    sig = getattr(signal, "_id", signal) or gen_id("switch")
    switch_id = kwargs.pop("id", sig)

    return Div(
        Div(
            HTMLLabel(
                label,
                HTMLSpan(" *", cls="text-destructive") if required else None,
                fr=switch_id,
                cls=cn(
                    "text-sm font-medium",
                    "cursor-pointer"
                    if not disabled
                    else "cursor-not-allowed opacity-50",
                    label_cls,
                ),
            ),
            Switch(
                checked=checked,
                signal=signal,
                disabled=disabled,
                required=required,
                size=size,
                cls=switch_cls,
                aria_invalid="true" if error_text else None,
                id=switch_id,
            ),
            cls="flex items-center gap-3",
        ),
        HTMLP(error_text, cls="text-sm text-destructive mt-1.5")
        if error_text
        else None,
        HTMLP(helper_text, cls="text-sm text-muted-foreground mt-1.5")
        if helper_text and not error_text
        else None,
        *attrs,
        cls=cn("space-y-1.5", cls),
        **kwargs,
    )
