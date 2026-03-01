"""
Command component documentation - Command palette for searching and executing actions.
"""

from starhtml import Div, P, Span, Icon, Kbd, clipboard
from starhtml.datastar import window
from starui.registry.components.command import (
    Command, CommandInput, CommandList, CommandEmpty,
    CommandGroup, CommandItem, CommandSeparator, CommandShortcut,
    CommandDialog
)
from starui.registry.components.button import Button
from starui.registry.components.badge import Badge
from utils import auto_generate_page, with_code, Component, build_api_reference

# Component metadata for auto-discovery
TITLE = "Command"
DESCRIPTION = "Command palette interface for searching, filtering, and executing actions."
CATEGORY = "ui"
ORDER = 30
STATUS = "stable"


@with_code
def hero_command_example():
    return Div(
        Command(
            CommandInput(placeholder="Search files and commands..."),
            CommandList(
                CommandEmpty("No results found."),
                CommandGroup(
                    "Files",
                    CommandItem(
                        Icon("lucide:file-text"),
                        "settings.py",
                        CommandShortcut("⌘P"),
                        value="settings.py",
                        keywords="config configuration env",
                    ),
                    CommandItem(
                        Icon("lucide:file-code"),
                        "deploy.yml",
                        Badge("Modified", variant="secondary", cls="ml-auto"),
                        value="deploy.yml",
                        keywords="ci cd pipeline github actions",
                    ),
                    CommandItem(
                        Icon("lucide:file-text"),
                        "README.md",
                        value="README.md",
                        keywords="docs documentation",
                    ),
                ),
                CommandSeparator(),
                CommandGroup(
                    "Commands",
                    CommandItem(
                        Icon("lucide:git-branch"),
                        "Switch Branch",
                        CommandShortcut("⌘B"),
                        value="switch-branch",
                        keywords="git checkout",
                    ),
                    CommandItem(
                        Icon("lucide:terminal"),
                        "Open Terminal",
                        CommandShortcut("⌘`"),
                        value="open-terminal",
                        keywords="shell console cli",
                    ),
                    CommandItem(
                        Icon("lucide:palette"),
                        "Change Theme",
                        value="change-theme",
                        keywords="color scheme appearance dark light",
                    ),
                ),
            ),
            signal="hero_cmd",
        ),
        cls="max-w-2xl mx-auto",
    )


@with_code
def search_and_keywords_example():
    return Div(
        Command(
            CommandInput(placeholder="Search settings..."),
            CommandList(
                CommandEmpty(
                    Div(
                        Icon("lucide:search-x", cls="size-10 text-muted-foreground/50 mx-auto mb-3"),
                        P("No matching settings.", cls="font-medium"),
                        P("Try a different search term.", cls="text-muted-foreground"),
                        cls="text-center text-sm",
                    )
                ),
                CommandGroup(
                    "General",
                    CommandItem(
                        Icon("lucide:globe"),
                        "Language & Region",
                        Span("English (US)", cls="ml-auto text-xs text-muted-foreground"),
                        value="language-region",
                        keywords="locale timezone i18n translation",
                    ),
                    CommandItem(
                        Icon("lucide:bell"),
                        "Notifications",
                        value="notifications",
                        keywords="alerts push email digest",
                    ),
                    CommandItem(
                        Icon("lucide:key"),
                        "Two-Factor Authentication",
                        Badge("Recommended", variant="secondary", cls="ml-auto"),
                        value="two-factor",
                        keywords="2fa security mfa totp",
                    ),
                ),
                CommandSeparator(),
                CommandGroup(
                    "Workspace",
                    CommandItem(
                        Icon("lucide:users"),
                        "Team Members",
                        value="team-members",
                        keywords="invite collaborators people roles",
                    ),
                    CommandItem(
                        Icon("lucide:webhook"),
                        "API Keys",
                        value="api-keys",
                        keywords="tokens secrets credentials",
                    ),
                    CommandItem(
                        Icon("lucide:database"),
                        "Data Export",
                        value="data-export",
                        keywords="download backup csv json",
                        disabled=True,
                    ),
                ),
            ),
            signal="settings_cmd",
        ),
        cls="max-w-2xl mx-auto",
    )


