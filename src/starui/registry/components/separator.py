from typing import Any, Literal

from starhtml import FT, Div

from .utils import cn


def Separator(
    orientation: Literal["horizontal", "vertical"] = "horizontal",
    cls: str = "",
    **kwargs: Any,
) -> FT:
    return Div(
        data_slot="separator",
        data_orientation=orientation,
        cls=cn(
            "shrink-0 bg-border",
            "h-px w-full" if orientation == "horizontal" else "w-px h-full",
            cls,
        ),
        **kwargs,
    )
