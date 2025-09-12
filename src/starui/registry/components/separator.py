from typing import Any, Literal

from starhtml import FT, Div

from .utils import cn


def Separator(
    orientation: Literal["horizontal", "vertical"] = "horizontal",
    cls: str = "",
    **kwargs: Any,
) -> FT:
    combined_classes = cls.split()

    has_custom_height = any(c.startswith("h-") for c in combined_classes)
    has_custom_width = any(c.startswith("w-") for c in combined_classes)
    has_custom_bg = any(c.startswith("bg-") for c in combined_classes)

    if orientation == "horizontal":
        default_size = f"{'h-px' if not has_custom_height else ''} {'w-full' if not has_custom_width else ''}".strip()
    else:
        default_size = f"{'w-px' if not has_custom_width else ''} {'h-full' if not has_custom_height else ''}".strip()

    return Div(
        data_slot="separator",
        data_orientation=orientation,
        cls=cn(
            "shrink-0",
            default_size,
            "bg-border" if not has_custom_bg else "",
            cls,
        ),
        **kwargs,
    )
