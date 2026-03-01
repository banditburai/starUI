from starhtml import FT, Div, Signal
from starhtml.datastar import Expr

from .utils import cn, gen_id


def Progress(
    value: float | None = None,
    max_value: float = 100,
    signal: str | Signal = "",
    cls: str = "",
    **kwargs,
) -> FT:
    sig = getattr(signal, "_id", signal) or gen_id("progress")
    initial = getattr(signal, "_initial", value) if value is None else value

    if isinstance(initial, Expr):
        pct = initial
    elif initial is not None and max_value > 0:
        pct = max(0, min(100, initial / max_value * 100))
        pct = int(pct) if pct == int(pct) else pct
    else:
        pct = 0

    reactive = isinstance(signal, Signal) or (isinstance(signal, str) and signal)
    ssr_pct = pct if isinstance(pct, (int, float)) else 0

    if reactive:
        s = Signal(sig, pct)
        return Div(
            s,
            Div(
                style=f"transform: translateX(-{100 - ssr_pct}%)",
                data_style_transform="translateX(-" + (100 - s) + "%)",
                cls="bg-primary h-full w-full flex-1",
            ),
            role="progressbar",
            aria_valuemin="0",
            aria_valuemax="100",
            data_attr_aria_valuenow=s,
            data_slot="progress",
            cls=cn(
                "bg-primary/20 relative h-2 w-full overflow-hidden rounded-full", cls
            ),
            **kwargs,
        )

    return Div(
        Div(
            style=f"transform: translateX(-{100 - ssr_pct}%)",
            cls="bg-primary h-full w-full flex-1",
        ),
        role="progressbar",
        aria_valuemin="0",
        aria_valuemax="100",
        aria_valuenow=str(ssr_pct),
        data_slot="progress",
        cls=cn("bg-primary/20 relative h-2 w-full overflow-hidden rounded-full", cls),
        **kwargs,
    )
