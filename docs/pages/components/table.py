"""
Table component documentation - Structured data display.
"""

# Component metadata for auto-discovery
TITLE = "Table"
DESCRIPTION = "A responsive table component for displaying structured data with support for sorting, selection, and custom styling."
CATEGORY = "ui"
ORDER = 30
STATUS = "stable"

from starhtml import Div, P, Icon, Span, Code, Signal, Style
from starui.registry.components.table import (
    Table, TableHeader, TableBody, TableFooter, TableRow,
    TableHead, TableCell, TableCaption
)
from starui.registry.components.button import Button
from starui.registry.components.checkbox import Checkbox
from starui.registry.components.badge import Badge
from utils import auto_generate_page, with_code, Prop, build_api_reference



@with_code
def basic_table_example():
    return Table(
        TableHeader(
            TableRow(
                TableHead("Name"),
                TableHead("Email"),
                TableHead("Role"),
                TableHead("Status")
            )
        ),
        TableBody(
            TableRow(
                TableCell("Alice Johnson"),
                TableCell("alice@company.com"),
                TableCell("Developer"),
                TableCell(Badge("Active", variant="default"))
            ),
            TableRow(
                TableCell("Bob Smith"),
                TableCell("bob@company.com"),
                TableCell("Designer"),
                TableCell(Badge("Active", variant="default"))
            ),
            TableRow(
                TableCell("Carol Davis"),
                TableCell("carol@company.com"),
                TableCell("Manager"),
                TableCell(Badge("Away", variant="secondary"))
            )
        ),
        TableCaption("Employee directory - 3 of 24 employees shown")
    )


@with_code
def interactive_table_example():
    tasks = [
        {"id": "task1", "name": "Fix login bug", "priority": "High", "variant": "destructive", "date": "2024-01-15"},
        {"id": "task2", "name": "Update documentation", "priority": "Medium", "variant": "secondary", "date": "2024-01-20"},
        {"id": "task3", "name": "Code review", "priority": "Low", "variant": "outline", "date": "2024-01-25"},
    ]

    task_sigs = {task["id"]: Signal(task["id"], False) for task in tasks}
    visible_sigs = {task["id"]: Signal(f"{task['id']}_visible", True) for task in tasks}
    select_all = Signal("select_all", False)

    # When any individual checkbox changes, sync select_all state
    sync_select_all = select_all.set(sum(task_sigs.values()).eq(len(tasks)))

    def create_task_row(task):
        return TableRow(
            TableCell(Checkbox(
                signal=task_sigs[task["id"]],
                data_on_change=sync_select_all
            )),
            TableCell(task["name"]),
            TableCell(Badge(task["priority"], variant=task["variant"])),
            TableCell(task["date"]),
            TableCell(
                Button(
                    Icon("lucide:edit", cls="h-4 w-4"),
                    variant="ghost",
                    size="icon",
                    data_on_click="alert('Edit task')"
                ),
                cls="text-right"
            ),
            data_show=visible_sigs[task["id"]]
        )

    complete_actions = [
        action
        for task_id, sig in task_sigs.items()
        for action in [
            sig.then(visible_sigs[task_id].set(False)),  # Hide checked tasks
            sig.set(False)  # Uncheck all
        ]
    ]

    return Div(
        select_all,
        *task_sigs.values(),
        *visible_sigs.values(),
        Table(
            TableHeader(
                TableRow(
                    TableHead(
                        Checkbox(
                            signal=select_all,
                            data_on_change=[sig.set(select_all) for sig in task_sigs.values()]
                        ),
                        cls="w-12"
                    ),
                    TableHead("Task"),
                    TableHead("Priority"),
                    TableHead("Due Date"),
                    TableHead("Actions", cls="text-right")
                )
            ),
            TableBody(*[create_task_row(task) for task in tasks]),
            cls="w-full"
        ),
        Div(
            P("Selected tasks: ",
              Span(data_text=sum(task_sigs.values()), cls="font-bold"),
              " of ",
              Span(data_text=sum(visible_sigs.values()), cls="font-bold"),
              " remaining"
            ),
            Button(
                "Complete Selected",
                data_on_click=complete_actions,
                data_attr_disabled=sum(task_sigs.values()).eq(0),
                size="sm",
                cls="mt-2 select-none"
            ),
            cls="mt-4 p-3 bg-muted rounded text-sm"
        ),
        cls="space-y-4 w-full max-w-3xl"
    )


