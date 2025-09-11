"""
Dropdown Menu component documentation - Contextual navigation and actions.
"""

# Component metadata for auto-discovery
TITLE = "Dropdown Menu"
DESCRIPTION = "Displays a menu of options that can be used for navigation, settings, or actions."
CATEGORY = "ui"
ORDER = 15
STATUS = "stable"

from uuid import uuid4
from starhtml import Div, P, Icon, Span, Strong, Code, H4
from starhtml.datastar import ds_signals, ds_text, ds_on_click, value
from starui.registry.components.dropdown_menu import (
    DropdownMenu, DropdownMenuTrigger, DropdownMenuContent, DropdownMenuItem,
    DropdownMenuCheckboxItem, DropdownMenuRadioGroup, DropdownMenuRadioItem,
    DropdownMenuSeparator, DropdownMenuLabel, DropdownMenuShortcut, DropdownMenuGroup
)
from starui.registry.components.button import Button
from utils import auto_generate_page, with_code, Prop, Component, build_api_reference
from widgets.component_preview import ComponentPreview


def examples():
    """Generate dropdown menu examples using ComponentPreview with tabs."""
    
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
                    onclick="alert('Open Profile')"
                ),
                DropdownMenuItem(
                    Icon("lucide:credit-card", cls="mr-2 h-4 w-4"),
                    "Billing",
                    onclick="alert('Open Billing')"
                ),
                DropdownMenuItem(
                    Icon("lucide:settings", cls="mr-2 h-4 w-4"),
                    "Settings",
                    onclick="alert('Open Settings')"
                ),
                DropdownMenuSeparator(),
                DropdownMenuItem(
                    Icon("lucide:log-out", cls="mr-2 h-4 w-4"),
                    "Log out",
                    variant="destructive",
                    onclick="alert('Logging out')"
                )
            )
        ),
            cls="flex items-center justify-center min-h-[200px]"
        )
    
    yield ComponentPreview(
        basic_menu_example(),
        basic_menu_example.code,
        title="Basic Menu",
        description="A simple dropdown menu with actions and a destructive item"
    )
    
    # Menu with checkboxes for preferences
    @with_code
    def checkbox_menu_example():
        checkbox_signal_id = uuid4().hex[:8]
        return Div(
            Div(
                Div(
                    Span("Grid: ", cls="text-muted-foreground"),
                    Span(ds_text("$show_grid ? 'On' : 'Off'"), cls="font-medium"),
                    Span(" • ", cls="text-muted-foreground mx-1"),
                    Span("Rulers: ", cls="text-muted-foreground"),
                    Span(ds_text("$show_rulers ? 'On' : 'Off'"), cls="font-medium"),
                    Span(" • ", cls="text-muted-foreground mx-1"),
                    Span("Guides: ", cls="text-muted-foreground"),
                    Span(ds_text("$show_guides ? 'On' : 'Off'"), cls="font-medium"),
                    Span(" • ", cls="text-muted-foreground mx-1"),
                    Span("Auto-save: ", cls="text-muted-foreground"),
                    Span(ds_text("$auto_save ? 'On' : 'Off'"), cls="font-medium"),
                    cls="flex items-center flex-wrap gap-1"
                ),
                cls="p-3 bg-muted/50 rounded-lg border border-border text-sm mb-4"
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
                        DropdownMenuCheckboxItem(
                            "Show Grid",
                            signal="show_grid"
                        ),
                        DropdownMenuCheckboxItem(
                            "Show Rulers",
                            signal="show_rulers"
                        ),
                        DropdownMenuCheckboxItem(
                            "Show Guides",
                            signal="show_guides"
                        ),
                        DropdownMenuSeparator(),
                        DropdownMenuCheckboxItem(
                            "Auto-save",
                            signal="auto_save"
                        )
                    ),
                    signal=f"view_menu_{checkbox_signal_id}"
                ),
                cls="flex justify-center"
            ),
            ds_signals(show_grid=True, show_rulers=False, show_guides=True, auto_save=True),
            cls="flex flex-col min-h-[200px] justify-center"
        )
    
    yield ComponentPreview(
        checkbox_menu_example(),
        checkbox_menu_example.code,
        title="Checkbox Menu",
        description="Menu with toggleable options and live state display"
    )
    
    # Radio group menu for selections
    @with_code
    def radio_group_menu_example():
        signal_id2 = uuid4().hex[:8]
        return Div(
            Div(
                Div(
                    Icon("lucide:palette", cls="h-4 w-4 text-muted-foreground"),
                    Span("Current theme: ", cls="text-muted-foreground ml-2"),
                    Strong(ds_text("$theme"), cls="capitalize ml-1"),
                    cls="flex items-center"
                ),
                cls="p-3 bg-muted/50 rounded-lg border border-border text-sm mb-4"
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
                                signal="theme"
                            ),
                            DropdownMenuRadioItem(
                                Icon("lucide:moon", cls="mr-2 h-4 w-4"),
                                "Dark", 
                                value="dark",
                                signal="theme"
                            ),
                            DropdownMenuRadioItem(
                                Icon("lucide:laptop", cls="mr-2 h-4 w-4"),
                                "System",
                                value="system", 
                                signal="theme"
                            ),
                            signal="theme"
                        )
                    ),
                    signal=f"theme_menu_{signal_id2}"
                ),
                cls="flex justify-center"
            ),
            ds_signals(theme=value("system")),
            cls="flex flex-col min-h-[200px] justify-center"
        )
    
    yield ComponentPreview(
        radio_group_menu_example(),
        radio_group_menu_example.code,
        title="Radio Group Menu",
        description="Menu with mutually exclusive options"
    )
    
    # Advanced menu with shortcuts and grouping
    @with_code
    def context_menu_example():
        return Div(
            DropdownMenu(
            DropdownMenuTrigger(
                Icon("lucide:more-horizontal", cls="h-4 w-4"),
                variant="ghost",
                size="icon"
            ),
            DropdownMenuContent(
                DropdownMenuGroup(
                    DropdownMenuItem(
                        Icon("lucide:copy", cls="mr-2 h-4 w-4"),
                        Span("Copy", cls="flex-1"),
                        Span("⌘C", cls="ml-auto text-xs tracking-widest text-muted-foreground"),
                        onclick="alert('Copy action')"
                    ),
                    DropdownMenuItem(
                        Icon("lucide:scissors", cls="mr-2 h-4 w-4"),
                        Span("Cut", cls="flex-1"),
                        Span("⌘X", cls="ml-auto text-xs tracking-widest text-muted-foreground"),
                        onclick="alert('Cut action')"
                    ),
                    DropdownMenuItem(
                        Icon("lucide:clipboard", cls="mr-2 h-4 w-4"),
                        Span("Paste", cls="flex-1"),
                        Span("⌘V", cls="ml-auto text-xs tracking-widest text-muted-foreground"),
                        onclick="alert('Paste action')"
                    )
                ),
                DropdownMenuSeparator(),
                DropdownMenuGroup(
                    DropdownMenuItem(
                        Icon("lucide:search", cls="mr-2 h-4 w-4"),
                        Span("Find", cls="flex-1"),
                        Span("⌘F", cls="ml-auto text-xs tracking-widest text-muted-foreground"),
                        onclick="alert('Find action')"
                    ),
                    DropdownMenuItem(
                        Icon("lucide:repeat", cls="mr-2 h-4 w-4"),
                        Span("Replace", cls="flex-1"),
                        Span("⌘H", cls="ml-auto text-xs tracking-widest text-muted-foreground"),
                        onclick="alert('Replace action')"
                    )
                ),
                DropdownMenuSeparator(),
                DropdownMenuItem(
                    Icon("lucide:trash", cls="mr-2 h-4 w-4"),
                    Span("Delete", cls="flex-1"),
                    Span("⌘⌫", cls="ml-auto text-xs tracking-widest text-muted-foreground"),
                    variant="destructive",
                    onclick="alert('Delete action')"
                ),
                align="end"
            )
        ),
            cls="flex items-center justify-center min-h-[200px]"
        )
    
    yield ComponentPreview(
        context_menu_example(),
        context_menu_example.code,
        title="Context Menu",
        description="Rich menu with keyboard shortcuts and grouped actions"
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
                    onclick="alert('View Profile')"
                ),
                DropdownMenuItem(
                    Icon("lucide:settings", cls="mr-2 h-4 w-4"),
                    "Account Settings",
                    onclick="alert('Account Settings')"
                ),
                DropdownMenuItem(
                    Icon("lucide:bell", cls="mr-2 h-4 w-4"),
                    "Notifications",
                    onclick="alert('Notifications')"
                ),
                DropdownMenuSeparator(),
                DropdownMenuItem(
                    Icon("lucide:help-circle", cls="mr-2 h-4 w-4"),
                    "Help & Support",
                    onclick="alert('Help & Support')"
                ),
                DropdownMenuItem(
                    Icon("lucide:log-out", cls="mr-2 h-4 w-4"),
                    "Sign Out",
                    variant="destructive",
                    onclick="alert('Signed out')"
                ),
                align="end"
            )
        ),
            cls="flex items-center justify-center min-h-[200px]"
        )
    
    yield ComponentPreview(
        user_profile_menu_example(),
        user_profile_menu_example.code,
        title="User Profile Menu",
        description="Complete user menu with avatar, profile info, and account actions"
    )
    
    # Content management menu
    @with_code
    def creation_menu_example():
        signal_id3 = uuid4().hex[:8]
        return Div(
            Div(
                Div(
                    Icon("lucide:plus-circle", cls="h-4 w-4 text-muted-foreground"),
                    Span("Action: ", cls="text-muted-foreground ml-2 mr-1"),
                    Span(ds_text("$created || 'No action taken yet'"), cls="font-medium italic"),
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
                                onclick=f"$created = 'Document created'"
                            ),
                            DropdownMenuItem(
                                Icon("lucide:table", cls="mr-2 h-4 w-4"),
                                "Spreadsheet",
                                onclick=f"$created = 'Spreadsheet created'"
                            ),
                            DropdownMenuItem(
                                Icon("lucide:presentation", cls="mr-2 h-4 w-4"),
                                "Presentation",
                                onclick=f"$created = 'Presentation created'"
                            )
                        ),
                        DropdownMenuSeparator(),
                        DropdownMenuGroup(
                            DropdownMenuItem(
                                Icon("lucide:folder-plus", cls="mr-2 h-4 w-4"),
                                "New Folder",
                                onclick=f"$created = 'Folder created'"
                            ),
                            DropdownMenuItem(
                                Icon("lucide:upload", cls="mr-2 h-4 w-4"),
                                "Upload File",
                                onclick=f"$created = 'File uploaded'"
                            )
                        )
                    ),
                    signal=f"create_menu_{signal_id3}"
                ),
                cls="flex justify-center"
            ),
            ds_signals(created=value("")),
            cls="flex flex-col min-h-[200px] justify-center"
        )
    
    yield ComponentPreview(
        creation_menu_example(),
        creation_menu_example.code,
        title="Creation Menu",
        description="Grouped menu for creating different types of content"
    )
    
    # Complex sorting menu with state
    @with_code
    def complex_data_controls_example():
        signal_id4 = uuid4().hex[:8]
        return Div(
            Div(
                Div(
                    Span("Sort: ", cls="text-muted-foreground"),
                    Span(ds_text("$sort_by"), cls="font-medium capitalize"),
                    Span(" (", cls="text-muted-foreground"),
                    Span(ds_text('$ascending ? "Ascending" : "Descending"'), cls="font-medium"),
                    Span(")", cls="text-muted-foreground"),
                    Span(" • ", cls="text-muted-foreground mx-1"),
                    Span("View: ", cls="text-muted-foreground"),
                    Span(ds_text("$view_mode"), cls="font-medium capitalize"),
                    Span(" • ", cls="text-muted-foreground mx-1"),
                    Span("Hidden: ", cls="text-muted-foreground"),
                    Span(ds_text('$show_hidden ? "On" : "Off"'), cls="font-medium"),
                    Span(" • ", cls="text-muted-foreground mx-1"),
                    Span("Extensions: ", cls="text-muted-foreground"),
                    Span(ds_text('$show_extensions ? "On" : "Off"'), cls="font-medium"),
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
                            DropdownMenuRadioItem(
                                "Name",
                                value="name",
                                signal="sort_by"
                            ),
                            DropdownMenuRadioItem(
                                "Date Created",
                                value="date",
                                signal="sort_by"
                            ),
                            DropdownMenuRadioItem(
                                "Size",
                                value="size",
                                signal="sort_by"
                            ),
                            DropdownMenuRadioItem(
                                "Type",
                                value="type",
                                signal="sort_by"
                            ),
                            signal="sort_by"
                        ),
                        DropdownMenuSeparator(),
                        DropdownMenuCheckboxItem(
                            "Ascending",
                            signal="ascending"
                        ),
                        align="end"
                    ),
                    signal=f"sort_menu_{signal_id4}"
                ),
                DropdownMenu(
                    DropdownMenuTrigger(
                        "View",
                        Icon("lucide:chevron-down", cls="ml-2 h-4 w-4"),
                        variant="outline",
                        cls="ml-2 w-28"
                    ),
                    DropdownMenuContent(
                        DropdownMenuCheckboxItem(
                            "Show Hidden Files",
                            signal="show_hidden"
                        ),
                        DropdownMenuCheckboxItem(
                            "Show File Extensions",
                            signal="show_extensions"
                        ),
                        DropdownMenuSeparator(),
                        DropdownMenuRadioGroup(
                            DropdownMenuRadioItem(
                                "Grid View",
                                value="grid",
                                signal="view_mode"
                            ),
                            DropdownMenuRadioItem(
                                "List View", 
                                value="list",
                                signal="view_mode"
                            ),
                            signal="view_mode"
                        ),
                        align="start"
                    ),
                    signal=f"view_menu_{signal_id4}"
                ),
                cls="flex items-center justify-center"
            ),
            ds_signals(sort_by=value("name"), ascending=True, view_mode=value("list"), show_hidden=False, show_extensions=True),
            cls="flex flex-col min-h-[200px] justify-center"
        )
    
    yield ComponentPreview(
        complex_data_controls_example(),
        complex_data_controls_example.code,
        title="Complex Data Controls",
        description="Multiple coordinated menus for table/list management"
    )


