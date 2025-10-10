"""
Table component documentation - Structured data display.
"""

# Component metadata for auto-discovery
TITLE = "Table"
DESCRIPTION = "A responsive table component for displaying structured data with support for sorting, selection, and custom styling."
CATEGORY = "ui"
ORDER = 30
STATUS = "stable"

from starhtml import Div, P, Icon, Span, Strong, Code, H4, Input, Signal, js
from starui.registry.components.table import (
    Table, TableHeader, TableBody, TableFooter, TableRow, 
    TableHead, TableCell, TableCaption
)
from starui.registry.components.button import Button
from starui.registry.components.checkbox import Checkbox
from starui.registry.components.badge import Badge
from utils import auto_generate_page, with_code, Component, build_api_reference
from widgets.component_preview import ComponentPreview


# ============================================================================
# EXAMPLE FUNCTIONS (decorated with @with_code for markdown generation)
# ============================================================================

# Basic data table
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


# Interactive table with selection
@with_code
def interactive_table_example():
    select_all = Signal("select_all", False)
    task1 = Signal("task1", False)
    task2 = Signal("task2", False)
    task3 = Signal("task3", False)
    task1_visible = Signal("task1_visible", True)
    task2_visible = Signal("task2_visible", True)
    task3_visible = Signal("task3_visible", True)

    def create_task_row(signal, visible_signal, task, priority, variant, date):
        return TableRow(
            TableCell(Checkbox(signal=signal)),
            TableCell(task),
            TableCell(Badge(priority, variant=variant)),
            TableCell(date),
            TableCell(
                Button(
                    Icon("lucide:edit", cls="h-4 w-4"),
                    variant="ghost",
                    size="icon",
                    onclick="alert('Edit task')"
                ),
                cls="text-right"
            ),
            data_show=js(f"${visible_signal}")
        )

    return Div(
        select_all, task1, task2, task3, task1_visible, task2_visible, task3_visible,
        Table(
            TableHeader(
                TableRow(
                    TableHead(
                        Checkbox(signal="select_all", cls="mr-2"),
                        cls="w-12"
                    ),
                    TableHead("Task"),
                    TableHead("Priority"),
                    TableHead("Due Date"),
                    TableHead("Actions", cls="text-right")
                )
            ),
            TableBody(
                *[create_task_row(signal, visible_signal, task, priority, variant, date)
                  for signal, visible_signal, task, priority, variant, date in [
                      ("task1", "task1_visible", "Fix login bug", "High", "destructive", "2024-01-15"),
                      ("task2", "task2_visible", "Update documentation", "Medium", "secondary", "2024-01-20"),
                      ("task3", "task3_visible", "Code review", "Low", "outline", "2024-01-25")
                  ]]
            )
        ),
        Div(
            P("Selected tasks: ",
              Span(
                  data_text=js("($task1 ? 1 : 0) + ($task2 ? 1 : 0) + ($task3 ? 1 : 0)"),
                  cls="font-bold"
              ),
              " of ",
              Span(
                  data_text=js("($task1_visible ? 1 : 0) + ($task2_visible ? 1 : 0) + ($task3_visible ? 1 : 0)"),
                  cls="font-bold"
              ),
              " remaining"
            ),
            Button(
                "Complete Selected",
                data_on_click=js("let count = ($task1 ? 1 : 0) + ($task2 ? 1 : 0) + ($task3 ? 1 : 0); if(count > 0) { alert('Completing ' + count + ' task' + (count !== 1 ? 's' : '')); if($task1) { $task1_visible = false; $task1 = false; } if($task2) { $task2_visible = false; $task2 = false; } if($task3) { $task3_visible = false; $task3 = false; } } else { alert('No tasks selected'); }"),
                size="sm",
                cls="mt-2"
            ),
            cls="mt-4 p-3 bg-muted rounded text-sm"
        ),
        cls="space-y-4"
    )


# Financial data table with footer
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


