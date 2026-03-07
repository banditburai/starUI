TITLE = "Collapsible"
DESCRIPTION = "Show and hide sections with smooth animation. Supports nesting, disabled state, and reactive open/close control."
CATEGORY = "ui"
ORDER = 62
STATUS = "stable"

from starhtml import Div, Icon, P, Span

from components.badge import Badge
from components.card import Card, CardContent, CardHeader, CardTitle
from components.checkbox import CheckboxWithLabel
from components.collapsible import Collapsible, CollapsibleContent, CollapsibleTrigger
from utils import Prop, Component, auto_generate_page, build_api_reference, with_code


@with_code
def hero_collapsible_example():
    return Collapsible(
        Div(
            P("Order #4189", cls="text-sm font-semibold"),
            CollapsibleTrigger(
                Icon("lucide:chevrons-up-down", cls="size-4"),
                Span("Toggle details", cls="sr-only"),
                cls="inline-flex items-center justify-center size-8 rounded-md "
                "hover:bg-accent hover:text-accent-foreground",
            ),
            cls="flex items-center justify-between gap-4 px-4",
        ),
        Div(
            Span("Status", cls="text-muted-foreground"),
            Span("Shipped", cls="font-medium"),
            cls="flex items-center justify-between rounded-md border px-4 py-2 text-sm",
        ),
        CollapsibleContent(
            Div(
                P("Shipping address", cls="font-medium"),
                P("100 Market St, San Francisco", cls="text-muted-foreground"),
                cls="rounded-md border px-4 py-2 text-sm",
            ),
            Div(
                P("Items", cls="font-medium"),
                P("2x Studio Headphones", cls="text-muted-foreground"),
                cls="rounded-md border px-4 py-2 text-sm",
            ),
            cls="flex flex-col gap-2",
        ),
        open=True,
        cls="flex w-[350px] flex-col gap-2",
    )


@with_code
def filter_panel_example():
    def section(title, *options, open=False):
        return Collapsible(
            CollapsibleTrigger(
                Span(title, cls="text-sm font-medium"),
                Icon(
                    "lucide:chevron-down",
                    cls="size-4 ml-auto shrink-0 transition-transform duration-200 "
                    "group-data-[state=open]:rotate-180",
                ),
                cls="group flex w-full items-center px-2 py-2 rounded-md "
                "hover:bg-accent hover:text-accent-foreground",
            ),
            CollapsibleContent(
                Div(*options, cls="space-y-3 px-2 pt-1 pb-3"),
            ),
            open=open,
        )

    return Card(
        CardHeader(CardTitle("Filters", cls="text-base")),
        CardContent(
            Div(
                section(
                    "Category",
                    CheckboxWithLabel(label="Electronics", checked=True),
                    CheckboxWithLabel(label="Clothing"),
                    CheckboxWithLabel(label="Books"),
                    CheckboxWithLabel(label="Home & Garden"),
                    open=True,
                ),
                section(
                    "Price Range",
                    CheckboxWithLabel(label="Under $25"),
                    CheckboxWithLabel(label="$25 – $50"),
                    CheckboxWithLabel(label="$50 – $100"),
                    CheckboxWithLabel(label="Over $100"),
                ),
                section(
                    "Rating",
                    CheckboxWithLabel(label="4 stars & up", checked=True),
                    CheckboxWithLabel(label="3 stars & up"),
                ),
                cls="space-y-1",
            ),
        ),
        cls="w-[280px]",
    )


