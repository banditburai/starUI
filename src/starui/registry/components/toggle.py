from typing import Any, Literal
from uuid import uuid4

from starhtml import FT, Signal
from starhtml import Button as HTMLButton

from .utils import cn, cva, gen_id

ToggleVariant = Literal["default", "outline"]
ToggleSize = Literal["default", "sm", "lg"]


toggle_variants = cva(
    base="inline-flex items-center justify-center gap-2 rounded-md text-sm font-medium hover:bg-muted hover:text-muted-foreground disabled:pointer-events-none disabled:opacity-50 data-[state=on]:bg-accent data-[state=on]:text-accent-foreground [&_svg]:pointer-events-none [&_svg:not([class*='size-'])]:size-4 [&_svg]:shrink-0 focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:ring-[3px] outline-none transition-[color,box-shadow] aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40 aria-invalid:border-destructive whitespace-nowrap",
    config={
        "variants": {
            "variant": {
                "default": "bg-transparent",
                "outline": "border border-input bg-transparent shadow-xs hover:bg-accent hover:text-accent-foreground",
            },
            "size": {
                "default": "h-9 px-3 min-w-9",
                "sm": "h-8 px-2 min-w-8",
                "lg": "h-10 px-4 min-w-10",
            },
        },
        "defaultVariants": {
            "variant": "default",
            "size": "default",
        },
    },
)


def Toggle(
    *children: Any,
    variant: ToggleVariant = "default",
    size: ToggleSize = "default",
    pressed: bool = False,
    signal: str | Signal = "",
    disabled: bool = False,
    aria_label: str | None = None,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    sig = getattr(signal, 'id', signal) or gen_id("toggle")
    toggle_id = kwargs.pop("id", gen_id("toggle"))
    toggle_signal = Signal(sig, pressed)

    return HTMLButton(
        toggle_signal,
        *children,
        data_on_click=toggle_signal.toggle() if not disabled else None,
        type="button",
        id=toggle_id,
        disabled=disabled,
        aria_label=aria_label,
        aria_pressed=str(pressed).lower(),
        data_slot="toggle",
        data_attr_aria_pressed=toggle_signal.if_('true', 'false'),
        data_attr_data_state=toggle_signal.if_('on', 'off'),
        cls=cn(
            toggle_variants(variant=variant, size=size),
            cls,
        ),
        **kwargs,
    )
