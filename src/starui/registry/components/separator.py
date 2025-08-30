from typing import Any, Literal

from starhtml import FT, Div

from .utils import cn


def Separator(
    orientation: Literal["horizontal", "vertical"] = "horizontal",
    decorative: bool = True,
    class_name: str = "",
    cls: str = "",
    **attrs: Any,
) -> FT:
    combined_classes = (cls + " " + class_name).split()

    has_custom_size = any(c.startswith(("h-", "w-")) for c in combined_classes)
    default_size = (
        ("h-px w-full" if orientation == "horizontal" else "w-px h-full")
        if not has_custom_size
        else ""
    )

    has_custom_bg = any(c.startswith("bg-") for c in combined_classes)
    default_bg = "bg-border" if not has_custom_bg else ""

    return Div(
        data_slot="separator",
        data_orientation=orientation,
        role=None if decorative else "separator",
        aria_orientation=None if decorative else orientation,
        cls=cn(
            "shrink-0",
            default_size,
            default_bg,
            class_name,
            cls,
        ),
        **attrs,
    )
