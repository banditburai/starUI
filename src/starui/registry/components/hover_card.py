from typing import Any, Literal

from starhtml import Div, FT, Signal

from .utils import cn, gen_id


def HoverCard(
    *children,
    signal: str = "",
    default_open: bool = False,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    sig = signal or gen_id("hover_card")
    open_state = Signal(f"{sig}_open", default_open)

    ctx = dict(sig=sig, open_state=open_state)

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
    def trigger(*, sig, open_state, **_):
        trigger_id = f"{sig}_trigger"

        return Div(
            *children,
            data_ref=trigger_id,
            data_on_mouseenter=open_state.set(True).with_(debounce=hover_delay),
            data_on_mouseleave=open_state.set(False).with_(debounce=hide_delay),
            data_attr_aria_expanded=open_state,
            aria_haspopup="dialog",
            aria_describedby=f"{sig}_content",
            data_slot="hover-card-trigger",
            id=trigger_id,
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
    def content(*, sig, open_state, **_):
        trigger_id = f"{sig}_trigger"
        content_id = f"{sig}_content"
        placement = side if align == "center" else f"{side}-{align}"

        return Div(
            *children,
            data_ref=content_id,
            data_show=open_state,
            data_position=(
                trigger_id,
                {
                    "placement": placement,
                    "offset": 8,
                    "flip": True,
                    "shift": True,
                    "hide": True,
                    "strategy": "fixed",
                },
            ),
            data_on_mouseenter=open_state.set(True),
            data_on_mouseleave=open_state.set(False).with_(debounce=hide_delay),
            id=content_id,
            role="dialog",
            aria_labelledby=trigger_id,
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