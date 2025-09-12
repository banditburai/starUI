from typing import Any

from starhtml import FT
from starhtml import Label as HTMLLabel

from .utils import cn


def Label(
    *children: Any,    
    cls: str = "",
    **kwargs: Any,
) -> FT:
    return HTMLLabel(
        *children,
        data_slot="label",
        cls=cn(
            "flex items-center gap-2 text-sm leading-none font-medium select-none",
            "group-data-[disabled=true]:pointer-events-none group-data-[disabled=true]:opacity-50",
            "peer-disabled:cursor-not-allowed peer-disabled:opacity-50",            
            cls,
        ),
        **kwargs,
    )
