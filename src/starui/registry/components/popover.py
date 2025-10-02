from typing import Callable, Literal

from starhtml import FT, Div

from .button import Button
from .utils import cn, ensure_signal


def Popover(
    *children: FT | Callable[[str], FT],
    signal: str | None = None,
    cls: str = "",
    **kwargs,
) -> FT:
    signal = ensure_signal(signal, "popover")
    return Div(
        *[child(signal) if callable(child) else child for child in children],
        data_slot="popover",
        cls=cn("relative inline-block", cls),
        **kwargs,
    )


def PopoverTrigger(
    *children: FT,
    variant: str = "default",
    cls: str = "",
    **kwargs,
) -> Callable[[str], FT]:
    def trigger(signal: str) -> FT:
        trigger_id = f"{signal}_trigger"
        content_id = f"{signal}_content"

        return Button(
            *children,
            data_ref=trigger_id,
            id=trigger_id,
            popovertarget=content_id,
            popoveraction="toggle",
            variant=variant,
            aria_haspopup="dialog",
            aria_describedby=content_id,
            data_slot="popover-trigger",
            cls=cls,
            **kwargs,
        )

    return trigger


def PopoverContent(
    *children: FT | Callable[[str], FT],
    cls: str = "",
    side: Literal["top", "right", "bottom", "left"] = "bottom",
    align: Literal["start", "center", "end"] = "center",
    offset: int | None = None,
    container: Literal["auto", "none", "parent"] = "auto",
    **kwargs,
) -> Callable[[str], FT]:
    def content(signal: str) -> FT:
        trigger_id = f"{signal}_trigger"
        content_id = f"{signal}_content"
        placement = side if align == "center" else f"{side}-{align}"

        def process_element(element: FT | Callable[[str], FT]):
            if callable(element) and getattr(element, '__name__', None) == 'close':
                return element(signal)

            children = getattr(element, "children", None)
            if children:
                return FT(element.tag, tuple(process_element(c) for c in children), element.attrs)

            return element

        processed_children = [process_element(child) for child in children]
        has_width = any(w in cls for w in ["w-", "max-w-", "min-w-"])
        has_padding = any(p in cls for p in ["p-", "px-", "py-", "pt-", "pr-", "pb-", "pl-"])

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
            *processed_children,
            data_ref=content_id,
            data_position=(trigger_id, position_mods),
            popover="auto",
            id=content_id,
            role="dialog",
            aria_labelledby=trigger_id,
            tabindex="-1",
            data_slot="popover-content",
            cls=cn(
                "z-50 rounded-md border border-input bg-popover text-popover-foreground shadow-md outline-none",
                "w-72" if not has_width else "",
                "p-4" if not has_padding else "",
                cls,
            ),
            **kwargs,
        )

    return content


def PopoverClose(
    *children: FT,
    cls: str = "",
    variant: str = "ghost",
    size: str = "sm",
    **kwargs,
) -> Callable[[str], FT]:
    def close(signal: str) -> FT:

        return Button(
            *children,
            popovertarget=f"{signal}_content",
            popoveraction="hide",
            variant=variant,
            size=size,
            data_slot="popover-close",
            cls=cn("absolute right-2 top-2", cls),
            aria_label="Close popover",
            **kwargs,
        )

    return close
