from typing import Literal

from starhtml import FT, A, Span
from starhtml import Button as HTMLButton

from .utils import cn, cva

__metadata__ = {"description": "Badge for labels"}


BadgeVariant = Literal["default", "secondary", "destructive", "outline"]


badge_variants = cva(
    base=(
        "inline-flex items-center justify-center rounded-md border px-2 py-0.5 text-xs font-medium "
        "w-fit shrink-0 gap-1 whitespace-nowrap [&_[data-icon-sh]]:pointer-events-none [&_[data-icon-sh]]:size-3 "
        "focus-visible:border-ring focus-visible:ring-[3px] focus-visible:ring-ring/50 "
        "aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40 "
        "overflow-hidden transition-[color,box-shadow] aria-invalid:border-destructive"
    ),
    config={
        "variants": {
            "variant": {
                "default": "border-transparent bg-primary text-primary-foreground [a&]:hover:bg-primary/90",
                "secondary": "border-transparent bg-secondary text-secondary-foreground [a&]:hover:bg-secondary/90",
                "destructive": "border-transparent bg-destructive text-white focus-visible:ring-destructive/20 dark:bg-destructive/60 dark:focus-visible:ring-destructive/40 [a&]:hover:bg-destructive/90",
                "outline": "text-foreground [a&]:hover:bg-accent [a&]:hover:text-accent-foreground",
            }
        },
        "defaultVariants": {"variant": "default"},
    },
)


def Badge(
    *children,
    variant: BadgeVariant = "default",
    href: str | None = None,
    clickable: bool = False,
    cls: str = "",
    **kwargs,
) -> FT:
    if href:
        return A(*children, href=href, cls=cn(badge_variants(variant=variant), cls), **kwargs)

    if clickable:
        return HTMLButton(
            *children,
            cls=cn(badge_variants(variant=variant), "cursor-pointer", cls),
            type="button",
            **kwargs,
        )

    return Span(*children, cls=cn(badge_variants(variant=variant), cls), **kwargs)
