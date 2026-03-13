"""
User Button 01 block documentation - Avatar + dropdown composition for auth actions.
"""

TITLE = "User Button 01"
DESCRIPTION = "A user avatar button with a dropdown menu for authentication and account actions."
CATEGORY = "blocks"
ORDER = 10
STATUS = "stable"

from pathlib import Path

from starhtml import Div, Icon
from components.dropdown_menu import (
    DropdownMenuGroup,
    DropdownMenuItem,
    DropdownMenuSeparator,
    DropdownMenuShortcut,
)
from blocks.user_button_01.user_button import UserButton
from utils import auto_generate_block_page, with_code

_BLOCK_DIR = Path(__file__).resolve().parents[3] / "registry" / "blocks" / "user_button_01"


@with_code
def preview():
    return Div(
        UserButton(
            DropdownMenuGroup(
                DropdownMenuItem(
                    Icon("lucide:user"),
                    "Profile",
                    DropdownMenuShortcut("\u2318P"),
                ),
                DropdownMenuItem(
                    Icon("lucide:settings"),
                    "Settings",
                    DropdownMenuShortcut("\u2318,"),
                ),
                DropdownMenuItem(
                    Icon("lucide:credit-card"),
                    "Billing",
                    DropdownMenuShortcut("\u2318B"),
                ),
            ),
            DropdownMenuSeparator(),
            DropdownMenuItem(
                Icon("lucide:log-out"),
                "Sign out",
                variant="destructive",
            ),
            name="Sarah Miller",
            email="sarah@example.com",
            avatar_src="https://avatars.githubusercontent.com/u/1024025?v=4",
            avatar_fallback="SM",
        ),
        cls="flex items-center justify-center min-h-[200px]",
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
