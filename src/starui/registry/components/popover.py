from typing import Literal

from starhtml import FT, Div, Signal

from .utils import cn, gen_id, inject_context


def Popover(
    *children,
    signal: str | Signal = "",
    cls: str = "",
    **kwargs,
) -> FT:
    sig = getattr(signal, "_id", signal) or gen_id("popover")
    ctx = {"sig": sig}

    return Div(
        *[inject_context(child, **ctx) for child in children],
        data_slot="popover",
        cls=cn("relative inline-block", cls),
        **kwargs,
    )


def PopoverTrigger(
    *children,
    variant: str = "default",
    cls: str = "",
    **kwargs,
):
    def trigger(*, sig, **_):
        from .button import Button

        trigger_ref = Signal(f"{sig}_trigger", _ref_only=True)

        return Button(
            *children,
            data_ref=trigger_ref,
            id=trigger_ref._id,
            popovertarget=f"{sig}_content",
            popoveraction="toggle",
            variant=variant,
            data_slot="popover-trigger",
            cls=cls,
            **kwargs,
        )

    return trigger


def PopoverContent(
    *children,
    cls: str = "",
    side: Literal["top", "right", "bottom", "left"] = "bottom",
    align: Literal["start", "center", "end"] = "center",
    offset: int | None = None,
    container: Literal["auto", "none", "parent"] = "auto",
    aria_label: str | None = None,
    **kwargs,
):
    def content(*, sig, **ctx):
        content_ref = Signal(f"{sig}_content", _ref_only=True)
        placement = side if align == "center" else f"{side}-{align}"

        position_mods = {
            "placement": placement,
            "flip": True,
            "shift": True,
            "hide": True,
            "container": container,
        }
        if offset is not None:
            position_mods["offset"] = offset

        return Div(
            *[inject_context(child, sig=sig, **ctx) for child in children],
            data_ref=content_ref,
            data_position=(f"{sig}_trigger", position_mods),
            popover="auto",
            id=content_ref._id,
            role="dialog",
            aria_label=aria_label,
            tabindex="-1",
            data_slot="popover-content",
            cls=cn(
                "z-50 rounded-md border bg-popover text-popover-foreground shadow-md outline-none",
                "w-72 p-4",
                cls,
            ),
            **kwargs,
        )

    return content


def PopoverClose(
    *children,
    cls: str = "",
    variant: str = "ghost",
    size: str = "sm",
    **kwargs,
):
    def close(*, sig, **_):
        from .button import Button

        return Button(
            *children,
            popovertarget=f"{sig}_content",
            popoveraction="hide",
            variant=variant,
            size=size,
            data_slot="popover-close",
            cls=cn("absolute right-2 top-2", cls),
            aria_label="Close popover",
            **kwargs,
        )

    return close
