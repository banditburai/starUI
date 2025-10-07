from typing import Any, Literal

from starhtml import Div, FT, Signal
from starhtml.datastar import evt

from .utils import cn, gen_id


def Tooltip(
    *children,
    signal: str | Signal = "",
    cls: str = "",
    **kwargs: Any,
) -> FT:
    sig = getattr(signal, 'id', signal) or gen_id("tooltip")
    open_state = Signal(f"{sig}_open", False)
    timer_state = Signal(f"{sig}_timer", 0)
    ctx = dict(sig=sig, open_state=open_state, timer_state=timer_state)

    return Div(
        open_state,
        timer_state,
        *[child(**ctx) if callable(child) else child for child in children],
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

        # Manual timer logic with setTimeout/clearTimeout
        mouseenter_expr = f"clearTimeout(${timer_state.id}); ${timer_state.id} = setTimeout(() => ${open_state.id} = true, {delay_duration})"

        if hide_delay > 0:
            mouseleave_expr = f"clearTimeout(${timer_state.id}); ${timer_state.id} = setTimeout(() => ${open_state.id} = false, {hide_delay})"
        else:
            mouseleave_expr = f"clearTimeout(${timer_state.id}); ${open_state.id} = false"

        focus_expr = f"clearTimeout(${timer_state.id}); ${timer_state.id} = setTimeout(() => ${open_state.id} = true, {delay_duration})"
        blur_expr = f"clearTimeout(${timer_state.id}); ${open_state.id} = false"
        keydown_expr = f"event.key === 'Escape' && (clearTimeout(${timer_state.id}), ${open_state.id} = false)"

        return Div(
            *children,
            data_ref=trigger_ref,
            data_on_mouseenter=mouseenter_expr,
            data_on_mouseleave=mouseleave_expr,
            data_on_focus=focus_expr,
            data_on_blur=blur_expr,
            data_on_keydown=keydown_expr,
            data_attr_aria_expanded=open_state,
            aria_describedby=f"{sig}_content",
            id=trigger_ref.id,
            tabindex="0",
            data_slot="tooltip-trigger",
            cls=cn("inline-block outline-none", cls),
            **kwargs,
        )

    return trigger


def TooltipContent(
    *children: Any,
    side: Literal["top", "right", "bottom", "left"] = "top",
    align: Literal["start", "center", "end"] = "center",
    side_offset: int = 8,
    allow_flip: bool = True,
    strategy: Literal["fixed", "absolute"] = "absolute",
    container: Literal["auto", "none", "parent"] = "auto",
    cls: str = "",
    **kwargs: Any,
):
    def content(*, sig, open_state, timer_state, **_):
        content_ref = Signal(f"{sig}_content", _ref_only=True)
        placement = side if align == "center" else f"{side}-{align}"

        arrow_classes = {
            "top": "bottom-0 left-1/2 -translate-x-1/2 translate-y-1/2",
            "bottom": "top-0 left-1/2 -translate-x-1/2 -translate-y-1/2",
            "left": "right-0 top-1/2 -translate-y-1/2 translate-x-1/2",
            "right": "left-0 top-1/2 -translate-y-1/2 -translate-x-1/2",
        }

        return Div(
            *children,
            Div(cls=cn("absolute w-2 h-2 bg-primary rotate-45", arrow_classes[side])),
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
            data_attr_data_state=open_state.if_('open', 'closed'),
            id=content_ref.id,
            role="tooltip",
            data_side=side,
            data_slot="tooltip-content",
            cls=cn(
                "z-50 w-fit rounded-md px-3 py-1.5",
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

    return content


def TooltipProvider(*children, **kwargs: Any) -> FT:
    return Div(*children, **kwargs)
