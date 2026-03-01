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
        aria_hidden="true",
        cls=cn(
            "bg-accent animate-pulse rounded-md motion-reduce:animate-none",
            cls,
        ),
        **kwargs,
    )
