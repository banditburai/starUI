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
from utils import auto_generate_page
from widgets.component_preview import ComponentPreview


def examples():
    """Generate dropdown menu examples using ComponentPreview with tabs."""
    
    # Basic menu with actions
    yield ComponentPreview(
        Div(
            DropdownMenu(
            DropdownMenuTrigger(
                Icon("lucide:settings", cls="mr-2 h-4 w-4"),
                "Settings"
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
        ),
        '''DropdownMenu(
    DropdownMenuTrigger(
        Icon("lucide:settings", cls="mr-2 h-4 w-4"),
        "Settings"
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
)''',
        title="Basic Menu",
        description="A simple dropdown menu with actions and a destructive item"
    )
    
    # Menu with checkboxes for preferences
    signal_id = uuid4().hex[:8]
    yield ComponentPreview(
        Div(
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
                            checked_signal="showGrid"
                        ),
                        DropdownMenuCheckboxItem(
                            "Show Rulers",
                            checked_signal="showRulers"
                        ),
                        DropdownMenuCheckboxItem(
                            "Show Guides",
                            checked_signal="showGuides"
                        ),
                        DropdownMenuSeparator(),
                        DropdownMenuCheckboxItem(
                            "Auto-save",
                            checked_signal="autoSave"
                        )
                    ),
                    signal=f"view_menu_{signal_id}"
                ),
                cls="flex justify-center"
            ),
            ds_signals(show_grid=True, show_rulers=False, show_guides=True, auto_save=True),
            cls="flex flex-col min-h-[200px] justify-center"
        ),
        '''DropdownMenu(
    DropdownMenuTrigger(
        Icon("lucide:eye", cls="mr-2 h-4 w-4"),
        "View Options"
    ),
    DropdownMenuContent(
        DropdownMenuLabel("Display Settings"),
        DropdownMenuSeparator(),
        DropdownMenuCheckboxItem("Show Grid", checked_signal="showGrid"),
        DropdownMenuCheckboxItem("Show Rulers", checked_signal="showRulers"),
        DropdownMenuCheckboxItem("Show Guides", checked_signal="showGuides"),
        DropdownMenuSeparator(),
        DropdownMenuCheckboxItem("Auto-save", checked_signal="autoSave")
    )
)''',
        title="Checkbox Menu",
        description="Menu with toggleable options and live state display"
    )
    
    # Radio group menu for selections
    signal_id2 = uuid4().hex[:8]
    yield ComponentPreview(
        Div(
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
                        "Theme"
                    ),
                    DropdownMenuContent(
                        DropdownMenuLabel("Appearance"),
                        DropdownMenuSeparator(),
                        DropdownMenuRadioGroup(
                            DropdownMenuRadioItem(
                                Icon("lucide:sun", cls="mr-2 h-4 w-4"),
                                "Light",
                                value="light",
                                value_signal="theme"
                            ),
                            DropdownMenuRadioItem(
                                Icon("lucide:moon", cls="mr-2 h-4 w-4"),
                                "Dark", 
                                value="dark",
                                value_signal="theme"
                            ),
                            DropdownMenuRadioItem(
                                Icon("lucide:laptop", cls="mr-2 h-4 w-4"),
                                "System",
                                value="system", 
                                value_signal="theme"
                            ),
                            value_signal="theme"
                        )
                    ),
                    signal=f"theme_menu_{signal_id2}"
                ),
                cls="flex justify-center"
            ),
            ds_signals(theme=value("system")),
            cls="flex flex-col min-h-[200px] justify-center"
        ),
        '''DropdownMenu(
    DropdownMenuTrigger(
        Icon("lucide:palette", cls="mr-2 h-4 w-4"),
        "Theme"
    ),
    DropdownMenuContent(
        DropdownMenuLabel("Appearance"),
        DropdownMenuSeparator(),
        DropdownMenuRadioGroup(
            DropdownMenuRadioItem(
                Icon("lucide:sun", cls="mr-2 h-4 w-4"),
                "Light",
                value="light",
                value_signal="theme"
            ),
            DropdownMenuRadioItem(
                Icon("lucide:moon", cls="mr-2 h-4 w-4"),
                "Dark",
                value="dark", 
                value_signal="theme"
            ),
            DropdownMenuRadioItem(
                Icon("lucide:laptop", cls="mr-2 h-4 w-4"),
                "System",
                value="system",
                value_signal="theme"
            ),
            value_signal="theme"
        )
    )
)''',
        title="Radio Group Menu",
        description="Menu with mutually exclusive options"
    )
    
    # Advanced menu with shortcuts and grouping
    yield ComponentPreview(
        Div(
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
        ),
        '''DropdownMenu(
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
        align="end"    )
)''',
        title="Context Menu",
        description="Rich menu with keyboard shortcuts and grouped actions"
    )
    
    # User profile menu
    yield ComponentPreview(
        Div(
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
        ),
        '''DropdownMenu(
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
)''',
        title="User Profile Menu",
        description="Complete user menu with avatar, profile info, and account actions"
    )
    
    # Content management menu
    signal_id3 = uuid4().hex[:8]
    yield ComponentPreview(
        Div(
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
                        Icon("lucide:chevron-down", cls="ml-2 h-4 w-4")
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
        ),
        '''DropdownMenu(
    DropdownMenuTrigger(
        "Create New",
        Icon("lucide:chevron-down", cls="ml-2 h-4 w-4")
    ),
    DropdownMenuContent(
        DropdownMenuGroup(
            DropdownMenuItem(
                Icon("lucide:file-text", cls="mr-2 h-4 w-4"),
                "Document",
                onclick="$created = 'Document created'"
            ),
            DropdownMenuItem(
                Icon("lucide:table", cls="mr-2 h-4 w-4"),
                "Spreadsheet",
                onclick="$created = 'Spreadsheet created'"
            ),
            DropdownMenuItem(
                Icon("lucide:presentation", cls="mr-2 h-4 w-4"),
                "Presentation",
                onclick="$created = 'Presentation created'"
            )
        ),
        DropdownMenuSeparator(),
        DropdownMenuGroup(
            DropdownMenuItem(
                Icon("lucide:folder-plus", cls="mr-2 h-4 w-4"),
                "New Folder",
                onclick="$created = 'Folder created'"
            ),
            DropdownMenuItem(
                Icon("lucide:upload", cls="mr-2 h-4 w-4"),
                "Upload File",
                onclick="$created = 'File uploaded'"
            )
        )
    )
)''',
        title="Creation Menu",
        description="Grouped menu for creating different types of content"
    )
    
    # Complex sorting menu with state
    signal_id4 = uuid4().hex[:8]
    yield ComponentPreview(
        Div(
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
                        variant="outline"
                    ),
                    DropdownMenuContent(
                        DropdownMenuRadioGroup(
                            DropdownMenuRadioItem(
                                "Name",
                                value="name",
                                value_signal="sortBy"
                            ),
                            DropdownMenuRadioItem(
                                "Date Created",
                                value="date",
                                value_signal="sortBy"
                            ),
                            DropdownMenuRadioItem(
                                "Size",
                                value="size",
                                value_signal="sortBy"
                            ),
                            DropdownMenuRadioItem(
                                "Type",
                                value="type",
                                value_signal="sortBy"
                            ),
                            value_signal="sortBy"
                        ),
                        DropdownMenuSeparator(),
                        DropdownMenuCheckboxItem(
                            "Ascending",
                            checked_signal="ascending"
                        )
                    ),
                    signal=f"sort_menu_{signal_id4}"
                ),
                DropdownMenu(
                    DropdownMenuTrigger(
                        "View",
                        Icon("lucide:chevron-down", cls="ml-2 h-4 w-4"),
                        variant="outline",
                        cls="ml-2"
                    ),
                    DropdownMenuContent(
                        DropdownMenuCheckboxItem(
                            "Show Hidden Files",
                            checked_signal="showHidden"
                        ),
                        DropdownMenuCheckboxItem(
                            "Show File Extensions",
                            checked_signal="showExtensions"
                        ),
                        DropdownMenuSeparator(),
                        DropdownMenuRadioGroup(
                            DropdownMenuRadioItem(
                                "Grid View",
                                value="grid",
                                value_signal="viewMode"
                            ),
                            DropdownMenuRadioItem(
                                "List View", 
                                value="list",
                                value_signal="viewMode"
                            ),
                            value_signal="viewMode"
                        )
                    ),
                    signal=f"view_menu_{signal_id4}"
                ),
                cls="flex items-center justify-center"
            ),
            ds_signals(sort_by=value("name"), ascending=True, view_mode=value("list"), show_hidden=False, show_extensions=True),
            cls="flex flex-col min-h-[200px] justify-center"
        ),
        '''# Multiple coordinated dropdown menus
DropdownMenu(
    DropdownMenuTrigger("Sort By", variant="outline"),
    DropdownMenuContent(
        DropdownMenuRadioGroup(
            DropdownMenuRadioItem("Name", value="name", value_signal="sortBy"),
            DropdownMenuRadioItem("Date Created", value="date", value_signal="sortBy"),
            DropdownMenuRadioItem("Size", value="size", value_signal="sortBy"),
            DropdownMenuRadioItem("Type", value="type", value_signal="sortBy"),
            value_signal="sortBy"
        ),
        DropdownMenuSeparator(),
        DropdownMenuCheckboxItem("Ascending", checked_signal="ascending")
    )
)

DropdownMenu(
    DropdownMenuTrigger("View", variant="outline"),
    DropdownMenuContent(
        DropdownMenuCheckboxItem("Show Hidden Files", checked_signal="showHidden"),
        DropdownMenuCheckboxItem("Show File Extensions", checked_signal="showExtensions"),
        DropdownMenuSeparator(),
        DropdownMenuRadioGroup(
            DropdownMenuRadioItem("Grid View", value="grid", value_signal="viewMode"),
            DropdownMenuRadioItem("List View", value="list", value_signal="viewMode"),
            value_signal="viewMode"
        )
    )
)''',
        title="Complex Data Controls",
        description="Multiple coordinated menus for table/list management"
    )


