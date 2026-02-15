from typing import Any, Literal

from starhtml import FT, Div, Signal
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
                "outline": "border border-input bg-transparent shadow-xs",
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
    sig = getattr(signal, '_id', signal) or gen_id("toggle")
    toggle_id = kwargs.pop("id", sig)

    pressed_state = Signal(sig, pressed)

    user_on_click = kwargs.pop('data_on_click', None)
    user_actions = user_on_click if isinstance(user_on_click, list) else ([user_on_click] if user_on_click else [])
    click_actions = [pressed_state.toggle()] + user_actions if not disabled else None

    return Div(
        pressed_state,
        HTMLButton(
            *children,
            data_on_click=click_actions,
            type="button",
            id=toggle_id,
            disabled=disabled,
            aria_label=aria_label,
            data_attr_aria_pressed=pressed_state.if_('true', 'false'),
            data_attr_data_state=pressed_state.if_('on', 'off'),
            data_slot="toggle",
            cls=cn(
                toggle_variants(variant=variant, size=size),
                cls,
            ),
            **kwargs,
        ),
    )
