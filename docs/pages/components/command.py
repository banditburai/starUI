"""
Command component documentation - Command palette for searching and executing actions.
"""

from starhtml import Div, P, Span, Icon, Hr, Kbd, Input, Signal, js, clipboard
from starui.registry.components.command import (
    Command, CommandInput, CommandList, CommandEmpty,
    CommandGroup, CommandItem, CommandSeparator, CommandShortcut,
    CommandDialog
)
from starui.registry.components.button import Button
from starui.registry.components.badge import Badge
from utils import auto_generate_page, with_code, Prop, Component, build_api_reference
from widgets.component_preview import ComponentPreview

# Component metadata for auto-discovery
TITLE = "Command"
DESCRIPTION = "Command palette interface for searching, filtering, and executing actions."
CATEGORY = "ui"
ORDER = 30
STATUS = "stable"





tasks = [
    {"id": "task1", "name": "Review pull requests", "status": "progress", "priority": "normal"},
    {"id": "task2", "name": "Fix critical bug", "status": "pending", "priority": "urgent"},
    {"id": "task3", "name": "Update documentation", "status": "pending", "priority": "normal"},
    {"id": "task4", "name": "Write unit tests", "status": "completed", "priority": "normal"},
    {"id": "task5", "name": "Deploy to staging", "status": "pending", "priority": "urgent"},
]


