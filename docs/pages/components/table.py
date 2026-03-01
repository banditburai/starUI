"""
Table component documentation - Structured data display.
"""

# Component metadata for auto-discovery
TITLE = "Table"
DESCRIPTION = "Displays tabular data with headers, rows, and optional footer."
CATEGORY = "ui"
ORDER = 30
STATUS = "stable"

from starhtml import Div, P, Icon, Span, Signal
from starui.registry.components.table import (
    Table, TableHeader, TableBody, TableFooter, TableRow,
    TableHead, TableCell, TableCaption
)
from starui.registry.components.button import Button
from starui.registry.components.checkbox import Checkbox
from starui.registry.components.badge import Badge
from starui.registry.components.avatar import Avatar, AvatarFallback
from starui.registry.components.dropdown_menu import (
    DropdownMenu, DropdownMenuTrigger, DropdownMenuContent,
    DropdownMenuItem, DropdownMenuSeparator,
)
from starui.registry.components.skeleton import Skeleton
from starui.registry.components.progress import Progress
from utils import auto_generate_page, with_code, Prop, Component, build_api_reference


@with_code
def hero_table_example():
    observations = [
        {"target": "Andromeda Galaxy", "catalog": "M31", "ra": "00h 42m 44s", "mag": "3.44"},
        {"target": "Orion Nebula", "catalog": "M42", "ra": "05h 35m 17s", "mag": "4.00"},
        {"target": "Crab Nebula", "catalog": "M1", "ra": "05h 34m 32s", "mag": "8.40"},
        {"target": "Whirlpool Galaxy", "catalog": "M51", "ra": "13h 29m 53s", "mag": "8.36"},
        {"target": "Ring Nebula", "catalog": "M57", "ra": "18h 53m 35s", "mag": "8.80"},
    ]
    return Table(
        TableHeader(
            TableRow(
                TableHead("Target", cls="w-[180px]"),
                TableHead("Catalog"),
                TableHead("Right Ascension"),
                TableHead("Magnitude", cls="text-right"),
            )
        ),
        TableBody(
            *[TableRow(
                TableCell(obs["target"], cls="font-medium"),
                TableCell(obs["catalog"]),
                TableCell(obs["ra"]),
                TableCell(obs["mag"], cls="text-right"),
            ) for obs in observations]
        ),
    )


@with_code
def caption_footer_example():
    seeds = [
        {"variety": "Cherokee Purple", "type": "Tomato", "count": 48, "germ": "89%"},
        {"variety": "Sugar Snap", "type": "Pea", "count": 117, "germ": "94%"},
        {"variety": "Danvers Half Long", "type": "Carrot", "count": 186, "germ": "78%"},
        {"variety": "Bloomsdale", "type": "Spinach", "count": 85, "germ": "91%"},
    ]
    total = sum(s["count"] for s in seeds)
    return Table(
        TableCaption("Spring seed inventory."),
        TableHeader(
            TableRow(
                TableHead("Variety"),
                TableHead("Type"),
                TableHead("Seeds", cls="text-right"),
                TableHead("Germination", cls="text-right"),
            )
        ),
        TableBody(
            *[TableRow(
                TableCell(s["variety"], cls="font-medium"),
                TableCell(s["type"]),
                TableCell(str(s["count"]), cls="text-right"),
                TableCell(s["germ"], cls="text-right"),
            ) for s in seeds]
        ),
        TableFooter(
            TableRow(
                TableCell("Total", cls="font-medium", colspan="3"),
                TableCell(str(total), cls="text-right font-medium"),
            )
        ),
    )


@with_code
def selected_rows_example():
    prs = [
        {"branch": "fix/null-pointer-feed", "author": "kezhou", "status": "Merged", "variant": "secondary", "selected": False},
        {"branch": "feat/dark-mode-toggle", "author": "priya-s", "status": "Open", "variant": "default", "selected": True},
        {"branch": "PROJ-412-rate-limit", "author": "tomek92", "status": "Open", "variant": "default", "selected": True},
        {"branch": "docs/api-examples", "author": "linchen", "status": "Draft", "variant": "outline", "selected": False},
    ]
    return Table(
        TableHeader(
            TableRow(
                TableHead("Branch"),
                TableHead("Author"),
                TableHead("Status"),
            )
        ),
        TableBody(
            *[TableRow(
                TableCell(pr["branch"], cls="font-medium font-mono text-sm"),
                TableCell(pr["author"]),
                TableCell(Badge(pr["status"], variant=pr["variant"])),
                selected=pr["selected"],
            ) for pr in prs]
        ),
        TableCaption("Pull requests with selected rows highlighted."),
    )


