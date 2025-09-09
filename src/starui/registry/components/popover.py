from uuid import uuid4

from starhtml import FT, Div
from starhtml.datastar import ds_position, ds_ref

from .button import Button
from .utils import cn


def Popover(*children, cls="relative inline-block", **kwargs):
    signal = f"popover_{uuid4().hex[:8]}"
    return Div(
        *[child(signal) if callable(child) else child for child in children],
        cls=cls,
        **kwargs,
    )


def PopoverTrigger(*children, variant="default", cls="", **kwargs):
    def _(signal):
        return Button(
            *children,
            ds_ref(f"{signal}_trigger"),
            variant=variant,
            popovertarget=f"{signal}_content",
            popoveraction="toggle",
            id=f"{signal}_trigger",
            cls=cls,
            **kwargs,
        )

    return _


def PopoverContent(*children, cls="", side="bottom", align="center", **kwargs):
    def _(signal):
        placement = f"{side}-{align}" if align != "center" else side

        def process_element(element):
            if callable(element) and getattr(element, "_is_popover_close", False):
                return element(signal)

            if (
                hasattr(element, "tag")
                and hasattr(element, "children")
                and element.children
            ):
                processed_children = tuple(
                    process_element(child) for child in element.children
                )
                return FT(element.tag, processed_children, element.attrs)

            return element

        processed_children = [process_element(child) for child in children]

        has_width = any(w in cls for w in ["w-", "max-w-", "min-w-"])
        has_padding = any(
            p in cls for p in ["p-", "px-", "py-", "pt-", "pr-", "pb-", "pl-"]
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
            ),
            popover="auto",
            id=f"{signal}_content",
            role="dialog",
            aria_labelledby=f"{signal}_trigger",
            tabindex="-1",
            cls=cn(
                "z-50 rounded-md border border-input bg-popover text-popover-foreground shadow-md outline-none",
                "w-72" if not has_width else "",
                "p-4" if not has_padding else "",
                cls,
            ),
            **kwargs,
        )

    return _


def PopoverClose(*children, cls="", variant="ghost", size="sm", **kwargs):
    def _(signal):
        return Button(
            *children,
            popovertarget=f"{signal}_content",
            popoveraction="hide",
            variant=variant,
            size=size,
            cls=cn("absolute right-2 top-2", cls),
            aria_label="Close popover",
            **kwargs,
        )

    _._is_popover_close = True
    return _
