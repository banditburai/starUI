from typing import Any
from uuid import uuid4

from starhtml import FT, Div
from starhtml import Button as HTMLButton
from starhtml import Label as HTMLLabel
from starhtml import P as HTMLP
from starhtml import Span as HTMLSpan
from starhtml.datastar import ds_class, ds_on_click, ds_signals, t, toggle_signal, toggle_class

from .utils import cn


def Switch(
    *children,
    checked: bool | None = None,
    signal: str | None = None,
    disabled: bool = False,
    required: bool = False,
    class_name: str = "",
    cls: str = "",
    **kwargs: Any,
) -> FT:
    signal = signal or f"switch_{str(uuid4())[:8]}"
    switch_id = kwargs.pop("id", f"switch_{str(uuid4())[:8]}")

    return Div(
        HTMLButton(
            *children,
            HTMLSpan(
                toggle_class(
                    f"${signal}",
                    "translate-x-3.5 dark:bg-primary-foreground",
                    "translate-x-0 dark:bg-white"
                ),
                cls="pointer-events-none block size-4 rounded-full bg-white ring-0 transition-transform",
                data_slot="switch-thumb",
            ),
            ds_on_click(toggle_signal(signal)),
            toggle_class(
                f"${signal}",
                "bg-primary",
                "bg-input"
            ),
            type="button",
            role="switch",
            id=switch_id,
            disabled=disabled,
            aria_checked=t("{signal}"),
            aria_required="true" if required else None,
            data_slot="switch",
            cls=cn(
                "peer inline-flex h-[1.15rem] w-8 shrink-0 items-center rounded-full",
                "border border-transparent shadow-xs transition-all outline-none",
                "focus-visible:ring-[3px] focus-visible:border-ring focus-visible:ring-ring/50",
                "disabled:cursor-not-allowed disabled:opacity-50",
                class_name,
                cls,
            ),
            **kwargs,
        ),
        ds_signals(**{signal: checked or False}),
    )


def SwitchWithLabel(
    *attrs: Any,
    label: str,
    checked: bool | None = None,
    signal: str | None = None,
    helper_text: str | None = None,
    error_text: str | None = None,
    disabled: bool = False,
    required: bool = False,
    class_name: str = "",
    cls: str = "",
    label_cls: str = "",
    switch_cls: str = "",
    **kwargs: Any,
) -> FT:
    signal = signal or f"switch_{str(uuid4())[:8]}"
    switch_id = f"switch_{str(uuid4())[:8]}"

    return Div(
        Div(
            HTMLLabel(
                label,
                HTMLSpan(" *", cls="text-destructive") if required else None,
                for_=switch_id,
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
        cls=cn("space-y-1.5", class_name, cls),
        *attrs,
        **kwargs,
    )
