"""
Dropdown Menu component documentation - Contextual navigation and actions.
"""

# Component metadata for auto-discovery
TITLE = "Dropdown Menu"
DESCRIPTION = "Displays a menu of options that can be used for navigation, settings, or actions."
CATEGORY = "ui"
ORDER = 15
STATUS = "stable"

from starhtml import Div, P, Icon, Span, Strong, Code, H4, Signal
from starhtml.datastar import js
from starui.registry.components.dropdown_menu import (
    DropdownMenu, DropdownMenuTrigger, DropdownMenuContent, DropdownMenuItem,
    DropdownMenuCheckboxItem, DropdownMenuRadioGroup, DropdownMenuRadioItem,
    DropdownMenuSeparator, DropdownMenuLabel, DropdownMenuShortcut, DropdownMenuGroup
)
from starui.registry.components.button import Button
from starui.registry.components.utils import gen_id
from utils import auto_generate_page, with_code, Prop, Component, build_api_reference
from widgets.component_preview import ComponentPreview



# Basic menu with actions
@with_code
def basic_menu_example():
    return Div(
        DropdownMenu(
            DropdownMenuTrigger(
                Icon("lucide:settings", cls="mr-2 h-4 w-4"),
                "Settings",
                cls="w-32"
            ),
            DropdownMenuContent(
                DropdownMenuItem(
                    Icon("lucide:user", cls="mr-2 h-4 w-4"),
                    "Profile",
                    data_on_click=js("alert('Open Profile')")
                ),
                DropdownMenuItem(
                    Icon("lucide:credit-card", cls="mr-2 h-4 w-4"),
                    "Billing",
                    data_on_click=js("alert('Open Billing')")
                ),
                DropdownMenuItem(
                    Icon("lucide:settings", cls="mr-2 h-4 w-4"),
                    "Settings",
                    data_on_click=js("alert('Open Settings')")
                ),
                DropdownMenuSeparator(),
                DropdownMenuItem(
                    Icon("lucide:log-out", cls="mr-2 h-4 w-4"),
                    "Log out",
                    variant="destructive",
                    data_on_click=js("alert('Logging out')")
                )
            )
        ),
        cls="flex items-center justify-center min-h-[200px]"
    )


@with_code
def checkbox_menu_example():
    return Div(
        (show_grid := Signal("show_grid", True)),
        (show_rulers := Signal("show_rulers", False)),
        (show_guides := Signal("show_guides", True)),
        (auto_save := Signal("auto_save", True)),
        Div(
            Span("Grid: ", cls="text-muted-foreground"),
            Span(data_text=show_grid.if_("On", "Off"), cls="font-medium"),
            Span(" • ", cls="text-muted-foreground mx-1"),
            Span("Rulers: ", cls="text-muted-foreground"),
            Span(data_text=show_rulers.if_("On", "Off"), cls="font-medium"),
            Span(" • ", cls="text-muted-foreground mx-1"),
            Span("Guides: ", cls="text-muted-foreground"),
            Span(data_text=show_guides.if_("On", "Off"), cls="font-medium"),
            Span(" • ", cls="text-muted-foreground mx-1"),
            Span("Auto-save: ", cls="text-muted-foreground"),
            Span(data_text=auto_save.if_("On", "Off"), cls="font-medium"),
            cls="flex items-center flex-wrap gap-1 p-3 bg-muted/50 rounded-lg border border-border text-sm mb-4"
        ),
        Div(
            DropdownMenu(
                DropdownMenuTrigger(
                    Icon("lucide:eye", cls="mr-2 h-4 w-4"),
                    "View Options"
                ),
                DropdownMenuContent(
                    DropdownMenuLabel("Display Settings"),
                    DropdownMenuSeparator(),
                    DropdownMenuCheckboxItem("Show Grid", signal=show_grid),
                    DropdownMenuCheckboxItem("Show Rulers", signal=show_rulers),
                    DropdownMenuCheckboxItem("Show Guides", signal=show_guides),
                    DropdownMenuSeparator(),
                    DropdownMenuCheckboxItem("Auto-save", signal=auto_save)
                )
            ),
            cls="flex justify-center"
        ),
        cls="flex flex-col min-h-[200px] justify-center"
    )


