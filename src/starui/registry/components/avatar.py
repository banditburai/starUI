from typing import Any

from starhtml import FT, Div, Img, Signal

from .utils import cn, ensure_signal


def Avatar(
    *children: Any,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    return Div(
        *children,
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
    cls: str = "",
    **kwargs: Any,
) -> FT:
    return Img(
        src=src,
        alt=alt,
        loading=loading,
        cls=cn("aspect-square size-full object-cover", cls),
        **kwargs,
    )


def AvatarFallback(
    *children: Any,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    return Div(
        *children,
        cls=cn(
            "flex size-full items-center justify-center rounded-full",
            "bg-muted" if "bg-" not in cls else "",
            cls,
        ),
        **kwargs,
    )


def AvatarWithFallback(
    src: str | None = None,
    alt: str = "",
    fallback: str = "?",
    loading: str = "lazy",
    signal: str = "",
    cls: str = "",
    **kwargs: Any,
) -> FT:
    if not src:
        return Avatar(
            AvatarFallback(fallback),
            cls=cls,
            **kwargs,
        )

    sig_name = ensure_signal(signal, "avatar_error")    

    return Avatar(
        (error_state := Signal(sig_name, False)),
        Img(
            src=src,
            alt=alt,
            loading=loading,
            data_show=~error_state,
            data_on_error=error_state.set(True),
            cls="aspect-square size-full object-cover",
        ),
        Div(
            fallback,
            data_show=error_state,
            cls="flex size-full items-center justify-center rounded-full bg-muted",
        ),
        cls=cls,
        **kwargs,
    )
