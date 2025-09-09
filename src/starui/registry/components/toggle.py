from typing import Any, Literal
from uuid import uuid4

from starhtml import FT, Div
from starhtml import Button as HTMLButton
from starhtml.datastar import ds_on_click, ds_signals, toggle_signal

from .utils import cn, cva

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
    signal: str = "",
    disabled: bool = False,
    aria_label: str | None = None,
    class_name: str = "",
    cls: str = "",
    **kwargs: Any,
) -> FT:
    signal = signal or f"toggle_{str(uuid4())[:8]}"
    toggle_id = kwargs.pop("id", f"toggle_{str(uuid4())[:8]}")

    return Div(
        HTMLButton(
            *children,
            ds_on_click(toggle_signal(signal)) if not disabled else None,
            type="button",
            id=toggle_id,
            disabled=disabled,
            aria_label=aria_label,
            aria_pressed=str(pressed).lower(),
            data_slot="toggle",
            data_attr_aria_pressed=f"${signal}.toString()",
            data_attr_data_state=f"${signal} ? 'on' : 'off'",
            cls=cn(
                toggle_variants(variant=variant, size=size),
                class_name,
                cls,
            ),
            **kwargs,
        ),
        ds_signals(**{signal: pressed}),
    )