@with_code
def radio_group_menu_example():
    return Div(
        (theme := Signal("theme", "system")),
        Div(
            Icon("lucide:palette", cls="h-4 w-4 text-muted-foreground"),
            Span("Current theme: ", cls="text-muted-foreground ml-2"),
            Strong(data_text=theme, cls="capitalize ml-1"),
            cls="flex items-center p-3 bg-muted/50 rounded-lg border border-border text-sm mb-4"
        ),
        Div(
            DropdownMenu(
                DropdownMenuTrigger(
                    Icon("lucide:palette", cls="mr-2 h-4 w-4"),
                    "Theme",
                    cls="w-32"
                ),
                DropdownMenuContent(
                    DropdownMenuLabel("Appearance"),
                    DropdownMenuSeparator(),
                    DropdownMenuRadioGroup(
                        DropdownMenuRadioItem(
                            Icon("lucide:sun", cls="mr-2 h-4 w-4"),
                            "Light",
                            value="light",
                            signal=theme
                        ),
                        DropdownMenuRadioItem(
                            Icon("lucide:moon", cls="mr-2 h-4 w-4"),
                            "Dark",
                            value="dark",
                            signal=theme
                        ),
                        DropdownMenuRadioItem(
                            Icon("lucide:laptop", cls="mr-2 h-4 w-4"),
                            "System",
                            value="system",
                            signal=theme
                        ),
                        signal=theme
                    )
                )
            ),
            cls="flex justify-center"
        ),
        cls="flex flex-col min-h-[200px] justify-center"
    )


@with_code
def context_menu_example():
    def create_menu_item_with_shortcut(icon, label, shortcut, action, variant=None):
        return DropdownMenuItem(
            Icon(icon, cls="mr-2 h-4 w-4"),
            Span(label, cls="flex-1"),
            Span(shortcut, cls="ml-auto text-xs tracking-widest text-muted-foreground"),
            data_on_click=js(f"alert('{action}')"),
            variant=variant
        )

    return Div(
        DropdownMenu(
        DropdownMenuTrigger(
            Icon("lucide:more-horizontal", cls="h-4 w-4"),
            variant="ghost",
            size="icon"
        ),
        DropdownMenuContent(
            DropdownMenuGroup(
                create_menu_item_with_shortcut("lucide:copy", "Copy", "⌘C", "Copy action"),
                create_menu_item_with_shortcut("lucide:scissors", "Cut", "⌘X", "Cut action"),
                create_menu_item_with_shortcut("lucide:clipboard", "Paste", "⌘V", "Paste action")
            ),
            DropdownMenuSeparator(),
            DropdownMenuGroup(
                create_menu_item_with_shortcut("lucide:search", "Find", "⌘F", "Find action"),
                create_menu_item_with_shortcut("lucide:repeat", "Replace", "⌘H", "Replace action")
            ),
            DropdownMenuSeparator(),
            create_menu_item_with_shortcut("lucide:trash", "Delete", "⌘⌫", "Delete action", "destructive"),
            align="end"
        )
    ),
        cls="flex items-center justify-center min-h-[200px]"
    )