def generate_task_items(tasks_list, status_filter, signals_dict):
    items = []
    all_task_ids = [t["id"] for t in tasks_list] + [f"task{i}" for i in range(len(tasks_list) + 1, len(tasks_list) + 6)]

    def create_task_icon(task_id, icon_name, icon_class=None):
        if icon_class:
            return Icon(icon_name, cls=f"h-4 w-4 mr-2 {icon_class}")

        priority_sig = signals_dict[f"{task_id}_priority"]
        return Icon(
            icon_name,
            cls="h-4 w-4 mr-2",
            data_class_text_yellow_500=priority_sig.eq("urgent"),
            data_class_text_gray_400=priority_sig.eq("normal")
        )

    def create_task_badge(task, task_id, status_filter):
        if task:
            if status_filter == "pending":
                badge_text = "Urgent" if task["priority"] == "urgent" else "Pending"
                badge_variant = "destructive" if task["priority"] == "urgent" else "secondary"
            elif status_filter == "progress":
                badge_text = "Urgent" if task["priority"] == "urgent" else "In Progress"
                badge_variant = "destructive" if task["priority"] == "urgent" else "default"
            else:
                badge_text = "Done"
                badge_variant = "outline"
            return Badge(badge_text, variant=badge_variant, cls="ml-auto")
        else:
            priority_sig = signals_dict[f"{task_id}_priority"]
            if status_filter == "pending":
                urgent_badge = Badge("Urgent", data_show=priority_sig.eq("urgent"),
                                   variant="destructive", cls="ml-auto")
                normal_badge = Badge("Pending", data_show=priority_sig.eq("normal"),
                                   variant="secondary", cls="ml-auto")
            elif status_filter == "progress":
                urgent_badge = Badge("Urgent", data_show=priority_sig.eq("urgent"),
                                   variant="destructive", cls="ml-auto")
                normal_badge = Badge("In Progress", data_show=priority_sig.eq("normal"),
                                   variant="default", cls="ml-auto")
            else:
                return Badge("Done", variant="outline", cls="ml-auto opacity-60")

            return Div(urgent_badge, normal_badge, cls="ml-auto")

    for task_id in all_task_ids:
        existing_task = next((t for t in tasks_list if t["id"] == task_id), None)
        show_condition = f"${task_id}_visible && ${task_id}_status === '{status_filter}'"

        if status_filter == "pending":
            if existing_task:
                icon_class = "text-yellow-500" if existing_task["priority"] == "urgent" else "text-gray-400"
                icon_name = "lucide:alert-circle" if existing_task["priority"] == "urgent" else "lucide:circle-dot"
                task_icon = create_task_icon(task_id, icon_name, icon_class)
                task_text = existing_task["name"]
                task_badge = create_task_badge(existing_task, task_id, status_filter)
            else:
                task_icon = create_task_icon(task_id, "lucide:circle-dot")
                task_text = Span(data_text=f"${task_id}_name")
                task_badge = create_task_badge(None, task_id, status_filter)

            items.append(
                CommandItem(
                    task_icon,
                    task_text,
                    task_badge,
                    value=f"{task_id}_pending",
                    onclick=f"${task_id}_status = 'progress'",
                    show=show_condition
                )
            )

        elif status_filter == "progress":
            if existing_task:
                icon_name = "lucide:alert-circle" if existing_task["priority"] == "urgent" else "lucide:circle"
                icon_color = "text-yellow-500" if existing_task["priority"] == "urgent" else "text-blue-500"
                task_icon = create_task_icon(task_id, icon_name, icon_color)
                task_text = existing_task["name"]
                task_badge = create_task_badge(existing_task, task_id, status_filter)
            else:
                priority_sig = signals_dict[f"{task_id}_priority"]
                task_icon = Icon(
                    "lucide:circle",
                    cls="h-4 w-4 mr-2",
                    data_class_text_yellow_500=priority_sig.eq("urgent"),
                    data_class_text_blue_500=priority_sig.eq("normal")
                )
                task_text = Span(data_text=f"${task_id}_name")
                task_badge = create_task_badge(None, task_id, status_filter)

            items.append(
                CommandItem(
                    task_icon,
                    task_text,
                    task_badge,
                    value=f"{task_id}_progress",
                    onclick=f"${task_id}_status = 'completed'",
                    show=show_condition
                )
            )

        else:
            task_icon = Icon("lucide:check-circle", cls="h-4 w-4 mr-2 text-green-500")
            task_badge = Badge("Done", variant="outline", cls="ml-auto opacity-60")

            if existing_task:
                task_text = Span(existing_task["name"], cls="line-through opacity-60")
            else:
                task_text = Span(data_text=f"${task_id}_name", cls="line-through opacity-60")

            items.append(
                CommandItem(
                    task_icon,
                    task_text,
                    task_badge,
                    value=f"{task_id}_completed",
                    onclick=f"${task_id}_visible = false",
                    show=show_condition
                )
            )

    empty_icons = {"pending": "lucide:inbox", "progress": "lucide:clock", "completed": "lucide:check"}
    empty_messages = {"pending": "No pending tasks", "progress": "No tasks in progress", "completed": "No completed tasks yet"}

    show_conditions = [f"${task_id}_visible && ${task_id}_status === '{status_filter}'" for task_id in all_task_ids]
    empty_show = " && ".join([f"!({cond})" for cond in show_conditions])

    items.append(
        CommandItem(
            Icon(empty_icons[status_filter], cls="h-4 w-4 mr-2 opacity-50"),
            Span(empty_messages[status_filter], cls="text-muted-foreground italic"),
            value=f"empty_{status_filter}",
            disabled=True,
            show=empty_show
        )
    )

    return items


all_task_ids = [t["id"] for t in tasks] + [f"task{i}" for i in range(len(tasks) + 1, len(tasks) + 6)]

task_signals_dict = {}
for task in tasks:
    task_signals_dict[f"{task['id']}_status"] = Signal(f"{task['id']}_status", task["status"])
    task_signals_dict[f"{task['id']}_visible"] = Signal(f"{task['id']}_visible", True)
    task_signals_dict[f"{task['id']}_name"] = Signal(f"{task['id']}_name", task["name"])
    task_signals_dict[f"{task['id']}_priority"] = Signal(f"{task['id']}_priority", task["priority"])

