from starhtml import FT, Div, Icon, P, Span

from .avatar import Avatar, AvatarFallback, AvatarImage
from .dropdown_menu import (
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuLabel,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
)
from .utils import cn

__metadata__ = {
    "description": "User avatar button with dropdown menu for auth actions",
    "handlers": ["position"],
}


def UserButton(
    *children,
    name: str = "",
    email: str = "",
    avatar_src: str = "",
    avatar_fallback: str = "",
    show_name: bool = False,
    signal: str = "",
    side: str = "bottom",
    align: str = "end",
    side_offset: int = 4,
    cls: str = "",
    **kwargs,
) -> FT:
    """User avatar button with dropdown menu for account/auth actions."""

    if not avatar_fallback and name:
        parts = name.split()
        avatar_fallback = (parts[0][0] + (parts[-1][0] if len(parts) > 1 else "")).upper()

    avatar = Avatar(
        AvatarImage(src=avatar_src, alt=name) if avatar_src else None,
        AvatarFallback(avatar_fallback) if avatar_fallback else None,
        cls="size-8",
    )

    if show_name and name:
        trigger_content = Span(
            avatar,
            Span(name, cls="truncate max-w-[150px]"),
            Icon("lucide:chevron-down", cls="size-3.5 opacity-50 shrink-0"),
            cls="flex items-center gap-2",
        )
        trigger_cls = cn("relative h-auto rounded-full py-1 pl-1 pr-3 aria-expanded:bg-accent", cls)
    else:
        trigger_content = avatar
        trigger_cls = cn(
            "relative h-8 w-8 px-0 rounded-full",
            "ring-offset-background transition-opacity hover:opacity-80",
            "focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2",
            "aria-expanded:ring-2 aria-expanded:ring-ring aria-expanded:ring-offset-2",
            cls,
        )

    trigger_label = f"{name}'s account menu" if name else "Account menu"

    header_parts = []
    if name or email:
        identity_avatar = Avatar(
            AvatarImage(src=avatar_src, alt=name) if avatar_src else None,
            AvatarFallback(avatar_fallback) if avatar_fallback else None,
            cls="size-10",
        )
        identity_info = Div(
            P(name, cls="text-sm font-semibold leading-none truncate") if name else None,
            P(email, cls="text-xs text-muted-foreground leading-none truncate") if email else None,
            cls="flex flex-col gap-1.5 min-w-0",
        )
        header_parts.append(
            DropdownMenuLabel(
                Div(identity_avatar, identity_info, cls="flex items-center gap-3"),
                cls="font-normal py-2",
            )
        )
        header_parts.append(DropdownMenuSeparator())

    return DropdownMenu(
        DropdownMenuTrigger(
            trigger_content,
            variant="ghost",
            aria_label=trigger_label,
            cls=trigger_cls,
        ),
        DropdownMenuContent(
            *header_parts,
            *children,
            side=side,
            align=align,
            side_offset=side_offset,
            cls="w-56",
        ),
        signal=signal,
        **kwargs,
    )