def create_dropdown_menu_docs():
    """Create dropdown menu documentation page using convention-based approach."""
    
    api_reference = build_api_reference(
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
    
    # Hero example
    @with_code
    def hero_dropdown_menu_example():
        hero_signal_id = uuid4().hex[:8]
        return Div(
            DropdownMenu(
                DropdownMenuTrigger(
                    "Open Menu",
                    Icon("lucide:chevron-down", cls="ml-2 h-4 w-4")
                ),
                DropdownMenuContent(
                    DropdownMenuItem(
                        Icon("lucide:plus", cls="mr-2 h-4 w-4"),
                        "New File"
                    ),
                    DropdownMenuItem(
                        Icon("lucide:download", cls="mr-2 h-4 w-4"),
                        "Download"
                    ),
                    DropdownMenuSeparator(),
                    DropdownMenuItem(
                        Icon("lucide:trash", cls="mr-2 h-4 w-4"),
                        "Delete",
                        variant="destructive"
                    )
                ),
                signal=f"hero_menu_{hero_signal_id}"
            ),
            cls="w-full max-w-xl flex justify-center"
        )
    
    hero_example = ComponentPreview(
        hero_dropdown_menu_example(),
        hero_dropdown_menu_example.code,
        copy_button=True
    )
    
    return auto_generate_page(
        TITLE,
        DESCRIPTION,
        list(examples()),
        cli_command="star add dropdown-menu", 
        api_reference=api_reference,
        hero_example=hero_example,
        component_slug="dropdown-menu"
    )