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
        cls=cn(
            "animate-pulse bg-muted rounded-md",
            cls,
        ),
        **kwargs,
    )