def create_dropdown_menu_docs():
    """Create dropdown menu documentation page using convention-based approach."""
    from utils import auto_generate_page
    
    api_reference = {
        "components": [
            {
                "name": "DropdownMenu",
                "props": [
                    {
                        "name": "signal",
                        "type": "str | None", 
                        "default": "None",
                        "description": "Custom signal name for the dropdown state"
                    },
                    {
                        "name": "cls",
                        "type": "str",
                        "default": "''",
                        "description": "Additional CSS classes"
                    }
                ]
            },
            {
                "name": "DropdownMenuTrigger",
                "props": [
                    {
                        "name": "variant",
                        "type": "Literal['default', 'destructive', 'outline', 'secondary', 'ghost', 'link']",
                        "default": "'outline'",
                        "description": "Button variant for the trigger"
                    },
                    {
                        "name": "size",
                        "type": "Literal['default', 'sm', 'lg', 'icon']",
                        "default": "'default'",
                        "description": "Button size for the trigger"
                    },
                    {
                        "name": "as_child",
                        "type": "bool",
                        "default": "False",
                        "description": "Render as child element instead of button"
                    }
                ]
            },
            {
                "name": "DropdownMenuContent",
                "props": [
                    {
                        "name": "side",
                        "type": "Literal['top', 'right', 'bottom', 'left']",
                        "default": "'bottom'",
                        "description": "Which side of trigger to position content"
                    },
                    {
                        "name": "align",
                        "type": "Literal['start', 'center', 'end']",
                        "default": "'start'",
                        "description": "How to align content with trigger"
                    },
                    {
                        "name": "side_offset",
                        "type": "int",
                        "default": "4",
                        "description": "Distance from trigger in pixels"
                    }
                ]
            },
            {
                "name": "DropdownMenuItem",
                "props": [
                    {
                        "name": "onclick",
                        "type": "str | None",
                        "default": "None",
                        "description": "JavaScript to execute on click"
                    },
                    {
                        "name": "variant",
                        "type": "Literal['default', 'destructive']",
                        "default": "'default'",
                        "description": "Visual style of the menu item"
                    },
                    {
                        "name": "inset",
                        "type": "bool",
                        "default": "False",
                        "description": "Add left padding for alignment with items that have icons"
                    },
                    {
                        "name": "disabled",
                        "type": "bool",
                        "default": "False",
                        "description": "Whether item is disabled"
                    }
                ]
            }
        ]
    }
    
    # Hero example
    hero_example = ComponentPreview(
        Div(
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
                )
            ),
            cls="w-full max-w-xl flex justify-center"
        ),
        '''DropdownMenu(
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
    )
)''',
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