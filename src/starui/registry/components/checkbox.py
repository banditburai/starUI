from starhtml import FT, Div, Icon, Signal
from starhtml import Input as HTMLInput
from starhtml import Label as HTMLLabel
from starhtml import P as HTMLP
from starhtml import Span as HTMLSpan

from .utils import cn, gen_id


def Checkbox(
    checked: bool | None = None,
    name: str | None = None,
    value: str | None = None,
    signal: str | Signal = "",
    indeterminate: bool = False,
    disabled: bool = False,
    required: bool = False,
    cls: str = "",
    indicator_cls: str = "",
    **kwargs,
) -> FT:
    sig = getattr(signal, "_id", signal) or gen_id("checkbox")
    initial = "indeterminate" if indeterminate else (checked or False)

    return Div(
        (checked_state := Signal(sig, initial)),
        HTMLInput(
            data_bind=checked_state,
            type="checkbox",
            name=name,
            value=value or "on",
            disabled=disabled,
            required=required,
            data_slot="checkbox",
            data_state="indeterminate"
            if indeterminate
            else checked_state.if_("checked", "unchecked"),
            cls=cn(
                "peer appearance-none size-4 shrink-0 rounded-[4px] border shadow-xs transition-shadow outline-none",
                "border-input dark:bg-input/30",
                "checked:bg-primary checked:border-primary dark:checked:bg-primary dark:checked:border-primary",
                "focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:ring-[3px]",
                "aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40 aria-invalid:border-destructive aria-invalid:checked:border-destructive",
                "disabled:cursor-not-allowed disabled:opacity-50",
                cls,
            ),
            **kwargs,
        ),
        HTMLSpan(
            Icon("lucide:minus" if indeterminate else "lucide:check", size=14),
            data_attr_style="'opacity: 1'"
            if indeterminate
            else checked_state.if_("opacity: 1", "opacity: 0"),
            data_slot="checkbox-indicator",
            cls=cn(
                "absolute inset-0 grid place-content-center text-primary-foreground transition-none pointer-events-none",
                indicator_cls,
            ),
        ),
        cls="relative inline-grid size-4",
    )


def CheckboxWithLabel(
    *attrs,
    label: str,
    checked: bool | None = None,
    name: str | None = None,
    value: str | None = None,
    signal: str | Signal = "",
    indeterminate: bool = False,
    helper_text: str | None = None,
    error_text: str | None = None,
    disabled: bool = False,
    required: bool = False,
    cls: str = "",
    label_cls: str = "",
    checkbox_cls: str = "",
    indicator_cls: str = "",
    **kwargs,
) -> FT:
    sig = getattr(signal, "_id", signal) or gen_id("checkbox")
    checkbox_id = kwargs.pop("id", None) or sig

    return Div(
        Div(
            Checkbox(
                checked=checked,
                name=name,
                value=value,
                signal=sig,
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
                    fr=checkbox_id,
                    cls=cn(
                        "flex items-center gap-2 text-sm leading-none font-medium select-none",
                        "peer-disabled:cursor-not-allowed peer-disabled:opacity-70",
                        label_cls,
                    ),
                    data_slot="label",
                ),
                HTMLP(
                    helper_text,
                    cls=cn("text-muted-foreground text-sm", disabled and "opacity-70"),
                )
                if helper_text
                else None,
                cls="grid gap-1.5",
            ),
            cls="flex items-start gap-3",
        ),
        HTMLP(error_text, cls="text-sm text-destructive mt-1.5")
        if error_text
        else None,
        *attrs,
        cls=cls,
        **kwargs,
    )
