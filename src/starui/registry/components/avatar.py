from typing import Any
from uuid import uuid4

from starhtml import FT, Div, Img
from starhtml.datastar import ds_on, ds_show, ds_signals

from .utils import cn


def Avatar(
    *children: Any,
    class_name: str = "",
    cls: str = "",
    **kwargs: Any,
) -> FT:
    return Div(
        *children,
        data_slot="avatar",
        cls=cn(
            "relative flex size-10 shrink-0 overflow-hidden rounded-full",
            class_name,
            cls,
        ),
        **kwargs,
    )


def AvatarImage(
    src: str,
    alt: str = "",
    loading: str = "lazy",
    class_name: str = "",
    cls: str = "",
    **kwargs: Any,
) -> FT:
    return Img(
        src=src,
        alt=alt,
        loading=loading,
        data_slot="avatar-image",
        cls=cn("aspect-square size-full object-cover", class_name, cls),
        **kwargs,
    )


def AvatarFallback(
    *children: Any,
    class_name: str = "",
    cls: str = "",
    **kwargs: Any,
) -> FT:
    has_bg = "bg-" in f"{class_name} {cls}"

    return Div(
        *children,
        data_slot="avatar-fallback",
        cls=cn(
            "flex size-full items-center justify-center rounded-full",
            "bg-muted" if not has_bg else "",
            class_name,
            cls,
        ),
        **kwargs,
    )


def AvatarWithFallback(
    src: str | None = None,
    alt: str = "",
    fallback: str = "?",
    loading: str = "lazy",
    class_name: str = "",
    cls: str = "",
    **kwargs: Any,
) -> FT:
    if not src:
        return Avatar(
            AvatarFallback(fallback),
            cls=cn(class_name, cls),
            **kwargs,
        )

    signal = f"avatar_{str(uuid4())[:8]}_error"

    return Avatar(
        ds_signals(**{signal: False}),
        Img(
            ds_show(f"!${signal}"),
            ds_on("error", f"${signal} = true"),
            src=src,
            alt=alt,
            loading=loading,
            cls="aspect-square size-full object-cover",
            data_slot="avatar-image",
        ),
        Div(
            fallback,
            ds_show(f"${signal}"),
            cls="flex size-full items-center justify-center rounded-full bg-muted",
            data_slot="avatar-fallback",
        ),
        cls=cn(class_name, cls),
        **kwargs,
    )
