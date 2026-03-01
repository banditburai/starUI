"""
Dropdown Menu component documentation - Contextual navigation and actions.
"""

# Component metadata for auto-discovery
TITLE = "Dropdown Menu"
DESCRIPTION = "Displays a menu of options that can be used for navigation, settings, or actions."
CATEGORY = "ui"
ORDER = 15
STATUS = "stable"

from starhtml import Div, Span, Strong, Icon, Signal
from starui.registry.components.dropdown_menu import (
    DropdownMenu, DropdownMenuTrigger, DropdownMenuContent, DropdownMenuItem,
    DropdownMenuCheckboxItem, DropdownMenuRadioGroup, DropdownMenuRadioItem,
    DropdownMenuSeparator, DropdownMenuLabel, DropdownMenuShortcut, DropdownMenuGroup,
    DropdownMenuSub, DropdownMenuSubTrigger, DropdownMenuSubContent,
)
from utils import auto_generate_page, with_code, Component, build_api_reference


@with_code
def hero_example():
    return Div(
        DropdownMenu(
            DropdownMenuTrigger(
                Icon("lucide:menu"),
                "Actions",
            ),
            DropdownMenuContent(
                DropdownMenuLabel("My Account"),
                DropdownMenuSeparator(),
                DropdownMenuGroup(
                    DropdownMenuItem(
                        Icon("lucide:user"),
                        "Profile",
                        DropdownMenuShortcut("⌘P"),
                    ),
                    DropdownMenuItem(
                        Icon("lucide:settings"),
                        "Settings",
                        DropdownMenuShortcut("⌘,"),
                    ),
                    DropdownMenuItem(
                        Icon("lucide:keyboard"),
                        "Keyboard Shortcuts",
                        DropdownMenuShortcut("⌘K"),
                    ),
                ),
                DropdownMenuSeparator(),
                DropdownMenuGroup(
                    DropdownMenuItem(
                        Icon("lucide:users"),
                        "Team",
                    ),
                    DropdownMenuSub(
                        DropdownMenuSubTrigger(
                            Icon("lucide:user-plus"),
                            "Invite Users",
                        ),
                        DropdownMenuSubContent(
                            DropdownMenuItem("Email"),
                            DropdownMenuItem("Message"),
                            DropdownMenuSeparator(),
                            DropdownMenuItem("More...", disabled=True),
                        ),
                    ),
                ),
                DropdownMenuSeparator(),
                DropdownMenuItem(
                    Icon("lucide:log-out"),
                    "Log Out",
                    DropdownMenuShortcut("⇧⌘Q"),
                    variant="destructive",
                ),
            ),
        ),
        cls="flex items-center justify-center min-h-[200px]",
    )


@with_code
def submenu_example():
    return Div(
        DropdownMenu(
            DropdownMenuTrigger(
                Icon("lucide:share-2"),
                "Share",
            ),
            DropdownMenuContent(
                DropdownMenuItem(
                    Icon("lucide:link"),
                    "Copy Link",
                    DropdownMenuShortcut("⌘L"),
                ),
                DropdownMenuSeparator(),
                DropdownMenuSub(
                    DropdownMenuSubTrigger(
                        Icon("lucide:send"),
                        "Send to...",
                    ),
                    DropdownMenuSubContent(
                        DropdownMenuItem(
                            Icon("lucide:mail"),
                            "Email",
                        ),
                        DropdownMenuItem(
                            Icon("lucide:message-circle"),
                            "Slack",
                        ),
                        DropdownMenuSeparator(),
                        DropdownMenuItem(
                            Icon("lucide:message-square"),
                            "Teams",
                            disabled=True,
                        ),
                    ),
                ),
                DropdownMenuSub(
                    DropdownMenuSubTrigger(
                        Icon("lucide:download"),
                        "Export as...",
                    ),
                    DropdownMenuSubContent(
                        DropdownMenuItem("PDF"),
                        DropdownMenuItem("CSV"),
                        DropdownMenuItem("JSON"),
                    ),
                ),
            ),
        ),
        cls="flex items-center justify-center min-h-[200px]",
    )


@with_code
def checkbox_example():
    return Div(
        (show_grid := Signal("show_grid", True)),
        (show_rulers := Signal("show_rulers", False)),
        (auto_save := Signal("auto_save", True)),
        Div(
            Span("Grid: ", cls="text-muted-foreground"),
            Span(data_text=show_grid.if_("On", "Off"), cls="font-medium"),
            Span(" · ", cls="text-muted-foreground mx-1"),
            Span("Rulers: ", cls="text-muted-foreground"),
            Span(data_text=show_rulers.if_("On", "Off"), cls="font-medium"),
            Span(" · ", cls="text-muted-foreground mx-1"),
            Span("Auto-save: ", cls="text-muted-foreground"),
            Span(data_text=auto_save.if_("On", "Off"), cls="font-medium"),
            cls="flex items-center flex-wrap gap-1 p-3 bg-muted/50 rounded-lg border border-border text-sm mb-4"
        ),
        Div(
            DropdownMenu(
                DropdownMenuTrigger(
                    Icon("lucide:eye"),
                    "View Options"
                ),
                DropdownMenuContent(
                    DropdownMenuLabel("Display"),
                    DropdownMenuSeparator(),
                    DropdownMenuCheckboxItem("Show Grid", signal=show_grid),
                    DropdownMenuCheckboxItem("Show Rulers", signal=show_rulers),
                    DropdownMenuSeparator(),
                    DropdownMenuCheckboxItem("Auto-save", signal=auto_save),
                )
            ),
            cls="flex justify-center"
        ),
        cls="flex flex-col min-h-[200px] justify-center"
    )


