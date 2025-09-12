from typing import Callable, Literal

from starhtml import FT, Div
from starhtml.datastar import ds_position, ds_ref

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
    def _(signal: str) -> FT:
        return Button(
            *children,
            ds_ref(f"{signal}_trigger"),
            variant=variant,
            popovertarget=f"{signal}_content",
            popoveraction="toggle",
            id=f"{signal}_trigger",
            aria_haspopup="dialog",
            aria_describedby=f"{signal}_content",
            data_slot="popover-trigger",
            cls=cls,
            **kwargs,
        )

    return _


def PopoverContent(
    *children: FT | Callable[[str], FT],
    cls: str = "",
    side: Literal["top", "right", "bottom", "left"] = "bottom",
    align: Literal["start", "center", "end"] = "center",
    **kwargs,
) -> Callable[[str], FT]:
    def _(signal: str) -> FT:
        placement = side if align == "center" else f"{side}-{align}"

        def process_element(element: FT | Callable[[str], FT]):
            if callable(element) and getattr(element, "_is_popover_close", False):
                return element(signal)

            if (
                hasattr(element, "tag")
                and hasattr(element, "children")
                and getattr(element, "children")
            ):
                processed_children = tuple(
                    process_element(child) for child in element.children
                )
                return FT(element.tag, processed_children, element.attrs)

            return element

        processed_children = [process_element(child) for child in children]

        combined_classes = cls
        has_width = any(w in combined_classes for w in ["w-", "max-w-", "min-w-"])
        has_padding = any(
            p in combined_classes for p in ["p-", "px-", "py-", "pt-", "pr-", "pb-", "pl-"]
        )

        return Div(
            *processed_children,
            ds_ref(f"{signal}_content"),
            ds_position(
                anchor=f"{signal}_trigger",
                placement=placement,
                offset=8,
                flip=True,
                shift=True,
                hide=True,
                strategy="fixed",
            ),
            popover="auto",
            id=f"{signal}_content",
            role="dialog",
            aria_labelledby=f"{signal}_trigger",
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

    return _


def PopoverClose(
    *children: FT,
    cls: str = "",
    variant: str = "ghost",
    size: str = "sm",
    **kwargs,
) -> Callable[[str], FT]:
    def _(signal: str) -> FT:
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

    _._is_popover_close = True
    return _
