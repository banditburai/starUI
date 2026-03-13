from components.avatar import Avatar, AvatarFallback, AvatarImage
from components.dropdown_menu import (
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuLabel,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
)
from components.utils import cn
from starhtml import FT, Icon, P, Span

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

    if not avatar_fallback and name and name.strip():
        parts = name.split()
        avatar_fallback = (parts[0][0] + (parts[-1][0] if len(parts) > 1 else "")).upper()

    avatar = Avatar(
        AvatarImage(src=avatar_src, alt="") if avatar_src else None,
        AvatarFallback(avatar_fallback) if avatar_fallback else None,
        cls="size-8",
    )

    if show_name and name:
        trigger_content = Span(
            avatar,
            Span(name, cls="max-w-[150px] truncate"),
            Icon("lucide:chevron-down", cls="size-3.5 shrink-0 opacity-50"),
            cls="flex items-center gap-2",
        )
        trigger_cls = cn(
            "relative h-auto cursor-pointer rounded-full py-1 pr-3 pl-1 ring-offset-background transition-colors",
            "hover:bg-accent/50 focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2",
            "aria-expanded:bg-accent",
            cls,
        )
    else:
        trigger_content = avatar
        trigger_cls = cn(
            "relative h-8 w-8 cursor-pointer rounded-full px-0",
            "ring-offset-background transition-shadow",
            "hover:ring-2 hover:ring-ring/50 hover:ring-offset-2",
            "focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2",
            "aria-expanded:ring-2 aria-expanded:ring-ring aria-expanded:ring-offset-2",
            cls,
        )

    trigger_label = f"{name}'s account menu" if name else "Account menu"

    header_parts = []
    if name or email:
        header_parts.append(
            DropdownMenuLabel(
                P(name, cls="truncate text-sm leading-none font-semibold") if name else None,
                P(email, cls="truncate text-xs leading-none text-muted-foreground") if email else None,
                cls="flex flex-col gap-1.5 font-normal",
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
            cls="min-w-48",
        ),
        signal=signal,
        **kwargs,
    )
