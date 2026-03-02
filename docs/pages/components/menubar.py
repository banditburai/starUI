"""
Menubar component documentation - Desktop-style persistent menu bar.
"""

# Component metadata for auto-discovery
TITLE = "Menubar"
DESCRIPTION = "A visually persistent menu common in desktop applications that provides quick access to a consistent set of commands."
CATEGORY = "ui"
ORDER = 55
STATUS = "stable"

from starhtml import Div, Icon, Signal
from components.menubar import (
    Menubar,
    MenubarCheckboxItem,
    MenubarContent,
    MenubarItem,
    MenubarLabel,
    MenubarMenu,
    MenubarRadioGroup,
    MenubarRadioItem,
    MenubarSeparator,
    MenubarShortcut,
    MenubarSub,
    MenubarSubContent,
    MenubarSubTrigger,
    MenubarTrigger,
)
from utils import auto_generate_page, with_code, Component, build_api_reference


@with_code
def hero_example():
    return Div(
        (show_bookmarks := Signal("hero_bookmarks", True)),  #: hide
        (show_urls := Signal("hero_urls", False)),  #: hide
        (profile := Signal("hero_profile", "benoit")),  #: hide
        Menubar(
            MenubarMenu(
                MenubarTrigger("File"),
                MenubarContent(
                    MenubarItem("New Tab", MenubarShortcut("⌘T")),
                    MenubarItem("New Window", MenubarShortcut("⌘N")),
                    MenubarItem("New Incognito Window", disabled=True),
                    MenubarSeparator(),
                    MenubarSub(
                        MenubarSubTrigger("Share"),
                        MenubarSubContent(
                            MenubarItem(Icon("lucide:mail"), "Email"),
                            MenubarItem(Icon("lucide:message-circle"), "Message"),
                            MenubarSeparator(),
                            MenubarItem(Icon("lucide:notebook"), "Notes"),
                        ),
                    ),
                    MenubarSeparator(),
                    MenubarItem("Print", MenubarShortcut("⌘P")),
                ),
            ),
            MenubarMenu(
                MenubarTrigger("Edit"),
                MenubarContent(
                    MenubarItem("Undo", MenubarShortcut("⌘Z")),
                    MenubarItem("Redo", MenubarShortcut("⇧⌘Z")),
                    MenubarSeparator(),
                    MenubarItem("Find", MenubarShortcut("⌘F")),
                    MenubarItem("Find and Replace", MenubarShortcut("⌘⇧H")),
                    MenubarSeparator(),
                    MenubarItem("Cut"),
                    MenubarItem("Copy"),
                    MenubarItem("Paste"),
                ),
            ),
            MenubarMenu(
                MenubarTrigger("View"),
                MenubarContent(
                    MenubarCheckboxItem("Always Show Bookmarks Bar", signal=show_bookmarks),
                    MenubarCheckboxItem("Always Show Full URLs", signal=show_urls),
                    MenubarSeparator(),
                    MenubarItem("Reload", MenubarShortcut("⌘R"), inset=True),
                    MenubarItem("Force Reload", MenubarShortcut("⇧⌘R"), inset=True, disabled=True),
                    MenubarSeparator(),
                    MenubarItem("Toggle Fullscreen", inset=True),
                    MenubarSeparator(),
                    MenubarItem("Hide Sidebar", inset=True),
                ),
            ),
            MenubarMenu(
                MenubarTrigger("Profiles"),
                MenubarContent(
                    MenubarRadioGroup(
                        MenubarRadioItem("Andy", value="andy"),
                        MenubarRadioItem("Benoit", value="benoit"),
                        MenubarRadioItem("Luis", value="luis"),
                        signal=profile,
                    ),
                    MenubarSeparator(),
                    MenubarItem("Edit…", inset=True),
                    MenubarSeparator(),
                    MenubarItem("Add Profile…", inset=True),
                ),
            ),
        ),
    )


@with_code
def minimal_example():
    return Menubar(
        MenubarMenu(
            MenubarTrigger("File"),
            MenubarContent(
                MenubarItem("New", MenubarShortcut("⌘N")),
                MenubarItem("Open…", MenubarShortcut("⌘O")),
                MenubarItem("Save", MenubarShortcut("⌘S")),
                MenubarSeparator(),
                MenubarItem("Quit", MenubarShortcut("⌘Q")),
            ),
        ),
        MenubarMenu(
            MenubarTrigger("Help"),
            MenubarContent(
                MenubarItem("Documentation"),
                MenubarItem("Release Notes"),
                MenubarSeparator(),
                MenubarItem("About"),
            ),
        ),
    )


@with_code
def labels_example():
    return Div(
        (sidebar := Signal("show_sidebar", True)),
        (console := Signal("show_console", False)),
        (terminal := Signal("show_terminal", True)),
        (theme := Signal("editor_theme", "system")),
        Menubar(
            MenubarMenu(
                MenubarTrigger("View"),
                MenubarContent(
                    MenubarLabel("Appearance"),
                    MenubarRadioGroup(
                        MenubarRadioItem(Icon("lucide:sun"), "Light", value="light"),
                        MenubarRadioItem(Icon("lucide:moon"), "Dark", value="dark"),
                        MenubarRadioItem(Icon("lucide:laptop"), "System", value="system"),
                        signal=theme,
                    ),
                    MenubarSeparator(),
                    MenubarLabel("Panels"),
                    MenubarCheckboxItem("Sidebar", signal=sidebar),
                    MenubarCheckboxItem("Console", signal=console),
                    MenubarCheckboxItem("Terminal", signal=terminal),
                ),
            ),
            MenubarMenu(
                MenubarTrigger("Canvas"),
                MenubarContent(
                    MenubarLabel("Zoom"),
                    MenubarItem("Zoom In", MenubarShortcut("⌘+")),
                    MenubarItem("Zoom Out", MenubarShortcut("⌘−")),
                    MenubarItem("Fit to Screen", MenubarShortcut("⌘0")),
                    MenubarSeparator(),
                    MenubarLabel("Snap"),
                    MenubarCheckboxItem("Show Grid", signal=Signal("show_grid", True)),
                    MenubarCheckboxItem("Snap to Grid", signal=Signal("snap_grid", False)),
                ),
            ),
        ),
    )


