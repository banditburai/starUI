from starhtml import FT, Div, Img, Signal

from .utils import cn, gen_id


def Avatar(
    *children,
    cls: str = "",
    **kwargs,
) -> FT:
    return Div(
        *children,
        data_slot="avatar",
        cls=cn(
            "relative flex size-10 shrink-0 overflow-hidden rounded-full",
            cls,
        ),
        **kwargs,
    )


def AvatarImage(
    src: str,
    alt: str = "",
    loading: str = "lazy",
    signal: str | Signal = "",
    cls: str = "",
    **kwargs,
) -> FT:
    sig = getattr(signal, "_id", signal) or gen_id("avatar_img_error")
    error_state = Signal(sig, False)

    return Div(
        error_state,
        Img(
            src=src,
            alt=alt,
            loading=loading,
            data_on_error=error_state.set(True),
            data_show=~error_state,
            cls=cn("aspect-square size-full object-cover", cls),
            **kwargs,
        ),
        cls="contents",
        data_slot="avatar-image",
    )


def AvatarFallback(
    *children,
    cls: str = "",
    **kwargs,
) -> FT:
    return Div(
        *children,
        cls=cn(
            "flex size-full items-center justify-center rounded-full bg-muted",
            cls,
        ),
        data_slot="avatar-fallback",
        **kwargs,
    )