# File browser table
@with_code
def file_browser_table_example():
    select_all = Signal("select_all", False)
    file1 = Signal("file1", False)
    file2 = Signal("file2", False)
    file3 = Signal("file3", False)
    file1_visible = Signal("file1_visible", True)
    file2_visible = Signal("file2_visible", True)
    file3_visible = Signal("file3_visible", True)

    return Div(
        select_all, file1, file2, file3, file1_visible, file2_visible, file3_visible,
        Table(
            TableHeader(
                TableRow(
                    TableHead(
                        Checkbox(signal="select_all"),
                        cls="w-12"
                    ),
                    TableHead("Name"),
                    TableHead("Modified"),
                    TableHead("Size", cls="text-right"),
                    TableHead("Actions", cls="text-right")
                )
            ),
            TableBody(
                TableRow(
                    TableCell(Checkbox(signal="file1")),
                    TableCell(
                        Div(
                            Icon("lucide:folder", cls="mr-2 h-4 w-4 text-blue-500"),
                            "Documents",
                            cls="flex items-center"
                        )
                    ),
                    TableCell("2 hours ago"),
                    TableCell("—", cls="text-right text-muted-foreground"),
                    TableCell(
                        Button(
                            Icon("lucide:more-horizontal", cls="h-4 w-4"),
                            variant="ghost",
                            size="icon",
                            onclick="alert('Folder actions')"
                        ),
                        cls="flex justify-end"
                    ),
                    data_show=js("$file1_visible")
                ),
                TableRow(
                    TableCell(Checkbox(signal="file2")),
                    TableCell(
                        Div(
                            Icon("lucide:file-text", cls="mr-2 h-4 w-4 text-gray-500"),
                            "report.pdf",
                            cls="flex items-center"
                        )
                    ),
                    TableCell("Yesterday"),
                    TableCell("2.4 MB", cls="text-right"),
                    TableCell(
                        Button(
                            Icon("lucide:download", cls="h-4 w-4"),
                            variant="ghost",
                            size="icon",
                            onclick="alert('Download file')"
                        ),
                        cls="flex justify-end"
                    ),
                    data_show=js("$file2_visible")
                ),
                TableRow(
                    TableCell(Checkbox(signal="file3")),
                    TableCell(
                        Div(
                            Icon("lucide:image", cls="mr-2 h-4 w-4 text-green-500"),
                            "screenshot.png",
                            cls="flex items-center"
                        )
                    ),
                    TableCell("3 days ago"),
                    TableCell("1.8 MB", cls="text-right"),
                    TableCell(
                        Button(
                            Icon("lucide:eye", cls="h-4 w-4"),
                            variant="ghost",
                            size="icon",
                            onclick="alert('Preview image')"
                        ),
                        cls="flex justify-end"
                    ),
                    data_show=js("$file3_visible")
                )
            )
        ),
        Div(
            P("Selected: ",
              Span(
                  data_text=js("($file1 ? 1 : 0) + ($file2 ? 1 : 0) + ($file3 ? 1 : 0)"),
                  cls="font-bold"
              ),
              " of ",
              Span(
                  data_text=js("($file1_visible ? 1 : 0) + ($file2_visible ? 1 : 0) + ($file3_visible ? 1 : 0)"),
                  cls="font-bold"
              ),
              " files",
              cls="text-sm"
            ),
            Button(
                "Delete Selected",
                data_on_click=js("let count = ($file1 ? 1 : 0) + ($file2 ? 1 : 0) + ($file3 ? 1 : 0); if(count > 0) { alert('Deleting ' + count + ' selected file' + (count > 1 ? 's' : '')); if($file1) { $file1_visible = false; $file1 = false; } if($file2) { $file2_visible = false; $file2 = false; } if($file3) { $file3_visible = false; $file3 = false; } } else { alert('No files selected'); }"),
                variant="destructive",
                size="sm",
                cls="mt-2"
            ),
            cls="mt-4 p-3 bg-muted rounded"
        ),
        cls="space-y-4"
    )


# Analytics dashboard table
@with_code
def analytics_dashboard_table_example():
    return Table(
        TableHeader(
            TableRow(
                TableHead("Page"),
                TableHead("Views", cls="text-right"),
                TableHead("Unique Visitors", cls="text-right"),
                TableHead("Bounce Rate", cls="text-right"),
                TableHead("Trend", cls="text-center")
            )
        ),
        TableBody(
            TableRow(
                TableCell("/dashboard"),
                TableCell("12,543", cls="text-right font-medium"),
                TableCell("8,234", cls="text-right"),
                TableCell("23.4%", cls="text-right"),
                TableCell(
                    Icon("lucide:trending-up", cls="h-4 w-4 text-green-500"),
                    cls="text-center"
                )
            ),
            TableRow(
                TableCell("/products"),
                TableCell("9,876", cls="text-right font-medium"),
                TableCell("7,123", cls="text-right"),
                TableCell("18.7%", cls="text-right"),
                TableCell(
                    Icon("lucide:trending-up", cls="h-4 w-4 text-green-500"),
                    cls="text-center"
                )
            ),
            TableRow(
                TableCell("/contact"),
                TableCell("2,341", cls="text-right font-medium"),
                TableCell("1,987", cls="text-right"),
                TableCell("45.2%", cls="text-right"),
                TableCell(
                    Icon("lucide:trending-down", cls="h-4 w-4 text-red-500"),
                    cls="text-center"
                )
            ),
            TableRow(
                TableCell("/about"),
                TableCell("1,567", cls="text-right font-medium"),
                TableCell("1,234", cls="text-right"),
                TableCell("31.8%", cls="text-right"),
                TableCell(
                    Icon("lucide:minus", cls="h-4 w-4 text-gray-400"),
                    cls="text-center"
                )
            )
        ),
        TableFooter(
            TableRow(
                TableCell("Total", cls="font-medium"),
                TableCell("26,327", cls="text-right font-bold"),
                TableCell("18,578", cls="text-right font-bold"),
                TableCell("27.1%", cls="text-right font-bold"),
                TableCell(
                    Icon("lucide:trending-up", cls="h-4 w-4 text-green-500"),
                    cls="text-center"
                )
            )
        )
    )


