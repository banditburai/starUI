"""
Command component documentation - Command palette for searching and executing actions.
"""

from starhtml import Div, P, Span, Icon, Hr, Kbd, Input
from starhtml.datastar import ds_signals, ds_on_click, ds_show, ds_class, ds_bind, ds_on_keydown, ds_text, value
from starui.registry.components.command import (
    Command, CommandInput, CommandList, CommandEmpty,
    CommandGroup, CommandItem, CommandSeparator, CommandShortcut,
    CommandDialog
)
from starui.registry.components.button import Button
from starui.registry.components.badge import Badge
from utils import auto_generate_page
from widgets.component_preview import ComponentPreview

# Component metadata for auto-discovery
TITLE = "Command"
DESCRIPTION = "Command palette interface for searching, filtering, and executing actions."
CATEGORY = "ui"
ORDER = 30
STATUS = "stable"


def examples():
    """Generate command examples using ComponentPreview with tabs."""
    
    # Interactive task manager with dynamic groups
    # Define tasks as Python data that will generate the UI
    tasks = [
        {"id": "task1", "name": "Review pull requests", "status": "progress", "priority": "normal"},
        {"id": "task2", "name": "Fix critical bug", "status": "pending", "priority": "urgent"},
        {"id": "task3", "name": "Update documentation", "status": "pending", "priority": "normal"},
        {"id": "task4", "name": "Write unit tests", "status": "completed", "priority": "normal"},
        {"id": "task5", "name": "Deploy to staging", "status": "pending", "priority": "urgent"},
    ]
    
    # Generate CommandItems for each status group (including dynamic slots)
    def generate_task_items(tasks_list, status_filter):
        items = []
        
        # Create all possible task IDs (existing + dynamic slots)
        all_task_ids = [t["id"] for t in tasks_list]
        for i in range(len(tasks_list) + 1, len(tasks_list) + 6):
            all_task_ids.append(f"task{i}")
        
        # Generate CommandItems for all possible tasks
        for task_id in all_task_ids:
            # Find existing task data or use dynamic placeholders
            existing_task = next((t for t in tasks_list if t["id"] == task_id), None)
            
            if status_filter == "pending":
                if existing_task:
                    # Use existing task data
                    icon_class = "text-yellow-500" if existing_task["priority"] == "urgent" else "text-gray-400"
                    icon_name = "lucide:alert-circle" if existing_task["priority"] == "urgent" else "lucide:circle-dot"
                    task_name = existing_task["name"]
                    show_condition = f"${task_id}_visible && ${task_id}_status === 'pending'"
                else:
                    # Dynamic task
                    icon_name = "lucide:circle-dot"
                    show_condition = f"${task_id}_visible && ${task_id}_status === 'pending'"
                    task_name = None  # Will use ds_text
                
                if task_name:  # Existing task
                    items.append(
                        CommandItem(
                            Icon(icon_name, cls=f"mr-2 h-4 w-4 {icon_class}"),
                            task_name,
                            Badge("Urgent" if existing_task["priority"] == "urgent" else "Pending", 
                                  variant="destructive" if existing_task["priority"] == "urgent" else "secondary", 
                                  cls="ml-auto"),
                            value=f"{task_id}_pending",
                            onclick=f"${task_id}_status = 'progress'",
                            show=show_condition
                        )
                    )
                else:  # Dynamic task
                    items.append(
                        CommandItem(
                            Span(
                                Icon(icon_name, cls="mr-2 h-4 w-4"),
                                ds_class(**{
                                    "text-yellow-500": f"${task_id}_priority === 'urgent'",
                                    "text-gray-400": f"${task_id}_priority === 'normal'"
                                })
                            ),
                            Span(ds_text(f"${task_id}_name")),
                            Div(
                                Badge(
                                    "Urgent",
                                    ds_show(f"${task_id}_priority === 'urgent'"),
                                    variant="destructive",
                                    cls="ml-auto"
                                ),
                                Badge(
                                    "Pending",
                                    ds_show(f"${task_id}_priority === 'normal'"),
                                    variant="secondary", 
                                    cls="ml-auto"
                                ),
                                cls="ml-auto"
                            ),
                            value=f"{task_id}_pending",
                            onclick=f"${task_id}_status = 'progress'",
                            show=show_condition
                        )
                    )
                    
            elif status_filter == "progress":
                if existing_task:
                    task_name = existing_task["name"]
                    show_condition = f"${task_id}_visible && ${task_id}_status === 'progress'"
                    badge_variant = "destructive" if existing_task["priority"] == "urgent" else "default"
                    badge_text = "Urgent" if existing_task["priority"] == "urgent" else "In Progress"
                    icon_name = "lucide:alert-circle" if existing_task["priority"] == "urgent" else "lucide:circle"
                    icon_color = "text-yellow-500" if existing_task["priority"] == "urgent" else "text-blue-500"
                    items.append(
                        CommandItem(
                            Icon(icon_name, cls=f"mr-2 h-4 w-4 {icon_color}"),
                            task_name,
                            Badge(badge_text, variant=badge_variant, cls="ml-auto"),
                            value=f"{task_id}_progress",
                            onclick=f"${task_id}_status = 'completed'",
                            show=show_condition
                        )
                    )
                else:  # Dynamic task
                    items.append(
                        CommandItem(
                            Span(
                                Icon("lucide:alert-circle", cls="mr-2 h-4 w-4"),
                                ds_class(**{
                                    "text-yellow-500": f"${task_id}_priority === 'urgent'",
                                    "text-blue-500": f"${task_id}_priority === 'normal'"
                                })
                            ),
                            Span(ds_text(f"${task_id}_name")),
                            Div(
                                Badge(
                                    "Urgent",
                                    ds_show(f"${task_id}_priority === 'urgent'"),
                                    variant="destructive",
                                    cls="ml-auto"
                                ),
                                Badge(
                                    "In Progress",
                                    ds_show(f"${task_id}_priority === 'normal'"),
                                    variant="default",
                                    cls="ml-auto"
                                ),
                                cls="ml-auto"
                            ),
                            value=f"{task_id}_progress",
                            onclick=f"${task_id}_status = 'completed'",
                            show=f"${task_id}_visible && ${task_id}_status === 'progress'",
                        )
                    )
                    
            else:  # completed
                if existing_task:
                    task_name = existing_task["name"]
                    show_condition = f"${task_id}_visible && ${task_id}_status === 'completed'"
                    items.append(
                        CommandItem(
                            Icon("lucide:check-circle", cls="mr-2 h-4 w-4 text-green-500"),
                            Span(task_name, cls="line-through opacity-60"),
                            Badge("Done", variant="outline", cls="ml-auto opacity-60"),
                            value=f"{task_id}_completed",
                            onclick=f"${task_id}_visible = false",
                            show=show_condition
                        )
                    )
                else:  # Dynamic task
                    items.append(
                        CommandItem(
                            Icon("lucide:check-circle", cls="mr-2 h-4 w-4 text-green-500"),
                            Span(ds_text(f"${task_id}_name"), cls="line-through opacity-60"),
                            Badge("Done", variant="outline", cls="ml-auto opacity-60"),
                            value=f"{task_id}_completed",
                            onclick=f"${task_id}_visible = false",
                            show=f"${task_id}_visible && ${task_id}_status === 'completed'",
                        )
                    )
        
        # Add empty state placeholder
        empty_icons = {"pending": "lucide:inbox", "progress": "lucide:clock", "completed": "lucide:check"}
        empty_messages = {"pending": "No pending tasks", "progress": "No tasks in progress", "completed": "No completed tasks yet"}
        
        # Generate show condition for empty state (when no tasks match this status)
        show_conditions = [f"${task_id}_visible && ${task_id}_status === '{status_filter}'" for task_id in all_task_ids]
        empty_show = " && ".join([f"!({cond})" for cond in show_conditions])
        
        items.append(
            CommandItem(
                Icon(empty_icons[status_filter], cls="mr-2 h-4 w-4 opacity-50"),
                Span(empty_messages[status_filter], cls="text-muted-foreground italic"),
                value=f"empty_{status_filter}",
                disabled=True,
                show=empty_show
            )
        )
        
        return items
    
    # Generate signals for all tasks + extra slots for dynamic tasks
    task_signals = {}
    for task in tasks:
        task_signals[f"{task['id']}_status"] = value(task["status"])
        task_signals[f"{task['id']}_visible"] = value(True)
        task_signals[f"{task['id']}_name"] = value(task["name"])
        task_signals[f"{task['id']}_priority"] = value(task["priority"])
    
    # Add 5 extra task slots for dynamic addition (task6-task10)
    for i in range(len(tasks) + 1, len(tasks) + 6):
        task_id = f"task{i}"
        task_signals[f"{task_id}_status"] = value("pending")
        task_signals[f"{task_id}_visible"] = value(False)
        task_signals[f"{task_id}_name"] = value("New task")
        task_signals[f"{task_id}_priority"] = value("normal")
    
    task_signals["task_cmd_new"] = value("")
    task_signals["task_cmd_next_id"] = value(len(tasks) + 1)
    
    # Custom CommandInput for task addition
    def TaskCommandInput(placeholder: str = "Add a new task...", **kwargs):
        def _(signal):
            return Div(
                Icon("lucide:plus", cls="size-4 shrink-0 opacity-50"),
                Input(
                    ds_bind("task_cmd_new"),
                    ds_on_keydown("""
                        if(event.key==='Enter' && $task_cmd_new.trim()) { 
                            const text = $task_cmd_new.trim();
                            const isUrgent = text.startsWith('!');
                            const name = text.replace(/^!/, '').trim();
                            if(name) {
                                // Find the next available task slot
                                const nextId = $task_cmd_next_id;
                                
                                // Set the signals for the new task using direct assignment
                                if(nextId === 6) {
                                    $task6_name = name;
                                    $task6_status = 'pending';
                                    $task6_priority = isUrgent ? 'urgent' : 'normal';
                                    $task6_visible = true;
                                } else if(nextId === 7) {
                                    $task7_name = name;
                                    $task7_status = 'pending';
                                    $task7_priority = isUrgent ? 'urgent' : 'normal';
                                    $task7_visible = true;
                                } else if(nextId === 8) {
                                    $task8_name = name;
                                    $task8_status = 'pending';
                                    $task8_priority = isUrgent ? 'urgent' : 'normal';
                                    $task8_visible = true;
                                } else if(nextId === 9) {
                                    $task9_name = name;
                                    $task9_status = 'pending';
                                    $task9_priority = isUrgent ? 'urgent' : 'normal';
                                    $task9_visible = true;
                                } else if(nextId === 10) {
                                    $task10_name = name;
                                    $task10_status = 'pending';
                                    $task10_priority = isUrgent ? 'urgent' : 'normal';
                                    $task10_visible = true;
                                }
                                
                                // Increment the next ID counter (max 10 slots)
                                if(nextId < 10) {
                                    $task_cmd_next_id = nextId + 1;
                                }
                                $task_cmd_new = '';
                            }
                        }
                    """),
                    placeholder=placeholder,
                    data_slot="command-input",
                    cls="flex h-10 w-full rounded-md bg-transparent py-3 text-sm outline-none placeholder:text-muted-foreground disabled:cursor-not-allowed disabled:opacity-50",
                    autocomplete="off",
                    autocorrect="off",
                    spellcheck="false",
                    type="text",
                    **kwargs
                ),
                data_slot="command-input-wrapper",
                cls="flex h-9 items-center gap-2 border-b border-border px-3"
            )
        return _
    
    yield ComponentPreview(
        Div(
            Command(
                TaskCommandInput(
                    placeholder="Add a new task (use ! for urgent)..."
                ),
                CommandList(
                    CommandEmpty("No tasks yet. Add your first task above!"),
                    CommandGroup(
                        "Pending Tasks",
                        *generate_task_items(tasks, "pending")
                    ),
                    CommandGroup(
                        "In Progress",
                        *generate_task_items(tasks, "progress")
                    ),
                    CommandSeparator(),
                    CommandGroup(
                        "Completed",
                        *generate_task_items(tasks, "completed")
                    ),
                    cls="max-h-none overflow-visible"
                ),
                signal="tasks",
                size="md"
            ),
            ds_signals(**task_signals)
        ),
        """# Custom CommandInput for task addition
def TaskCommandInput(placeholder="Add a new task...", **kwargs):
    def _(signal):
        return Div(
            Icon("lucide:plus", cls="size-4 shrink-0 opacity-50"),
            Input(
                ds_bind("task_cmd_new"),
                ds_on_keydown("...task addition logic..."),
                placeholder=placeholder,
                **kwargs
            ),
            cls="flex h-9 items-center gap-2 border-b border-border px-3"
        )
    return _

Command(
    TaskCommandInput(placeholder="Add a new task (use ! for urgent)..."),
    CommandList(
        CommandEmpty("No tasks found."),
        CommandGroup(
            "Active Tasks",
            CommandItem(
                Icon("lucide:circle", cls="mr-2 h-4 w-4 text-blue-500"),
                "Review pull requests",
                Badge("In Progress", variant="default", cls="ml-auto"),
                value="task1",
                onclick="alert('Task marked as complete')"
            )
        ),
        CommandGroup(
            "Completed",
            CommandItem(
                Icon("lucide:check-circle", cls="mr-2 h-4 w-4 text-green-500"),
                Span("Deploy to production", cls="line-through opacity-60"),
                Badge("Done", variant="outline", cls="ml-auto"),
                value="task4",
                disabled=True
            )
        )
    ),
    signal="task_cmd"
)""",
        title="Interactive Task Manager",
        description="Command component as a task manager with state transitions. Click tasks to move them: Pending → In Progress → Completed. Add new tasks with Enter (use ! prefix for urgent)."
    )
    
    # Command palette with real actions
    yield ComponentPreview(
        Div(
            CommandDialog(
                Button(
                    Icon("lucide:terminal", cls="mr-2 h-4 w-4"),
                    "Open command palette",
                    Kbd("⌘K", cls="ml-auto text-xs"),
                    variant="outline",
                    cls="w-64 justify-start text-sm text-muted-foreground"
                ),
                [
                    CommandInput(placeholder="Type a command or search..."),
                    CommandList(
                        CommandEmpty("No commands found."),
                        CommandGroup(
                            "Navigation",
                            CommandItem(
                                Icon("lucide:home", cls="mr-2 h-4 w-4"),
                                "Go to Home",
                                value="home",
                                onclick="window.location.href='/'",
                                ),
                            CommandItem(
                                Icon("lucide:book-open", cls="mr-2 h-4 w-4"),
                                "Documentation",
                                Icon("lucide:external-link", cls="ml-auto h-3 w-3 opacity-50"),
                                value="docs",
                                onclick="window.open('https://docs.example.com', '_blank')",
                                ),
                            CommandItem(
                                Icon("lucide:github", cls="mr-2 h-4 w-4"),
                                "GitHub Repository",
                                Icon("lucide:external-link", cls="ml-auto h-3 w-3 opacity-50"),
                                value="github",
                                onclick="window.open('https://github.com', '_blank')",
                                ),
                        ),
                        CommandSeparator(),
                        CommandGroup(
                            "Utilities",
                            CommandItem(
                                Icon("lucide:copy", cls="mr-2 h-4 w-4"),
                                "Copy Email",
                                CommandShortcut("⌘C"),
                                value="copy-email",
                                onclick="navigator.clipboard.writeText('user@example.com').then(() => alert('Email copied!'))",
                                ),
                            CommandItem(
                                Icon("lucide:link", cls="mr-2 h-4 w-4"),
                                "Copy Share Link",
                                CommandShortcut("⌘L"),
                                value="copy-link",
                                onclick="navigator.clipboard.writeText(window.location.href).then(() => alert('Link copied!'))",
                                ),
                            CommandItem(
                                Icon("lucide:download", cls="mr-2 h-4 w-4"),
                                "Export Data",
                                Badge("CSV", variant="secondary", cls="ml-auto"),
                                value="export",
                                onclick="alert('Exporting data as CSV...')",
                                ),
                        ),
                        CommandSeparator(),
                        CommandGroup(
                            "System",
                            CommandItem(
                                Icon("lucide:moon", cls="mr-2 h-4 w-4"),
                                "Toggle Dark Mode",
                                CommandShortcut("⌘D"),
                                value="dark-mode",
                                onclick="document.documentElement.classList.toggle('dark')",
                                ),
                            CommandItem(
                                Icon("lucide:log-out", cls="mr-2 h-4 w-4 text-red-500"),
                                Span("Sign Out", cls="text-red-500"),
                                value="signout",
                                onclick="if(confirm('Sign out?')) window.location.href='/logout'",
                                ),
                        ),
                        signal="action_cmd",
                        cls="max-h-none overflow-visible"
                    )
                ],
                signal="action_cmd"
            ),
            cls="flex justify-center"
        ),
        """CommandDialog(
    Button(
        Icon("lucide:terminal", cls="mr-2 h-4 w-4"),
        "Open command palette",
        Kbd("⌘K", cls="ml-auto text-xs"),
        variant="outline"
    ),
    [
        CommandInput(placeholder="Type a command..."),
        CommandList(
            CommandEmpty("No commands found."),
            CommandGroup(
                "Navigation",
                CommandItem(
                    Icon("lucide:home", cls="mr-2 h-4 w-4"),
                    "Go to Home",
                    value="home",
                    onclick="window.location.href='/'",
                ),
            ),
            CommandGroup(
                "Utilities",
                CommandItem(
                    Icon("lucide:copy", cls="mr-2 h-4 w-4"),
                    "Copy Email",
                    CommandShortcut("⌘C"),
                    value="copy-email",
                    onclick="navigator.clipboard.writeText('user@example.com')",
                ),
            ),
        )
    ],
    signal="cmd"
)""",
        title="Command Palette with Actions",
        description="Interactive command dialog with real actions: navigation, clipboard operations, and system controls"
    )
    
    # Compact context menu
    yield ComponentPreview(
        Div(
            Command(
                CommandList(
                    CommandGroup(
                        "Item Actions",
                        CommandItem(
                            Icon("lucide:edit", cls="mr-2 h-4 w-4"),
                            "Edit",
                            CommandShortcut("⌘E"),
                            value="edit",
                            onclick="alert('Edit mode activated')",
                        ),
                        CommandItem(
                            Icon("lucide:copy", cls="mr-2 h-4 w-4"),
                            "Duplicate",
                            CommandShortcut("⌘D"),
                            value="duplicate",
                            onclick="alert('Item duplicated')",
                        ),
                        CommandItem(
                            Icon("lucide:archive", cls="mr-2 h-4 w-4"),
                            "Archive",
                            value="archive",
                            onclick="alert('Item archived')",
                        ),
                    ),
                    CommandSeparator(),
                    CommandGroup(
                        "Share",
                        CommandItem(
                            Icon("lucide:link", cls="mr-2 h-4 w-4"),
                            "Copy Link",
                            value="copy-link",
                            onclick="navigator.clipboard.writeText('https://example.com/item/123')",
                        ),
                        CommandItem(
                            Icon("lucide:mail", cls="mr-2 h-4 w-4"),
                            "Email",
                            value="email",
                            onclick="window.location.href='mailto:?subject=Check this out'",
                        ),
                        CommandItem(
                            Icon("lucide:message-circle", cls="mr-2 h-4 w-4"),
                            "Send to Slack",
                            Icon("lucide:external-link", cls="ml-auto h-3 w-3 opacity-50"),
                            value="slack",
                            onclick="alert('Opening Slack...')",
                        ),
                    ),
                    CommandSeparator(),
                    CommandItem(
                        Icon("lucide:trash", cls="mr-2 h-4 w-4 text-red-500"),
                        Span("Delete", cls="text-red-500"),
                        CommandShortcut("Del"),
                        value="delete",
                        onclick="if(confirm('Delete this item?')) alert('Item deleted')",
                    ),
                ),
                signal="context_cmd",
                size="sm"
            ),
            cls="max-w-xs"
        ),
        """Command(
    CommandList(
        CommandGroup(
            "Item Actions",
            CommandItem(
                Icon("lucide:edit", cls="mr-2 h-4 w-4"),
                "Edit",
                CommandShortcut("⌘E"),
                value="edit",
                onclick="alert('Edit mode')",
                ),
            CommandItem(
                Icon("lucide:copy", cls="mr-2 h-4 w-4"),
                "Duplicate",
                value="duplicate",
                onclick="alert('Duplicated')",
                ),
        ),
        CommandSeparator(),
        CommandItem(
            Icon("lucide:trash", cls="mr-2 h-4 w-4 text-red-500"),
            Span("Delete", cls="text-red-500"),
            value="delete",
            onclick="if(confirm('Delete?')) alert('Deleted')",
        ),
    ),
    signal="context_cmd",
    size="sm"
)""",
        title="Compact Context Menu",
        description="Small command menu for context-specific actions, perfect for dropdowns and right-click menus"
    )


