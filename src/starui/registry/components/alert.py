from typing import Literal

from starhtml import FT, Div

from .utils import cn, cva

AlertVariant = Literal["default", "destructive"]


alert_variants = cva(
    base=(
        "relative w-full rounded-lg border px-4 py-3 text-sm grid "
        "has-[[data-icon-sh]]:grid-cols-[calc(var(--spacing)*4)_1fr] grid-cols-[0_1fr] "
        "has-[[data-icon-sh]]:gap-x-3 gap-y-0.5 items-start "
        "[&_[data-icon-sh]]:size-4 [&_[data-icon-sh]]:translate-y-0.5"
    ),
    config={
        "variants": {
            "variant": {
                "default": "bg-card text-card-foreground",
                "destructive": "text-destructive bg-card [&_[data-icon-sh]]:text-destructive",
            }
        },
        "defaultVariants": {"variant": "default"},
    },
)


def Alert(
    *children,
    variant: AlertVariant = "default",
    cls: str = "",
    **kwargs,
) -> FT:
    return Div(
        *children,
        role="alert",
        cls=cn(alert_variants(variant=variant), cls),
        **kwargs,
    )


def AlertTitle(
    *children,
    cls: str = "",
    **kwargs,
) -> FT:
    return Div(
        *children,
        cls=cn(
            "col-start-2 line-clamp-1 min-h-4 font-medium tracking-tight",
            cls,
        ),
        **kwargs,
    )


def AlertDescription(
    *children,
    cls: str = "",
    **kwargs,
) -> FT:
    return Div(
        *children,
        cls=cn(
            "col-start-2 grid justify-items-start gap-1 text-sm [&_p]:leading-relaxed",
            cls,
        ),
        **kwargs,
    )
