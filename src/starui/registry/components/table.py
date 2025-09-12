from typing import Any

from starhtml import (
    FT,
    Caption,
    Div,
    Tbody,
    Td,
    Tfoot,
    Th,
    Thead,
    Tr,
)
from starhtml import (
    Table as HTMLTable,
)

from .utils import cn


def Table(
    *children: Any,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    classes = cn("w-full caption-bottom text-sm", cls)
    return Div(
        HTMLTable(*children, data_slot="table", cls=classes, **kwargs),
        data_slot="table-container",
        cls="relative w-full overflow-x-auto",
    )


def TableHeader(
    *children: Any,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    classes = cn("[&_tr]:border-b [&_tr]:border-input", cls)
    return Thead(*children, data_slot="table-header", cls=classes, **kwargs)


def TableBody(
    *children: Any,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    classes = cn("[&_tr:last-child]:border-0", cls)
    return Tbody(*children, data_slot="table-body", cls=classes, **kwargs)


def TableFooter(
    *children: Any,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    classes = cn(
        "bg-muted/50 border-t border-input font-medium [&>tr]:last:border-b-0",
        cls,
    )
    return Tfoot(*children, data_slot="table-footer", cls=classes, **kwargs)


def TableRow(
    *children: Any,
    selected: bool = False,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    classes = cn(
        "border-b border-input transition-colors hover:bg-muted/50 data-[state=selected]:bg-muted",
        cls,
    )

    if selected:
        kwargs["data_state"] = "selected"
        kwargs["aria_selected"] = "true"

    return Tr(*children, data_slot="table-row", cls=classes, **kwargs)


def TableHead(
    *children: Any,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    classes = cn(
        "text-foreground h-10 px-2 text-left align-middle font-medium whitespace-nowrap [&:has([role=checkbox])]:pr-0 [&>[role=checkbox]]:translate-y-[2px]",
        cls,
    )
    return Th(*children, data_slot="table-head", cls=classes, **kwargs)


def TableCell(
    *children: Any,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    classes = cn(
        "p-2 align-middle whitespace-nowrap [&:has([role=checkbox])]:pr-0 [&>[role=checkbox]]:translate-y-[2px]",
        cls,
    )
    return Td(*children, data_slot="table-cell", cls=classes, **kwargs)


def TableCaption(
    *children: Any,
    cls: str = "",
    **kwargs: Any,
) -> FT:
    classes = cn("mt-4 text-sm text-muted-foreground", cls)
    return Caption(*children, data_slot="table-caption", cls=classes, **kwargs)
