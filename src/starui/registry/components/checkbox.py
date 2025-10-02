from typing import Any

from starhtml import FT, Div, Icon, Signal
from starhtml import Input as HTMLInput
from starhtml import Label as HTMLLabel
from starhtml import P as HTMLP
from starhtml import Span as HTMLSpan

from .utils import cn, gen_id, ensure_signal


def Checkbox(
    checked: bool | None = None,
    name: str | None = None,
    value: str | None = None,
    signal: str = "",
    indeterminate: bool = False,
    disabled: bool = False,
    required: bool = False,
    cls: str = "",
    indicator_cls: str = "",
    **kwargs: Any,
) -> FT:
    sig_name = ensure_signal(signal, "checkbox")
    initial = "indeterminate" if indeterminate else (checked or False)

    return Div(
        (sig := Signal(sig_name, initial)),
        HTMLInput(
            data_bind=sig_name,
            type="checkbox",
            name=name,
            value=value or "on",
            disabled=disabled,
            required=required,
            data_slot="checkbox",
            data_state="indeterminate" if indeterminate else sig.if_("checked", "unchecked"),
            cls=cn(
                "peer appearance-none size-4 shrink-0 rounded-[4px] border shadow-xs transition-all outline-none",
                "border-input bg-background dark:bg-input/30",
                "checked:bg-foreground checked:border-foreground",
                "dark:checked:bg-foreground dark:checked:border-foreground",
                "focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:ring-[3px]",
                "aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40",
                "aria-invalid:border-destructive aria-invalid:checked:border-destructive",
                "disabled:cursor-not-allowed disabled:opacity-50",
                cls,
            ),
            **kwargs,
        ),
        HTMLSpan(
            Icon("lucide:minus" if indeterminate else "lucide:check"),
            data_attr_style="opacity: 1" if indeterminate else sig.if_("opacity: 1", "opacity: 0"),
            data_slot="checkbox-indicator",
            cls=cn(
                "absolute inset-0 flex items-center justify-center text-background text-sm transition-opacity pointer-events-none",
                indicator_cls,
            ),
        ),
        cls="relative inline-block",
    )


def CheckboxWithLabel(
    *attrs: Any,
    label: str,
    checked: bool | None = None,
    name: str | None = None,
    value: str | None = None,
    signal: str = "",
    indeterminate: bool = False,
    helper_text: str | None = None,
    error_text: str | None = None,
    disabled: bool = False,
    required: bool = False,
    cls: str = "",
    label_cls: str = "",
    checkbox_cls: str = "",
    indicator_cls: str = "",
    **kwargs: Any,
) -> FT:
    sig_name = ensure_signal(signal, "checkbox")
    checkbox_id = kwargs.pop("id", None) or sig_name

    return Div(
        Div(
            Checkbox(
                checked=checked,
                name=name,
                value=value,
                signal=signal,
                indeterminate=indeterminate,
                disabled=disabled,
                required=required,
                id=checkbox_id,
                aria_invalid="true" if error_text else None,
                cls=checkbox_cls,
                indicator_cls=indicator_cls,
            ),
            Div(
                HTMLLabel(
                    label,
                    HTMLSpan(" *", cls="text-destructive") if required else None,
                    for_=checkbox_id,
                    cls=cn(
                        "flex items-center gap-2 text-sm leading-none font-medium select-none",
                        "peer-disabled:cursor-not-allowed peer-disabled:opacity-50",
                        "opacity-50 cursor-not-allowed" if disabled else "",
                        label_cls,
                    ),
                    data_slot="label",
                ),
                HTMLP(
                    helper_text,
                    cls=cn(
                        "text-muted-foreground text-sm",
                        "opacity-50" if disabled else "",
                    ),
                ) if helper_text else None,
                cls="grid gap-1.5" if helper_text else None,
            ),
            cls="flex items-start gap-3",
        ),
        HTMLP(error_text, cls="text-sm text-destructive mt-1.5") if error_text else None,
        cls=cls,
        *attrs,
        **kwargs,
    )