@with_code
def file_tree_example():
    def folder(name, *children, open=True):
        return Collapsible(
            CollapsibleTrigger(
                Icon(
                    "lucide:chevron-right",
                    cls="size-3.5 shrink-0 text-muted-foreground "
                    "transition-transform duration-200 group-data-[state=open]:rotate-90",
                ),
                Icon("lucide:folder", cls="size-4 shrink-0 text-amber-500 dark:text-amber-400"),
                Span(name, cls="text-sm"),
                cls="group flex items-center gap-1.5 w-full py-1 px-1 rounded-sm "
                "hover:bg-accent",
            ),
            CollapsibleContent(
                Div(*children, cls="ml-[9px] border-l pl-[13px]"),
            ),
            open=open,
        )

    def file(name, icon="lucide:file", icon_cls="text-muted-foreground"):
        return Div(
            Icon(icon, cls="size-4 shrink-0 " + icon_cls),
            Span(name, cls="text-sm"),
            cls="flex items-center gap-1.5 py-1 px-1 ml-5",
        )

    return Card(
        CardContent(
            Div(
                folder(
                    "src",
                    folder(
                        "components",
                        file("button.py"),
                        file("card.py"),
                        file("dialog.py"),
                    ),
                    folder(
                        "lib",
                        file("utils.py"),
                        file("cn.py"),
                    ),
                    file("app.py", "lucide:file-code", "text-emerald-600 dark:text-emerald-400"),
                ),
                folder(
                    "docs",
                    file("README.md", "lucide:file-text"),
                    file("CHANGELOG.md", "lucide:file-text"),
                    open=False,
                ),
                file("pyproject.toml", "lucide:settings-2"),
                file(".gitignore"),
            ),
            cls="pt-6 pb-2",
        ),
        cls="w-[280px]",
    )


@with_code
def disabled_collapsible_example():
    return Div(
        Collapsible(
            Div(
                P("Release Notes", cls="text-sm font-semibold"),
                CollapsibleTrigger(
                    Icon("lucide:chevrons-up-down", cls="size-4"),
                    Span("Toggle release notes", cls="sr-only"),
                    cls="inline-flex items-center justify-center size-8 rounded-md "
                    "hover:bg-accent hover:text-accent-foreground",
                ),
                cls="flex items-center justify-between gap-4 px-4",
            ),
            CollapsibleContent(
                Div(
                    Span("v2.1.0 – Bug fixes and performance improvements", cls="text-sm"),
                    cls="rounded-md border px-4 py-2",
                ),
                Div(
                    Span("v2.0.0 – New component architecture", cls="text-sm"),
                    cls="rounded-md border px-4 py-2",
                ),
                cls="flex flex-col gap-2",
            ),
            open=True,
            cls="flex flex-col gap-2",
        ),
        Collapsible(
            Div(
                Div(
                    P("Internal Roadmap", cls="text-sm font-semibold"),
                    Badge("Restricted", variant="outline", cls="text-xs"),
                    cls="flex items-center gap-2",
                ),
                CollapsibleTrigger(
                    Icon("lucide:lock", cls="size-4"),
                    Span("Toggle roadmap", cls="sr-only"),
                    cls="inline-flex items-center justify-center size-8 rounded-md",
                ),
                cls="flex items-center justify-between gap-4 px-4",
            ),
            CollapsibleContent(
                Div(
                    Span("This content requires admin access.", cls="text-sm text-muted-foreground"),
                    cls="rounded-md border border-dashed px-4 py-2",
                ),
                cls="flex flex-col gap-2",
            ),
            disabled=True,
            cls="flex flex-col gap-2",
        ),
        cls="w-[350px] space-y-6",
    )


API_REFERENCE = build_api_reference(
    main_props=[
        Prop("open", "bool", "Whether the content is initially expanded", "False"),
        Prop("disabled", "bool", "Prevents the trigger from toggling", "False"),
        Prop("signal", "str | Signal", "Datastar signal name for reactive state management", "auto-generated"),
        Prop("cls", "str", "Additional CSS classes", "''"),
    ],
    components=[
        Component("Collapsible", "Root container that manages open/close state"),
        Component("CollapsibleTrigger", "Clickable element that toggles the content. Renders a bare <button> — style with cls"),
        Component("CollapsibleContent", "Collapsible content panel with CSS grid animation. Accepts role (str, default 'region')"),
    ],
)


EXAMPLES_DATA = [
    {"fn": hero_collapsible_example},
    {
        "fn": filter_panel_example,
        "title": "Filter Panel",
        "description": "Multiple independent collapsible sections inside a card. Category uses open=True to start expanded.",
    },
    {
        "fn": file_tree_example,
        "title": "File Tree",
        "description": "Nested collapsibles with chevron rotation to build hierarchical navigation.",
    },
    {
        "fn": disabled_collapsible_example,
        "title": "Disabled",
        "description": "Use disabled=True to lock a section. The trigger becomes non-interactive.",
    },
]


def create_collapsible_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)
