from starhtml import FT, Div

from .utils import cn

__metadata__ = {"description": "Aspect ratio container"}


def AspectRatio(
    *children,
    ratio: float = 16 / 9,
    cls: str = "",
    **kwargs,
) -> FT:
    return Div(
        *children,
        data_slot="aspect-ratio",
        style=f"aspect-ratio: {ratio}",
        cls=cn("relative w-full overflow-hidden", cls),
        **kwargs,
    )
