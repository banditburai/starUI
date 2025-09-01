"""
Table component documentation - Structured data display.
"""

# Component metadata for auto-discovery
TITLE = "Table"
DESCRIPTION = "A responsive table component for displaying structured data with support for sorting, selection, and custom styling."
CATEGORY = "ui"
ORDER = 30
STATUS = "stable"

from uuid import uuid4
from starhtml import Div, P, Icon, Span, Strong, Code, H4, Input
from starhtml.datastar import ds_signals, ds_text, ds_on_click, ds_bind, ds_show, value
from starui.registry.components.table import (
    Table, TableHeader, TableBody, TableFooter, TableRow, 
    TableHead, TableCell, TableCaption
)
from starui.registry.components.button import Button
from starui.registry.components.checkbox import Checkbox
from starui.registry.components.badge import Badge
from utils import auto_generate_page
from widgets.component_preview import ComponentPreview


def examples():
    """Generate table examples using ComponentPreview with tabs."""
    
    # Basic data table
    yield ComponentPreview(
        Table(
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
        ),
        '''Table(
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
)''',
        title="Basic Table",
        description="Simple data table with headers, content, and caption"
    )
    
    # Interactive table with selection
    signal_id = uuid4().hex[:8]
    yield ComponentPreview(
        Div(
            Table(
                TableHeader(
                    TableRow(
                        TableHead(
                            Checkbox(checked_signal="selectAll", cls="mr-2"),
                            cls="w-12"
                        ),
                        TableHead("Task"),
                        TableHead("Priority"),
                        TableHead("Due Date"),
                        TableHead("Actions", cls="text-right")
                    )
                ),
                TableBody(
                    TableRow(
                        TableCell(Checkbox(checked_signal="task1")),
                        TableCell("Fix login bug"),
                        TableCell(Badge("High", variant="destructive")),
                        TableCell("2024-01-15"),
                        TableCell(
                            Button(
                                Icon("lucide:edit", cls="h-4 w-4"),
                                variant="ghost",
                                size="icon",
                                onclick="alert('Edit task')"
                            ),
                            cls="text-right"
                        ),
                        selected=True
                    ),
                    TableRow(
                        TableCell(Checkbox(checked_signal="task2")),
                        TableCell("Update documentation"),
                        TableCell(Badge("Medium", variant="secondary")),
                        TableCell("2024-01-20"),
                        TableCell(
                            Button(
                                Icon("lucide:edit", cls="h-4 w-4"),
                                variant="ghost",
                                size="icon",
                                onclick="alert('Edit task')"
                            ),
                            cls="text-right"
                        )
                    ),
                    TableRow(
                        TableCell(Checkbox(checked_signal="task3")),
                        TableCell("Code review"),
                        TableCell(Badge("Low", variant="outline")),
                        TableCell("2024-01-25"),
                        TableCell(
                            Button(
                                Icon("lucide:edit", cls="h-4 w-4"),
                                variant="ghost",
                                size="icon",
                                onclick="alert('Edit task')"
                            ),
                            cls="text-right"
                        )
                    )
                )
            ),
            Div(
                P("Selected tasks: ", 
                  Span(
                      ds_text("($task1 ? 1 : 0) + ($task2 ? 1 : 0) + ($task3 ? 1 : 0)"),
                      cls="font-bold"
                  )
                ),
                Button(
                    "Complete Selected",
                    ds_on_click("alert('Complete ' + (($task1 ? 1 : 0) + ($task2 ? 1 : 0) + ($task3 ? 1 : 0)) + ' tasks')"),
                    size="sm",
                    cls="mt-2"
                ),
                cls="mt-4 p-3 bg-muted rounded text-sm"
            ),
            ds_signals(selectAll=False, task1=True, task2=False, task3=False),
            cls="space-y-4"
        ),
        '''Table(
    TableHeader(
        TableRow(
            TableHead(Checkbox(checked_signal="selectAll")),
            TableHead("Task"),
            TableHead("Priority"),
            TableHead("Due Date"),
            TableHead("Actions", cls="text-right")
        )
    ),
    TableBody(
        TableRow(
            TableCell(Checkbox(checked_signal="task1")),
            TableCell("Fix login bug"),
            TableCell(Badge("High", variant="destructive")),
            TableCell("2024-01-15"),
            TableCell(
                Button(Icon("lucide:edit"), variant="ghost", size="icon"),
                cls="text-right"
            ),
            selected=True
        ),
        # ... more rows
    )
)''',
        title="Interactive Table",
        description="Table with selectable rows, actions, and live selection count"
    )
    
    # Financial data table with footer
    yield ComponentPreview(
        Table(
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
        ),
        '''Table(
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
        # ... more transactions
    ),
    TableFooter(
        TableRow(
            TableCell("Total", cls="font-medium", colspan="2"),
            TableCell("+$4,295.50", cls="text-right font-medium text-green-600"),
            TableCell("$4,295.50", cls="text-right font-bold")
        )
    ),
    TableCaption("Account transactions for January 2024")
)''',
        title="Financial Data",
        description="Table with footer totals and formatted currency values"
    )
    
    # Sortable product table
    signal_id2 = uuid4().hex[:8]
    yield ComponentPreview(
        Div(
            Div(
                Input(
                    ds_bind("search"),
                    type="text",
                    placeholder="Search products...",
                    cls="w-full px-3 py-2 border rounded-md mb-4"
                ),
                P("Search: ", Span(ds_text("$search"), cls="font-mono"), cls="text-sm text-muted-foreground mb-4")
            ),
            Table(
                TableHeader(
                    TableRow(
                        TableHead(
                            Button(
                                "Product Name",
                                Icon("lucide:chevron-up" if True else "lucide:chevron-down", cls="ml-1 h-3 w-3"),
                                variant="ghost",
                                size="sm",
                                ds_on_click="$sortBy = 'name'; $sortDesc = !$sortDesc",
                                cls="p-0 font-medium hover:bg-transparent"
                            )
                        ),
                        TableHead("Category"),
                        TableHead(
                            Button(
                                "Price",
                                Icon("lucide:chevron-up", cls="ml-1 h-3 w-3"),
                                variant="ghost", 
                                size="sm",
                                ds_on_click="$sortBy = 'price'; $sortDesc = !$sortDesc",
                                cls="p-0 font-medium hover:bg-transparent"
                            ),
                            cls="text-right"
                        ),
                        TableHead("Stock", cls="text-right")
                    )
                ),
                TableBody(
                    TableRow(
                        TableCell("Wireless Headphones"),
                        TableCell(Badge("Electronics")),
                        TableCell("$199.99", cls="text-right font-medium"),
                        TableCell(
                            Span("42", cls="text-green-600 font-medium"),
                            cls="text-right"
                        )
                    ),
                    TableRow(
                        TableCell("Coffee Mug"),
                        TableCell(Badge("Kitchen", variant="secondary")),
                        TableCell("$12.99", cls="text-right font-medium"),
                        TableCell(
                            Span("156", cls="text-green-600 font-medium"),
                            cls="text-right"
                        )
                    ),
                    TableRow(
                        TableCell("Desk Lamp"),
                        TableCell(Badge("Furniture", variant="outline")),
                        TableCell("$89.99", cls="text-right font-medium"),
                        TableCell(
                            Span("3", cls="text-red-600 font-medium"),
                            cls="text-right"
                        )
                    ),
                    TableRow(
                        TableCell("Notebook Set"),
                        TableCell(Badge("Office", variant="secondary")),
                        TableCell("$24.99", cls="text-right font-medium"),
                        TableCell(
                            Span("89", cls="text-green-600 font-medium"),
                            cls="text-right"
                        )
                    )
                ),
                TableCaption("Product inventory as of January 2024")
            ),
            Div(
                P("Sorting by: ", Strong(ds_text("$sortBy")), 
                  " (", ds_text("$sortDesc ? 'Descending' : 'Ascending'"), ")",
                  cls="text-sm text-muted-foreground"
                ),
                cls="mt-4"
            ),
            ds_signals(search=value(""), sortBy=value("name"), sortDesc=False),
            cls="space-y-4"
        ),
        '''# Searchable and sortable table
Input(
    ds_bind("search"),
    type="text",
    placeholder="Search products...",
    cls="w-full px-3 py-2 border rounded-md"
)

Table(
    TableHeader(
        TableRow(
            TableHead(
                Button(
                    "Product Name",
                    Icon("lucide:chevron-up", cls="ml-1 h-3 w-3"),
                    variant="ghost",
                    ds_on_click("$sortBy = 'name'; $sortDesc = !$sortDesc")
                )
            ),
            TableHead("Category"),
            TableHead(
                Button(
                    "Price",
                    Icon("lucide:chevron-up", cls="ml-1 h-3 w-3"),
                    variant="ghost",
                    ds_on_click="$sortBy = 'price'; $sortDesc = !$sortDesc"
                ),
                cls="text-right"
            ),
            TableHead("Stock", cls="text-right")
        )
    ),
    TableBody(
        TableRow(
            TableCell("Wireless Headphones"),
            TableCell(Badge("Electronics")),
            TableCell("$199.99", cls="text-right font-medium"),
            TableCell(Span("42", cls="text-green-600"), cls="text-right")
        ),
        # ... more rows
    ),
    TableCaption("Product inventory as of January 2024")
)''',
        title="Sortable Product Table",
        description="Interactive table with search, sortable columns, and status indicators"
    )
    
    # File browser table
    signal_id3 = uuid4().hex[:8]
    yield ComponentPreview(
        Div(
            Table(
                TableHeader(
                    TableRow(
                        TableHead(
                            Checkbox(checked_signal="selectAll"),
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
                        TableCell(Checkbox(checked_signal="file1")),
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
                        )
                    ),
                    TableRow(
                        TableCell(Checkbox(checked_signal="file2")),
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
                        )
                    ),
                    TableRow(
                        TableCell(Checkbox(checked_signal="file3")),
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
                        )
                    )
                )
            ),
            Div(
                P("Selected files: ",
                  Span(
                      ds_text("($file1 ? 1 : 0) + ($file2 ? 1 : 0) + ($file3 ? 1 : 0)"),
                      cls="font-bold"
                  ),
                  cls="text-sm"
                ),
                Button(
                    "Delete Selected",
                    variant="destructive",
                    size="sm",
                    ds_on_click="alert('Delete selected files')",
                    cls="mt-2"
                ),
                cls="mt-4 p-3 bg-muted rounded"
            ),
            ds_signals(selectAll=False, file1=False, file2=True, file3=False),
            cls="space-y-4"
        ),
        '''Table(
    TableHeader(
        TableRow(
            TableHead(Checkbox(checked_signal="selectAll")),
            TableHead("Name"),
            TableHead("Modified"),
            TableHead("Size", cls="text-right"),
            TableHead("Actions", cls="text-right")
        )
    ),
    TableBody(
        TableRow(
            TableCell(Checkbox(checked_signal="file1")),
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
                    Icon("lucide:more-horizontal"),
                    variant="ghost", 
                    size="icon"
                ),
                cls="flex justify-end"
            )
        ),
        # ... more file rows
    )
)''',
        title="File Browser",
        description="File management table with icons, selection, and contextual actions"
    )
    
    # Analytics dashboard table
    yield ComponentPreview(
        Table(
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
        ),
        '''Table(
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
        # ... more analytics rows
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
)''',
        title="Analytics Dashboard",
        description="Data table with metrics, trends, and summary totals"
    )
    
    # Responsive mobile-friendly table
    yield ComponentPreview(
        Div(
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
        ),
        '''Table(
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
            TableCell(Code("#1001", cls="font-mono text-xs")),
            TableCell(
                Div(
                    P("John Doe", cls="font-medium"),
                    P("john@example.com", cls="text-xs text-muted-foreground")
                )
            ),
            TableCell(Badge("Shipped", variant="default")),
            TableCell("$127.50", cls="text-right font-medium")
        ),
        TableRow(
            TableCell(Code("#1002", cls="font-mono text-xs")),
            TableCell(
                Div(
                    P("Jane Smith", cls="font-medium"),
                    P("jane@example.com", cls="text-xs text-muted-foreground")
                )
            ),
            TableCell(Badge("Processing", variant="secondary")),
            TableCell("$89.99", cls="text-right font-medium")
        ),
        # ... more orders
    )
)''',
        title="Order Management",
        description="Customer order table with rich cell content and status badges"
    )