for i in range(len(tasks) + 1, len(tasks) + 6):
    task_id = f"task{i}"
    task_signals_dict[f"{task_id}_status"] = Signal(f"{task_id}_status", "pending")
    task_signals_dict[f"{task_id}_visible"] = Signal(f"{task_id}_visible", False)
    task_signals_dict[f"{task_id}_name"] = Signal(f"{task_id}_name", "New task")
    task_signals_dict[f"{task_id}_priority"] = Signal(f"{task_id}_priority", "normal")

task_signals_dict["task_cmd_next_id"] = Signal("task_cmd_next_id", len(tasks) + 1)

task_signals = list(task_signals_dict.values())


def TaskCommandInput(placeholder: str = "Add a new task...", **kwargs):
    def _(sig=None, **ctx):
        task_input = Signal("task_cmd_new", "", _ref_only=True)
        return Div(
            Icon("lucide:plus", cls="h-4 w-4 opacity-50"),
            Input(
                task_input,
                data_bind=task_input,
                data_on_keydown="""
                    if(evt.key==='Enter' && $task_cmd_new.trim()) {
                        const text = $task_cmd_new.trim();
                        const isUrgent = text.startsWith('!');
                        const name = text.replace(/^!/, '').trim();
                        if(name) {
                            const nextId = $task_cmd_next_id;

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

                            if(nextId < 10) {
                                $task_cmd_next_id = nextId + 1;
                            }
                            $task_cmd_new = '';
                        }
                    }
                """,
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





@with_code
def hero_command_example():
    return Div(
        Command(
            CommandInput(
                placeholder="Type a command or search...",
            ),
            CommandList(
                CommandEmpty("No results found."),
                CommandGroup(
                    "Suggestions",
                    CommandItem(
                        Icon("lucide:rocket", cls="h-4 w-4 mr-2"),
                        "Launch",
                        CommandShortcut("⌘L"),
                        value="launch",
                        onclick="alert('Launching...')",
                    ),
                    CommandItem(
                        Icon("lucide:search", cls="h-4 w-4 mr-2"),
                        "Search",
                        CommandShortcut("⌘K"),
                        value="search",
                        onclick="alert('Opening search...')",
                    ),
                    CommandItem(
                        Icon("lucide:terminal", cls="h-4 w-4 mr-2"),
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
                        Icon("lucide:file", cls="h-4 w-4 mr-2"),
                        "Project Alpha",
                        Badge("Active", variant="default", cls="ml-auto"),
                        value="project-alpha",
                        onclick="alert('Opening Project Alpha')",
                    ),
                    CommandItem(
                        Icon("lucide:file", cls="h-4 w-4 mr-2"),
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
    )


@with_code
def interactive_task_manager_example():
    return Div(
        *task_signals,
        Command(
            TaskCommandInput(
                placeholder="Add a new task (use ! for urgent)..."
            ),
            CommandList(
                CommandEmpty("No tasks yet. Add your first task above!"),
                CommandGroup(
                    "Pending Tasks",
                    *generate_task_items(tasks, "pending", task_signals_dict)
                ),
                CommandGroup(
                    "In Progress",
                    *generate_task_items(tasks, "progress", task_signals_dict)
                ),
                CommandSeparator(),
                CommandGroup(
                    "Completed",
                    *generate_task_items(tasks, "completed", task_signals_dict)
                ),
                cls="max-h-none overflow-visible"
            ),
            signal="tasks",
            size="md"
        )
    )


@with_code
def command_palette_with_actions_example():
    return Div(
        CommandDialog(
            Button(
                Icon("lucide:terminal", cls="h-4 w-4 mr-2"),
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
                            Icon("lucide:home", cls="h-4 w-4 mr-2"),
                            "Go to Home",
                            value="home",
                            onclick="window.location.href='/'",
                            ),
                        CommandItem(
                            Icon("lucide:book-open", cls="h-4 w-4 mr-2"),
                            "Documentation",
                            Icon("lucide:external-link", cls="h-3 w-3 ml-auto opacity-50"),
                            value="docs",
                            onclick="window.open('https://docs.example.com', '_blank')",
                            ),
                        CommandItem(
                            Icon("lucide:github", cls="h-4 w-4 mr-2"),
                            "GitHub Repository",
                            Icon("lucide:external-link", cls="h-3 w-3 ml-auto opacity-50"),
                            value="github",
                            onclick="window.open('https://github.com', '_blank')",
                            ),
                    ),
                    CommandSeparator(),
                    CommandGroup(
                        "Utilities",
                        CommandItem(
                            Icon("lucide:copy", cls="h-4 w-4 mr-2"),
                            "Copy Email",
                            CommandShortcut("⌘C"),
                            value="copy-email",
                            data_on_click=clipboard("user@example.com"),
                            ),
                        CommandItem(
                            Icon("lucide:link", cls="h-4 w-4 mr-2"),
                            "Copy Share Link",
                            CommandShortcut("⌘L"),
                            value="copy-link",
                            data_on_click=clipboard(js("window.location.href")),
                            ),
                        CommandItem(
                            Icon("lucide:download", cls="h-4 w-4 mr-2"),
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
                            Icon("lucide:moon", cls="h-4 w-4 mr-2"),
                            "Toggle Dark Mode",
                            CommandShortcut("⌘D"),
                            value="dark-mode",
                            onclick="document.documentElement.classList.toggle('dark')",
                            ),
                        CommandItem(
                            Icon("lucide:log-out", cls="h-4 w-4 mr-2 text-red-500"),
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
    )


@with_code
def compact_context_menu_example():
    return Div(
        Command(
            CommandList(
                CommandGroup(
                    "Item Actions",
                    CommandItem(
                        Icon("lucide:edit", cls="h-4 w-4 mr-2"),
                        "Edit",
                        CommandShortcut("⌘E"),
                        value="edit",
                        onclick="alert('Edit mode activated')",
                    ),
                    CommandItem(
                        Icon("lucide:copy", cls="h-4 w-4 mr-2"),
                        "Duplicate",
                        CommandShortcut("⌘D"),
                        value="duplicate",
                        onclick="alert('Item duplicated')",
                    ),
                    CommandItem(
                        Icon("lucide:archive", cls="h-4 w-4 mr-2"),
                        "Archive",
                        value="archive",
                        onclick="alert('Item archived')",
                    ),
                ),
                CommandSeparator(),
                CommandGroup(
                    "Share",
                    CommandItem(
                        Icon("lucide:link", cls="h-4 w-4 mr-2"),
                        "Copy Link",
                        value="copy-link",
                        data_on_click=clipboard("https://example.com/item/123"),
                    ),
                    CommandItem(
                        Icon("lucide:mail", cls="h-4 w-4 mr-2"),
                        "Email",
                        value="email",
                        onclick="window.location.href='mailto:?subject=Check this out'",
                    ),
                    CommandItem(
                        Icon("lucide:message-circle", cls="h-4 w-4 mr-2"),
                        "Send to Slack",
                        Icon("lucide:external-link", cls="h-3 w-3 ml-auto opacity-50"),
                        value="slack",
                        onclick="alert('Opening Slack...')",
                    ),
                ),
                CommandSeparator(),
                CommandItem(
                    Icon("lucide:trash", cls="h-4 w-4 mr-2 text-red-500"),
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
    )


EXAMPLES_DATA = [
    {"title": "Basic Command Menu", "description": "Simple command palette with search, keyboard shortcuts, and grouped items", "fn": hero_command_example},
    {"title": "Interactive Task Manager", "description": "Command component as a task manager with state transitions. Click tasks to move them: Pending → In Progress → Completed. Add new tasks with Enter (use ! prefix for urgent).", "fn": interactive_task_manager_example},
    {"title": "Command Palette with Actions", "description": "Interactive command dialog with real actions: navigation, clipboard operations, and system controls", "fn": command_palette_with_actions_example},
    {"title": "Compact Context Menu", "description": "Small command menu for context-specific actions, perfect for dropdowns and right-click menus", "fn": compact_context_menu_example},
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
