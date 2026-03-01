from typing import Literal

from starhtml import FT, Div

from .utils import cn


def Separator(
    orientation: Literal["horizontal", "vertical"] = "horizontal",
    decorative: bool = True,
    cls: str = "",
    **kwargs,
) -> FT:
    return Div(
        role=None if decorative else "separator",
        aria_orientation=None if decorative else orientation,
        aria_hidden="true" if decorative else None,
        data_slot="separator",
        data_orientation=orientation,
        cls=cn(
            "shrink-0 bg-border",
            "h-px w-full" if orientation == "horizontal" else "w-px self-stretch",
            cls,
        ),
        **kwargs,
    )