def create_table_docs():
    """Create table documentation page using convention-based approach."""
    from utils import auto_generate_page
    
    api_reference = {
        "components": [
            {
                "name": "Table",
                "props": [
                    {
                        "name": "cls",
                        "type": "str",
                        "default": "''",
                        "description": "Additional CSS classes"
                    },
                    {
                        "name": "class_name",
                        "type": "str",
                        "default": "''",
                        "description": "Additional CSS classes (alternative to cls)"
                    }
                ]
            },
            {
                "name": "TableRow",
                "props": [
                    {
                        "name": "selected",
                        "type": "bool",
                        "default": "False",
                        "description": "Whether the row is selected"
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
                "name": "TableHead",
                "props": [
                    {
                        "name": "cls",
                        "type": "str",
                        "default": "''",
                        "description": "Additional CSS classes for header styling"
                    }
                ]
            },
            {
                "name": "TableCell",
                "props": [
                    {
                        "name": "cls",
                        "type": "str",
                        "default": "''",
                        "description": "Additional CSS classes for cell styling"
                    }
                ]
            }
        ]
    }
    
    # Hero example
    hero_example = ComponentPreview(
        Table(
            TableHeader(
                TableRow(
                    TableHead("Name"),
                    TableHead("Status"),
                    TableHead("Role")
                )
            ),
            TableBody(
                TableRow(
                    TableCell("Alice Cooper"),
                    TableCell(Badge("Active")),
                    TableCell("Admin")
                ),
                TableRow(
                    TableCell("Bob Wilson"),
                    TableCell(Badge("Active")),
                    TableCell("User")
                ),
                TableRow(
                    TableCell("Carol Martinez"),
                    TableCell(Badge("Inactive", variant="secondary")),
                    TableCell("User")
                )
            )
        ),
        '''Table(
    TableHeader(
        TableRow(
            TableHead("Name"),
            TableHead("Status"),
            TableHead("Role")
        )
    ),
    TableBody(
        TableRow(
            TableCell("Alice Cooper"),
            TableCell(Badge("Active")),
            TableCell("Admin")
        ),
        TableRow(
            TableCell("Bob Wilson"),
            TableCell(Badge("Active")),
            TableCell("User")
        ),
        TableRow(
            TableCell("Carol Martinez"),
            TableCell(Badge("Inactive", variant="secondary")),
            TableCell("User")
        )
    )
)''',
        copy_button=True
    )
    
    return auto_generate_page(
        TITLE,
        DESCRIPTION,
        list(examples()),
        cli_command="star add table", 
        api_reference=api_reference,
        hero_example=hero_example,
        component_slug="table"
    )