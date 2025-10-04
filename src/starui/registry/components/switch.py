from typing import Any

from starhtml import FT, Div
from starhtml import Button as HTMLButton
from starhtml import Label as HTMLLabel
from starhtml import P as HTMLP
from starhtml import Span as HTMLSpan
from starhtml.datastar import ds_on_click, ds_signals, toggle_signal, toggle_class, t

from .utils import cn, gen_id, ensure_signal


def Switch(
    *children,
    checked: bool | None = None,
    signal: str | None = None,
    disabled: bool = False,
    required: bool = False,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    
    sig = signal or gen_id("switch")
    switch_id = kwargs.pop("id", gen_id("switch"))

    return Div(
        HTMLButton(
            *children,
            HTMLSpan(
                toggle_class(
                    signal,
                    "translate-x-3.5 dark:bg-primary-foreground",
                    "translate-x-0 dark:bg-white",
                    base="pointer-events-none block size-4 rounded-full bg-white ring-0 transition-transform"
                ),
                data_slot="switch-thumb",
            ),
            ds_on_click(toggle_signal(signal)),
            toggle_class(
                signal,
                "bg-primary",
                "bg-input",
                base=cn(
                    "peer inline-flex h-[1.15rem] w-8 shrink-0 items-center rounded-full",
                    "border border-transparent shadow-xs transition-all outline-none",
                    "focus-visible:ring-[3px] focus-visible:border-ring focus-visible:ring-ring/50",
                    "disabled:cursor-not-allowed disabled:opacity-50",
                    cls,
                )
            ),
            type="button",
            role="switch",
            id=switch_id,
            disabled=disabled,
            aria_checked=t(signal),
            aria_required="true" if required else None,
            data_slot="switch",
            **kwargs,
        ),
        ds_signals(**{signal: checked or False}),
    )


def SwitchWithLabel(
    *attrs: Any,
    label: str,
    checked: bool | None = None,
    signal: str | None = None,
    id: str | None = None,
    helper_text: str | None = None,
    error_text: str | None = None,
    disabled: bool = False,
    required: bool = False,
    cls: str = "",
    label_cls: str = "",
    switch_cls: str = "",
    **kwargs: Any,
) -> FT:
    sig = signal or gen_id("switch")
    switch_id = id or gen_id("switch")

    return Div(
        Div(
            HTMLLabel(
                label,
                required and HTMLSpan(" *", cls="text-destructive") or None,
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
                cls=switch_cls,
                aria_invalid="true" if error_text else None,
                id=switch_id,
            ),
            cls="flex items-center gap-3",
        ),
        error_text and HTMLP(error_text, cls="text-sm text-destructive mt-1.5") or None,
        helper_text
        and not error_text
        and HTMLP(helper_text, cls="text-sm text-muted-foreground mt-1.5")
        or None,
        cls=cn("space-y-1.5", cls),
        *attrs,
        **kwargs,
    )
