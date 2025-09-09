from typing import Literal

from starhtml import FT, Div
from starhtml.datastar import (
    ds_on_mouseenter,
    ds_on_mouseleave,
    ds_position,
    ds_ref,
    ds_show,
    ds_signals,
)

from .utils import cn


def HoverCard(
    *children,
    signal: str = "hover_card",
    default_open: bool = False,
    class_name: str = "",
    cls: str = "",
    **kwargs,
) -> FT:
    return Div(
        *children,
        ds_signals({f"{signal}_open": default_open}),
        data_slot="hover-card",
        cls=cn("relative inline-block", class_name, cls),
        **kwargs,
    )


def HoverCardTrigger(
    *children,
    signal: str = "hover_card",
    hover_delay: int = 700,
    hide_delay: int = 300,
    class_name: str = "",
    cls: str = "",
    **kwargs,
) -> FT:
    timer_var = f"window._hc_timer_{signal}"
    open_signal = f"${signal}_open"
    
    return Div(
        *children,
        ds_ref(f"{signal}_trigger"),
        ds_on_mouseenter(f"clearTimeout({timer_var});{timer_var}=setTimeout(()=>{open_signal}=true,{hover_delay})"),
        ds_on_mouseleave(f"clearTimeout({timer_var});{timer_var}=setTimeout(()=>{open_signal}=false,{hide_delay})"),
        aria_expanded=open_signal,
        aria_haspopup="dialog",
        aria_describedby=f"{signal}_content",
        data_slot="hover-card-trigger",
        id=f"{signal}_trigger",
        cls=cn("inline-block cursor-pointer", class_name, cls),
        **kwargs,
    )


def HoverCardContent(
    *children,
    signal: str = "hover_card",
    side: Literal["top", "right", "bottom", "left"] = "bottom",
    align: Literal["start", "center", "end"] = "center",
    hide_delay: int = 300,
    class_name: str = "",
    cls: str = "",
    **kwargs,
) -> FT:
    placement = f"{side}-{align}" if align != "center" else side
    timer_var = f"window._hc_timer_{signal}"
    open_signal = f"${signal}_open"
    
    return Div(
        *children,
        ds_ref(f"{signal}_content"),
        ds_show(open_signal),
        ds_position(
            anchor=f"{signal}_trigger",
            placement=placement,
            offset=8,
            flip=True,
            shift=True,
            hide=True,
            strategy="fixed",
        ),
        ds_on_mouseenter(f"clearTimeout({timer_var});{open_signal}=true"),
        ds_on_mouseleave(f"clearTimeout({timer_var});{timer_var}=setTimeout(()=>{open_signal}=false,{hide_delay})"),
        id=f"{signal}_content",
        role="dialog",
        aria_labelledby=f"{signal}_trigger",
        tabindex="-1",
        data_slot="hover-card-content",
        cls=cn(
            "fixed z-50 w-72 max-w-[90vw] pointer-events-auto",
            "rounded-md border bg-popover p-4 text-popover-foreground shadow-md outline-none",
            "overflow-hidden",
            class_name,
            cls,
        ),
        **kwargs,
    )
