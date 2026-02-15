from typing import Any

from starhtml import Div, FT, Signal

from .utils import cn, gen_id


def Progress(
    value: float | None = None,
    max_value: float = 100,
    signal: str | Signal = "",
    cls: str = "",
    **kwargs: Any,
) -> FT:
    sig = getattr(signal, '_id', signal) or gen_id("progress")
    initial_value = getattr(signal, '_initial', value) if value is None else value
    pct = max(0, min(100, (initial_value / max_value * 100) if initial_value is not None and max_value > 0 else 0))
    pct = int(pct) if pct == int(pct) else pct

    return Div(
        (progress := Signal(sig, pct)),
        Div(
            data_style_width=progress + '%',
            cls="bg-primary h-full transition-all duration-300 ease-out",
        ),
        role="progressbar",
        aria_valuemin="0",
        aria_valuemax=str(max_value),
        aria_valuenow=str(value) if value is not None else None,
        data_slot="progress",
        cls=cn(
            "bg-primary/20 relative h-2 w-full overflow-hidden rounded-full",
            cls,
        ),
        **kwargs,
    )
