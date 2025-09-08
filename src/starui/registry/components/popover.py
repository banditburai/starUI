from uuid import uuid4

from starhtml import FT, Div, Style
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

        has_width = any(w in cls for w in ["w-", "max-w-", "min-w-"])
        has_padding = any(
            p in cls for p in ["p-", "px-", "py-", "pt-", "pr-", "pb-", "pl-"]
        )

        return Div(
            Style(f"""
                @keyframes popover-show-{signal} {{
                    from {{ opacity: 0; }}
                    to {{ opacity: 1; }}
                }}
                #{signal}-content {{
                    opacity: 0;
                }}
                #{signal}-content:popover-open {{
                    animation: popover-show-{signal} 150ms ease-out 75ms forwards;
                }}
            """),
            *processed_children,
            ds_ref(f"{signal}Content"),
            ds_position(
                anchor=f"{signal}-trigger",
                placement=placement,
                offset=8,
                flip=True,
                shift=True,
                hide=True,
                strategy="fixed",
            ),
            popover="auto",
            id=f"{signal}-content",
            role="dialog",
            aria_labelledby=f"{signal}-trigger",
            tabindex="-1",
            cls=cn(
                "z-50 rounded-md border border-input bg-popover text-popover-foreground shadow-md outline-none",
                "w-72" if not has_width else "",
                "p-4" if not has_padding else "",
                cls,
            ),
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
