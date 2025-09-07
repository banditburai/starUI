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

    if orientation == "horizontal":
        has_custom_height = any(c.startswith("h-") for c in combined_classes)
        has_custom_width = any(c.startswith("w-") for c in combined_classes)
        default_size = f"{'h-px' if not has_custom_height else ''} {'w-full' if not has_custom_width else ''}".strip()
    else:  # vertical
        has_custom_height = any(c.startswith("h-") for c in combined_classes)
        has_custom_width = any(c.startswith("w-") for c in combined_classes)
        default_size = f"{'w-px' if not has_custom_width else ''} {'h-full' if not has_custom_height else ''}".strip()

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
