from collections.abc import Callable
from typing import Any, Literal
from uuid import uuid4

from starhtml import FT, Div
from starhtml.datastar import (
    ds_on_blur,
    ds_on_focus,
    ds_on_keydown,
    ds_on_mouseenter,
    ds_on_mouseleave,
    ds_position,
    ds_ref,
    ds_show,
    ds_signals,
)

from .utils import cn


def Tooltip(*children, cls: str = "relative inline-block", **kwargs: Any) -> FT:
    tooltip_id = f"tooltip_{uuid4().hex[:8]}"
    return Div(
        *[child(tooltip_id) if callable(child) else child for child in children],
        ds_signals({f"{tooltip_id}_open": False}),
        cls=cls,
        **kwargs,
    )


def TooltipTrigger(
    *children,
    delay_duration: int = 700,
    hide_delay: int = 0,
    class_name: str = "",
    cls: str = "",
    **kwargs: Any,
) -> Callable[[str], FT]:
    def _(tooltip_id: str) -> FT:
        return Div(
            *children,
            ds_ref(f"{tooltip_id}Trigger"),
            ds_on_mouseenter(
                f"clearTimeout(window.tooltipTimer_{tooltip_id}); window.tooltipTimer_{tooltip_id} = setTimeout(() => ${tooltip_id}_open = true, {delay_duration})"
            ),
            ds_on_mouseleave(
                f"clearTimeout(window.tooltipTimer_{tooltip_id}); window.tooltipTimer_{tooltip_id} = setTimeout(() => ${tooltip_id}_open = false, {hide_delay})"
                if hide_delay > 0
                else f"clearTimeout(window.tooltipTimer_{tooltip_id}); ${tooltip_id}_open = false"
            ),
            ds_on_focus(
                f"clearTimeout(window.tooltipTimer_{tooltip_id}); window.tooltipTimer_{tooltip_id} = setTimeout(() => ${tooltip_id}_open = true, {delay_duration})"
            ),
            ds_on_blur(
                f"clearTimeout(window.tooltipTimer_{tooltip_id}); ${tooltip_id}_open = false"
            ),
            ds_on_keydown(
                f"event.key === 'Escape' && (clearTimeout(window.tooltipTimer_{tooltip_id}), ${tooltip_id}_open = false)"
            ),
            id=f"{tooltip_id}-trigger",
            tabindex="0",
            aria_describedby=f"{tooltip_id}-content",
            aria_expanded=f"${tooltip_id}_open",
            cls=cn("inline-block outline-none", class_name, cls),
            **kwargs,
        )

    return _


def TooltipContent(
    *children,
    side: Literal["top", "right", "bottom", "left"] = "top",
    align: Literal["start", "center", "end"] = "center",
    side_offset: int = 8,
    allow_flip: bool = True,
    class_name: str = "",
    cls: str = "",
    **kwargs: Any,
) -> Callable[[str], FT]:
    def _(tooltip_id: str) -> FT:
        placement = f"{side}-{align}" if align != "center" else side
        arrow_classes = {
            "top": "bottom-0 left-1/2 -translate-x-1/2 translate-y-1/2",
            "bottom": "top-0 left-1/2 -translate-x-1/2 -translate-y-1/2",
            "left": "right-0 top-1/2 -translate-y-1/2 translate-x-1/2",
            "right": "left-0 top-1/2 -translate-y-1/2 -translate-x-1/2",
        }

        return Div(
            *children,
            Div(cls=cn("absolute w-2 h-2 bg-primary rotate-45", arrow_classes[side])),
            ds_ref(f"{tooltip_id}Content"),
            ds_show(f"${tooltip_id}_open"),
            ds_position(
                anchor=f"{tooltip_id}-trigger",
                placement=placement,
                offset=side_offset,
                flip=allow_flip,
                shift=True,
                hide=True,
            ),
            id=f"{tooltip_id}-content",
            role="tooltip",
            data_state=f"${tooltip_id}_open ? 'open' : 'closed'",
            data_side=side,
            cls=cn(
                "relative z-50 w-fit rounded-md px-3 py-1.5",
                "bg-primary text-primary-foreground text-xs text-balance",
                "pointer-events-none",
                "animate-in fade-in-0 zoom-in-95",
                "data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=closed]:zoom-out-95",
                "data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2",
                "data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2",
                class_name,
                cls,
            ),
            **kwargs,
        )

    return _


def TooltipProvider(*children, **kwargs: Any) -> FT:
    return Div(*children, **kwargs)