@with_code
def submenu_example():
    return Menubar(
        MenubarMenu(
            MenubarTrigger("File"),
            MenubarContent(
                MenubarItem("New Tab", MenubarShortcut("⌘T")),
                MenubarSeparator(),
                MenubarSub(
                    MenubarSubTrigger("Open Recent"),
                    MenubarSubContent(
                        MenubarItem("project-alpha.py"),
                        MenubarItem("notes.md"),
                        MenubarItem("config.toml"),
                        MenubarSeparator(),
                        MenubarItem("Clear Recent"),
                    ),
                ),
                MenubarSeparator(),
                MenubarItem("Save", MenubarShortcut("⌘S")),
                MenubarItem("Save As…", MenubarShortcut("⇧⌘S")),
            ),
        ),
        MenubarMenu(
            MenubarTrigger("Edit"),
            MenubarContent(
                MenubarSub(
                    MenubarSubTrigger("Find"),
                    MenubarSubContent(
                        MenubarItem("Find…", MenubarShortcut("⌘F")),
                        MenubarItem("Find Next", MenubarShortcut("⌘G")),
                        MenubarItem("Find Previous", MenubarShortcut("⇧⌘G")),
                    ),
                ),
                MenubarSub(
                    MenubarSubTrigger("Replace"),
                    MenubarSubContent(
                        MenubarItem("Replace…", MenubarShortcut("⌘H")),
                        MenubarItem("Replace All", MenubarShortcut("⇧⌘H")),
                    ),
                ),
            ),
        ),
    )


@with_code
def icons_example():
    return Menubar(
        MenubarMenu(
            MenubarTrigger("File"),
            MenubarContent(
                MenubarItem(Icon("lucide:plus"), "New Tab", MenubarShortcut("⌘T")),
                MenubarItem(Icon("lucide:app-window"), "New Window", MenubarShortcut("⌘N")),
                MenubarSeparator(),
                MenubarItem(Icon("lucide:share"), "Share"),
            ),
        ),
        MenubarMenu(
            MenubarTrigger("More"),
            MenubarContent(
                MenubarItem(Icon("lucide:settings"), "Settings"),
                MenubarSeparator(),
                MenubarItem(Icon("lucide:flag"), "Report Issue"),
                MenubarSeparator(),
                MenubarItem(Icon("lucide:log-out"), "Log Out", MenubarShortcut("⇧⌘Q"), variant="destructive"),
            ),
        ),
    )


EXAMPLES_DATA = [
    {
        "title": "Menubar",
        "description": "Complete menubar with File, Edit, View, and Profiles menus. Demonstrates items with shortcuts, a disabled item, a submenu, checkbox items with inset alignment, and a radio group for profile selection — all in one persistent bar.",
        "fn": hero_example,
        "preview_class": "[&>*]:w-full [&>*]:max-w-2xl",
    },
    {
        "title": "Minimal",
        "description": "Two menus, five items — the smallest useful menubar. A good starting point for adding a menu bar to any app.",
        "fn": minimal_example,
    },
    {
        "title": "With Labels",
        "description": "MenubarLabel adds non-interactive section headings inside menus. This design-tool menubar groups appearance, panel toggles, and canvas settings under labeled sections.",
        "fn": labels_example,
    },
    {
        "title": "Submenus",
        "description": "Nested menus using MenubarSub, MenubarSubTrigger, and MenubarSubContent. File has a recent-files submenu; Edit cascades Find and Replace into their own sub-panels.",
        "fn": submenu_example,
    },
    {
        "title": "With Icons",
        "description": "Icons paired with menu items. The destructive Log Out variant renders both icon and text in the destructive color.",
        "fn": icons_example,
    },
]

API_REFERENCE = build_api_reference(
    components=[
        Component("Menubar", "Root container managing active menu state via signal"),
        Component("MenubarMenu", "Wrapper for a single menu (trigger + content pair)"),
        Component(
            "MenubarTrigger",
            "Button that opens the menu; supports hover-open when another menu is active",
        ),
        Component(
            "MenubarContent",
            "Positioned content panel with side, align, and side_offset",
        ),
        Component(
            "MenubarItem",
            "Clickable item with optional icon, variant, disabled, and inset",
        ),
        Component("MenubarCheckboxItem", "Toggleable item bound to a boolean signal"),
        Component(
            "MenubarRadioGroup",
            "Container for mutually exclusive radio items sharing a signal",
        ),
        Component("MenubarRadioItem", "Single-select item within a radio group"),
        Component("MenubarSub", "Wrapper for nested submenu with its own open state"),
        Component(
            "MenubarSubTrigger",
            "Item that opens a submenu (chevron-right added automatically)",
        ),
        Component("MenubarSubContent", "Positioned panel for submenu items"),
        Component("MenubarSeparator", "Horizontal rule between menu sections"),
        Component(
            "MenubarLabel",
            "Non-interactive heading with optional inset alignment",
        ),
        Component("MenubarShortcut", "Right-aligned keyboard shortcut hint"),
    ]
)


def create_menubar_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)
