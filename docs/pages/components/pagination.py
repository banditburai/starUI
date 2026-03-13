"""
Pagination component documentation - Page navigation with next and previous links.
"""

# Component metadata for auto-discovery
TITLE = "Pagination"
DESCRIPTION = "Pagination with page navigation, next and previous links."
CATEGORY = "ui"
ORDER = 80
STATUS = "stable"

from starhtml import A, Div, Icon, Nav, Signal, Span
from starhtml import Button as HTMLButton
from components.pagination import (
    Pagination,
    PaginationContent,
    PaginationItem,
    PaginationLink,
    SimplePagination,
)
from components.table import (
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
)
from utils import auto_generate_page, with_code, Component, build_api_reference


@with_code
def hero_example():
    return Div(
        (page := Signal("hero_page", 1)),
        Div(
            Span("Page ", cls="text-muted-foreground"),
            Span(data_text=page, cls="font-medium"),
            Span(" of 20", cls="text-muted-foreground"),
            cls="mb-4 text-sm",
        ),
        SimplePagination(
            current_page=1,
            total_pages=20,
            signal="hero_page",
        ),
        cls="flex min-h-[120px] flex-col items-center justify-center",
    )


@with_code
def table_pagination_example():
    screenings = [
        ("Stalker", "Tarkovsky", 1979),
        ("Solaris", "Tarkovsky", 1972),
        ("8½", "Fellini", 1963),
        ("La Dolce Vita", "Fellini", 1960),
        ("Persona", "Bergman", 1966),
        ("The Seventh Seal", "Bergman", 1957),
        ("In the Mood for Love", "Wong Kar-wai", 2000),
        ("Chungking Express", "Wong Kar-wai", 1994),
        ("Paris, Texas", "Wenders", 1984),
        ("Wings of Desire", "Wenders", 1987),
        ("Yi Yi", "Edward Yang", 2000),
        ("A Brighter Summer Day", "Edward Yang", 1991),
    ]
    per_page = 4
    total = len(screenings)
    total_pages = (total + per_page - 1) // per_page
    sig = Signal("tbl_page", 1)

    rows = []
    for i, (title, director, year) in enumerate(screenings):
        p = (i // per_page) + 1
        rows.append(
            TableRow(
                TableCell(title, cls="font-medium"),
                TableCell(director),
                TableCell(str(year)),
                data_show=sig == p,
            )
        )

    range_spans = []
    for p in range(1, total_pages + 1):
        start = (p - 1) * per_page + 1
        end = min(p * per_page, total)
        range_spans.append(
            Span(
                f"Showing {start}\u2013{end} of {total}",
                data_show=sig == p,
                cls="text-sm text-muted-foreground",
            )
        )

    at_start = sig <= 1
    at_end = sig >= total_pages

    return Div(
        sig,
        Table(
            TableHeader(
                TableRow(
                    TableHead("Title", cls="w-[200px]"),
                    TableHead("Director"),
                    TableHead("Year", cls="text-right"),
                ),
            ),
            TableBody(*rows),
        ),
        Div(
            Div(*range_spans),
            Div(
                HTMLButton(
                    Icon("lucide:chevron-left", cls="size-4"),
                    data_on_click=sig.set((sig - 1).max(1)),
                    data_attr_disabled=at_start,
                    type="button",
                    aria_label="Previous page",
                    cls="inline-flex size-8 cursor-pointer items-center justify-center rounded-md hover:bg-accent"
                    " disabled:pointer-events-none disabled:opacity-50",
                ),
                HTMLButton(
                    Icon("lucide:chevron-right", cls="size-4"),
                    data_on_click=sig.set((sig + 1).min(total_pages)),
                    data_attr_disabled=at_end,
                    type="button",
                    aria_label="Next page",
                    cls="inline-flex size-8 cursor-pointer items-center justify-center rounded-md hover:bg-accent"
                    " disabled:pointer-events-none disabled:opacity-50",
                ),
                cls="flex gap-1",
            ),
            cls="flex items-center justify-between pt-4",
        ),
    )


@with_code
def content_nav_example():
    return Nav(
        A(
            Div(Icon("lucide:chevron-left", cls="size-4"), cls="flex items-center"),
            Div(
                Span("Previous", cls="text-sm text-muted-foreground"),
                Span("Getting Started with Signals", cls="text-sm font-medium"),
                cls="flex flex-col items-start",
            ),
            href="#",
            cls="flex items-center gap-3 rounded-lg px-4 py-3 transition-colors hover:bg-accent",
        ),
        A(
            Div(
                Span("Next", cls="text-sm text-muted-foreground"),
                Span("Advanced Reactivity", cls="text-sm font-medium"),
                cls="flex flex-col items-end",
            ),
            Div(Icon("lucide:chevron-right", cls="size-4"), cls="flex items-center"),
            href="#",
            cls="flex items-center gap-3 rounded-lg px-4 py-3 transition-colors hover:bg-accent",
        ),
        role="navigation", aria_label="content",
        cls="mx-auto flex w-full justify-between",
    )


@with_code
def primitives_example():
    total_pages = 5
    page = Signal("prim_page", 1)

    return Div(
        page,
        Div(
            Span("Page ", cls="text-muted-foreground"),
            Span(data_text=page, cls="font-medium"),
            Span(f" of {total_pages}", cls="text-muted-foreground"),
            cls="mb-4 text-center text-sm",
        ),
        Pagination(
            PaginationContent(
                PaginationItem(
                    PaginationLink(
                        Icon("lucide:chevrons-left", cls="size-4"),
                        page=1,
                        aria_label="First page",
                    ),
                ),
                *[
                    PaginationItem(
                        PaginationLink(str(p), page=p),
                    )
                    for p in range(1, total_pages + 1)
                ],
                PaginationItem(
                    PaginationLink(
                        Icon("lucide:chevrons-right", cls="size-4"),
                        page=total_pages,
                        aria_label="Last page",
                    ),
                ),
            ),
            signal="prim_page",
            total_pages=total_pages,
            current_page=1,
        ),
        cls="flex min-h-[120px] flex-col items-center justify-center",
    )


EXAMPLES_DATA = [
    {
        "title": "Pagination",
        "description": "SimplePagination auto-generates page numbers, ellipsis, and prev/next buttons. The page indicator above is bound to the same signal and updates on every click. Previous is disabled at page 1.",
        "fn": hero_example,
    },
    {
        "title": "Paginated Table",
        "description": "Table rows controlled by a shared page signal via data_show. The result count and disabled states update reactively. [Signal, data_show, Table]",
        "fn": table_pagination_example,
        "preview_class": "[&>*]:w-full",
    },
    {
        "title": "Content Navigation",
        "description": "Article-style prev/next with real links. For URL-based navigation, use plain Nav and A elements instead of the Pagination component.",
        "fn": content_nav_example,
        "preview_class": "[&>*]:w-full",
    },
    {
        "title": "With Primitives",
        "description": "Custom layout from PaginationLink primitives with reactive active states. First/last buttons that SimplePagination doesn't provide.",
        "fn": primitives_example,
    },
]

API_REFERENCE = build_api_reference(
    components=[
        Component(
            "SimplePagination",
            "Convenience wrapper that auto-generates page numbers, ellipsis, and prev/next controls",
        ),
        Component(
            "Pagination",
            "Root navigation container with role='navigation' and aria label",
        ),
        Component("PaginationContent", "Flex container (ul) for pagination items"),
        Component(
            "PaginationItem", "List item wrapper (li) for each pagination element"
        ),
        Component(
            "PaginationLink",
            "Clickable page number link with active state and signal binding",
        ),
        Component(
            "PaginationPrevious",
            "Previous page button with chevron icon and optional text label",
        ),
        Component(
            "PaginationNext",
            "Next page button with chevron icon and optional text label",
        ),
        Component(
            "PaginationEllipsis",
            "Ellipsis indicator for skipped page ranges with sr-only label",
        ),
    ]
)


def create_pagination_docs():
    return auto_generate_page(TITLE, DESCRIPTION, EXAMPLES_DATA, API_REFERENCE)