# Responsive mobile-friendly table
@with_code
def order_management_table_example():
    return Div(
        P("Responsive design - stacks on small screens", cls="text-sm text-muted-foreground mb-4"),
        Table(
            TableHeader(
                TableRow(
                    TableHead("Order #"),
                    TableHead("Customer"),
                    TableHead("Status"),
                    TableHead("Amount", cls="text-right")
                )
            ),
            TableBody(
                TableRow(
                    TableCell(
                        Code("#1001", cls="font-mono text-xs")
                    ),
                    TableCell(
                        Div(
                            P("John Doe", cls="font-medium"),
                            P("john@example.com", cls="text-xs text-muted-foreground"),
                            cls="space-y-1"
                        )
                    ),
                    TableCell(Badge("Shipped", variant="default")),
                    TableCell("$127.50", cls="text-right font-medium")
                ),
                TableRow(
                    TableCell(
                        Code("#1002", cls="font-mono text-xs")
                    ),
                    TableCell(
                        Div(
                            P("Jane Smith", cls="font-medium"),
                            P("jane@example.com", cls="text-xs text-muted-foreground"),
                            cls="space-y-1"
                        )
                    ),
                    TableCell(Badge("Processing", variant="secondary")),
                    TableCell("$89.99", cls="text-right font-medium")
                ),
                TableRow(
                    TableCell(
                        Code("#1003", cls="font-mono text-xs")
                    ),
                    TableCell(
                        Div(
                            P("Mike Johnson", cls="font-medium"),
                            P("mike@example.com", cls="text-xs text-muted-foreground"),
                            cls="space-y-1"
                        )
                    ),
                    TableCell(Badge("Cancelled", variant="destructive")),
                    TableCell("$45.00", cls="text-right font-medium line-through")
                )
            )
        ),
        cls="w-full max-w-2xl"
    )


# ============================================================================
# MODULE-LEVEL DATA (for markdown API)
# ============================================================================

EXAMPLES_DATA = [
    {"title": "Basic Table", "description": "Simple data table with headers, content, and caption", "fn": basic_table_example},
    {"title": "Interactive Table", "description": "Table with selectable rows, actions, and live selection count", "fn": interactive_table_example},
    {"title": "Financial Data", "description": "Table with footer totals and formatted currency values", "fn": financial_table_example},
    {"title": "File Browser", "description": "File management table with icons, selection, and contextual actions", "fn": file_browser_table_example},
    {"title": "Analytics Dashboard", "description": "Data table with metrics, trends, and summary totals", "fn": analytics_dashboard_table_example},
    {"title": "Order Management", "description": "Customer order table with rich cell content and status badges", "fn": order_management_table_example},
]

API_REFERENCE = build_api_reference(
    components=[
        Component("Table", "Root container for tabular data"),
        Component("TableHeader", "Container for header rows"),
        Component("TableBody", "Container for data rows"),
        Component("TableFooter", "Optional footer for totals/summary"),
        Component("TableRow", "Row element for header, body, or footer"),
        Component("TableHead", "Header cell (column label)"),
        Component("TableCell", "Data cell for row content"),
        Component("TableCaption", "Caption describing the table"),
    ]
)


def examples():
    """Generate all table examples."""
    yield ComponentPreview(
        basic_table_example(),
        basic_table_example.code,
        title="Basic Table",
        description="Simple data table with headers, content, and caption"
    )

    yield ComponentPreview(
        interactive_table_example(),
        interactive_table_example.code,
        title="Interactive Table",
        description="Table with selectable rows, actions, and live selection count"
    )

    yield ComponentPreview(
        financial_table_example(),
        financial_table_example.code,
        title="Financial Data",
        description="Table with footer totals and formatted currency values"
    )

    yield ComponentPreview(
        file_browser_table_example(),
        file_browser_table_example.code,
        title="File Browser",
        description="File management table with icons, selection, and contextual actions"
    )

    yield ComponentPreview(
        analytics_dashboard_table_example(),
        analytics_dashboard_table_example.code,
        title="Analytics Dashboard",
        description="Data table with metrics, trends, and summary totals"
    )

    yield ComponentPreview(
        order_management_table_example(),
        order_management_table_example.code,
        title="Order Management",
        description="Customer order table with rich cell content and status badges"
    )


def create_table_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)