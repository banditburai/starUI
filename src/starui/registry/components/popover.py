from uuid import uuid4

from starhtml import FT, Div
from starhtml.datastar import ds_position, ds_ref

from .button import Button
from .utils import cn


def Popover(*children, cls="relative inline-block", **attrs):
    signal = f"popover_{uuid4().hex[:8]}"
    return Div(
        *[child(signal) if callable(child) else child for child in children],
        cls=cls,
        **attrs,
    )


def PopoverTrigger(*children, variant="default", cls="", **attrs):
    def create(signal):
        return Button(
            *children,
            ds_ref(f"{signal}Trigger"),
            variant=variant,
            popovertarget=f"{signal}-content",
            popoveraction="toggle",
            id=f"{signal}-trigger",
            cls=cls,
            **attrs,
        )

    return create


def PopoverContent(*children, cls="", side="bottom", align="center", **attrs):
    def create_content(signal):
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
        
        # Determine if we should add default width/padding
        has_width = any(c in cls for c in ["w-auto", "w-fit", "w-full", "w-[", "w-0", "w-1", "w-2", "w-3", "w-4", "w-5", "w-6", "w-7", "w-8", "w-9", "max-w-", "min-w-"])
        has_padding = any(c in cls for c in ["p-0", "p-1", "p-2", "p-3", "p-4", "p-5", "p-6", "p-7", "p-8", "p-9", "p-[", "px-", "py-", "pt-", "pr-", "pb-", "pl-"])
        
        # Build the base classes
        base_classes = ["z-50", "rounded-md", "border", "bg-popover", "text-popover-foreground", "shadow-md", "outline-none", "dark:border-input"]
        
        # Add defaults only if not overridden
        if not has_width:
            base_classes.append("w-72")
        if not has_padding:
            base_classes.append("p-4")

        return Div(
            *processed_children,
            ds_ref(f"{signal}Content"),
            ds_position(
                anchor=f"{signal}-trigger",
                placement=placement,
                offset=8,
                flip=True,
                shift=True,
                hide=True,
            ),
            popover="auto",
            id=f"{signal}-content",
            role="dialog",
            aria_labelledby=f"{signal}-trigger",
            tabindex="-1",
            cls=cn(" ".join(base_classes), cls),
            **attrs,
        )

    return create_content


def PopoverClose(*children, cls="", variant="ghost", size="sm", **attrs):
    def close_button(signal):
        return Button(
            *children,
            popovertarget=f"{signal}-content",
            popoveraction="hide",
            variant=variant,
            size=size,
            cls=cn("absolute right-2 top-2", cls),
            aria_label="Close popover",
            **attrs,
        )

    close_button._is_popover_close = True
    return close_button
