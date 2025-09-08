from typing import Literal
from uuid import uuid4

from starhtml import Div
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
    signal: str | None = None,
    default_open: bool = False,
    cls: str = "",
    **attrs,
):
    signal = signal or f"hover_card_{uuid4().hex[:8]}"
    return Div(
        *children,
        ds_signals({f"{signal}_open": default_open}),
        cls=cn("relative inline-block", cls),
        **attrs,
    )


def HoverCardTrigger(
    *children,
    signal: str | None = None,
    hover_delay: int = 700,
    hide_delay: int = 300,
    cls: str = "",
    **attrs,
):
    signal = signal or "hover_card"

    return Div(
        *children,
        ds_ref(f"{signal}Trigger"),
        ds_on_mouseenter(f"""
            clearTimeout(window.hoverTimer_{signal});
            window.hoverTimer_{signal} = setTimeout(() => {{
                ${signal}_open = true;
            }}, {hover_delay});
        """),
        ds_on_mouseleave(f"""
            clearTimeout(window.hoverTimer_{signal});
            window.hoverTimer_{signal} = setTimeout(() => {{
                ${signal}_open = false;
            }}, {hide_delay});
        """),
        aria_expanded=f"${signal}_open",
        aria_haspopup="dialog",
        aria_describedby=f"{signal}-content",
        cls=cn("inline-block cursor-pointer", cls),
        id=f"{signal}-trigger",
        **attrs,
    )


def HoverCardContent(
    *children,
    signal: str | None = None,
    side: Literal["top", "right", "bottom", "left"] = "bottom",
    align: Literal["start", "center", "end"] = "center",
    hide_delay: int = 300,
    cls: str = "",
    **attrs,
):
    signal = signal or "hover_card"
    placement = f"{side}-{align}" if align != "center" else side

    return Div(
        *children,
        ds_ref(f"{signal}Content"),
        ds_show(f"${signal}_open"),
        ds_position(
            anchor=f"{signal}-trigger",
            placement=placement,
            offset=8,
            flip=True,
            shift=True,
            hide=True,
            strategy="fixed",
        ),
        ds_on_mouseenter(
            f"clearTimeout(window.hoverTimer_{signal}); ${signal}_open = true;"
        ),
        ds_on_mouseleave(f"""
            clearTimeout(window.hoverTimer_{signal});
            window.hoverTimer_{signal} = setTimeout(() => {{
                ${signal}_open = false;
            }}, {hide_delay});
        """),
        id=f"{signal}-content",
        role="dialog",
        aria_labelledby=f"{signal}-trigger",
        tabindex="-1",
        cls=cn(
            "fixed z-50 w-72 max-w-[90vw] pointer-events-auto",
            "rounded-md border bg-popover p-4 text-popover-foreground shadow-md outline-none dark:border-input",
            "overflow-hidden",
            cls,
        ),
        **attrs,
    )