# User profile menu
@with_code
def user_profile_menu_example():
    return Div(
        DropdownMenu(
        DropdownMenuTrigger(
            Div(
                Div(cls="w-8 h-8 bg-gradient-to-r from-purple-400 to-pink-400 rounded-full"),
                cls="flex items-center"
            ),
            variant="ghost",
            size="icon"
        ),
        DropdownMenuContent(
            DropdownMenuLabel(
                Div(
                    P("Sarah Chen", cls="font-medium"),
                    P("sarah@company.com", cls="text-xs text-muted-foreground"),
                    cls="space-y-1"
                )
            ),
            DropdownMenuSeparator(),
            DropdownMenuItem(
                Icon("lucide:user", cls="mr-2 h-4 w-4"),
                "Profile",
                data_on_click=js("alert('View Profile')")
            ),
            DropdownMenuItem(
                Icon("lucide:settings", cls="mr-2 h-4 w-4"),
                "Account Settings",
                data_on_click=js("alert('Account Settings')")
            ),
            DropdownMenuItem(
                Icon("lucide:bell", cls="mr-2 h-4 w-4"),
                "Notifications",
                data_on_click=js("alert('Notifications')")
            ),
            DropdownMenuSeparator(),
            DropdownMenuItem(
                Icon("lucide:help-circle", cls="mr-2 h-4 w-4"),
                "Help & Support",
                data_on_click=js("alert('Help & Support')")
            ),
            DropdownMenuItem(
                Icon("lucide:log-out", cls="mr-2 h-4 w-4"),
                "Sign Out",
                variant="destructive",
                data_on_click=js("alert('Signed out')")
            ),
            align="end"
        )
    ),
        cls="flex items-center justify-center min-h-[200px]"
    )


# Content management menu
@with_code
def creation_menu_example():
    return Div(
        (created := Signal("created", "")),
        Div(
            Div(
                Icon("lucide:plus-circle", cls="h-4 w-4 text-muted-foreground"),
                Span("Action: ", cls="text-muted-foreground ml-2 mr-1"),
                Span(data_text=created.or_("No action taken yet"), cls="font-medium italic"),
                cls="flex items-center"
            ),
            cls="p-3 bg-muted/50 rounded-lg border border-border text-sm mb-4"
        ),
        Div(
            DropdownMenu(
                DropdownMenuTrigger(
                    "Create New",
                    Icon("lucide:chevron-down", cls="ml-2 h-4 w-4"),
                    cls="w-36"
                ),
                DropdownMenuContent(
                    DropdownMenuGroup(
                        DropdownMenuItem(
                            Icon("lucide:file-text", cls="mr-2 h-4 w-4"),
                            "Document",
                            data_on_click=created.set('Document created')
                        ),
                        DropdownMenuItem(
                            Icon("lucide:table", cls="mr-2 h-4 w-4"),
                            "Spreadsheet",
                            data_on_click=created.set('Spreadsheet created')
                        ),
                        DropdownMenuItem(
                            Icon("lucide:presentation", cls="mr-2 h-4 w-4"),
                            "Presentation",
                            data_on_click=created.set('Presentation created')
                        )
                    ),
                    DropdownMenuSeparator(),
                    DropdownMenuGroup(
                        DropdownMenuItem(
                            Icon("lucide:folder-plus", cls="mr-2 h-4 w-4"),
                            "New Folder",
                            data_on_click=created.set('Folder created')
                        ),
                        DropdownMenuItem(
                            Icon("lucide:upload", cls="mr-2 h-4 w-4"),
                            "Upload File",
                            data_on_click=created.set('File uploaded')
                        )
                    )
                )
            ),
            cls="flex justify-center"
        ),
        cls="flex flex-col min-h-[200px] justify-center"
    )