def create_command_docs():
    """Create command documentation page using convention-based approach."""
    
    # Hero example - comprehensive command palette
    hero_example = ComponentPreview(
        Div(
            Command(
                CommandInput(
                    placeholder="Type a command or search...",
                ),
                CommandList(
                    CommandEmpty("No results found."),
                    CommandGroup(
                        "Suggestions",
                        CommandItem(
                            Icon("lucide:rocket", cls="mr-2 h-4 w-4"),
                            "Launch",
                            CommandShortcut("⌘L"),
                            value="launch",
                            onclick="alert('Launching...')",
                        ),
                        CommandItem(
                            Icon("lucide:search", cls="mr-2 h-4 w-4"),
                            "Search",
                            CommandShortcut("⌘K"),
                            value="search",
                            onclick="alert('Opening search...')",
                        ),
                        CommandItem(
                            Icon("lucide:terminal", cls="mr-2 h-4 w-4"),
                            "Terminal",
                            CommandShortcut("⌘T"),
                            value="terminal",
                            onclick="alert('Opening terminal...')",
                        ),
                    ),
                    CommandSeparator(),
                    CommandGroup(
                        "Recent",
                        CommandItem(
                            Icon("lucide:file", cls="mr-2 h-4 w-4"),
                            "Project Alpha",
                            Badge("Active", variant="default", cls="ml-auto"),
                            value="project-alpha",
                            onclick="alert('Opening Project Alpha')",
                        ),
                        CommandItem(
                            Icon("lucide:file", cls="mr-2 h-4 w-4"),
                            "Project Beta",
                            value="project-beta",
                            onclick="alert('Opening Project Beta')",
                        ),
                    ),
                ),
                signal="hero_cmd",
                size="md"
            ),
            cls="max-w-2xl mx-auto"
        ),
        """from starui.registry.components.command import *

Command(
    CommandInput(placeholder="Type a command or search..."),
    CommandList(
        CommandEmpty("No results found."),
        CommandGroup(
            "Suggestions",
            CommandItem(
                Icon("lucide:rocket", cls="mr-2 h-4 w-4"),
                "Launch",
                CommandShortcut("⌘L"),
                value="launch"
            ),
            CommandItem(
                Icon("lucide:search", cls="mr-2 h-4 w-4"),
                "Search",
                CommandShortcut("⌘K"),
                value="search"
            ),
        ),
    ),
    signal="cmd"
)""",
        title="",
        description=""
    )
    
    return auto_generate_page(
        TITLE,
        DESCRIPTION,
        list(examples()),
        cli_command="star add command",
        hero_example=hero_example,
        component_slug="command",
        api_reference={
            "components": [
                {
                    "name": "Command",
                    "description": "The root command container"
                },
                {
                    "name": "CommandInput",
                    "description": "Search input for filtering command items"
                },
                {
                    "name": "CommandList",
                    "description": "Container for command items and groups"
                },
                {
                    "name": "CommandEmpty",
                    "description": "Empty state when no results match the search"
                },
                {
                    "name": "CommandGroup",
                    "description": "Group related command items with a heading"
                },
                {
                    "name": "CommandItem",
                    "description": "Individual selectable command item"
                },
                {
                    "name": "CommandSeparator",
                    "description": "Visual separator between command groups"
                },
                {
                    "name": "CommandShortcut",
                    "description": "Display keyboard shortcut for a command"
                },
                {
                    "name": "CommandDialog",
                    "description": "Command palette in a modal dialog"
                }
            ],
            "props": [
                {
                    "name": "signal",
                    "type": "str",
                    "description": "Unique identifier for command state management"
                },
                {
                    "name": "size",
                    "type": "Literal['sm', 'md', 'lg']",
                    "description": "Size of the command palette",
                    "default": "md"
                },
                {
                    "name": "placeholder",
                    "type": "str",
                    "description": "Placeholder text for search input"
                },
                {
                    "name": "on_select",
                    "type": "str",
                    "description": "JavaScript code to execute when item is selected"
                },
                {
                    "name": "value",
                    "type": "str",
                    "description": "Value for search filtering (defaults to text content)"
                },
                {
                    "name": "disabled",
                    "type": "bool",
                    "description": "Whether the command item is disabled",
                    "default": "False"
                }
            ]
        }
    )


# Register the page
__all__ = ["create_command_docs", "TITLE", "DESCRIPTION", "CATEGORY", "ORDER", "STATUS"]