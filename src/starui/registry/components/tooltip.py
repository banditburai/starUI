from collections.abc import Callable
from typing import Any, Literal

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

from .utils import cn, ensure_signal


def Tooltip(
    *children: FT | Callable[[str], FT],
    signal: str | None = None,
    cls: str = "relative inline-block",
    **kwargs: Any,
) -> FT:
    signal = ensure_signal(signal, "tooltip")
    return Div(
        *[child(signal) if callable(child) else child for child in children],
        ds_signals({f"{signal}_open": False}),
        data_slot="tooltip",
        cls=cls,
        **kwargs,
    )


def TooltipTrigger(
    *children: FT,
    delay_duration: int = 700,
    hide_delay: int = 0,
    cls: str = "",
    **kwargs: Any,
) -> Callable[[str], FT]:
    def _(signal: str) -> FT:
        timer = f"_tt_{signal}_timer"
        return Div(
            *children,
            ds_ref(f"{signal}_trigger"),
            ds_on_mouseenter(
                f"clearTimeout({timer}); {timer} = setTimeout(() => ${signal}_open = true, {delay_duration})"
            ),
            ds_on_mouseleave(
                f"clearTimeout({timer}); {timer} = setTimeout(() => ${signal}_open = false, {hide_delay})"
                if hide_delay > 0
                else f"clearTimeout({timer}); ${signal}_open = false"
            ),
            ds_on_focus(
                f"clearTimeout({timer}); {timer} = setTimeout(() => ${signal}_open = true, {delay_duration})"
            ),
            ds_on_blur(f"clearTimeout({timer}); ${signal}_open = false"),
            ds_on_keydown(
                f"event.key === 'Escape' && (clearTimeout({timer}), ${signal}_open = false)"
            ),
            id=f"{signal}_trigger",
            tabindex="0",
            aria_describedby=f"{signal}_content",
            aria_expanded=f"${signal}_open",
            data_slot="tooltip-trigger",
            cls=cn("inline-block outline-none", cls),
            **kwargs,
        )

    return _


def TooltipContent(
    *children: FT,
    side: Literal["top", "right", "bottom", "left"] = "top",
    align: Literal["start", "center", "end"] = "center",
    side_offset: int = 8,
    allow_flip: bool = True,
    cls: str = "",
    **kwargs: Any,
) -> Callable[[str], FT]:
    def _(signal: str) -> FT:
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
            ds_ref(f"{signal}_content"),
            ds_show(f"${signal}_open"),
            ds_position(
                anchor=f"{signal}_trigger",
                placement=placement,
                offset=side_offset,
                flip=allow_flip,
                shift=True,
                hide=True,
                strategy="fixed",
            ),
            id=f"{signal}_content",
            role="tooltip",
            data_state=f"${signal}_open ? 'open' : 'closed'",
            data_side=side,
            data_slot="tooltip-content",
            cls=cn(
                "fixed z-50 w-fit rounded-md px-3 py-1.5",
                "bg-primary text-primary-foreground text-xs text-balance",
                "pointer-events-none",
                "animate-in fade-in-0 zoom-in-95",
                "data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=closed]:zoom-out-95",
                "data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2",
                "data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2",
                cls,
            ),
            **kwargs,
        )

    return _


def TooltipProvider(*children, **kwargs: Any) -> FT:
    return Div(*children, **kwargs)
