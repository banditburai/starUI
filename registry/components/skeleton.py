from typing import Any

from starhtml import FT, Div

from .utils import cn

__metadata__ = {"description": "Loading placeholder"}


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
            "animate-pulse rounded-md bg-accent motion-reduce:animate-none",
            cls,
        ),
        **kwargs,
    )
