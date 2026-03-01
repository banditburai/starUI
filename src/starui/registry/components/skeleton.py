from typing import Any

from starhtml import FT, Div

from .utils import cn


def Skeleton(
    *children,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    return Div(
        *children,
        data_slot="skeleton",
        cls=cn(
            "bg-accent animate-pulse rounded-md",
            cls,
        ),
        **kwargs,
    )
