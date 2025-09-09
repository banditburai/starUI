from starhtml import FT
from starhtml import Label as HtmlLabel

from .utils import cn


def Label(
    *children,
    class_name: str = "",
    cls: str = "",
    **kwargs,
) -> FT:
    return HtmlLabel(
        *children,
        data_slot="label",
        cls=cn(
            "flex items-center gap-2 text-sm leading-none font-medium select-none",
            "group-data-[disabled=true]:pointer-events-none group-data-[disabled=true]:opacity-50",
            "peer-disabled:cursor-not-allowed peer-disabled:opacity-50",
            class_name,
            cls,
        ),
        **kwargs,
    )
