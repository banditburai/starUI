from typing import Literal

from starhtml import FT, Div

from .utils import cn, cva

AlertVariant = Literal["default", "destructive"]


alert_variants = cva(
    base="relative w-full rounded-lg border px-4 py-3 text-sm grid has-[>iconify-icon]:grid-cols-[calc(var(--spacing)*4)_1fr] grid-cols-[0_1fr] has-[>iconify-icon]:gap-x-3 gap-y-0.5 items-start [&>iconify-icon]:size-4 [&>iconify-icon]:translate-y-0.5",
    config={
        "variants": {
            "variant": {
                "default": "bg-card text-card-foreground",
                "destructive": "text-destructive bg-card [&>iconify-icon]:text-destructive *:data-[slot=alert-description]:text-destructive/90",
            }
        },
        "defaultVariants": {"variant": "default"},
    },
)


def Alert(
    *children,
    variant: AlertVariant = "default",
    class_name: str = "",
    cls: str = "",
    **kwargs,
) -> FT:
    return Div(
        *children,
        role="alert",
        data_slot="alert",
        cls=cn(
            alert_variants(variant=variant),
            class_name,
            cls,
        ),
        **kwargs,
    )


def AlertTitle(
    *children,
    class_name: str = "",
    cls: str = "",
    **kwargs,
) -> FT:
    return Div(
        *children,
        data_slot="alert-title",
        cls=cn(
            "col-start-2 line-clamp-1 min-h-4 font-medium tracking-tight",
            class_name,
            cls,
        ),
        **kwargs,
    )


def AlertDescription(
    *children,
    class_name: str = "",
    cls: str = "",
    **kwargs,
) -> FT:
    return Div(
        *children,
        data_slot="alert-description",
        cls=cn(
            "text-muted-foreground col-start-2 grid justify-items-start gap-1 text-sm [&_p]:leading-relaxed",
            class_name,
            cls,
        ),
        **kwargs,
    )