@with_code
def radio_group_example():
    return Div(
        (theme := Signal("dm_theme", "system")),
        Div(
            Icon("lucide:palette", cls="size-4 text-muted-foreground"),
            Span("Current theme: ", cls="text-muted-foreground ml-2"),
            Strong(data_text=theme, cls="capitalize ml-1"),
            cls="flex items-center p-3 bg-muted/50 rounded-lg border border-border text-sm mb-4"
        ),
        Div(
            DropdownMenu(
                DropdownMenuTrigger(
                    Icon("lucide:palette"),
                    "Theme",
                    cls="w-32"
                ),
                DropdownMenuContent(
                    DropdownMenuLabel("Appearance"),
                    DropdownMenuSeparator(),
                    DropdownMenuRadioGroup(
                        DropdownMenuRadioItem(
                            Icon("lucide:sun"),
                            "Light",
                            value="light",
                        ),
                        DropdownMenuRadioItem(
                            Icon("lucide:moon"),
                            "Dark",
                            value="dark",
                        ),
                        DropdownMenuRadioItem(
                            Icon("lucide:laptop"),
                            "System",
                            value="system",
                        ),
                        signal=theme,
                    ),
                ),
            ),
            cls="flex justify-center"
        ),
        cls="flex flex-col min-h-[200px] justify-center"
    )


@with_code
def shortcuts_example():
    return Div(
        DropdownMenu(
            DropdownMenuTrigger(
                Icon("lucide:more-horizontal"),
                variant="ghost",
                size="icon",
                aria_label="More actions",
            ),
            DropdownMenuContent(
                DropdownMenuGroup(
                    DropdownMenuItem(
                        Icon("lucide:copy"),
                        "Copy",
                        DropdownMenuShortcut("⌘C"),
                    ),
                    DropdownMenuItem(
                        Icon("lucide:scissors"),
                        "Cut",
                        DropdownMenuShortcut("⌘X"),
                    ),
                    DropdownMenuItem(
                        Icon("lucide:clipboard"),
                        "Paste",
                        DropdownMenuShortcut("⌘V"),
                        disabled=True,
                    ),
                ),
                DropdownMenuSeparator(),
                DropdownMenuGroup(
                    DropdownMenuItem(
                        Icon("lucide:search"),
                        "Find",
                        DropdownMenuShortcut("⌘F"),
                    ),
                    DropdownMenuItem(
                        Icon("lucide:repeat"),
                        "Replace",
                        DropdownMenuShortcut("⌘H"),
                    ),
                ),
                DropdownMenuSeparator(),
                DropdownMenuItem(
                    Icon("lucide:trash"),
                    "Delete",
                    DropdownMenuShortcut("⌘⌫"),
                    variant="destructive",
                ),
                align="end",
            ),
        ),
        cls="flex items-center justify-center min-h-[200px]",
    )


EXAMPLES_DATA = [
    {
        "title": "Dropdown Menu",
        "description": "Full-featured menu with label, groups, shortcuts, a submenu, a disabled item, and a destructive action. Shows the complete composition pattern in one example.",
        "fn": hero_example,
    },
    {
        "title": "Submenu",
        "description": "Nested menus using DropdownMenuSub, SubTrigger, and SubContent. The chevron-right icon is added automatically. Two independent submenus demonstrate cascading navigation.",
        "fn": submenu_example,
    },
    {
        "title": "Checkbox Items",
        "description": "Toggle settings on and off with DropdownMenuCheckboxItem. Each item binds to a boolean signal — the status bar above reflects state changes in real time.",
        "fn": checkbox_example,
    },
    {
        "title": "Radio Group",
        "description": "Single-select within a group via shared signal on DropdownMenuRadioGroup. Selecting one item deselects the others automatically.",
        "fn": radio_group_example,
    },
    {
        "title": "Shortcuts",
        "description": "Icon-button trigger (variant='ghost', size='icon') with DropdownMenuShortcut for keyboard hints. Groups separate related actions. Paste is disabled to show the disabled state.",
        "fn": shortcuts_example,
    },
]

API_REFERENCE = build_api_reference(
    components=[
        Component("DropdownMenu", "Root container with signal-driven open state"),
        Component("DropdownMenuTrigger", "Button that toggles the menu via popover API"),
        Component("DropdownMenuContent", "Positioned content panel with side, align, and side_offset"),
        Component("DropdownMenuItem", "Clickable item with optional icon, variant, disabled, and inset"),
        Component("DropdownMenuCheckboxItem", "Toggleable item bound to a boolean signal"),
        Component("DropdownMenuRadioGroup", "Container for mutually exclusive radio items sharing a signal"),
        Component("DropdownMenuRadioItem", "Single-select item within a radio group"),
        Component("DropdownMenuSub", "Wrapper for nested submenu with its own open state"),
        Component("DropdownMenuSubTrigger", "Item that opens a submenu (chevron-right added automatically)"),
        Component("DropdownMenuSubContent", "Positioned panel for submenu items"),
        Component("DropdownMenuSeparator", "Horizontal rule between menu sections"),
        Component("DropdownMenuLabel", "Non-interactive heading with optional inset alignment"),
        Component("DropdownMenuShortcut", "Right-aligned keyboard shortcut hint"),
        Component("DropdownMenuGroup", "Semantic grouping container for related items"),
    ]
)


def create_dropdown_menu_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)