@with_code
def row_actions_example():
    recipes = [
        {"name": "Miso-Glazed Eggplant", "cuisine": "Japanese", "time": "35 min"},
        {"name": "Shakshuka", "cuisine": "Tunisian", "time": "25 min"},
        {"name": "Cacio e Pepe", "cuisine": "Italian", "time": "20 min"},
        {"name": "Aglio e Olio", "cuisine": "Italian", "time": "15 min"},
        {"name": "Arepas Reinas Pepiadas", "cuisine": "Venezuelan", "time": "45 min"},
    ]
    return Table(
        TableHeader(
            TableRow(
                TableHead("Recipe", cls="w-[200px]"),
                TableHead("Cuisine"),
                TableHead("Time"),
                TableHead(cls="w-[50px]"),
            )
        ),
        TableBody(
            *[TableRow(
                TableCell(r["name"], cls="font-medium"),
                TableCell(r["cuisine"]),
                TableCell(r["time"]),
                TableCell(
                    DropdownMenu(
                        DropdownMenuTrigger(
                            Icon("lucide:ellipsis", cls="h-4 w-4"),
                            variant="ghost",
                            size="icon",
                            cls="h-8 w-8",
                            aria_label="Recipe options",
                        ),
                        DropdownMenuContent(
                            DropdownMenuItem(Icon("lucide:book-open", cls="h-4 w-4"), "View recipe"),
                            DropdownMenuItem(Icon("lucide:pencil", cls="h-4 w-4"), "Edit"),
                            DropdownMenuSeparator(),
                            DropdownMenuItem(Icon("lucide:trash-2", cls="h-4 w-4"), "Delete", variant="destructive"),
                        ),
                    ),
                ),
            ) for r in recipes]
        ),
    )


@with_code
def composition_example():
    learners = [
        {"name": "Ren Matsuda", "initials": "RM", "lang": "Portuguese", "level": "B1", "level_variant": "secondary", "progress": 62},
        {"name": "Amira Kovacs", "initials": "AK", "lang": "Mandarin", "level": "A2", "level_variant": "outline", "progress": 38},
        {"name": "Sofia Kovacs", "initials": "SK", "lang": "Mandarin", "level": "B1", "level_variant": "secondary", "progress": 71},
    ]
    return Table(
        TableHeader(
            TableRow(
                TableHead("Learner", cls="w-[200px]"),
                TableHead("Language"),
                TableHead("Level"),
                TableHead("Progress", cls="w-[140px]"),
            )
        ),
        TableBody(
            *[TableRow(
                TableCell(
                    Div(
                        Avatar(AvatarFallback(l["initials"]), cls="h-8 w-8"),
                        Span(l["name"], cls="font-medium"),
                        cls="flex items-center gap-3",
                    )
                ),
                TableCell(l["lang"]),
                TableCell(Badge(l["level"], variant=l["level_variant"])),
                TableCell(
                    Div(
                        Progress(value=l["progress"], cls="h-2"),
                        Span(f'{l["progress"]}%', cls="text-xs text-muted-foreground ml-2 tabular-nums"),
                        cls="flex items-center",
                    )
                ),
            ) for l in learners],
            TableRow(
                TableCell(
                    Div(
                        Skeleton(cls="h-8 w-8 rounded-full"),
                        Skeleton(cls="h-4 w-24"),
                        cls="flex items-center gap-3",
                    )
                ),
                TableCell(Skeleton(cls="h-4 w-16")),
                TableCell(Skeleton(cls="h-5 w-10 rounded-md")),
                TableCell(Skeleton(cls="h-2 w-full rounded-full")),
            ),
        ),
        TableCaption("Language learning progress tracker with a loading placeholder row."),
    )


