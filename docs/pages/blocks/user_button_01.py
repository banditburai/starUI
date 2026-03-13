"""
User Button 01 block documentation - Avatar + dropdown composition for auth actions.
"""

TITLE = "User Button 01"
DESCRIPTION = "A user avatar button with a dropdown menu for authentication and account actions."
CATEGORY = "blocks"
ORDER = 10
STATUS = "stable"

from pathlib import Path

from starhtml import Div, FT, Icon, Span
from components.dropdown_menu import (
    DropdownMenuGroup,
    DropdownMenuItem,
    DropdownMenuSeparator,
)
from blocks.user_button_01.user_button import UserButton
from utils import auto_generate_block_page, with_code

_BLOCK_DIR = Path(__file__).resolve().parents[3] / "registry" / "blocks" / "user_button_01"


def card_preview() -> FT:
    """Skeleton mockup for the blocks index card."""
    return Div(
        # Avatar circle
        Div(
            Span("SM", cls="text-[9px] font-medium text-primary-foreground"),
            cls="flex size-8 items-center justify-center rounded-full bg-primary",
        ),
        # Dropdown
        Div(
            # Header: name + email (no avatar)
            Div(
                Div(cls="h-1.5 w-16 rounded bg-foreground/70"),
                Div(cls="h-1.5 w-20 rounded bg-muted-foreground/30"),
                cls="space-y-1 px-2 py-1.5",
            ),
            Div(cls="my-0.5 h-px w-full bg-border"),
            # Menu items
            Div(
                Icon("lucide:user", width="8", height="8", cls="shrink-0 text-muted-foreground"),
                Div(cls="h-1.5 w-10 rounded bg-muted-foreground/20"),
                cls="flex items-center gap-1.5 px-2 py-1",
            ),
            Div(
                Icon("lucide:settings", width="8", height="8", cls="shrink-0 text-muted-foreground"),
                Div(cls="h-1.5 w-12 rounded bg-muted-foreground/20"),
                cls="flex items-center gap-1.5 px-2 py-1",
            ),
            Div(
                Icon("lucide:credit-card", width="8", height="8", cls="shrink-0 text-muted-foreground"),
                Div(cls="h-1.5 w-9 rounded bg-muted-foreground/20"),
                cls="flex items-center gap-1.5 px-2 py-1",
            ),
            Div(cls="my-0.5 h-px w-full bg-border"),
            # Sign out (default styling, not destructive)
            Div(
                Icon("lucide:log-out", width="8", height="8", cls="shrink-0 text-muted-foreground"),
                Div(cls="h-1.5 w-11 rounded bg-muted-foreground/20"),
                cls="flex items-center gap-1.5 px-2 py-1",
            ),
            cls="w-36 rounded-lg border border-border bg-background p-1 shadow-lg",
        ),
        cls="flex flex-col items-center gap-1.5",
    )


@with_code
def preview():
    return Div(
        Div(
            Span("Acme", cls="font-semibold tracking-tight"),
            Div(
                Icon("lucide:bell", cls="size-4 text-muted-foreground"),
                UserButton(
                    DropdownMenuGroup(
                        DropdownMenuItem(Icon("lucide:user"), "Profile"),
                        DropdownMenuItem(Icon("lucide:settings"), "Settings"),
                        DropdownMenuItem(Icon("lucide:credit-card"), "Billing"),
                    ),
                    DropdownMenuSeparator(),
                    DropdownMenuItem(Icon("lucide:log-out"), "Sign out"),
                    name="Sarah Miller",
                    email="sarah@example.com",
                    avatar_src="https://avatars.githubusercontent.com/u/1024025?v=4",
                    avatar_fallback="SM",
                ),
                cls="flex items-center gap-3",
            ),
            cls="flex h-14 items-center justify-between border-b border-border px-4",
        ),
        Div(cls="flex-1"),
        cls="flex min-h-[180px] w-full flex-col rounded-lg border bg-background",
    )


def create_user_button_01_docs():
    return auto_generate_block_page(
        TITLE,
        DESCRIPTION,
        preview_fn=preview,
        source_files=[
            {"name": "user_button.py", "content": (_BLOCK_DIR / "user_button.py").read_text()},
        ],
        cli_command="star add user-button-01",
        dependencies=["avatar", "dropdown_menu"],
    )