@with_code
def command_dialog_example():
    return Div(
        CommandDialog(
            Button(
                Icon("lucide:search"),
                Span("Search...", cls="text-muted-foreground font-normal"),
                Kbd("⌘K", cls="ml-auto text-xs"),
                variant="outline",
                cls="w-64 justify-start text-sm",
            ),
            [
                CommandInput(placeholder="What do you need?"),
                CommandList(
                    CommandEmpty("Nothing found."),
                    CommandGroup(
                        "Quick Actions",
                        CommandItem(
                            Icon("lucide:plus"),
                            "New Document",
                            CommandShortcut("⌘N"),
                            value="new-doc",
                            keywords="create file page",
                        ),
                        CommandItem(
                            Icon("lucide:upload"),
                            "Import File",
                            value="import",
                            keywords="upload add",
                        ),
                        CommandItem(
                            Icon("lucide:link"),
                            "Copy Page Link",
                            CommandShortcut("⌘L"),
                            value="copy-link",
                            data_on_click=clipboard(window.location.href),
                        ),
                    ),
                    CommandSeparator(),
                    CommandGroup(
                        "Navigate",
                        CommandItem(
                            Icon("lucide:layout-dashboard"),
                            "Dashboard",
                            value="dashboard",
                            onclick="window.location.href='/'",
                        ),
                        CommandItem(
                            Icon("lucide:folder"),
                            "Projects",
                            value="projects",
                            keywords="workspace repos",
                        ),
                        CommandItem(
                            Icon("lucide:bar-chart-3"),
                            "Analytics",
                            value="analytics",
                            keywords="stats metrics usage",
                        ),
                    ),
                ),
            ],
            signal="dialog_cmd",
            shortcut="k",
        ),
        cls="flex justify-center",
    )


@with_code
def file_context_menu_example():
    return Div(
        Command(
            CommandList(
                CommandGroup(
                    CommandItem(
                        Icon("lucide:pencil"),
                        "Rename",
                        CommandShortcut("F2"),
                        value="rename",
                    ),
                    CommandItem(
                        Icon("lucide:folder-input"),
                        "Move to...",
                        value="move",
                    ),
                    CommandItem(
                        Icon("lucide:copy"),
                        "Duplicate",
                        CommandShortcut("⌘D"),
                        value="duplicate",
                    ),
                ),
                CommandSeparator(),
                CommandGroup(
                    CommandItem(
                        Icon("lucide:share-2"),
                        "Share",
                        value="share",
                    ),
                    CommandItem(
                        Icon("lucide:star"),
                        "Add to Favorites",
                        value="favorite",
                    ),
                    CommandItem(
                        Icon("lucide:info"),
                        "Get Info",
                        CommandShortcut("⌘I"),
                        value="info",
                    ),
                ),
                CommandSeparator(),
                CommandGroup(
                    CommandItem(
                        Icon("lucide:trash", cls="text-destructive"),
                        Span("Move to Trash", cls="text-destructive"),
                        CommandShortcut("⌘⌫"),
                        value="delete",
                    ),
                ),
            ),
            signal="file_ctx",
            size="sm",
        ),
        cls="max-w-xs",
    )


EXAMPLES_DATA = [
    {
        "title": "Basic Command Menu",
        "description": "A searchable command palette with grouped items and keyboard shortcuts. Try typing 'git' or 'docs' — items match on hidden keywords, not just their visible label.",
        "fn": hero_command_example,
    },
    {
        "title": "Search with Keywords and Disabled Items",
        "description": "Items have keyword aliases for search discovery — type '2fa' to find Two-Factor Authentication, or 'csv' to find Data Export. The Data Export item is disabled to indicate an unavailable feature. Custom empty state content replaces the default string.",
        "fn": search_and_keywords_example,
    },
    {
        "title": "Command Dialog",
        "description": "A modal command palette triggered by a button or keyboard shortcut (⌘K). Includes clipboard integration and navigation actions.",
        "fn": command_dialog_example,
    },
    {
        "title": "File Context Menu",
        "description": "A compact command menu without a search input, used as a file context menu. The size='sm' variant and no CommandInput keep it tight.",
        "fn": file_context_menu_example,
    },
]

API_REFERENCE = build_api_reference(
    components=[
        Component("Command", "The root command container with search and filtering"),
        Component("CommandInput", "Search input for filtering command items"),
        Component("CommandList", "Container for command items and groups"),
        Component("CommandEmpty", "Empty state when no results match the search"),
        Component("CommandGroup", "Group related command items with a heading"),
        Component("CommandItem", "Individual selectable command item with actions"),
        Component("CommandSeparator", "Visual separator between command groups"),
        Component("CommandShortcut", "Display keyboard shortcut for a command"),
        Component("CommandDialog", "Command palette in a modal dialog overlay"),
    ]
)


def create_command_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)