@with_code
def selection_example():
    messages = [
        {"id": "msg1", "from": "Loom", "subject": "Your recording is ready", "date": "Feb 21"},
        {"id": "msg2", "from": "GitHub", "subject": "New comment on starui#417", "date": "Feb 20"},
        {"id": "msg3", "from": "Cal.com", "subject": "Booking confirmed: Wed 10 AM", "date": "Feb 19"},
        {"id": "msg4", "from": "Stripe", "subject": "Payout of $1,247.63 initiated", "date": "Feb 18"},
        {"id": "msg5", "from": "Linear", "subject": "Sprint 14 starts Monday", "date": "Feb 17"},
    ]

    sigs = [Signal(f"tbl_{m['id']}", False) for m in messages]
    archs = [Signal(f"tbl_arch_{m['id']}", False) for m in messages]
    select_all = Signal("tbl_select_all", False)

    selected_count = sum(sigs)
    visible_count = len(messages) - sum(archs)

    sync_select_all = select_all.set(
        (visible_count > 0) & selected_count.eq(visible_count)
    )

    archive_selected = [
        *[sig.then(arch.set(True)) for sig, arch in zip(sigs, archs)],
        *[sig.set(False) for sig in sigs],
        select_all.set(False),
    ]

    return Div(
        select_all,
        sigs,
        archs,
        Table(
            TableHeader(
                TableRow(
                    TableHead(
                        Checkbox(
                            signal=select_all,
                            data_on_change=[
                                (~arch).then(sig.set(select_all))
                                for sig, arch in zip(sigs, archs)
                            ],
                        ),
                        cls="w-12",
                    ),
                    TableHead("From"),
                    TableHead("Subject"),
                    TableHead("Date", cls="text-right"),
                )
            ),
            TableBody(
                *[TableRow(
                    TableCell(Checkbox(
                        signal=sig,
                        data_on_change=sync_select_all,
                    )),
                    TableCell(m["from"], cls="font-medium"),
                    TableCell(m["subject"]),
                    TableCell(m["date"], cls="text-right text-muted-foreground"),
                    data_show=~arch,
                ) for m, sig, arch in zip(messages, sigs, archs)]
            ),
        ),
        Div(
            Span(data_text=selected_count, cls="font-bold"),
            Span(data_text=" of " + visible_count + " selected"),
            Button(
                "Archive",
                size="sm",
                variant="outline",
                data_on_click=archive_selected,
                data_attr_disabled=selected_count.eq(0),
                cls="ml-auto",
            ),
            cls="mt-3 flex items-center gap-1 text-sm text-muted-foreground",
        ),
        cls="w-full max-w-3xl",
    )


@with_code
def empty_state_example():
    return Table(
        TableHeader(
            TableRow(
                TableHead("Endpoint"),
                TableHead("Method"),
                TableHead("Latency"),
            )
        ),
        TableBody(
            TableRow(
                TableCell(
                    Div(
                        Icon("lucide:inbox", cls="h-8 w-8 text-muted-foreground/50"),
                        P("No results found.", cls="text-sm text-muted-foreground"),
                        cls="flex flex-col items-center gap-2 py-8",
                    ),
                    colspan="3",
                ),
            )
        ),
    )


EXAMPLES_DATA = [
    {"title": "Table", "description": "Basic anatomy with header, body, and aligned columns", "fn": hero_table_example},
    {"title": "Caption & Footer", "description": "TableFooter with totals and TableCaption for description", "fn": caption_footer_example},
    {"title": "Selected Rows", "description": "TableRow selected prop for persistent highlighted background", "fn": selected_rows_example},
    {"title": "Row Actions", "description": "DropdownMenu composed in table cells for per-row actions", "fn": row_actions_example},
    {"title": "Rich Composition", "description": "Avatar, Badge, Progress, and Skeleton composed in table cells", "fn": composition_example},
    {"title": "Selection", "description": "Checkbox select-all with functional Archive using .then() conditional actions [Signal, sum(), .then()]", "fn": selection_example},
    {"title": "Empty State", "description": "Empty table body with icon and message using colspan", "fn": empty_state_example},
]

API_REFERENCE = build_api_reference(
    main_props=[
        Prop("selected", "bool", "Sets data-state='selected' on TableRow for highlighted background", "False"),
        Prop("cls", "str", "Additional CSS classes for any subcomponent", "''"),
        Prop("wrapper_cls", "str", "CSS classes for the Table scroll container wrapper", "''"),
    ],
    components=[
        Component("Table", "Root container. Wraps the HTML table in a scroll-enabled div. Use wrapper_cls for the outer div and cls for the inner table"),
        Component("TableHeader", "Groups header rows. Adds a bottom border to child rows"),
        Component("TableBody", "Groups data rows. Removes the border from the last row"),
        Component("TableFooter", "Summary row area with muted background and top border"),
        Component("TableRow", "Row with hover highlight. Set selected=True for persistent muted background"),
        Component("TableHead", "Header cell with muted text, medium font weight, and h-10 height"),
        Component("TableCell", "Data cell with p-2 padding. Use colspan for spanning columns"),
        Component("TableCaption", "Descriptive text below the table. Renders as HTML caption element"),
    ]
)


def create_table_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)
