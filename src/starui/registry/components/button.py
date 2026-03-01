from typing import Literal

from starhtml import FT
from starhtml import Button as HTMLButton

from .utils import cn, cva

ButtonVariant = Literal[
    "default", "destructive", "outline", "secondary", "ghost", "link"
]
ButtonSize = Literal["default", "sm", "lg", "icon"]


button_variants = cva(
    base=(
        "inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium "
        "transition-all disabled:pointer-events-none disabled:opacity-50 "
        "[&_[data-icon-sh]]:pointer-events-none [&_[data-icon-sh]]:shrink-0 outline-none "
        "focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:ring-[3px] "
        "aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40 "
        "aria-invalid:border-destructive"
    ),
    config={
        "variants": {
            "variant": {
                "default": "bg-primary text-primary-foreground shadow-xs hover:bg-primary/90",
                "destructive": "bg-destructive text-white shadow-xs hover:bg-destructive/90 focus-visible:ring-destructive/20 dark:focus-visible:ring-destructive/40 dark:bg-destructive/60",
                "outline": "border bg-background shadow-xs hover:bg-accent hover:text-accent-foreground dark:bg-input/30 dark:border dark:hover:bg-input/50",
                "secondary": "bg-secondary text-secondary-foreground shadow-xs hover:bg-secondary/80",
                "ghost": "hover:bg-accent hover:text-accent-foreground dark:hover:bg-accent/50",
                "link": "text-primary underline-offset-4 hover:underline",
            },
            "size": {
                "default": "h-9 px-4 py-2 has-[[data-icon-sh]]:px-3",
                "sm": "h-8 rounded-md gap-1.5 px-3 has-[[data-icon-sh]]:px-2.5",
                "lg": "h-10 rounded-md px-6 has-[[data-icon-sh]]:px-4",
                "icon": "size-9 gap-0",
            },
        },
        "defaultVariants": {"variant": "default", "size": "default"},
    },
)


def Button(
    *children,
    variant: ButtonVariant = "default",
    size: ButtonSize = "default",
    disabled: bool = False,
    type: Literal["button", "submit", "reset"] = "button",
    cls: str = "",
    **kwargs,
) -> FT:
    return HTMLButton(
        *children,
        cls=cn(button_variants(variant=variant, size=size), cls),
        disabled=disabled,
        type=type,
        **kwargs,
    )