@with_code
def financial_table_example():
    return Table(
        TableHeader(
            TableRow(
                TableHead("Transaction"),
                TableHead("Date"),
                TableHead("Amount", cls="text-right"),
                TableHead("Balance", cls="text-right")
            )
        ),
        TableBody(
            TableRow(
                TableCell("Initial Deposit"),
                TableCell("2024-01-01"),
                TableCell("+$1,000.00", cls="text-right text-green-600 font-medium"),
                TableCell("$1,000.00", cls="text-right font-medium")
            ),
            TableRow(
                TableCell("Coffee Purchase"),
                TableCell("2024-01-02"),
                TableCell("-$4.50", cls="text-right text-red-600"),
                TableCell("$995.50", cls="text-right font-medium")
            ),
            TableRow(
                TableCell("Online Transfer"),
                TableCell("2024-01-03"),
                TableCell("-$200.00", cls="text-right text-red-600"),
                TableCell("$795.50", cls="text-right font-medium")
            ),
            TableRow(
                TableCell("Salary Deposit"),
                TableCell("2024-01-15"),
                TableCell("+$3,500.00", cls="text-right text-green-600 font-medium"),
                TableCell("$4,295.50", cls="text-right font-medium")
            )
        ),
        TableFooter(
            TableRow(
                TableCell("Total", cls="font-medium", colspan="2"),
                TableCell("+$4,295.50", cls="text-right font-medium text-green-600"),
                TableCell("$4,295.50", cls="text-right font-bold")
            )
        ),
        TableCaption("Account transactions for January 2024")
    )

@with_code
def sortable_table_example():
    files = [
        {"name": "Documentation.pdf", "size": 2.4, "type": "PDF"},
        {"name": "Image.png", "size": 5.2, "type": "Image"},
        {"name": "Archive.zip", "size": 10.8, "type": "Archive"},
        {"name": "Video.mp4", "size": 45.3, "type": "Video"},
        {"name": "Backup.tar", "size": 1.2, "type": "Archive"},
    ]

    def calc_sort_orders(items, fields):
        """Auto-calculate CSS order values for each item in all sort states."""
        orders = []
        for i, item in enumerate(items):
            item_orders = {"none": i}
            for field in fields:
                sorted_asc = sorted(enumerate(items), key=lambda x: x[1][field])
                sorted_desc = sorted(enumerate(items), key=lambda x: x[1][field], reverse=True)
                item_orders[f"{field}_asc"] = next(pos for pos, (idx, _) in enumerate(sorted_asc) if idx == i)
                item_orders[f"{field}_desc"] = next(pos for pos, (idx, _) in enumerate(sorted_desc) if idx == i)
            orders.append(item_orders)
        return orders

    sort_orders = calc_sort_orders(files, ["name", "size"])
    sort_by = Signal("file_sort_by", "none")
    sort_dir = Signal("file_sort_dir", "asc")

    def create_sort_toggle(field):
        """Create toggle actions for a sortable field."""
        return [
            sort_dir.set(sort_by.eq(field).if_(sort_dir.eq("asc").if_("desc", "asc"), "asc")),
            sort_by.set(field)
        ]

    def create_file_row(file, orders):
        return TableRow(
            TableCell(
                Div(
                    P(file["name"], cls="font-medium"),
                    P(file["type"], cls="text-xs text-muted-foreground")
                ),
                cls="w-full"
            ),
            TableCell(f"{file['size']} MB", cls="text-right w-24"),
            data_style_order=(
                f"$file_sort_by === 'none' ? {orders['none']} : ("
                f"$file_sort_by === 'name' ? ($file_sort_dir === 'asc' ? {orders['name_asc']} : {orders['name_desc']}) : "
                f"($file_sort_dir === 'asc' ? {orders['size_asc']} : {orders['size_desc']}))"
            )
        )

    return Div(
        sort_by,
        sort_dir,
        Style("""
            .sortable-table thead tr {
                display: flex;
            }
            .sortable-table tbody {
                display: flex;
                flex-direction: column;
            }
            .sortable-table tbody tr {
                display: flex;
            }
            .sortable-table th {
                cursor: pointer;
                user-select: none;
            }
            .sortable-table th:hover {
                background: hsl(var(--muted));
            }
        """),
        Table(
            TableHeader(
                TableRow(
                    TableHead(
                        Div(
                            Span("File Name"),
                            Icon("lucide:chevron-down",
                                 cls="h-4 w-4 ml-1 shrink-0 transition-transform duration-200",
                                 data_class_rotate_180=sort_by.eq("name") & sort_dir.eq("asc"),
                                 data_show=sort_by.eq("name")),
                            cls="flex items-center gap-1"
                        ),
                        data_on_click=create_sort_toggle("name"),
                        cls="cursor-pointer w-full"
                    ),
                    TableHead(
                        Div(
                            Span("Size"),
                            Icon("lucide:chevron-down",
                                 cls="h-4 w-4 ml-1 shrink-0 transition-transform duration-200",
                                 data_class_rotate_180=sort_by.eq("size") & sort_dir.eq("asc"),
                                 data_show=sort_by.eq("size")),
                            cls="flex items-center justify-end gap-1"
                        ),
                        data_on_click=create_sort_toggle("size"),
                        cls="text-right cursor-pointer w-24"
                    )
                )
            ),
            TableBody(
                *[create_file_row(file, orders) for file, orders in zip(files, sort_orders)]
            ),
            cls="sortable-table"
        ),
        cls="w-full max-w-2xl"
    )


