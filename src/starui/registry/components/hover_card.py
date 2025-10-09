from typing import Any, Literal

from starhtml import Div, FT, Signal

from .utils import cn, gen_id, reset_timeout, clear_timeout


def HoverCard(
    *children,
    signal: str | Signal = "",
    default_open: bool = False,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    sig = getattr(signal, 'id', signal) or gen_id("hover_card")
    open_state = Signal(f"{sig}_open", default_open)
    timer_state = Signal(f"{sig}_timer", _ref_only=True)

    ctx = dict(sig=sig, open_state=open_state, timer_state=timer_state)

    return Div(
        open_state,
        *[child(**ctx) if callable(child) else child for child in children],
        data_slot="hover-card",
        cls=cn("relative inline-block", cls),
        **kwargs,
    )


def HoverCardTrigger(
    *children: Any,
    hover_delay: int = 700,
    hide_delay: int = 300,
    cls: str = "",
    **kwargs: Any,
):
    def trigger(*, sig, open_state, timer_state, **_):
        trigger_ref = Signal(f"{sig}_trigger", _ref_only=True)

        return Div(
            *children,
            data_ref=trigger_ref,
            data_on_mouseenter=reset_timeout(timer_state, hover_delay, open_state.set(True)),
            data_on_mouseleave=reset_timeout(timer_state, hide_delay, open_state.set(False)),
            data_attr_aria_expanded=open_state,
            aria_haspopup="dialog",
            aria_describedby=f"{sig}_content",
            data_slot="hover-card-trigger",
            id=trigger_ref.id,
            cls=cn("inline-block cursor-pointer", cls),
            **kwargs,
        )

    return trigger


def HoverCardContent(
    *children: Any,
    side: Literal["top", "right", "bottom", "left"] = "bottom",
    align: Literal["start", "center", "end"] = "center",
    hide_delay: int = 300,
    cls: str = "",
    **kwargs: Any,
):
    def content(*, sig, open_state, timer_state, **_):
        content_ref = Signal(f"{sig}_content", _ref_only=True)
        placement = side if align == "center" else f"{side}-{align}"

        return Div(
            *children,
            data_ref=content_ref,
            data_show=open_state,
            data_position=(
                f"{sig}_trigger",
                {
                    "placement": placement,
                    "offset": 8,
                    "flip": True,
                    "shift": True,
                    "hide": True,
                    "strategy": "fixed",
                },
            ),
            data_on_mouseenter=clear_timeout(timer_state, open_state.set(True)),
            data_on_mouseleave=reset_timeout(timer_state, hide_delay, open_state.set(False)),
            id=content_ref.id,
            role="dialog",
            aria_labelledby=f"{sig}_trigger",
            tabindex="-1",
            data_slot="hover-card-content",
            cls=cn(
                "fixed z-50 w-72 max-w-[90vw] pointer-events-auto",
                "rounded-md border bg-popover p-4 text-popover-foreground shadow-md outline-none overflow-hidden",
                cls,
            ),
            **kwargs,
        )

    return content