@with_code
def complex_data_controls_example():
    sort_options = [
        ("name", "Name"),
        ("date", "Date Created"),
        ("size", "Size"),
        ("type", "Type")
    ]

    view_options = [
        ("grid", "Grid View"),
        ("list", "List View")
    ]

    return Div(
        (sort_by := Signal("sort_by", "name")),
        (ascending := Signal("ascending", True)),
        (view_mode := Signal("view_mode", "list")),
        (show_hidden := Signal("show_hidden", False)),
        (show_extensions := Signal("show_extensions", True)),
        Div(
            Div(
                Span("Sort: ", cls="text-muted-foreground"),
                Span(data_text=sort_by, cls="font-medium capitalize"),
                Span(" (", cls="text-muted-foreground"),
                Span(data_text=ascending.if_("Ascending", "Descending"), cls="font-medium"),
                Span(")", cls="text-muted-foreground"),
                Span(" • ", cls="text-muted-foreground mx-1"),
                Span("View: ", cls="text-muted-foreground"),
                Span(data_text=view_mode, cls="font-medium capitalize"),
                Span(" • ", cls="text-muted-foreground mx-1"),
                Span("Hidden: ", cls="text-muted-foreground"),
                Span(data_text=show_hidden.if_("On", "Off"), cls="font-medium"),
                Span(" • ", cls="text-muted-foreground mx-1"),
                Span("Extensions: ", cls="text-muted-foreground"),
                Span(data_text=show_extensions.if_("On", "Off"), cls="font-medium"),
                cls="flex items-center flex-wrap gap-1"
            ),
            cls="p-3 bg-muted/50 rounded-lg border border-border text-sm mb-4"
        ),
        Div(
            DropdownMenu(
                DropdownMenuTrigger(
                    "Sort By",
                    Icon("lucide:chevron-down", cls="ml-2 h-4 w-4"),
                    variant="outline",
                    cls="w-32"
                ),
                DropdownMenuContent(
                    DropdownMenuRadioGroup(
                        *[DropdownMenuRadioItem(label, value=value, signal=sort_by)
                          for value, label in sort_options],
                        signal=sort_by
                    ),
                    DropdownMenuSeparator(),
                    DropdownMenuCheckboxItem("Ascending", signal=ascending),
                    align="end"
                )
            ),
            DropdownMenu(
                DropdownMenuTrigger(
                    "View",
                    Icon("lucide:chevron-down", cls="ml-2 h-4 w-4"),
                    variant="outline",
                    cls="ml-2 w-28"
                ),
                DropdownMenuContent(
                    DropdownMenuCheckboxItem("Show Hidden Files", signal=show_hidden),
                    DropdownMenuCheckboxItem("Show File Extensions", signal=show_extensions),
                    DropdownMenuSeparator(),
                    DropdownMenuRadioGroup(
                        *[DropdownMenuRadioItem(label, value=value, signal=view_mode)
                          for value, label in view_options],
                        signal=view_mode
                    ),
                    align="start"
                )
            ),
            cls="flex items-center justify-center"
        ),
        cls="flex flex-col min-h-[200px] justify-center"
    )



EXAMPLES_DATA = [
    {"title": "Dropdown Menu", "description": "A simple dropdown menu with actions and a destructive item", "fn": basic_menu_example},
    {"title": "Checkbox Menu", "description": "Menu with toggleable options and live state display", "fn": checkbox_menu_example},
    {"title": "Radio Group Menu", "description": "Menu with mutually exclusive options", "fn": radio_group_menu_example},
    {"title": "Context Menu", "description": "Rich menu with keyboard shortcuts and grouped actions", "fn": context_menu_example},
    {"title": "User Profile Menu", "description": "Complete user menu with avatar, profile info, and account actions", "fn": user_profile_menu_example},
    {"title": "Creation Menu", "description": "Grouped menu for creating different types of content", "fn": creation_menu_example},
    {"title": "Complex Data Controls", "description": "Multiple coordinated menus for table/list management", "fn": complex_data_controls_example},
]

API_REFERENCE = build_api_reference(
    components=[
        Component("DropdownMenu", "Main container component for dropdown menus with positioning and state management"),
        Component("DropdownMenuTrigger", "Button or element that opens the dropdown menu when clicked"),
        Component("DropdownMenuContent", "Container for all dropdown menu items with proper positioning and styling"),
        Component("DropdownMenuItem", "Individual clickable menu item for actions and navigation"),
        Component("DropdownMenuCheckboxItem", "Menu item with checkbox state for toggleable options"),
        Component("DropdownMenuRadioGroup", "Container for radio button menu items with shared state"),
        Component("DropdownMenuRadioItem", "Menu item with radio button for single selection from group"),
        Component("DropdownMenuSeparator", "Visual separator line to organize menu sections"),
        Component("DropdownMenuLabel", "Text label for categorizing and organizing menu items"),
        Component("DropdownMenuShortcut", "Keyboard shortcut display for menu items"),
        Component("DropdownMenuGroup", "Logical grouping container for related menu items"),
    ]
)


def create_dropdown_menu_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)