@with_code
def responsive_table_example():
    orders = [
        {"id": "#1001", "customer": "John Doe", "email": "john@example.com", "status": "Shipped", "variant": "default", "amount": "$127.50"},
        {"id": "#1002", "customer": "Jane Smith", "email": "jane@example.com", "status": "Processing", "variant": "secondary", "amount": "$89.99"},
        {"id": "#1003", "customer": "Mike Johnson", "email": "mike@example.com", "status": "Cancelled", "variant": "destructive", "amount": "$45.00"},
    ]

    return Div(
        P("Resize window - becomes stacked cards on mobile", cls="text-sm text-muted-foreground mb-4"),
        Div(
            Table(
                TableHeader(
                    TableRow(
                        TableHead("Order"),
                        TableHead("Customer"),
                        TableHead("Status"),
                        TableHead("Amount")
                    )
                ),
                TableBody(
                    *[TableRow(
                        TableCell(Code(order["id"], cls="font-mono text-xs"), data_label="Order"),
                        TableCell(
                            Div(
                                P(order["customer"], cls="font-medium"),
                                P(order["email"], cls="text-xs text-muted-foreground")
                            ),
                            data_label="Customer"
                        ),
                        TableCell(Badge(order["status"], variant=order["variant"]), data_label="Status"),
                        TableCell(order["amount"], cls="font-medium", data_label="Amount")
                    ) for order in orders]
                )
            ),
            cls="responsive-table"
        ),
        Style("""
            @media (max-width: 640px) {
                .responsive-table table,
                .responsive-table thead,
                .responsive-table tbody,
                .responsive-table tr,
                .responsive-table th,
                .responsive-table td {
                    display: block;
                }

                .responsive-table thead {
                    display: none;
                }

                .responsive-table tr {
                    margin-bottom: 1rem;
                    border: 1px solid hsl(var(--border));
                    border-radius: 0.5rem;
                    padding: 0.75rem;
                }

                .responsive-table td {
                    text-align: left !important;
                    padding: 0.5rem 0;
                    border: none;
                    position: relative;
                    padding-left: 40%;
                }

                .responsive-table td::before {
                    content: attr(data-label);
                    position: absolute;
                    left: 0;
                    font-weight: 600;
                    font-size: 0.875rem;
                }
            }
        """),
        cls="w-full max-w-2xl"
    )


EXAMPLES_DATA = [
    {"title": "Basic Table", "description": "Simple data table with headers, content, and caption", "fn": basic_table_example},
    {"title": "Interactive Table", "description": "Table with selectable rows, actions, and live selection count", "fn": interactive_table_example},
    {"title": "Sortable Table", "description": "Click column headers to sort by name or size, with ascending/descending toggle", "fn": sortable_table_example},
    {"title": "Financial Data", "description": "Table with footer totals and formatted currency values", "fn": financial_table_example},
    {"title": "Responsive Table", "description": "Mobile-friendly table that adapts layout and hides/shows columns at different breakpoints", "fn": responsive_table_example},
]

API_REFERENCE = build_api_reference(
    main_props=[
        Prop("cls", "str", "Additional CSS classes", "''"),
    ]
)


def create_table_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)