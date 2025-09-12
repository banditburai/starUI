from typing import Any

from starhtml import FT, Div
from starhtml.datastar import ds_signals, ds_style, value

from .utils import cn, ensure_signal


def Progress(
    progress_value: float | None = None,
    max_value: float = 100,
    signal: str | None = None,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    signal = ensure_signal(signal, "progress")

    percentage = max(
        0,
        min(
            100,
            (progress_value / max_value) * 100
            if progress_value is not None and max_value > 0
            else 0,
        ),
    )
    percentage = int(percentage) if percentage.is_integer() else percentage

    return Div(
        ds_signals({signal: value(percentage)}),
        Div(
            ds_style(width=f"${signal} + '%'"),
            cls="bg-primary h-full transition-all duration-300 ease-out",
            style=f"width: {percentage}%",
        ),
        role="progressbar",
        aria_valuemin="0",
        aria_valuemax=str(max_value),
        aria_valuenow=str(progress_value) if progress_value is not None else None,
        cls=cn(
            "bg-primary/20 relative h-2 w-full overflow-hidden rounded-full",
            cls,
        ),
        data_slot="progress",
        **kwargs,
    )
