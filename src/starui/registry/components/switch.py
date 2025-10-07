from typing import Any

from starhtml import FT, Div, Signal
from starhtml import Button as HTMLButton
from starhtml import Label as HTMLLabel
from starhtml import P as HTMLP
from starhtml import Span as HTMLSpan

from .utils import cn, gen_id


def Switch(
    checked: bool | None = None,
    signal: str | Signal | None = None,
    disabled: bool = False,
    required: bool = False,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    sig = getattr(signal, 'id', signal) or gen_id("switch")
    switch_id = kwargs.pop("id", sig)

    return Div(
        (checked_state := Signal(sig, checked or False)),
        HTMLButton(
            HTMLSpan(
                cls="pointer-events-none block size-4 rounded-full bg-background ring-0 transition-transform",
                data_attr_cls=checked_state.if_(
                    "translate-x-3.5 dark:bg-primary-foreground",
                    "translate-x-0 dark:bg-foreground"
                ),
                data_slot="switch-thumb",
            ),
            data_on_click=checked_state.toggle(),
            cls=cn(
                "peer inline-flex h-[1.15rem] w-8 shrink-0 items-center rounded-full",
                "border border-transparent shadow-xs transition-all outline-none",
                "focus-visible:ring-[3px] focus-visible:border-ring focus-visible:ring-ring/50",
                "disabled:cursor-not-allowed disabled:opacity-50",
                cls,
            ),
            data_attr_cls=checked_state.if_("bg-primary", "bg-input"),
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
    *attrs: Any,
    label: str,
    checked: bool | None = None,
    signal: str | Signal | None = None,
    helper_text: str | None = None,
    error_text: str | None = None,
    disabled: bool = False,
    required: bool = False,
    cls: str = "",
    label_cls: str = "",
    switch_cls: str = "",
    **kwargs: Any,
) -> FT:
    sig = getattr(signal, 'id', signal) or gen_id("switch")
    switch_id = kwargs.pop("id", sig)

    return Div(
        Div(
            HTMLLabel(
                label,
                HTMLSpan(" *", cls="text-destructive") if required else None,
                fr=switch_id,
                cls=cn(
                    "text-sm font-medium",
                    "cursor-pointer" if not disabled else "cursor-not-allowed opacity-50",
                    label_cls,
                ),
            ),
            Switch(
                checked=checked,
                signal=signal,
                disabled=disabled,
                required=required,
                cls=switch_cls,
                aria_invalid="true" if error_text else None,
                id=switch_id,
            ),
            cls="flex items-center gap-3",
        ),
        HTMLP(error_text, cls="text-sm text-destructive mt-1.5") if error_text else None,
        HTMLP(helper_text, cls="text-sm text-muted-foreground mt-1.5") if helper_text and not error_text else None,
        cls=cn("space-y-1.5", cls),
        *attrs,
        **kwargs,
    )
