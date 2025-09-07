from starhtml import FT, Div

from .utils import cn


def Skeleton(
    *children,
    class_name: str = "",
    cls: str = "",
    **attrs,
) -> FT:
    return Div(
        *children,
        data_slot="skeleton",
        cls=cn(
            "animate-pulse bg-muted",
            {"rounded-md": not any(c.startswith("rounded") 
                                   for c in f"{class_name} {cls}".split())},
            class_name,
            cls,
        ),
        **attrs,
    )
