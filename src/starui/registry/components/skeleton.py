from typing import Any

from starhtml import FT, Div

from .utils import cn


def Skeleton(
    *children,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    combined = cls.split()
    has_custom_rounded = any(c.startswith("rounded") for c in combined)

    return Div(
        *children,
        data_slot="skeleton",
        cls=cn(
            "animate-pulse bg-muted",
            "rounded-md" if not has_custom_rounded else "",
            cls,
        ),
        **kwargs,
    )
