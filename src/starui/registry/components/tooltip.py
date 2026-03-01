from typing import Any, Literal

from starhtml import FT, Div, Signal, clear_timeout, reset_timeout
from starhtml.datastar import evt

from .utils import cn, gen_id, inject_context


def Tooltip(
    *children,
    signal: str | Signal = "",
    cls: str = "",
    **kwargs: Any,
) -> FT:
    sig = getattr(signal, "_id", signal) or gen_id("tooltip")
    open_state = Signal(f"{sig}_open", False)
    timer_state = Signal(f"{sig}_timer", 0)
    ctx = {"sig": sig, "open_state": open_state, "timer_state": timer_state}

    return Div(
        open_state,
        timer_state,
        *[inject_context(child, **ctx) for child in children],
        data_slot="tooltip",
        cls=cn("relative inline-block", cls),
        **kwargs,
    )


def TooltipTrigger(
    *children: Any,
    delay_duration: int = 700,
    hide_delay: int = 0,
    cls: str = "",
    **kwargs: Any,
):
    def trigger(*, sig, open_state, timer_state, **_):
        trigger_ref = Signal(f"{sig}_trigger", _ref_only=True)

        open_expr = reset_timeout(timer_state, delay_duration, open_state.set(True))
        close_expr = clear_timeout(timer_state, open_state.set(False))
        focus_open_expr = clear_timeout(timer_state, open_state.set(True))

        return Div(
            *children,
            data_ref=trigger_ref,
            data_on_mouseenter=open_expr,
            data_on_mouseleave=reset_timeout(
                timer_state, hide_delay, open_state.set(False)
            )
            if hide_delay > 0
            else close_expr,
            data_on_focusin=focus_open_expr,
            data_on_focusout=close_expr,
            data_on_keydown=(
                (evt.key == "Escape") | (evt.key == " ") | (evt.key == "Enter")
            ).then(close_expr),
            aria_describedby=f"{sig}_content",
            id=trigger_ref._id,
            data_slot="tooltip-trigger",
            cls=cn("inline-block outline-none", cls),
            **kwargs,
        )

    return trigger


def TooltipContent(
    *children: Any,
    side: Literal["top", "right", "bottom", "left"] = "top",
    align: Literal["start", "center", "end"] = "center",
    side_offset: int = 0,
    allow_flip: bool = True,
    strategy: Literal["fixed", "absolute"] = "fixed",
    container: Literal["auto", "none", "parent"] = "auto",
    cls: str = "",
    **kwargs: Any,
):
    def content(*, sig, open_state, **_):
        content_ref = Signal(f"{sig}_content", _ref_only=True)
        placement = side if align == "center" else f"{side}-{align}"

        arrow_classes = {
            "top": "bottom-0 left-1/2 -translate-x-1/2 translate-y-[calc(50%-2px)]",
            "bottom": "top-0 left-1/2 -translate-x-1/2 -translate-y-[calc(50%-2px)]",
            "left": "right-0 top-1/2 -translate-y-1/2 translate-x-[calc(50%-2px)]",
            "right": "left-0 top-1/2 -translate-y-1/2 -translate-x-[calc(50%-2px)]",
        }

        return Div(
            *children,
            Div(
                cls=cn(
                    "absolute size-2.5 rotate-45 rounded-[2px] z-50 bg-foreground",
                    arrow_classes[side],
                )
            ),
            data_ref=content_ref,
            data_show=open_state,
            style="display: none",
            data_position=(
                f"{sig}_trigger",
                {
                    "placement": placement,
                    "offset": side_offset,
                    "flip": allow_flip,
                    "shift": True,
                    "hide": True,
                    "strategy": strategy,
                    "container": container,
                },
            ),
            data_attr_data_state=open_state.if_("open", "closed"),
            id=content_ref._id,
            role="tooltip",
            data_side=side,
            data_slot="tooltip-content",
            cls=cn(
                "fixed z-50 w-fit max-w-xs rounded-md px-3 py-1.5",
                "bg-foreground text-background text-xs text-pretty",
                "pointer-events-none",
                "animate-in fade-in-0 zoom-in-95",
                "data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=closed]:zoom-out-95",
                "data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2",
                "data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2",
                cls,
            ),
            **kwargs,
        )

    return content


def TooltipProvider(*children, **kwargs: Any) -> FT:
    return Div(*children, data_slot="tooltip-provider", **kwargs)
